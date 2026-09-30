"""Executive summary: prepare all eight frozen financial cases for a fresh, answer-blind human reviewer."""

import hashlib
import json
import os

from grader_comparison.protocol import ROOT, frozen, digest, jsonl, write, now


def main():
    rows = [r for r in frozen() if r["domain"] == "finance"]
    if len(rows) != 8 or len({r["id"] for r in rows}) != 8:
        raise ValueError("Financial review denominator changed")
    destination = ROOT / "outputs/finance-human-core-review-v1"
    destination.mkdir(exist_ok=False)
    packet, key, form = [], [], []
    for row in rows:
        review_id = hashlib.sha256(("financial-core-human-v1|" + row["id"]).encode()).hexdigest()[:16]
        packet.append({"review_id": review_id, "question": row["prompt"]})
        key.append({"review_id": review_id, "case_id": row["id"]})
        form.append({"review_id": review_id, "status": "", "requested_quantity": "",
                     "unit": "", "value": "", "derivation": "", "assumptions": [],
                     "rounding_instruction": "", "admissible_final_values": [],
                     "uncertainty": "", "prior_exposure": ""})
    packet.sort(key=lambda r: r["review_id"])
    form.sort(key=lambda r: r["review_id"])
    jsonl(destination / "question_only_packet.jsonl", packet)
    jsonl(destination / "blank_review_form.jsonl", form)
    fd = os.open(destination / "private_case_map.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as stream:
        json.dump(key, stream, indent=2)
    instructions = ("# Blinded financial question review\n\n"
        "Interpret and solve every question before viewing any released label, model answer or study result. "
        "Record relevant financial expertise, tools used, start/end times and previous exposure. "
        "The preparer has seen these cases; their frozen cohort was selected before model generation, "
        "but it is mechanism focused rather than population representative.\n\n"
        "For each case record the requested financial quantity, formula/derivation, units, compounding "
        "assumptions and rounding instructions. Use determinate, conditional, ambiguous or insufficient "
        "as the status. Preserve uncertainty and alternative defensible interpretations. Do not infer "
        "an intended answer from an unseen label. Return the complete original form and lock/hash it "
        "before any comparison is revealed. This is review of final numerical meaning, not certification "
        "of every source reasoning trace.\n\n")
    sheet = instructions
    for row in packet:
        sheet += f"## Case {row['review_id']}\n\n{row['question']}\n\n"
    (destination / "review_sheet.md").write_text(sheet)
    write(destination / "reviewer_metadata_blank.json", {"reviewer_name_or_pseudonym": "",
          "qualifications": "", "relevant_financial_expertise": "", "prior_exposure": "",
          "tools_used": [], "started_utc": "", "completed_utc": ""})
    write(destination / "receipt.json", {"prepared_utc": now(), "questions": 8,
          "cohort_freeze_sha256": digest(ROOT / "outputs/grader-comparison-v1/freeze.json"),
          "preparer_has_prior_exposure": True, "reviewer_recruited": False,
          "human_annotations_completed": False,
          "files": {p.name: digest(p) for p in destination.iterdir() if p.is_file()}})
    print(json.dumps({"prepared": 8, "human_reviews_completed": 0,
                      "review_sheet": str(destination / "review_sheet.md")}))


if __name__ == "__main__":
    main()
