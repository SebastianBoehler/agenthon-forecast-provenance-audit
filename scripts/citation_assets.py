"""Executive summary: snapshot declared primary sources and preserve physical PDF pages."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


class VisibleHTML(HTMLParser):
    """Extract visible text without script/style bodies; this is not a browser render."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self.hidden += 1
        if tag in {"p", "div", "section", "h1", "h2", "h3", "li", "tr", "br"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"}:
            self.hidden -= 1
        if tag in {"p", "div", "section", "h1", "h2", "h3", "li", "tr"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def extract(path: Path, kind: str) -> list[str]:
    if kind == "pdf":
        from pypdf import PdfReader
        # Preserve empty pages. Dropping them would corrupt later page locators.
        return [page.extract_text() or "" for page in PdfReader(path).pages]
    text = path.read_text(encoding="utf-8")
    if kind == "html":
        parser = VisibleHTML()
        parser.feed(text)
        text = "".join(parser.parts)
        if any(term in text.lower() for term in ("just a moment...", "verify you are human")):
            raise ValueError("Access challenge is not source evidence")
    return [text]


def snapshot(root: Path, entry: dict, output: Path, fetch: bool) -> dict:
    """Failures remain explicit and are not replaced by another source."""
    record = dict(entry, captured_utc=datetime.now(timezone.utc).isoformat(), assets=[])
    try:
        if entry.get("asset"):
            paths = [root / entry["asset"], *[root / p for p in entry.get("extra_assets", [])]]
            record["acquisition"] = "existing_local_primary_asset"
        else:
            kind = entry.get("format", "pdf")
            cached = root / "literature/pdfs/citation-workspace" / f"{entry['key']}.{kind}"
            if not cached.exists():
                if not fetch:
                    raise FileNotFoundError("Source not cached; run with --fetch to acquire the declared URL")
                request = Request(entry["asset_url"], headers={"User-Agent": "CiteProof-local-audit/0.1"})
                with urlopen(request, timeout=25) as response:
                    raw = response.read()
                    record["response_final_url"] = response.url
                if kind == "pdf" and not raw.startswith(b"%PDF-"):
                    raise ValueError("Declared PDF URL did not return PDF bytes")
                cached.parent.mkdir(parents=True, exist_ok=True)
                cached.write_bytes(raw)
                write_json(cached.with_suffix(cached.suffix + ".acquisition.json"), {
                    "url": entry["asset_url"], "final_url": record["response_final_url"],
                    "captured_utc": record["captured_utc"], "sha256": digest(raw)})
            else:
                acquisition = cached.with_suffix(cached.suffix + ".acquisition.json")
                if not acquisition.exists():
                    raise ValueError("Downloaded cache lacks its acquisition record")
                saved = json.loads(acquisition.read_text())
                if saved["sha256"] != digest(cached.read_bytes()) or saved["url"] != entry["asset_url"]:
                    raise ValueError("Downloaded cache changed or URL no longer matches")
                record["cached_acquisition"] = saved
            paths = [cached]
            record["acquisition"] = "declared_primary_url_snapshot"
        for index, path in enumerate(paths):
            raw = path.read_bytes()
            kind = entry.get("format") or ("pdf" if path.suffix == ".pdf" else "text")
            pages = extract(path, kind)
            if not any(page.strip() for page in pages):
                raise ValueError("Source has no extracted text")
            asset_id = f"{entry['key']}:{index}"
            stored = output / "assets" / f"{entry['key']}-{index}{path.suffix}"
            stored.parent.mkdir(parents=True, exist_ok=True)
            stored.write_bytes(raw)
            page_path = output / "pages" / f"{entry['key']}-{index}.json"
            page_path.parent.mkdir(parents=True, exist_ok=True)
            write_json(page_path, pages)
            record["assets"].append({
                "source_id": asset_id, "origin_path": str(path.relative_to(root)),
                "snapshot": str(stored.relative_to(output)), "sha256": digest(raw),
                "pages_file": str(page_path.relative_to(output)),
                "pages_sha256": digest(page_path.read_bytes()), "format": kind,
                "physical_page_count": len(pages) if kind == "pdf" else None,
                "blank_page_count": sum(not p.strip() for p in pages),
                "extractor": "pypdf.PdfReader.page.extract_text" if kind == "pdf" else kind,
            })
        record["status"] = "available"
    except (OSError, ValueError, UnicodeError) as exc:
        record["status"] = "unavailable"
        record["error"] = f"{type(exc).__name__}: {exc}"
        record["assets"] = []
    return record
