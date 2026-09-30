"""Executive summary: freeze outcome-masked posthoc review of all eligible saved expressions."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/finance-expression-review-v1"
DIAGNOSTICS = ROOT / "outputs/finance-document-diagnostics-v1"
SALT = "finance-expression-semantic-v1-20260930"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def write(name, records):
    with (OUT / name).open("x") as stream:
        for row in records:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    for name in ("protocol_freeze.json", "implementation_freeze.json"):
        frozen = json.loads((DIAGNOSTICS / name).read_text())
        for path, expected in frozen["files_sha256"].items():
            if digest(ROOT / path) != expected:
                raise ValueError("Original frozen diagnostic input changed: " + path)
    diagnostics = rows(DIAGNOSTICS / "rows.jsonl")
    packets = {
        row["case_id"]: row
        for row in rows(ROOT / "outputs/finance-document-audit-v1/reviewer_a.jsonl")
    }
    selected = [
        row for row in diagnostics
        if row["arithmetic"]["supported"] and row["recovered_locked"]["eligible"]
    ]
    if len(diagnostics) != 384 or len(selected) != 131:
        raise ValueError("Original review membership changed")
    OUT.mkdir(exist_ok=False)
    review, key = [], []
    for row in selected:
        identity = json.dumps([SALT, row["effective_ledger_line"]])
        review_id = "expr-" + hashlib.sha256(identity.encode()).hexdigest()[:16]
        packet = packets[row["case_id"]]
        candidate = row["recovered_candidate"]
        review.append({
            "review_id": review_id, "source": row["source"],
            "question": packet["question"],
            "original_context": packet["original_context"],
            "calculation": candidate["calculation"],
            "reported_unit": candidate["unit"], "reported_scale": candidate["scale"],
            "model_evidence": candidate["evidence"],
        })
        key.append({"review_id": review_id, "case_id": row["case_id"],
                    "effective_ledger_line": row["effective_ledger_line"]})
    review.sort(key=lambda r: r["review_id"])
    key.sort(key=lambda r: r["review_id"])
    write("review_packet.jsonl", review)
    write("private_join_key.jsonl", key)
    by_case = {row["case_id"]: packets[row["case_id"]] for row in selected}
    human = []
    for case_id, packet in sorted(by_case.items()):
        human_id = "question-" + hashlib.sha256((SALT + case_id).encode()).hexdigest()[:16]
        human.append({"review_id": human_id, "question": packet["question"],
                      "original_context": packet["original_context"]})
    write("human_question_only_packet.jsonl", human)
    bindings = [
        "docs/FINANCE_EXPRESSION_SEMANTIC_REVIEW_PROTOCOL_V1.md",
        "scripts/prepare_finance_expression_review.py",
        "outputs/finance-document-diagnostics-v1/rows.jsonl",
        "outputs/finance-document-audit-v1/reviewer_a.jsonl",
    ]
    bindings += [str(path.relative_to(ROOT)) for path in OUT.iterdir()]
    frozen = {
        "executive_summary": "Posthoc outcome-masked technical review; original scoring unchanged.",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "expressions": len(review), "unique_questions": len(human),
        "original_attempts": len(diagnostics), "salt": SALT,
        "reviewer_results_seen": False, "expert_adjudication": False,
        "files_sha256": {name: digest(ROOT / name) for name in sorted(bindings)},
    }
    with (OUT / "freeze.json").open("x") as stream:
        json.dump(frozen, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"expressions": len(review), "unique_questions": len(human),
                      "freeze_sha256": digest(OUT / "freeze.json")}))


if __name__ == "__main__":
    main()
