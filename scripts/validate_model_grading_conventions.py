"""Executive summary: independently check the two declared binomial rate conventions.

Nominal rates use exact Fraction arithmetic. Continuous rates use a separately
implemented replicating-portfolio identity at 100-digit mpmath precision. Original
grades and raw responses are preserved; this is a supplementary numeric check.
"""
import json
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path

import mpmath as mp
import pandas as pd

from independent_contract_validation import N, SOURCES, answer, exact_value, extract
from validate_model_grading_outputs import MODELS, score, sha, summarize

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "outputs/model-grading-v1"
OUT = ROOT / "outputs/model-grading-review"
ALL_MODELS = MODELS + ("qwen3-4b",)
mp.mp.dps = 100


def high(value):
    return mp.mpf(value.numerator) / value.denominator


def price(question):
    s, u, d, k, r = extract(rf"S0={N}, u={N}, d={N}, K={N}, rf={N}%", question)
    su, sd = s * u, s * d
    cu, cd = max(su - k, F(0)), max(sd - k, F(0))
    delta = (cu - cd) / (su - sd)
    terminal_debt = delta * su - cu
    gross = mp.exp(high(r) / 100)
    assert high(d) < gross < high(u), question
    continuous = high(delta * s) - high(terminal_debt) / gross
    assert delta * sd - terminal_debt == cd
    nominal, _ = exact_value("deriv_binomial_call", question)
    return nominal, continuous


def compatible(candidate, target):
    return abs(high(candidate) - target) <= mp.mpf(".005")


def compare_primary(checks, grades):
    path = STUDY / "convention_sensitivity.json"
    if not path.exists():
        return {"status": "primary convention artifact not yet available"}
    original = json.loads(path.read_text())
    source_raw = (STUDY / "convention_source_rows.jsonl").read_bytes()
    source_rows = [json.loads(s) for s in source_raw.decode().splitlines()]
    sources = {r["case_id"]: r for r in source_rows}
    assert len(source_rows) == len(sources) == 1000
    for row in checks:
        other = sources[row["case_id"]]
        assert F(row["gold"]) == F(other["gold"])
        assert abs(F(row["nominal_fraction"]) - F(other["simple_price"])) <= F(1, 10**35)
        assert abs(mp.mpf(row["continuous_price"]) - mp.mpf(other["continuous_price"])) <= mp.mpf("1e-35")
        for key, their_key in (("gold_nominal_compatible", "simple_valid"),
                              ("gold_continuous_compatible", "continuous_valid"),
                              ("gold_either_compatible", "either_valid")):
            assert row[key] == other[their_key], (row["case_id"], key)
    assert original["source_binomial"]["simple_invalid"] == sum(not r["gold_nominal_compatible"] for r in checks)
    assert original["source_binomial"]["either_invalid"] == sum(not r["gold_either_compatible"] for r in checks)
    assert original["source_binomial"]["continuous_only_added"] == sum(r["gold_continuous_compatible"] and not r["gold_nominal_compatible"] for r in checks)
    for key, predicate in (("simple_only", lambda r: r["gold_nominal_compatible"] and not r["gold_continuous_compatible"]),
                           ("continuous_only", lambda r: r["gold_continuous_compatible"] and not r["gold_nominal_compatible"]),
                           ("both", lambda r: r["gold_nominal_compatible"] and r["gold_continuous_compatible"])):
        assert original["source_binomial"][key] == sum(predicate(r) for r in checks)
    assert original["source_binomial"]["continuous_no_arbitrage_failures"] == 0
    compared = {}
    for endpoint in ("strict", "numeric"):
        raw = (STUDY / f"convention_{endpoint}_scored.jsonl").read_bytes()
        rows = [json.loads(s) for s in raw.decode().splitlines()]
        lookup = {(r["model_key"], r["case_id"]): r for r in rows}
        ours = [r for r in grades if r["endpoint"] == endpoint]
        assert len(rows) == len(lookup) == len(ours) == 800
        merged = []
        for row in ours:
            other = lookup[(row["model_key"], row["case_id"])]
            assert row["declared_valid"] == other["declared_simple_valid"]
            assert row["continuous_valid"] == other["continuous_valid"]
            assert row["either_valid"] == other["visible_valid"]
            assert row["parse_error"] == other["parse_error"]
            value = F(other["value"]) if other["value"] is not None else None
            assert value == (F(row["fraction_value"]) if row["fraction_value"] is not None else None)
            decisions = row["unchanged_source_policy_decisions"] | {"visible_contract": row["either_valid"]}
            assert decisions == other["decisions"]
            merged.append(row | {"visible_valid": row["either_valid"], "decisions": decisions})
        for model in ALL_MODELS:
            model_rows = [r for r in merged if r["model_key"] == model]
            primary = original[f"{endpoint}_models"][model]
            assert primary["continuous_only_added"] == sum(r["newly_valid"] for r in model_rows)
            binomial = [r for r in model_rows if r["family"] == "deriv_binomial_call"]
            cells = {"simple_only": sum(r["declared_valid"] and not r["continuous_valid"] for r in binomial),
                     "continuous_only": sum(r["continuous_valid"] and not r["declared_valid"] for r in binomial),
                     "both": sum(r["declared_valid"] and r["continuous_valid"] for r in binomial),
                     "neither_parsed": sum(r["fraction_value"] is not None and not r["either_valid"] for r in binomial),
                     "unparsed": sum(r["fraction_value"] is None for r in binomial)}
            assert cells == primary["binomial_compatibility"]
            groups = [(model_rows, primary["aggregate"])]
            groups += [([r for r in model_rows if r["family"] == f], v) for f, v in primary["families"].items()]
            for group, aggregate in groups:
                independent = summarize(group)
                for key in ("attempts", "parsed_completed", "visible_valid", "failures"):
                    assert independent[key] == aggregate[key]
                for policy, values in aggregate["policies"].items():
                    assert all(independent["policies"][policy][k] == v for k, v in values.items())
        compared[endpoint] = {"rows": 800, "sha256": sha(raw), "all_decisions_values_errors_and_aggregates_agree": True}
    return {"status": "all 1000 source prices/decisions and 1600 endpoint decisions agree",
            "results_sha256": sha(path.read_bytes()), "source_rows_sha256": sha(source_raw), "endpoints": compared}


def main():
    freeze_path = STUDY / "convention_sensitivity_freeze.json"
    freeze = json.loads(freeze_path.read_text())
    for name, digest in freeze["files"].items():
        path = STUDY / "convention-original" / Path(name).name if name.endswith(".py") else ROOT / name
        assert sha(path.read_bytes()) == digest, str(path)
    corrected_freeze = STUDY / "convention_sensitivity_freeze_v2.json"
    corrected = json.loads(corrected_freeze.read_text())
    assert sha(freeze_path.read_bytes()) == corrected["original_freeze_sha256"]
    for name, digest in corrected["files"].items():
        assert sha((ROOT / name).read_bytes()) == digest, name
    source = ROOT / "literature/pdfs" / SOURCES["cosimo"][0]
    assert sha(source.read_bytes()) == SOURCES["cosimo"][1]
    public = pd.read_parquet(source).to_dict("records")
    pool = [r for r in public if r["metadata"]["generator"] == "deriv_binomial_call"]
    assert len(pool) == 1000
    checks = []
    for row in pool:
        nominal, continuous = price(row["question"])
        gold = answer(row["answer"])
        nominal_ok, continuous_ok = abs(gold - nominal) <= F(1, 200), compatible(gold, continuous)
        checks.append({"case_id": row["id"], "question": row["question"], "gold": str(gold),
                       "nominal_fraction": str(nominal), "continuous_price": mp.nstr(continuous, 100),
                       "gold_nominal_compatible": nominal_ok, "gold_continuous_compatible": continuous_ok,
                       "gold_either_compatible": nominal_ok or continuous_ok})
    selection = {r["case_id"]: r for r in map(json.loads, (STUDY / "selection.jsonl").read_text().splitlines())}
    counts, grades, hashes = {}, [], {}
    targets = {r["case_id"]: price(r["prompt"])[1] for r in selection.values() if r["family"] == "deriv_binomial_call"}
    for model in ALL_MODELS:
        path = STUDY / f"{model}_responses.jsonl"
        if not path.exists():
            counts[model] = 0
            continue
        raw = path.read_bytes()
        assert not raw or raw.endswith(b"\n"), "Partial append; rerun when complete"
        responses = [json.loads(s) for s in raw.decode().splitlines()]
        assert len({r["case_id"] for r in responses}) == len(responses)
        counts[model], hashes[path.name] = len(responses), sha(raw)
        for response in responses:
            selected = selection[response["case_id"]]
            for endpoint in ("strict", "numeric"):
                original = score(response, selected, numeric=endpoint == "numeric")
                value = F(original["fraction_value"]) if original["fraction_value"] is not None else None
                continuous_ok = (selected["family"] == "deriv_binomial_call" and value is not None
                                 and compatible(value, targets[response["case_id"]]))
                grades.append({"model_key": model, "case_id": response["case_id"], "family": selected["family"],
                               "endpoint": endpoint, "parse_error": original["parse_error"],
                               "fraction_value": original["fraction_value"],
                               "declared_valid": original["visible_valid"],
                               "continuous_valid": continuous_ok,
                               "either_valid": original["visible_valid"] or continuous_ok,
                               "newly_valid": continuous_ok and not original["visible_valid"],
                               "unchanged_source_policy_decisions": {k: v for k, v in original["decisions"].items() if k != "visible_contract"}})
    source_counts = {k: sum(r[k] for r in checks) for k in ("gold_nominal_compatible", "gold_continuous_compatible", "gold_either_compatible")}
    result = {"status": "complete_800" if all(v == 200 for v in counts.values()) else "partial_response_snapshot",
              "executed_utc": datetime.now(timezone.utc).isoformat(),
              "source_rows": 1000, "source_unique_questions": len({r["question"] for r in checks}),
              "source_counts": source_counts,
              "source_invalid_under_both": 1000 - source_counts["gold_either_compatible"],
              "responses_by_model": counts, "mpmath_version": mp.__version__, "decimal_precision": mp.mp.dps,
              "script_sha256": sha(Path(__file__).read_bytes()), "source_sha256": sha(source.read_bytes()),
              "dependency_sha256": {name: sha((ROOT / "scripts" / name).read_bytes())
                                    for name in ("independent_contract_validation.py", "validate_model_grading_outputs.py")},
              "response_sha256": hashes,
              "original_freeze_sha256": sha(freeze_path.read_bytes()),
              "corrected_freeze_sha256": sha(corrected_freeze.read_bytes()),
              "primary_comparison": compare_primary(checks, grades),
              "models": {m: {e: {"attempts": sum(r["model_key"] == m and r["endpoint"] == e for r in grades),
                                   **{k: sum(r["model_key"] == m and r["endpoint"] == e and r[k] for r in grades)
                                      for k in ("declared_valid", "continuous_valid", "either_valid", "newly_valid")},
                                   "newly_valid_case_ids": [r["case_id"] for r in grades if r["model_key"] == m and r["endpoint"] == e and r["newly_valid"]]}
                              for e in ("strict", "numeric")} for m in ALL_MODELS}}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "independent-convention-source.jsonl").write_text("".join(json.dumps(r) + "\n" for r in checks))
    (OUT / "independent-convention-responses.jsonl").write_text("".join(json.dumps(r) + "\n" for r in grades))
    result["result_sha256"] = {name: sha((OUT / name).read_bytes()) for name in ("independent-convention-source.jsonl", "independent-convention-responses.jsonl")}
    (OUT / "independent-convention-summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "source_counts": source_counts,
                      "source_invalid_under_both": result["source_invalid_under_both"], "counts": counts,
                      "models": result["models"]}, indent=2))


if __name__ == "__main__":
    main()
