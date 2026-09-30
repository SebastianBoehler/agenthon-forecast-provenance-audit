"""Executive summary: bind excerpts to exact saved characters; never infer semantic support."""

from __future__ import annotations

import re

from citation_assets import digest


def normalized_map(text: str) -> tuple[str, list[tuple[int, int]]]:
    """Only collapse whitespace; retain an invertible map to raw character spans."""
    chars, offsets = [], []
    for match in re.finditer(r"\s+|\S", text):
        value = " " if match.group().isspace() else match.group()
        chars.append(value)
        offsets.append(match.span())
    return "".join(chars), offsets


def locate_excerpt(page: str, candidate: str) -> dict:
    """A normalized candidate is not itself an exact quotation of the raw extraction."""
    haystack, offsets = normalized_map(page)
    needle = re.sub(r"\s+", " ", candidate).strip()
    if not needle:
        return {"integrity": "unlocated", "reason": "Empty candidate"}
    starts, cursor = [], 0
    while (start := haystack.find(needle, cursor)) >= 0:
        starts.append(start)
        cursor = start + 1
    if not starts:
        return {"integrity": "unlocated", "reason": "Not a contiguous whitespace-equivalent source span"}
    start = offsets[starts[0]][0]
    end = offsets[starts[0] + len(needle) - 1][1]
    excerpt = page[start:end]
    assert re.sub(r"\s+", " ", excerpt).strip() == needle
    return {
        "integrity": "exact_saved_extraction_slice", "start_char": start, "end_char": end,
        "excerpt": excerpt, "excerpt_sha256": digest(excerpt.encode()),
        "match_count": len(starts), "match_policy": "whitespace collapse only; no fuzzy text matching",
        "locator_note": "Character offsets refer to saved page text, not the original PDF byte stream.",
    }


def check_excerpt(page: str, record: dict) -> None:
    """Reject a changed quote, shifted offset, or malformed interval."""
    start, end = record["start_char"], record["end_char"]
    if not isinstance(start, int) or not isinstance(end, int) or not 0 <= start < end <= len(page):
        raise ValueError("Invalid excerpt interval")
    if page[start:end] != record["excerpt"]:
        raise ValueError("Excerpt no longer equals its exact source slice")
    if digest(record["excerpt"].encode()) != record["excerpt_sha256"]:
        raise ValueError("Excerpt digest differs")
