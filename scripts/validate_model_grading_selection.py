"""Executive summary: reproduce the frozen panel directly from the pinned public parquet.

This is AI-assisted technical validation. It imports only the independent Fraction
calculator, never the primary selection code, parser, oracle or scoring modules.
"""
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import pandas as pd

from independent_contract_validation import N, SOURCES, answer, exact_value, extract, round_whole, valid

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "outputs/model-grading-v1"
OUT = ROOT / "outputs/model-grading-review"
FAMILIES = ("cr_eq_gordon", "deriv_binomial_call", "eq_gordon", "corp_wacc")
SALT = "model-grading-v1-20260929"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def operands(question):
    return tuple(extract(rf"D0 = \${N}, growth g = {N}%, required return r = {N}%", question))


def main():
    source = ROOT / "literature/pdfs" / SOURCES["cosimo"][0]
    assert sha(source.read_bytes()) == SOURCES["cosimo"][1]
    public = pd.read_parquet(source).to_dict("records")
    manifest = json.loads((STUDY / "selection_manifest.json").read_text())
    assert manifest["selection_salt"] == SALT
    selection = [json.loads(s) for s in (STUDY / "selection.jsonl").read_text().splitlines()]
    replicated, populations, conflicts = [], {}, {}
    for family in FAMILIES:
        pool = [r for r in public if r["metadata"]["generator"] == family]
        grouped = {}
        labels = {}
        for row in sorted(pool, key=lambda r: r["id"]):
            grouped.setdefault(row["question"], row)
            labels.setdefault(row["question"], set()).add(answer(row["answer"]))
        populations[family] = len(grouped)
        conflicts[family] = sum(len(values) > 1 for values in labels.values())
        replicated.extend(sorted(grouped.values(), key=lambda r: sha((SALT + r["question"]).encode()))[:50])
    assert populations == manifest["family_unique_populations"]
    assert len(selection) == len(replicated) == len({r["question"] for r in replicated}) == 200
    assert [(r["id"], r["question"]) for r in replicated] == [(r["case_id"], r["prompt"]) for r in selection]
    checks = []
    for source_row, row in zip(replicated, selection):
        family = source_row["metadata"]["generator"]
        assert row["family"] == family and row["question_hash"] == sha(row["prompt"].encode())
        value, identities = exact_value(family, row["prompt"])
        whole = "nearest whole unit" in row["prompt"].lower()
        target, tie = round_whole(value) if whole else (value, False)
        assert whole == row["requested_rounding"]
        assert answer(source_row["answer"]) == F(row["gold"])
        assert abs(value - F(row["formula"])) <= F(1, 10**35)
        assert abs(target - F(row["target"])) <= F(1, 10**35)
        checks.append({"case_id": row["case_id"], "family": family,
                       "fraction_formula": str(value), "fraction_target": str(target),
                       "half_tie": tie, "gold_valid": valid(F(row["gold"]), value, whole),
                       "identities": {k: str(v) if isinstance(v, F) else v for k, v in identities.items()}})
    gordon = {f: {operands(r["prompt"]) for r in selection if r["family"] == f}
              for f in ("cr_eq_gordon", "eq_gordon")}
    result = {"selection_sha256": sha((STUDY / "selection.jsonl").read_bytes()),
              "questions": 200, "all_formulas_agree": True, "all_targets_agree": True,
              "cross_gordon_operand_overlap": len(gordon["cr_eq_gordon"] & gordon["eq_gordon"]),
              "family_counts": dict(Counter(r["family"] for r in selection)),
              "gold_invalid_by_family": {f: sum(not r["gold_valid"] for r in checks if r["family"] == f) for f in FAMILIES},
              "half_ties": sum(r["half_tie"] for r in checks), "rows": checks,
              "source_sha256": sha(source.read_bytes()), "unique_populations": populations,
              "duplicate_question_label_conflicts": conflicts,
              "script_sha256": sha(Path(__file__).read_bytes()),
              "method": "separate direct-parquet sampling and exact Fraction calculations; no human review"}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "selection-validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
