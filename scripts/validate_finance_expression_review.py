"""Executive summary: lock structural checks without certifying semantic judgments."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from financial_review_io import digest, review_record, rows

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/finance-expression-review-v1"
FIELDS = {
    "review_id", "status", "requested_quantity", "entity", "time_scope", "assumptions",
    "operand_bindings", "unit_assessment", "reference_expression", "rationale", "evidence_paths",
}
STATUSES = {"supported", "contradicted", "ambiguous", "unresolved"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reviewer", choices=("a", "b"))
    args = parser.parse_args()
    freeze = json.loads((OUT / "freeze.json").read_text())
    for path, expected in freeze["files_sha256"].items():
        if digest(ROOT / path) != expected:
            raise ValueError("Frozen review input changed: " + path)
    packet = {r["review_id"]: r for r in rows(OUT / "review_packet.jsonl")}
    path = OUT / ("review_" + args.reviewer + ".jsonl")
    reviewed = rows(path)
    if len(reviewed) != 131 or {r["review_id"] for r in reviewed} != set(packet):
        raise ValueError("Review membership incomplete or duplicated")
    count = 0
    for record in reviewed:
        check = review_record(record, packet[record["review_id"]], FIELDS, STATUSES, "review_id")
        if not isinstance(record["unit_assessment"], str) or not record["unit_assessment"].strip():
            raise ValueError("Missing unit assessment")
        count += check["source_pointers_checked"]
    receipt = {
        "executive_summary": "PASS: review identity/schema/pointers/arithmetic; no semantic or expert certification.",
        "created_utc": datetime.now(timezone.utc).isoformat(), "reviewer": args.reviewer,
        "review_sha256": digest(path), "freeze_sha256": digest(OUT / "freeze.json"),
        "records": len(reviewed), "source_pointers_checked": count,
        "validator_sha256": digest(__file__),
        "helper_sha256": digest(ROOT / "src/financial_review_io.py"),
        "expert_adjudication": False, "private_outcome_key_read": False,
    }
    with (OUT / ("validation_" + args.reviewer + ".json")).open("x") as stream:
        json.dump(receipt, stream, indent=2); stream.write("\n")
    print(json.dumps({"reviewer": args.reviewer, "records": len(reviewed),
                      "source_pointers_checked": count, "status": "PASS"}))


if __name__ == "__main__":
    main()
