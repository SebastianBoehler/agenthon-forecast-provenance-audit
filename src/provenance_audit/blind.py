"""Executive summary: validate matched cases and randomize one hidden provenance condition per reviewer and pair."""

from __future__ import annotations

import json
import os
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROVENANCE = {"derived", "answer_first"}
CASE_FIELDS = {
    "case_id", "pair_id", "provenance", "context", "forecast", "rationale", "generation_record"
}


class StudyInputError(ValueError):
    """Invalid or internally inconsistent case data supplied to the public CLI."""


@dataclass(frozen=True)
class Case:
    case_id: str
    pair_id: str
    provenance: str
    context: dict[str, Any]
    forecast: dict[str, Any]
    rationale: str
    generation_record: dict[str, Any]


def load_cases(path: Path) -> list[Case]:
    """Read JSONL cases and verify exact matching before any blinded output is written."""
    cases: list[Case] = []
    seen_ids: set[str] = set()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise StudyInputError(f"cannot read case manifest {path}: {exc}") from exc
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise StudyInputError(f"line {line_number}: invalid JSON: {exc.msg}") from exc
        if not isinstance(record, dict) or set(record) != CASE_FIELDS:
            raise StudyInputError(f"line {line_number}: expected exactly these fields: {sorted(CASE_FIELDS)}")
        for name in ("case_id", "pair_id", "provenance", "rationale"):
            if not isinstance(record[name], str) or not record[name].strip():
                raise StudyInputError(f"line {line_number}: {name} must be a non-empty string")
        if record["case_id"] in seen_ids:
            raise StudyInputError(f"line {line_number}: duplicate case_id {record['case_id']!r}")
        seen_ids.add(record["case_id"])
        if record["provenance"] not in PROVENANCE:
            raise StudyInputError(f"line {line_number}: provenance must be one of {sorted(PROVENANCE)}")
        if not all(isinstance(record[field], dict) for field in ("context", "forecast", "generation_record")):
            raise StudyInputError(f"line {line_number}: context, forecast, and generation_record must be JSON objects")
        cases.append(Case(**record))
    if not cases:
        raise StudyInputError("case manifest has no cases")
    _validate_pairs(cases)
    return cases


def _validate_pairs(cases: list[Case]) -> dict[str, list[Case]]:
    pairs: dict[str, list[Case]] = defaultdict(list)
    for case in cases:
        pairs[case.pair_id].append(case)
    for pair_id, members in pairs.items():
        if len(members) != 2 or {member.provenance for member in members} != PROVENANCE:
            raise StudyInputError(f"pair {pair_id!r} must contain exactly one case per provenance condition")
        first, second = members
        if first.context != second.context or first.forecast != second.forecast:
            raise StudyInputError(f"pair {pair_id!r} must have identical context and forecast objects")
        if first.rationale == second.rationale:
            raise StudyInputError(f"pair {pair_id!r} has identical rationales")
    return pairs


def write_blinded_packets(
    cases: list[Case], *, packet_dir: Path, key_path: Path, reviewers: int, seed: int
) -> int:
    """Write reviewer-specific shuffled packets and an owner-only source/condition key."""
    if reviewers < 2:
        raise StudyInputError("at least two reviewers are required for counterbalanced assignment")
    pairs = _validate_pairs(cases)
    packet_root = packet_dir.resolve()
    resolved_key = key_path.resolve()
    if resolved_key == packet_root or packet_root in resolved_key.parents:
        raise StudyInputError("the unblinding key must be stored outside the reviewer packet directory")
    if packet_root.exists() or resolved_key.exists():
        raise StudyInputError("packet directory and key path must not already exist")

    rng = random.Random(seed)
    assigned: list[list[tuple[Case, str]]] = [[] for _ in range(reviewers)]
    for members in pairs.values():
        shuffled_members = members.copy()
        reviewer_order = list(range(reviewers))
        rng.shuffle(shuffled_members)
        rng.shuffle(reviewer_order)
        schedule = shuffled_members * (reviewers // 2) + shuffled_members[: reviewers % 2]
        for reviewer_index, case in zip(reviewer_order, schedule):
            token = f"{rng.getrandbits(128):032x}"
            assigned[reviewer_index].append((case, token))

    packet_root.mkdir(parents=True)
    key_records: list[dict[str, str]] = []
    for reviewer_index, reviewer_cases in enumerate(assigned, start=1):
        rng.shuffle(reviewer_cases)
        reviewer_dir = packet_root / f"reviewer-{reviewer_index:02d}"
        reviewer_dir.mkdir()
        packet_path = reviewer_dir / "cases.jsonl"
        with packet_path.open("x", encoding="utf-8") as packet_file:
            for case, token in reviewer_cases:
                packet_file.write(json.dumps({
                    "case_token": token,
                    "context": case.context,
                    "forecast": case.forecast,
                    "rationale": case.rationale,
                }, ensure_ascii=False, separators=(",", ":")) + "\n")
                key_records.append({
                    "reviewer": f"reviewer-{reviewer_index:02d}",
                    "case_token": token,
                    "case_id": case.case_id,
                    "pair_id": case.pair_id,
                    "provenance": case.provenance,
                    "generation_record": case.generation_record,
                })

    resolved_key.parent.mkdir(parents=True, exist_ok=True)
    with resolved_key.open("x", encoding="utf-8") as key_file:
        json.dump({"seed": seed, "reviewers": reviewers, "assignments": key_records}, key_file, ensure_ascii=False, indent=2)
        key_file.write("\n")
    os.chmod(resolved_key, 0o600)
    return len(pairs)
