"""Executive summary: verify frozen packet coverage and arithmetic, without opening native targets."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from .arithmetic import calculate

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "outputs/finance-document-review-v1"
FIELDS = {
    "case_id", "reviewer", "review_status", "requested_quantity", "evidence",
    "operands", "expression", "answer_values", "answer_unit", "requested_precision",
    "rounding_policy", "assumptions", "alternative_interpretations", "confidence", "notes",
}
STATUSES = {"determinate", "conditional", "insufficient_information", "unresolved"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def validate(reviewer: str) -> dict:
    if reviewer not in {"a", "b"}:
        raise ValueError("Reviewer must be a or b")
    freeze = json.loads((OUTPUT / "stage_freeze.json").read_text())
    for relative, expected in freeze["files_sha256"].items():
        if digest(ROOT / relative) != expected:
            raise ValueError(f"Review-stage frozen input changed: {relative}")
    packet = ROOT / f"outputs/finance-document-audit-v1/reviewer_{reviewer}.jsonl"
    expected_ids = {row["case_id"] for row in read_rows(packet)}
    path = OUTPUT / f"review_{reviewer}.jsonl"
    rows = read_rows(path)
    ids = [row["case_id"] for row in rows]
    if len(rows) != 96 or len(set(ids)) != 96 or set(ids) != expected_ids:
        raise ValueError("Review does not cover all 96 original cases exactly once")
    calculations, arithmetic_errors, projections = [], [], []
    for row in rows:
        missing = FIELDS - row.keys()
        if missing or row["reviewer"] != reviewer or row["review_status"] not in STATUSES:
            raise ValueError(f"Invalid required review fields: {row['case_id']}, {sorted(missing)}")
        if row["confidence"] not in {"high", "medium", "low"}:
            raise ValueError(f"Invalid confidence: {row['case_id']}")
        if not isinstance(row["answer_values"], list):
            raise ValueError(f"Answer values must be a list: {row['case_id']}")
        values = [Decimal(value) for value in row["answer_values"]]
        if any(not value.is_finite() for value in values):
            raise ValueError(f"Nonfinite answer: {row['case_id']}")
        if row["review_status"] in {"determinate", "conditional"} and (
            not values or not row["answer_unit"] or not row["evidence"]
        ):
            raise ValueError(f"Missing independently supported answer: {row['case_id']}")
        if row["expression"]:
            try:
                computed = calculate(row["expression"])
                difference = min(abs(value - computed) for value in values)
                calculations.append({"case_id": row["case_id"], "calculated": str(computed),
                                     "minimum_answer_difference": str(difference)})
                if difference > Decimal("1e-12") * max(Decimal(1), abs(computed)):
                    projections.append({"case_id": row["case_id"], "difference": str(difference),
                                        "rounding_policy": row["rounding_policy"],
                                        "requested_precision": row["requested_precision"]})
            except (ArithmeticError, ValueError, SyntaxError) as error:
                arithmetic_errors.append({"case_id": row["case_id"], "error": str(error)})
        elif values:
            raise ValueError(f"Numeric answer without reproducible expression: {row['case_id']}")
    return {
        "executive_summary": "All original cases and declared review fields checked without native targets; projections and arithmetic exceptions remain explicit.",
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS_COVERAGE_AND_SCHEMA" if not arithmetic_errors else "ARITHMETIC_EXCEPTIONS",
        "reviewer": reviewer, "cases": len(rows), "packet_sha256": digest(packet),
        "review_sha256": digest(path), "stage_freeze_sha256": digest(OUTPUT / "stage_freeze.json"),
        "statuses": dict(Counter(row["review_status"] for row in rows)),
        "source_cases": dict(Counter(row["case_id"].split(":", 1)[0] for row in rows)),
        "calculations": calculations, "arithmetic_errors": arithmetic_errors,
        "reported_output_projection_checks": projections, "native_targets_accessed": False,
        "limits": ["Arithmetic agreement is not semantic correctness or human expert review.",
                   "Reported rounding projections require explicit interpretation; no answer was silently changed."]
    }
