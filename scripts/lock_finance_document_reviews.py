"""Executive summary: combine complete independent reviews and lock them before native targets."""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal

from finance_document_review.review_validation import OUTPUT, ROOT, digest, read_rows, validate
from finance_document_review.units import canonical_values, compatible_units, signature


def main() -> None:
    lock_path = OUTPUT / "pre_target_lock.json"
    if lock_path.exists():
        raise ValueError("Existing pre-target lock; original interpretation must not be rewritten")
    paths = []
    indexed = {}
    for reviewer in ["a", "b"]:
        result = validate(reviewer)
        if result["arithmetic_errors"]:
            raise ValueError("Reviewer arithmetic exceptions remain unresolved")
        path = OUTPUT / f"review_{reviewer}.jsonl"
        receipt = OUTPUT / f"review_{reviewer}_receipt.json"
        receipt_data = json.loads(receipt.read_text())
        expected = receipt_data.get("output_sha256", receipt_data.get("review_sha256"))
        if expected != digest(path):
            raise ValueError(f"Reviewer {reviewer} receipt does not match completed review")
        indexed[reviewer] = {row["case_id"]: row for row in read_rows(path)}
        paths.extend([path, receipt])
    packet_path = ROOT / "outputs/finance-document-audit-v1/reviewer_a.jsonl"
    records = []
    for packet in read_rows(packet_path):
        case_id = packet["case_id"]
        a, b = indexed["a"][case_id], indexed["b"][case_id]
        unit_a, unit_b = signature(a["answer_unit"]), signature(b["answer_unit"])
        values_a, values_b = canonical_values(a["answer_values"], unit_a), canonical_values(b["answer_values"], unit_b)
        value_agreement = bool(values_a and values_b and compatible_units(unit_a, unit_b)) and any(
            abs(first - second) <= max(Decimal("1e-12"), abs(first) * Decimal("1e-10"),
                                      abs(second) * Decimal("1e-10"))
            for first in values_a for second in values_b
        )
        # Original question form establishes this one nonnumeric case, before annotation access.
        boolean = case_id == "finqa:PPG/2018/page_85.pdf-1"
        if boolean:
            status = "nonnumeric_boolean"
        elif a["review_status"] == b["review_status"] == "insufficient_information":
            status = "agreed_insufficient_information"
        elif "insufficient_information" in {a["review_status"], b["review_status"]}:
            status = "disputed_information_sufficiency"
        elif "unresolved" in {a["review_status"], b["review_status"]}:
            status = "unresolved"
        elif not value_agreement:
            status = "disputed_numeric_or_units"
        elif unit_a.get("scale_unspecified") or unit_b.get("scale_unspecified"):
            status = "agreed_numeric_scale_unspecified"
        elif a["review_status"] == b["review_status"] == "determinate":
            status = "agreed_determinate_numeric"
        else:
            status = "agreed_numeric_conditional"
        records.append({"case_id": case_id, "source": case_id.split(":", 1)[0],
                        "joint_status": status, "value_agreement": bool(value_agreement),
                        "review_a_status": a["review_status"], "review_b_status": b["review_status"],
                        "unit_a": unit_a, "unit_b": unit_b,
                        "canonical_values_a": [str(value) for value in values_a],
                        "canonical_values_b": [str(value) for value in values_b],
                        "reference_expression": a["expression"],
                        "reference_values": a["answer_values"],
                        "reference_unit": a["answer_unit"],
                        "requested_quantity_a": a["requested_quantity"],
                        "requested_quantity_b": b["requested_quantity"],
                        "semantic_agreement_certified": False,
                        "nonnumeric_pre_target_answer": "yes" if boolean else None})
    combined_path = OUTPUT / "pre_target_combined.jsonl"
    with combined_path.open("x") as stream:
        for row in records:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    paths.extend([combined_path, packet_path, OUTPUT / "stage_freeze.json",
                  OUTPUT / "comparison_protocol_freeze.json",
                  ROOT / "docs/FINANCE_DOCUMENT_COMPARISON_PROTOCOL_V1.md",
                  ROOT / "src/finance_document_review/units.py",
                  ROOT / "scripts/lock_finance_document_reviews.py"])
    result = {"executive_summary": "Completed independent technical reviews combined and hash-locked before native targets or scientific model responses; no human semantic certification.",
              "created_utc": datetime.now(timezone.utc).isoformat(), "cases": len(records),
              "files_sha256": {str(path.relative_to(ROOT)): digest(path) for path in paths},
              "status_counts": dict(Counter(row["joint_status"] for row in records)),
              "source_status_counts": {source: dict(Counter(row["joint_status"] for row in records
                                         if row["source"] == source)) for source in ["finqa", "tatqa"]},
              "native_targets_accessed": False, "model_responses_accessed": False,
              "independent_semantic_or_human_adjudication_completed": False,
              "limits": ["Numeric/unit agreement is a technical endpoint, not proof the two requested-quantity descriptions are semantically identical.",
                         "Conditional and disputed interpretations remain outside agreed-determinate numerical comparisons.",
                         "Canonical units use original reviewer descriptions and no native target fitting."]}
    with lock_path.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps({key: result[key] for key in ["created_utc", "cases", "status_counts", "source_status_counts"]}, indent=2))


if __name__ == "__main__":
    main()
