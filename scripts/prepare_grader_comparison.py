"""Executive summary: census 500 references, author equivalence controls, then freeze 16 prompts."""

from collections import Counter
from decimal import localcontext
import importlib.util
import json
from pathlib import Path
import re

from answer_contract.sources import cosimo_cases, SOURCES
from grader_comparison.protocol import ROOT, OUT, CONFIG, MODELS, REPEATS, digest, write, jsonl, read, now
from grader_comparison.scalars import scalar, canonical, controls
from grader_comparison.native import load, normalized_comparison


def order(identifier):
    import hashlib
    return hashlib.sha256(("grader-comparison-v1|" + identifier).encode()).hexdigest()


def main():
    source = OUT / "source"
    manifest = json.loads((source / "source_manifest.json").read_text())
    for entry in manifest["files"]:
        if digest(source / entry["path"]) != entry["sha256"]:
            raise ValueError("MATH500 source changed")
    rows = read(source / "test.jsonl")
    if len(rows) != 500 or len({r["unique_id"] for r in rows}) != 500:
        raise ValueError("MATH500 denominator changed")
    env, dataset = load()
    census, authored, eligible = [], [], []
    for row in rows:
        value = scalar(row["answer"])
        flags = sorted(set(re.findall(r"nearest|round(?:ed|ing)?|approximat\w*", row["problem"], re.I)))
        census.append({"id": row["unique_id"], "subject": row["subject"], "level": row["level"],
                       "problem_sha256": order(row["problem"]), "reference": row["answer"],
                       "eligible": value is not None, "exclusion": None if value is not None else "outside_scalar_rational_grammar",
                       "question_semantic_flags": flags})
        if value is None:
            continue
        if not flags:
            eligible.append(row)
        for name, candidate, equal in controls(row["answer"]):
            native = env["compare_answers"](row["answer"], "Final Answer: " + candidate, dataset)
            # Check the normalization ablation against the unchanged native branch.
            same = normalized_comparison(env, native[0], native[1])
            if same[0] != native[2]:
                raise ValueError("Native scoring/normalization decomposition changed")
            authored.append({"id": row["unique_id"], "kind": name, "reference": row["answer"],
                            "candidate": candidate, "equal": equal, "native": native[2],
                            "native_strategy": same[1],
                            "without_intpart": normalized_comparison(env, native[0], native[1], ("intpart",))[0],
                            "without_digits": normalized_comparison(env, native[0], native[1], ("digits",))[0],
                            "without_both": normalized_comparison(env, native[0], native[1], ("intpart", "digits"))[0],
                            "literal": row["answer"].strip() == candidate.strip(), "exact": scalar(candidate) == value})
    jsonl(OUT / "reference_census.jsonl", census)
    jsonl(OUT / "authored_controls.jsonl", authored)
    cohort = [{"id": "math:" + r["unique_id"], "domain": "math", "family": r["subject"],
               "prompt": r["problem"], "reference": r["answer"], "canonical": canonical(scalar(r["answer"]))}
              for r in sorted(eligible, key=lambda r: order(r["unique_id"]))[:8]]
    used = {r["question_hash"] for r in read(ROOT / "outputs/model-grading-v1/selection.jsonl")}
    spec = importlib.util.spec_from_file_location("independent_finance", ROOT / "scripts/independent_contract_validation.py")
    independent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(independent)
    import hashlib
    with localcontext() as ctx:
        ctx.prec = 60
        cases = cosimo_cases()
        for family in ("cr_eq_gordon", "deriv_binomial_call", "eq_gordon", "corp_wacc"):
            pool = {c.prompt: c for c in cases if c.family == family and hashlib.sha256(c.prompt.encode()).hexdigest() not in used}
            chosen = sorted(pool.values(), key=lambda c: order(c.prompt))[:2]
            if len(chosen) != 2:
                raise ValueError("Insufficient unused financial question groups")
            for c in chosen:
                exact, _ = independent.exact_value(family, c.prompt)
                if abs(scalar(str(c.formula)) - exact) > scalar("0.00000000000000000001"):
                    raise ValueError("Independent financial target disagrees")
                prompt = c.prompt
                if family == "deriv_binomial_call":
                    prompt += "\nUse simple per-period compounding: R = 1 + rf/100."
                cohort.append({"id": "finance:" + c.case_id, "domain": "finance", "family": family,
                               "prompt": prompt, "original_prompt": c.prompt,
                               "original_question_sha256": hashlib.sha256(c.prompt.encode()).hexdigest(),
                               "reference": str(c.gold), "formula": str(c.formula), "target": str(c.target),
                               "exact_unrounded_target": canonical(exact), "requested_rounding": c.requested_rounding})
    if len(cohort) != 16:
        raise ValueError("Cohort denominator changed")
    jsonl(OUT / "cohort.jsonl", cohort)
    summary = {"all_references": 500, "grammar_eligible": sum(r["eligible"] for r in census),
               "grammar_excluded": sum(not r["eligible"] for r in census),
               "eligible_without_question_flags": len(eligible), "authored_controls": len(authored),
               "positive_controls": sum(r["equal"] for r in authored),
               "negative_controls": sum(not r["equal"] for r in authored),
               "native_false_accepts": sum(r["native"] and not r["equal"] for r in authored),
               "native_false_rejects": sum(not r["native"] and r["equal"] for r in authored),
               "subjects": dict(Counter(r["subject"] for r in census if r["eligible"]))}
    write(OUT / "census_summary.json", summary)
    inputs = [*sorted((ROOT / "src/grader_comparison").glob("*.py")), Path(__file__),
              ROOT / "docs/GRADER_COMPARISON_PROTOCOL_V1.md", ROOT / "tests/test_grader_comparison.py",
              *sorted((ROOT / "artifacts/recursivemas-scoring-source-v1").rglob("*.txt")),
              ROOT / "artifacts/recursivemas-scoring-source-v1/source_manifest.json",
              ROOT / "scripts/validate_recursivemas_authored_controls.py",
              ROOT / "scripts/independent_contract_validation.py", ROOT / "src/answer_contract/formulas.py",
              ROOT / "src/answer_contract/types.py", ROOT / "src/answer_contract/sources.py",
              ROOT / SOURCES["cosimo"]["path"], ROOT / "outputs/model-grading-v1/selection.jsonl",
              *[p for p in OUT.rglob("*") if p.is_file()]]
    write(OUT / "freeze.json", {"frozen_utc": now(), "config": CONFIG, "models": MODELS,
                               "repeats": REPEATS, "scheduled_calls": 96,
                               "files": {str(p.relative_to(ROOT)): digest(p) for p in inputs}})
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
