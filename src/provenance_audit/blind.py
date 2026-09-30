"""Executive summary: validate matched cases and assign one hidden condition per selected reviewer and pair."""

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
    cases: list[Case], *, packet_dir: Path, key_path: Path, reviewers: int, seed: int,
    reviewers_per_pair: int | None = None,
) -> int:
    """Write balanced reviewer packets and an owner-only source/condition key."""
    if reviewers < 2:
        raise StudyInputError("at least two reviewers are required for counterbalanced assignment")
    pair_reviewers = reviewers if reviewers_per_pair is None else reviewers_per_pair
    if pair_reviewers < 2 or pair_reviewers > reviewers:
        raise StudyInputError("reviewers_per_pair must be between 2 and the total reviewer count")
    pairs = _validate_pairs(cases)
    packet_root = packet_dir.resolve()
    resolved_key = key_path.resolve()
    if resolved_key == packet_root or packet_root in resolved_key.parents:
        raise StudyInputError("the unblinding key must be stored outside the reviewer packet directory")
    if packet_root.exists() or resolved_key.exists():
        raise StudyInputError("packet directory and key path must not already exist")

    rng = random.Random(seed)
    assigned: list[list[tuple[Case, str]]] = [[] for _ in range(reviewers)]
    reviewer_load = [0] * reviewers
    derived_load = [0] * reviewers
    condition_totals = {"derived": 0, "answer_first": 0}
    for members in pairs.values():
        reviewer_order = list(range(reviewers))
        rng.shuffle(reviewer_order)
        reviewer_order.sort(key=lambda index: reviewer_load[index])
        selected_reviewers = reviewer_order[:pair_reviewers]

        derived_count = pair_reviewers // 2
        if pair_reviewers % 2 and condition_totals["derived"] <= condition_totals["answer_first"]:
            derived_count += 1
        condition_order = selected_reviewers.copy()
        rng.shuffle(condition_order)
        condition_order.sort(key=lambda index: derived_load[index])
        derived_reviewers = set(condition_order[:derived_count])
        by_condition = {case.provenance: case for case in members}

        for reviewer_index in selected_reviewers:
            condition = "derived" if reviewer_index in derived_reviewers else "answer_first"
            case = by_condition[condition]
            token = f"{rng.getrandbits(128):032x}"
            assigned[reviewer_index].append((case, token))
            reviewer_load[reviewer_index] += 1
            condition_totals[condition] += 1
            if condition == "derived":
                derived_load[reviewer_index] += 1

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
    key_fd = os.open(resolved_key, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(key_fd, "w", encoding="utf-8") as key_file:
        json.dump({"seed": seed, "reviewers": reviewers, "assignments": key_records}, key_file, ensure_ascii=False, indent=2)
        key_file.write("\n")
    return len(pairs)
