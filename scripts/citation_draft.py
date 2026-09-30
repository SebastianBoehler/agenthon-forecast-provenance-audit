"""Executive summary: inventory every citation occurrence and preserve its exact draft context."""

from __future__ import annotations

import re
from pathlib import Path

from citation_assets import digest

CITE = re.compile(r"\\cite[a-zA-Z*]*\{([^}]+)\}")


def inventory(path: Path) -> tuple[list[dict], list[dict]]:
    from citeproof.parser import parse_claims

    text = path.read_text()
    start = text.index(r"\begin{document}")
    # Exclude the inline bibliography, while preserving appendix citations.
    intervals = [m.span() for m in re.finditer(
        r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", text, re.S)]
    sections = [(m.start(), m.group(1)) for m in re.finditer(r"\\section\{([^}]+)\}", text)]
    claims, occurrences = [], []
    for block in re.finditer(r"\S(?:.*?)(?=\n\s*\n|\Z)", text[start:], re.S):
        begin, end = start + block.start(), start + block.end()
        if any(lo <= begin < hi for lo, hi in intervals):
            continue
        raw = block.group()
        visible = "\n".join(line for line in raw.splitlines() if not line.lstrip().startswith("%"))
        citations = list(CITE.finditer(visible))
        if not citations:
            continue
        section = next((name for pos, name in reversed(sections) if pos <= begin), "Front matter")
        location = {
            "section": section, "draft_start_char": begin, "draft_end_char": end,
            "line_start": text.count("\n", 0, begin) + 1,
            "line_end": text.count("\n", 0, end) + 1,
            "draft_context": raw, "context_sha256": digest(raw.encode()),
        }
        if r"\begin{table}" in visible:
            # CiteProof intentionally drops tables. Inventory cited prose cells explicitly.
            parsed = [claim for line in visible.splitlines() if CITE.search(line)
                      for claim in parse_claims(line.split("&", 1)[0])]
        else:
            parsed = parse_claims(visible)
        for match in citations:
            keys = [key.strip() for key in match.group(1).split(",")]
            occurrences.append(dict(location, citation_keys=keys,
                                    parser_covers_keys=all(any(k in c.citation_keys for c in parsed) for k in keys)))
        for claim in parsed:
            fingerprint = digest((claim.text + "\0" + ",".join(claim.citation_keys)).encode())
            claims.append(dict(location, claim_id=f"claim-{len(claims)+1:03d}",
                               claim_fingerprint=fingerprint, claim=claim.text,
                               citation_keys=list(claim.citation_keys), review_status="pending_author_review"))
    return claims, occurrences


def audit_bib(entries: list[dict], cited: set[str]) -> str:
    """Alignment-only BibTeX. The inline manuscript remains the publication bibliography."""
    lines = ["% Executive summary: title/key alignment for CiteProof; not externally certified full metadata."]
    for entry in entries:
        if entry["key"] not in cited:
            continue
        fields = {"title": entry["title"], "year": str(entry["year"]), "url": entry["url"]}
        if entry.get("doi"):
            fields["doi"] = entry["doi"]
        lines.append("@misc{" + entry["key"] + ",")
        lines.extend("  " + key + " = {" + value + "}," for key, value in fields.items())
        lines.append("}")
    return "\n".join(lines) + "\n"
