"""Executive summary: freeze unused-company/context questions without using answer values."""

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "outputs/finance-document-audit-v1"
OUT = ROOT / "outputs/finance-quantity-transfer-v1"
SALT = "finance-quantity-transfer-v1-20260930"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def company(row):
    return row["native_report_id"].split("/")[0]


def inputs():
    manifest = json.loads((OLD / "selection_manifest.json").read_text())
    for name in ("admitted_pool_metadata.jsonl", "selection_metadata.jsonl", "reviewer_a.jsonl"):
        if digest(OLD / name) != manifest["artifacts_sha256"][name]:
            raise ValueError("Original cohort input changed: " + name)
    ingestion = json.loads((OLD / "ingestion_manifest.json").read_text())
    for artifact in ingestion["artifacts"]:
        if digest(ROOT / artifact["path"]) != artifact["sha256"]:
            raise ValueError("Pinned original source changed")
    return rows(OLD / "admitted_pool_metadata.jsonl"), rows(OLD / "selection_metadata.jsonl")


def select(pool, old):
    contexts = {r["context_sha256"] for r in old}
    questions = {r["question_sha256"] for r in old}
    companies = {company(r) for r in old if r["source"] == "finqa"}
    tat_groups = {r["group_id"] for r in old if r["source"] == "tatqa"}
    selected, counts = [], {}
    for source in ("finqa", "tatqa"):
        candidates = []
        for row in pool:
            if row["source"] != source or row["context_sha256"] in contexts or row["question_sha256"] in questions:
                continue
            if source == "finqa" and company(row) in companies or source == "tatqa" and row["group_id"] in tat_groups:
                continue
            order = hashlib.sha256(canonical([SALT, source, row["native_id"], row["question_sha256"]]).encode()).hexdigest()
            candidates.append({**row, "followup_order_sha256": order})
        groups, chosen = set(), []
        for row in sorted(candidates, key=lambda r: (r["followup_order_sha256"], r["native_id"])):
            group = company(row) if source == "finqa" else row["group_id"]
            if group in groups or row["context_sha256"] in contexts or row["question_sha256"] in questions:
                continue
            chosen.append(row)
            groups.add(group)
            contexts.add(row["context_sha256"])
            questions.add(row["question_sha256"])
            if len(chosen) == 16:
                break
        if len(chosen) != 16:
            raise ValueError("Frozen grouping cannot supply 16 questions: " + source)
        selected.extend(chosen)
        counts[source] = {"eligible_rows_before_group_cap": len(candidates), "selected": len(chosen)}
    return selected, counts


def packets(selected):
    finqa = {r["id"]: r for r in json.loads((OLD / "raw/finqa/dataset/test.json").read_text())}
    tatqa = {}
    for context in json.loads((OLD / "raw/tatqa/dataset_raw/tatqa_dataset_test.json").read_text()):
        for question in context["questions"]:
            tatqa[question["uid"]] = (context, question)
    result = []
    for row in selected:
        if row["source"] == "finqa":
            original = finqa[row["native_id"]]
            question = original["qa"]["question"]
            context = {k: original[k] for k in ("pre_text", "table", "post_text")}
        else:
            original, q = tatqa[row["native_id"]]
            question = q["question"]
            context = {"table": {k: original["table"][k] for k in ("uid", "table")},
                       "paragraphs": [{k: p[k] for k in ("uid", "order", "text")} for p in original["paragraphs"]]}
        result.append({"case_id": row["source"] + ":" + row["native_id"], "source": row["source"],
                       "question": question, "original_context": context})
    return result


def main():
    pool, old = inputs()
    selected, counts = select(pool, old)
    packet = packets(selected)
    local = rows(ROOT / "outputs/finance-local-interface-v1/selection.jsonl")
    old_ids = {r["source"] + ":" + r["native_id"] for r in old}
    if not {r["case_id"] for r in local} <= old_ids:
        raise ValueError("Earlier local pilot has additional exclusion cases")
    assert len(packet) == len({r["case_id"] for r in packet}) == 32
    OUT.mkdir(exist_ok=False)
    for name, records in (("selection_metadata.jsonl", selected), ("question_packet.jsonl", packet)):
        with (OUT / name).open("x") as stream:
            stream.write("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n")
    names = ["docs/FINANCE_QUANTITY_TRANSFER_COHORT_PROTOCOL_V1.md", "scripts/prepare_finance_quantity_transfer.py",
             "outputs/finance-document-audit-v1/selection_manifest.json",
             "outputs/finance-document-audit-v1/ingestion_manifest.json",
             "outputs/finance-document-audit-v1/selection_metadata.jsonl",
             "outputs/finance-document-audit-v1/admitted_pool_metadata.jsonl",
             "outputs/finance-local-interface-v1/selection.jsonl"]
    names += [str(p.relative_to(ROOT)) for p in OUT.iterdir()]
    freeze = {"executive_summary": "Unused-company FinQA and unused-context TAT cohort, selected without answer values.",
              "created_utc": datetime.now(timezone.utc).isoformat(), "salt": SALT, "counts": counts,
              "old_union_exclusions": len(old_ids), "reference_reviews_seen": False,
              "source_targets_unblinded": False, "model_requests": 0,
              "source_counts": dict(Counter(r["source"] for r in packet)),
              "files_sha256": {name: digest(ROOT / name) for name in sorted(names)}}
    with (OUT / "cohort_freeze.json").open("x") as stream:
        json.dump(freeze, stream, indent=2); stream.write("\n")
    print(json.dumps({"cases": len(packet), "counts": counts, "freeze_sha256": digest(OUT / "cohort_freeze.json")}))


if __name__ == "__main__":
    main()
