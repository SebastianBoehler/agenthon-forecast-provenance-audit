"""Executive summary: preserve raw binomial answers that mention exponential compounding.

This is a descriptive text census, not a replacement for the frozen 1+rf oracle.
An exponential marker can be mentioned without being consistently implemented.
"""
import hashlib
import json
import re
from datetime import datetime, timezone
from decimal import Decimal as D, localcontext
from pathlib import Path

from independent_contract_validation import N, extract
from validate_model_grading_outputs import extract_numeric

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "outputs/model-grading-v1"
OUT = ROOT / "outputs/model-grading-review"
MODELS = ("qwen3-1.7b", "qwen2.5-coder-3b", "deepseek-v3.2", "qwen3-4b")
PATTERN = re.compile(r"\bcontinuous(?:ly)?\b|\bexp\s*\(|\be\s*(?:\^|\*\*)", re.IGNORECASE)


def main():
    selection = {r["case_id"]: r for r in map(json.loads, (STUDY / "selection.jsonl").read_text().splitlines())}
    counts, cases, hashes = {}, [], {}
    for model in MODELS:
        path = STUDY / f"{model}_responses.jsonl"
        if not path.exists():
            counts[model] = {"collected_binomial": 0, "completed_binomial": 0, "exponential_text_markers": 0}
            continue
        raw = path.read_bytes()
        hashes[path.name] = hashlib.sha256(raw).hexdigest()
        rows = [json.loads(s) for s in raw.decode().splitlines()]
        binomial = [r for r in rows if selection[r["case_id"]]["family"] == "deriv_binomial_call"]
        completed = [r for r in binomial if r["finish_reason"] in ("eos", "stop")]
        matches = [r for r in completed if PATTERN.search(r["text"])]
        counts[model] = {"collected_binomial": len(binomial), "completed_binomial": len(completed),
                         "exponential_text_markers": len(matches)}
        for row in matches:
            question = selection[row["case_id"]]
            spot, up, down, strike, rate = extract(rf"S0={N}, u={N}, d={N}, K={N}, rf={N}%", question["prompt"])
            with localcontext() as context:
                context.prec = 50
                s, u, d, k, r = [D(x.numerator) / D(x.denominator) for x in (spot, up, down, strike, rate)]
                gross = (r / 100).exp()
                no_arbitrage = d < gross < u
                cu, cd = max(s * u - k, D(0)), max(s * d - k, D(0))
                q = (gross - d) / (u - d)
                alternative = (q * cu + (1 - q) * cd) / gross
                value, error, units = extract_numeric(row["text"], "deriv_binomial_call", row["finish_reason"])
                scalar = D(value.numerator) / D(value.denominator) if value is not None else None
                alt_valid = no_arbitrage and scalar is not None and abs(scalar - alternative) <= D(".005")
                declared_valid = scalar is not None and abs(scalar - D(question["formula"])) <= D(".005")
            contexts = [row["text"][max(0, m.start() - 75):m.end() + 110] for m in list(PATTERN.finditer(row["text"]))[:3]]
            cases.append({"model_key": model, "case_id": row["case_id"], "question": question["prompt"],
                          "text_census_status": "literal exponential/continuous marker; implementation needs case inspection",
                          "raw_text": row["text"], "raw_last_nonempty_line": next(s for s in reversed(row["text"].splitlines()) if s.strip()),
                          "source_gold": question["gold"], "declared_gross_convention": "1+rf", "declared_formula": question["formula"],
                          "alternative_gross_convention": "exp(rf), period=1", "continuous_formula": str(alternative),
                          "continuous_no_arbitrage": no_arbitrage,
                          "numeric_final_value": str(value) if value is not None else None,
                          "numeric_parse_error": error, "unit_state": units,
                          "valid_under_declared_numeric_oracle": declared_valid,
                          "valid_within_cent_under_continuous_convention": alt_valid,
                          "marker_contexts": contexts})
    result = {"status": "complete_binomial_census" if all(v["collected_binomial"] == 50 for v in counts.values()) else "partial_binomial_census",
              "executed_utc": datetime.now(timezone.utc).isoformat(),
              "definition": PATTERN.pattern, "only_completed_responses_examined": True,
              "no_primary_grade_replacement": True, "model_counts": counts, "cases": cases,
              "response_snapshot_sha256": hashes, "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT / "model-case-notes.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "models": counts,
                      "continuous_convention_would_validate": [r["model_key"] + "/" + r["case_id"] for r in cases if r["valid_within_cent_under_continuous_convention"]]}, indent=2))


if __name__ == "__main__":
    main()
