"""Executive summary: reuse CiteProof retrieval and attach independently checked excerpt identities."""

from __future__ import annotations

import json
from pathlib import Path

from citation_assets import digest
from citation_excerpt_integrity import locate_excerpt


def loaded_sources(manifest: list[dict], output: Path):
    from citeproof.models import Source

    sources, lookup = [], {}
    for entry in manifest:
        if entry["status"] != "available":
            continue
        for asset in entry["assets"]:
            pages = json.loads((output / asset["pages_file"]).read_text())
            source = Source(
                source_id=asset["source_id"], citation_key=entry["key"], title=entry["title"],
                text="\n\n".join(pages), path=asset["snapshot"],
                pages=tuple(pages) if asset["format"] == "pdf" else (),
            )
            sources.append(source)
            lookup[source.source_id] = (entry, asset, pages)
    return sources, lookup


def bind_evidence(evidence: dict, lookup: dict) -> dict:
    entry, asset, pages = lookup[evidence["source_id"]]
    if evidence.get("citation_key") != entry["key"]:
        raise ValueError("Evidence citation key does not match its declared source")
    page = evidence.get("page")
    index = page - 1 if page is not None else 0
    if not 0 <= index < len(pages):
        raise ValueError("CiteProof evidence page is outside the saved physical pages")
    binding = locate_excerpt(pages[index], evidence["text"])
    result = {
        "citation_key": entry["key"], "source_id": evidence["source_id"],
        "source_url": entry["url"], "asset_url": entry.get("asset_url"),
        "access_scope": entry["scope"], "physical_pdf_page": page,
        "source_snapshot": asset["snapshot"], "source_sha256": asset["sha256"],
        "pages_file": asset["pages_file"], "pages_sha256": asset["pages_sha256"],
        "page_text_sha256": digest(pages[index].encode()),
        "retrieval_text": evidence["text"], "retrieval_score": evidence.get("score"),
        **binding,
    }
    if binding["integrity"] == "exact_saved_extraction_slice":
        result["extraction_line_start"] = pages[index].count("\n", 0, binding["start_char"]) + 1
        result["extraction_line_end"] = pages[index].count("\n", 0, binding["end_char"]) + 1
    return result


def check_run(root: Path, output: Path) -> dict:
    from citation_excerpt_integrity import check_excerpt

    receipt = json.loads((output / "receipt.json").read_text())
    if digest((root / receipt["draft"]).read_bytes()) != receipt["draft_sha256"]:
        raise ValueError("Draft changed: rerun citation retrieval for this revision")
    if digest((root / receipt["catalog"]).read_bytes()) != receipt["catalog_sha256"]:
        raise ValueError("Source catalog changed: rerun the citation audit")
    for name, expected in receipt["code_sha256"].items():
        if digest(Path(name).read_bytes()) != expected:
            raise ValueError("Recorded implementation changed: " + name)
    for name, expected in receipt["output_sha256"].items():
        if digest((output / name).read_bytes()) != expected:
            raise ValueError("Saved citation output changed: " + name)
    claims = json.loads((output / "claims.json").read_text())
    draft = (root / receipt["draft"]).read_text()
    for claim in claims:
        raw = draft[claim["draft_start_char"]:claim["draft_end_char"]]
        if raw != claim["draft_context"] or digest(raw.encode()) != claim["context_sha256"]:
            raise ValueError("Claim context no longer matches its draft interval")
    checked = 0
    for record in (json.loads(line) for line in (output / "excerpt_ledger.jsonl").read_text().splitlines()):
        if record["integrity"] != "exact_saved_extraction_slice":
            continue
        pages = json.loads((output / record["pages_file"]).read_text())
        index = record["physical_pdf_page"] - 1 if record["physical_pdf_page"] is not None else 0
        if digest(pages[index].encode()) != record["page_text_sha256"]:
            raise ValueError("Page text digest differs")
        check_excerpt(pages[index], record)
        checked += 1
    return {"status": "PASS", "exact_excerpts_checked": checked,
            "semantic_support_certified": False, "current_draft_identity_checked": True}
