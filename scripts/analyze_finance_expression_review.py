"""Executive summary: aggregate locked AI expression reviews without revising scores."""

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from finance_document_review.arithmetic import calculate
from financial_review_io import digest, rows

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/finance-expression-review-v1"
DIAG = ROOT / "outputs/finance-document-diagnostics-v1/rows.jsonl"
STATUSES = ("supported", "contradicted", "ambiguous", "unresolved")


def write(name, value, jsonl=False):
    with (OUT / name).open("x") as stream:
        if jsonl:
            for record in value:
                stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        else:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")


def category(a, b):
    if "contradicted" in (a, b):
        return "contradicted_either"
    if a == b == "supported":
        return "supported_both"
    if a == b:
        return "consensus_" + a
    return "status_disagreement"


def summarize(records):
    cross = {a: {b: 0 for b in STATUSES} for a in STATUSES}
    binary = {a: {b: 0 for b in ("supported", "not_supported")}
              for a in ("supported", "not_supported")}
    for record in records:
        a, b = record["review_a"]["status"], record["review_b"]["status"]
        cross[a][b] += 1
        binary["supported" if a == "supported" else "not_supported"][
            "supported" if b == "supported" else "not_supported"] += 1
    counts = Counter(r["joint_category"] for r in records)
    return {
        "expressions": len(records),
        "unique_questions": len({r["case_id"] for r in records}),
        "reviewer_status_cross_table": cross,
        "reviewer_support_2x2": binary,
        "joint_categories": dict(counts),
        "unique_questions_by_category_nonexclusive": {
            c: len({r["case_id"] for r in records if r["joint_category"] == c})
            for c in sorted(counts)},
        "status_disagreements": sum(r["review_a"]["status"] != r["review_b"]["status"]
                                    for r in records),
        "ambiguous_or_unresolved_either": sum(
            any(r[reviewer]["status"] in ("ambiguous", "unresolved")
                for reviewer in ("review_a", "review_b")) for r in records),
    }


def main():
    started = datetime.now(timezone.utc).isoformat()
    lock = json.loads((OUT / "joint_review_lock.json").read_text())
    for path, expected in lock["files_sha256"].items():
        assert digest(ROOT / path) == expected, path
    freeze = json.loads((OUT / "freeze.json").read_text())
    for path, expected in freeze["files_sha256"].items():
        assert digest(ROOT / path) == expected, path
    # Private contents are loaded only after the immutable joint lock verifies.
    key = rows(OUT / "private_join_key.jsonl")
    diagnostics = rows(DIAG)
    packet = {r["review_id"]: r for r in rows(OUT / "review_packet.jsonl")}
    reviews = [{r["review_id"]: r for r in rows(OUT / f"review_{a}.jsonl")}
               for a in ("a", "b")]
    assert len(diagnostics) == 384
    by_line = {r["effective_ledger_line"]: r for r in diagnostics}
    assert set(by_line) == set(range(1, 385))
    selected = {r["effective_ledger_line"] for r in diagnostics
                if r["arithmetic"]["supported"] and r["recovered_locked"]["eligible"]}
    assert len(key) == len(packet) == len(reviews[0]) == len(reviews[1]) == 131
    assert {r["effective_ledger_line"] for r in key} == selected
    assert len({r["review_id"] for r in key}) == 131
    assert set(packet) == set(reviews[0]) == set(reviews[1]) == {r["review_id"] for r in key}
    joined = []
    for entry in key:
        rid, line = entry["review_id"], entry["effective_ledger_line"]
        d, p = by_line[line], packet[rid]
        expected_id = hashlib.sha256(json.dumps([freeze["salt"], line]).encode()).hexdigest()[:16]
        assert rid == "expr-" + expected_id and entry["case_id"] == d["case_id"]
        c = d["recovered_candidate"]
        assert (p["calculation"], p["reported_unit"], p["reported_scale"], p["model_evidence"]) == (
            c["calculation"], c["unit"], c["scale"], c["evidence"])
        assert p["source"] == d["source"]
        executed = calculate(p["calculation"])
        assert executed == Decimal(d["arithmetic"]["executed_value"])
        a, b = reviews[0][rid], reviews[1][rid]
        reported_match = d["recovered_locked"]["matches"]
        executed_match = d["arithmetic"]["locked_comparator"]["matches"]
        assert isinstance(reported_match, bool) and isinstance(executed_match, bool)
        joined.append({
            **entry, "diagnostic_jsonl_line": diagnostics.index(d) + 1,
            "source": d["source"], "model_key": d["model_key"], "condition": d["condition"],
            "question": p["question"], "calculation": p["calculation"],
            "reported_unit": p["reported_unit"], "reported_scale": p["reported_scale"],
            "reported_value": c["value"], "executed_value": str(executed),
            "original_reported_locked_match": reported_match,
            "original_executed_locked_match": executed_match,
            "numeric_mismatch_to_expression_match": not reported_match and executed_match,
            "review_a": a, "review_b": b,
            "reference_values": {
                k: str(calculate(r["reference_expression"])) if r["reference_expression"] else None
                for k, r in (("a", a), ("b", b))},
            "joint_category": category(a["status"], b["status"]),
            "context_reference": "outputs/finance-expression-review-v1/review_packet.jsonl#" + rid,
            "semantic_truth_certified": False,
        })
    transitions = [r for r in joined if r["numeric_mismatch_to_expression_match"]]
    others = [r for r in joined if not r["numeric_mismatch_to_expression_match"]]
    numerical_cells = Counter(
        f'{r["original_reported_locked_match"]}->{r["original_executed_locked_match"]}'
        for r in joined)
    assert numerical_cells == {"False->True": 47, "True->True": 41, "False->False": 43}
    all_stats, transition_stats, other_stats = map(summarize, (joined, transitions, others))
    assert all_stats["joint_categories"] == {
        "supported_both": 104, "contradicted_either": 14,
        "consensus_ambiguous": 3, "status_disagreement": 10}
    assert transition_stats["joint_categories"] == {"supported_both": 41, "status_disagreement": 6}
    groups = defaultdict(list)
    for record in joined:
        groups[record["case_id"]].append(record)
    clusters = [{"case_id": c, "question": rs[0]["question"],
                 "review_ids": [r["review_id"] for r in rs], **summarize(rs)}
                for c, rs in sorted(groups.items())]
    assert len(clusters) == 58 and transition_stats["unique_questions"] == 24
    stratified = {}
    for field in ("source", "model_key", "condition"):
        stratified[field] = {
            value: {"all_reviewed": summarize([r for r in joined if r[field] == value]),
                    "numeric_transitions": summarize([r for r in transitions if r[field] == value]),
                    "original_attempts": sum(d[field] == value for d in diagnostics)}
            for value in sorted({r[field] for r in joined})}
    results = {
        "executive_summary": "41 of 47 numeric transitions have consensus AI technical support under assumptions; six retain interpretation disagreement. No expert semantic truth certification.",
        "created_utc": datetime.now(timezone.utc).isoformat(), "posthoc": True,
        "original_attempt_denominator": 384, "whole_expression_supported_original": sum(
            d["arithmetic"]["supported"] for d in diagnostics),
        "reviewed_expression_denominator": 131, "outside_review_subset": 253,
        "joint_review_lock_sha256": digest(OUT / "joint_review_lock.json"),
        "all_reviewed": all_stats, "numeric_transitions": transition_stats,
        "other_84_records": other_stats, "numeric_transition_cells": dict(numerical_cells),
        "by_numeric_cell": {cell: summarize([r for r in joined if
            f'{r["original_reported_locked_match"]}->{r["original_executed_locked_match"]}' == cell])
            for cell in sorted(numerical_cells)},
        "question_cluster_multiplicity": dict(sorted(Counter(len(rs) for rs in groups.values()).items())),
        "questions_all_reviewed_expressions_supported_both": sum(
            all(r["joint_category"] == "supported_both" for r in rs) for rs in groups.values()),
        "stratified_descriptive_only": stratified,
        "uncertain_transition_cases": sorted({r["case_id"] for r in transitions
                                               if r["joint_category"] != "supported_both"}),
        "limitations": [
            "Both reviewers are AI assistants with disclosed prior study exposure; masking does not establish historical blinding or independent conceptual errors.",
            "Question clusters overlap categories; 131 expression records are not 131 independent questions.",
            "Reported-to-executed transitions retain the locked unrounded broad-unit comparator and do not certify financially correct final answers.",
            "Supported means defensible under assumptions, including displayed precision and interpretation of monetary magnitude declarations.",
            "The original baseline/reminder calculation-format confound and selection into the whole-expression subset remain.",
            "No inference, scoring/parser change, expert adjudication or repair of original outputs occurred.",
        ],
    }
    write("semantic_joined_rows.jsonl", joined, True)
    write("question_clusters.json", clusters)
    write("semantic_results.json", results)
    receipt = {
        "executive_summary": "PASS: immutable review hashes, full membership, original outcome joins and numerical aggregation assertions; no semantic truth certification.",
        "started_utc": started, "completed_utc": datetime.now(timezone.utc).isoformat(),
        "joint_lock_precedes_this_analysis": lock["created_utc"] < started,
        "outcome_unmasking_note": "First exploratory join was read only after the joint lock completed; this script reproduces that post-lock aggregation.",
        "command": "PYTHONPATH=src .venv/bin/python scripts/analyze_finance_expression_review.py",
        "code_sha256": digest(__file__),
        "input_sha256": {str(p.relative_to(ROOT)): digest(p) for p in (
            OUT / "joint_review_lock.json", OUT / "private_join_key.jsonl", DIAG)},
        "output_sha256": {"outputs/finance-expression-review-v1/" + name: digest(OUT / name)
                          for name in ("semantic_joined_rows.jsonl", "question_clusters.json", "semantic_results.json")},
        "original_files_modified": False, "inference_performed": False,
        "semantic_truth_certified": False,
    }
    assert receipt["joint_lock_precedes_this_analysis"]
    write("semantic_analysis_receipt.json", receipt)
    print(json.dumps({"all": all_stats["joint_categories"],
                      "transitions": transition_stats["joint_categories"],
                      "results_sha256": digest(OUT / "semantic_results.json")}, indent=2))


if __name__ == "__main__":
    main()
