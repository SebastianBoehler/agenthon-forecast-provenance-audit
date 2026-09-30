"""Executive summary: replay paired finite counts; separate extraction abstention and target repair."""

from collections import Counter, defaultdict
from fractions import Fraction
import json

from .native import load, normalized_comparison
from .protocol import OUT, read, write, frozen
from .scalars import scalar, final_scalar


def financial_scores(case, value):
    exact = scalar(case["exact_unrounded_target"])
    if case["requested_rounding"]:
        # Nearest integer, with both allowed at an exact half tie.
        floor = exact.numerator // exact.denominator
        distance = exact - floor
        targets = {floor} if distance < Fraction(1, 2) else {floor + 1}
        if distance == Fraction(1, 2):
            targets = {floor, floor + 1}
        contract = value in targets
    else:
        contract = abs(value - exact) <= Fraction(1, 200)
    return {"released_label_cent": abs(value - scalar(case["reference"])) <= Fraction(1, 200),
            "corrected_unrounded_cent": abs(value - exact) <= Fraction(1, 200),
            "complete_contract": contract}


def analyze(base=OUT, validate_freeze=True):
    cohort = frozen() if validate_freeze else read(base / "cohort.jsonl")
    cases = {c["id"]: c for c in cohort}
    env, dataset = load()
    authored = read(base / "authored_controls.jsonl")
    controls = {}
    for endpoint in ("native", "without_intpart", "without_digits", "without_both", "literal", "exact"):
        controls[endpoint] = {"false_accepts": sum(r[endpoint] and not r["equal"] for r in authored),
                              "false_rejects": sum(not r[endpoint] and r["equal"] for r in authored)}
    if controls["exact"] != {"false_accepts": 0, "false_rejects": 0}:
        raise ValueError("Exact-value control consistency failed")
    results, counts, seen = [], defaultdict(Counter), set()
    for name in ("gemma", "qwen"):
        for path in sorted((base / name).glob("attempt-*.json")):
            record = json.loads(path.read_text())
            key = (name, record["repetition"], record["case_id"])
            if key in seen or record["model"] != name or record["case_id"] not in cases:
                raise ValueError("Unexpected or duplicate scheduled attempt")
            seen.add(key)
            case = cases[record["case_id"]]
            if record["request"]["input"] != case["prompt"]:
                raise ValueError("Prompt changed during collection")
            group = f"{name}/{record['repetition']}/{case['domain']}"
            counter = counts[group]
            counter["attempted"] += 1
            row = {"model": name, "repetition": record["repetition"], "case_id": case["id"],
                   "domain": case["domain"], "family": case["family"], "status": record["status"]}
            if record["status"] != "returned":
                counter["runtime_nondecision"] += 1
                results.append(row)
                continue
            counter["returned"] += 1
            if record["at_output_cap"]:
                counter["output_cap_nondecision"] += 1
                results.append(dict(row, status="output_cap_nondecision"))
                continue
            text = record["text"]
            answer = final_scalar(text)
            row.update(final_scalar=answer, response_sha256=__import__("hashlib").sha256(text.encode()).hexdigest())
            if case["domain"] == "math":
                native = env["compare_answers"](case["reference"], text, dataset)
                row.update(native_full_accept=native[2], native_extracted=native[1])
                counter["native_full_accept"] += int(native[2])
                native_value = scalar(native[1]) if native[1] is not None else None
                row["native_extraction_exact"] = (None if native_value is None
                                                   else native_value == scalar(case["reference"]))
                if row["native_extraction_exact"] is not None:
                    counter["native_extraction_admitted"] += 1
                    counter["native_full_unequal_credit"] += int(native[2] and not row["native_extraction_exact"])
            if answer is None:
                counter["final_scalar_nondecision"] += 1
                results.append(row)
                continue
            counter["final_scalar_admitted"] += 1
            value = scalar(answer)
            if case["domain"] == "math":
                equal = value == scalar(case["reference"])
                row["exact_reference_equal"] = equal
                counter["exact_reference_equal"] += int(equal)
                for label, omit in (("native_shared", ()), ("without_both_shared", ("intpart", "digits"))):
                    accepted, strategy = normalized_comparison(env, case["reference"], answer, omit)
                    row[label] = accepted
                    row[label + "_strategy"] = strategy
                    counter[label + "_accept"] += int(accepted)
                    counter[label + "_false_accept"] += int(accepted and not equal)
                    counter[label + "_false_reject"] += int(not accepted and equal)
            else:
                scores = financial_scores(case, value)
                row.update(scores)
                for endpoint, accepted in scores.items():
                    counter[endpoint + "_accept"] += int(accepted)
                counter["valid_denied_by_label"] += int(scores["complete_contract"] and not scores["released_label_cent"])
                counter["label_credit_contract_invalid"] += int(scores["released_label_cent"] and not scores["complete_contract"])
            results.append(row)
    for name in ("gemma", "qwen"):
        for repetition in range(3):
            for domain in ("math", "finance"):
                group = f"{name}/{repetition}/{domain}"
                counts[group]["scheduled"] = 8
                counts[group]["unattempted"] = 8 - counts[group]["attempted"]
    return {"scheduled_calls": 96, "recorded_attempts": len(seen), "controls": controls,
            "counts": {k: dict(v) for k, v in sorted(counts.items())}, "rows": results,
            "scope": "finite selected responses and authored reference-value controls; no full-benchmark model accuracy"}


def main():
    report = analyze()
    write(OUT / "analysis.json", report)
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))
