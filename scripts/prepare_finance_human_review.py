"""Executive summary: prepare all 32 questions for a fresh financial reviewer without AI targets or outcomes.

The local packet preserves original questions and contexts. Salted review IDs hide
case identities; the private mapping and blank response form remain separate.
Preparing a packet neither recruits a reviewer nor creates human annotations.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "outputs/finance-quantity-transfer-v1/question_packet.jsonl"
FREEZE = ROOT / "outputs/finance-quantity-transfer-v1/cohort_freeze.json"
OUT = ROOT / "outputs/finance-human-review-v1"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_rows(path, rows):
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows))


def main():
    source_hash = digest(SOURCE)
    frozen = json.loads(FREEZE.read_text())
    # The exact source packet is already part of the original cohort commitment.
    if source_hash not in json.dumps(frozen):
        raise ValueError("Question-only packet is not bound by the cohort freeze")
    rows = [json.loads(line) for line in SOURCE.read_text().splitlines()]
    if len(rows) != 32 or len({r["case_id"] for r in rows}) != 32:
        raise ValueError("Exactly all 32 distinct questions are required")
    OUT.mkdir(exist_ok=False)
    packet, mapping, form = [], [], []
    for row in rows:
        review_id = hashlib.sha256(("finance-human-review-v1:" + row["case_id"]).encode()).hexdigest()[:20]
        packet.append({"review_id": review_id, "question": row["question"],
                       "original_context": row["original_context"]})
        mapping.append({"review_id": review_id, "case_id": row["case_id"], "source": row["source"]})
        form.append({"review_id": review_id, "status": "", "requested_quantity": "",
                     "entity": "", "time": "", "value": "", "unit": "", "scale": "",
                     "calculation": "", "operands": [], "assumptions": [],
                     "uncertainty_reason": "", "rationale": ""})
    packet.sort(key=lambda r: r["review_id"])
    form.sort(key=lambda r: r["review_id"])
    write_rows(OUT / "question_only_packet.jsonl", packet)
    write_rows(OUT / "private_case_map.jsonl", mapping)
    write_rows(OUT / "blank_review_form.jsonl", form)
    receipt = {"executive_summary": "Prepared, not reviewed: all 32 cases; no AI references, labels or generated answers provided.",
               "created_utc": datetime.now(timezone.utc).isoformat(), "questions": 32,
               "source_packet_sha256": source_hash, "cohort_freeze_sha256": digest(FREEZE),
               "preparer_has_prior_case_exposure": True, "reviewer_recruited": False,
               "human_annotations_completed": False,
               "files_sha256": {p.name: digest(p) for p in OUT.glob("*.jsonl")}}
    (OUT / "preparation_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
