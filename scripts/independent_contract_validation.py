"""Executive summary: independently audit pinned finance rows with exact fractions.

No audit-module import or upstream solution execution is permitted. Cosimo families
use 20 hash-selected rows per preference-pair availability stratum, except that
constructed-response Gordon, binomial, CAPM and ordinary RLVR DCF receive censuses.
"""
import ast
import hashlib
import json
import platform
import re
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/answer-contract-independent"
SOURCES = {
    "cosimo": ("cosimo-cfa-level-i.parquet", "afa7e9241e0f06df090916e289a8e39d7fc9c4245c3b21c0c0f1188edafb0abb"),
    "rlvr": ("financial-rlvr-10k-6cfa9a71.jsonl", "86968a146a09e2ba1b19aac3a5ca2bec7e878358341a7972fddeb4b8cd7754af"),
}
FAMILIES = ["cr_eq_gordon", "eq_gordon", "deriv_binomial_call", "tvm_annuity_fv",
            "v_tvm_annuity_fv", "corp_wacc", "m_corp_wacc", "port_capm",
            "tvm_pv_lump", "tvm_eay"]
N = r"([0-9][0-9,]*(?:\.[0-9]+)?)"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract(pattern, text):
    match = re.search(pattern, text)
    if match is None:
        raise ValueError(f"Unparsed question: {text}")
    return [F(s.replace(",", "")) for s in match.groups()]


def answer(text):
    tokens = re.findall(r"-?[0-9][0-9,]*(?:\.[0-9]+)?", text)
    if len(tokens) != 1:
        raise ValueError(f"Non-scalar source answer: {text}")
    return F(tokens[0].replace(",", ""))


def exact_value(family, question):
    evidence = {}
    if family in {"cr_eq_gordon", "eq_gordon"}:
        dividend, growth, rate = extract(rf"D0 = \${N}, growth g = {N}%, required return r = {N}%", question)
        assert rate > growth
        value = dividend * (100 + growth) / (rate - growth)
    elif family in {"tvm_annuity_fv", "v_tvm_annuity_fv"}:
        payment, annual, months = extract(rf"deposits \${N}.*?paying {N}% compounded monthly.*?after {N} months", question)
        assert months.denominator == 1 and months > 0
        value, gross = F(0), 1 + annual / 1200
        for _ in range(int(months)):
            value = value * gross + payment
        assert value == payment * (gross ** int(months) - 1) / (gross - 1)
        evidence["cashflow_identity"] = True
    elif family in {"corp_wacc", "m_corp_wacc"}:
        equity, debt, re_, rd, tax = extract(rf"market equity {N}, market debt {N}, cost of equity {N}%, cost of debt {N}%, and a marginal tax rate {N}%", question)
        assert equity > 0 and debt > 0 and 0 <= tax <= 100
        value = (equity * re_ + debt * rd * (100 - tax) / 100) / (equity + debt)
    elif family == "port_capm":
        rf, market, beta = extract(rf"rf = {N}%, E\(Rm\) = {N}%, β = {N}", question)
        value = beta * market + (1 - beta) * rf
        endpoints = [b * market + (1 - b) * rf for b in (beta - F(1, 200), beta + F(1, 200))]
        evidence = {"rounded_beta_interval_low": min(endpoints),
                    "rounded_beta_interval_high": max(endpoints)}
    elif family == "tvm_pv_lump":
        cash, years, annual = extract(rf"amount of \${N} is received in {N} years.*?rate is {N}%", question)
        assert years.denominator == 1 and years > 0
        value, gross = cash, 1 + annual / 100
        for _ in range(int(years)):
            value /= gross
        assert value * gross ** int(years) == cash
        evidence["cashflow_identity"] = True
    elif family == "tvm_eay":
        annual, periods = extract(rf"annual rate of {N}% is compounded {N} times", question)
        assert periods.denominator == 1 and periods > 0
        accumulated = F(1)
        for _ in range(int(periods)):
            accumulated *= 1 + annual / (100 * periods)
        value = 100 * (accumulated - 1)
    elif family == "deriv_binomial_call":
        spot, up, down, strike, rate = extract(rf"S0={N}, u={N}, d={N}, K={N}, rf={N}%", question)
        gross = 1 + rate / 100
        assert down < gross < up
        su, sd = spot * up, spot * down
        cu, cd = max(su - strike, F(0)), max(sd - strike, F(0))
        stock_units = (cu - cd) / (su - sd)
        signed_bond = (cu - stock_units * su) / gross
        assert stock_units * sd + signed_bond * gross == cd
        value = stock_units * spot + signed_bond
        q = (gross - down) / (up - down)
        assert value == (q * cu + (1 - q) * cd) / gross
        lower, upper = max(spot - strike / gross, F(0)), spot
        assert lower <= value <= upper
        evidence = {"replication_identity": True, "state_payoffs_match": True,
                    "source_bond_debt": -signed_bond, "lower_bound": lower,
                    "upper_bound": upper}
    else:
        raise ValueError(f"Unknown family: {family}")
    return value, evidence


def round_whole(value):
    lower = value.numerator // value.denominator
    remainder = value - lower
    tie = remainder == F(1, 2)
    return F(lower + int(remainder >= F(1, 2))), tie


def valid(candidate, value, whole):
    if not whole:
        return abs(candidate - value) <= F(1, 200)
    target, tie = round_whole(value)
    return candidate == target or (tie and candidate == target - 1)


def rank(row):
    return hashlib.sha256(("independent-contract-v1:" + row["id"]).encode()).hexdigest()


def cosimo_rows(frame):
    results = []
    for family in FAMILIES:
        population = frame[frame.metadata.map(lambda m: m["generator"] == family)].to_dict("records")
        if family in {"cr_eq_gordon", "deriv_binomial_call", "port_capm"}:
            selected = sorted(population, key=rank)
        else:
            selected = []
            for has_pair in (False, True):
                pool = [r for r in population if (r["preference_pair"] is not None) == has_pair]
                selected += sorted(pool, key=rank)[:20]
        for row in selected:
            value, evidence = exact_value(family, row["question"])
            whole = "nearest whole unit" in row["question"].lower()
            gold = answer(row["answer"])
            target, tie = round_whole(value) if whole else (value, False)
            result = {"source": "cosimo", "family": family, "id": row["id"],
                      "question": row["question"], "gold": gold, "formula": value,
                      "target": target, "requested_rounding": whole, "half_tie": tie,
                      "gold_valid": valid(gold, value, whole), "raw_formula_gold_valid": valid(gold, value, False),
                      "population_rows": len(population), "source_verified": bool(row["verified"]), **evidence}
            pair = row["preference_pair"]
            if pair is not None:
                chosen, rejected = answer(pair["chosen"]["answer"]), answer(pair["rejected"]["answer"])
                result.update(chosen=chosen, rejected=rejected,
                              chosen_valid=valid(chosen, value, whole),
                              rejected_valid=valid(rejected, value, whole))
                if whole:
                    result["rounded_rejected"] = round_whole(rejected)[0]
                    result["rounded_rejected_valid"] = valid(result["rounded_rejected"], value, True)
                    result["rounded_chosen_valid"] = valid(round_whole(chosen)[0], value, True)
            if "source_bond_debt" in evidence:
                result["gold_matches_bond"] = valid(gold, evidence["source_bond_debt"], False)
                result["gold_violates_bounds"] = not evidence["lower_bound"] <= gold <= evidence["upper_bound"]
            if "rounded_beta_interval_low" in evidence:
                result["gold_feasible_rounded_beta"] = evidence["rounded_beta_interval_low"] - F(1, 200) <= gold <= evidence["rounded_beta_interval_high"] + F(1, 200)
            results.append(result)
    return results


def rlvr_rows(path):
    results = []
    for line in path.read_text().splitlines():
        row = json.loads(line)
        if row["domain"] != "DCF Valuation" or row["is_edge_case"]:
            continue
        cash, rate, growth = extract(rf"FCF_1=\${N}, Discount Rate r={N}%, Growth Rate g={N}%", row["prompt"])
        gap = rate - growth
        assert gap > F(1, 10)
        value, gold = cash * 100 / gap, F(str(row["ground_truth"]))
        low, high = cash * 100 / (gap + F(1, 10)), cash * 100 / (gap - F(1, 10))
        results.append({"source": "rlvr", "family": "DCF_ordinary", "id": row["id"],
                        "question": row["prompt"], "gold": gold, "formula": value,
                        "gold_misses_abs_1e_4": abs(gold - value) > F(1, 10000),
                        "relative_over_0_1_percent": abs(gold - value) / value > F(1, 1000),
                        "relative_over_1_percent": abs(gold - value) / value > F(1, 100),
                        "interval_low": low, "interval_high": high,
                        "gold_feasible_rounded_rates": low - F(1, 20000) <= gold <= high + F(1, 20000),
                        "relative_interval_width": (high - low) / value, "gap_bucket": "under_5pp" if gap < 5 else "at_least_5pp"})
    return results


def summarize(rows):
    groups = {}
    for family in FAMILIES + ["DCF_ordinary"]:
        subset = [r for r in rows if r["family"] == family]
        counts = Counter()
        for row in subset:
            counts.update({k: int(v) for k, v in row.items() if isinstance(v, bool)})
        groups[family] = {"checked_rows": len(subset), "unique_questions": len({r["question"] for r in subset}),
                          "preference_pairs": sum("chosen" in r for r in subset), **dict(counts)}
    return groups


def encode(value):
    if isinstance(value, F):
        return {"fraction": str(value), "float": float(value)}
    raise TypeError(type(value))


def inspect_source():
    manifest = json.loads((ROOT / "literature/pdfs/cosimo-source-manifest.json").read_text())
    assert manifest["revision"] == "20668622104bf8237837efd67debd1419f7bbe33"
    for item in manifest["files"]:
        assert digest(ROOT / item["local_path"]) == item["sha256"]
    item = next(f for f in manifest["files"] if f["path"].endswith("cfa_l1.py"))
    tree = ast.parse((ROOT / item["local_path"]).read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "deriv_binomial_call")
    node = next(n for n in ast.walk(fn) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "c" for t in n.targets))
    expression = ast.unparse(node.value)
    assert expression == "(h * su - cu) / (1 + rf)"
    return {"revision": manifest["revision"], "files": manifest["files"],
            "binomial_assignment": expression, "assignment_line": node.lineno,
            "method": "text and AST inspection; no imports or execution"}


def compare_primary(rows):
    path = ROOT / "outputs/answer-contract-v1/rows.jsonl"
    primary = {r["id"]: r for r in map(json.loads, path.read_text().splitlines())}
    counts = Counter()
    for row in rows:
        other = primary[row["id"]]
        assert abs(F(other["formula"]) - row["formula"]) <= F(1, 10 ** 35), row["id"]
        counts["formulas_agree"] += 1
        if row["source"] == "cosimo":
            for key in ("gold_valid", "chosen_valid", "rejected_valid"):
                if key in row:
                    assert row[key] == other[key], (row["id"], key)
                    counts[key + "_agrees"] += 1
    return {"primary_rows_sha256": digest(path), "absolute_numeric_agreement_tolerance": "1e-35", **counts}


def check_numerical_patches(rows):
    path = ROOT / 'outputs/answer-contract-v1/numerical-patches.jsonl'
    patches = {row['id']: row for row in map(json.loads, path.read_text().splitlines())}
    for row in rows:
        patch = patches[row['id']]
        candidate = F(patch['repaired_numeric_answer'])
        if row.get('requested_rounding'):
            assert candidate == round_whole(row['formula'])[0], row['id']
        else:
            tolerance = F(1, 20000) if row['source'] == 'rlvr' else F(1, 200)
            assert abs(candidate - row['formula']) <= tolerance, row['id']
    return {'checked_patches': len(rows), 'patches_sha256': digest(path),
            'method': 'materialized decimal answers checked against independent exact fractions'}


def main():
    paths = {}
    for name, (filename, expected) in SOURCES.items():
        paths[name] = ROOT / "literature/pdfs" / filename
        assert digest(paths[name]) == expected, f"Input hash mismatch: {name}"
    cosimo = cosimo_rows(pd.read_parquet(paths["cosimo"]))
    rlvr = rlvr_rows(paths["rlvr"])
    OUT.mkdir(parents=True, exist_ok=True)
    all_rows = cosimo + rlvr
    (OUT / "rows.jsonl").write_text("".join(json.dumps(r, default=encode, sort_keys=True) + "\n" for r in all_rows))
    sample = []
    for family in FAMILIES:
        pool = [r for r in cosimo if r["family"] == family]
        for has_pair in (False, True):
            sample += sorted([r for r in pool if ("chosen" in r) == has_pair], key=rank)[:20]
    for stratum in sorted({r["gap_bucket"] for r in rlvr}):
        sample += sorted([r for r in rlvr if r["gap_bucket"] == stratum], key=rank)[:20]
    (OUT / "review_sample.jsonl").write_text("".join(json.dumps(r, default=encode, sort_keys=True) + "\n" for r in sample))
    widths = sorted(r["relative_interval_width"] for r in rlvr)
    summary = {"independence": "AI-assisted technical validation; Fraction arithmetic; no upstream execution or main formula import",
               "sample_rule": "SHA256(independent-contract-v1:<row id>), first 20 per preference availability; CR Gordon, binomial, CAPM and DCF census",
               "families": summarize(all_rows), "median_relative_dcf_interval_width": widths[len(widths) // 2],
               "input_hashes": {k: digest(p) for k, p in paths.items()}, "protocol_sha256": digest(ROOT / "docs/ANSWER_CONTRACT_PROTOCOL_V1.md"),
               "script_sha256": digest(Path(__file__)), "python_version": platform.python_version(), "pandas_version": pd.__version__,
               "result_hashes": {p.name: digest(p) for p in sorted(OUT.glob("*.jsonl"))},
               "source_inspection": inspect_source(), "primary_comparison": compare_primary(all_rows),
               "numerical_patch_validation": check_numerical_patches(all_rows)}
    (OUT / "summary.json").write_text(json.dumps(summary, default=encode, indent=2) + "\n")
    print(json.dumps(summary["families"], indent=2))


if __name__ == "__main__":
    main()
