"""Executive summary: hash-check the portable scalar artifact and replay all paired grading values."""

from collections import Counter, defaultdict
import json

from grader_comparison.analysis import financial_scores
from grader_comparison.native import load, normalized_comparison
from grader_comparison.protocol import ROOT, read, digest
from grader_comparison.scalars import scalar


def replay(base):
    manifest = json.loads((base / "manifest.json").read_text())
    for path, checksum in manifest["files"].items():
        if digest(base / path) != checksum:
            raise ValueError("Portable scalar artifact changed: " + path)
    cases = {r["id"]: r for r in read(base / "cohort_projection.jsonl")}
    report = json.loads((base / "analysis.json").read_text())
    expected = {(r["model"], r["repetition"], r["case_id"]): r for r in report["rows"]}
    env, dataset = load()
    checked, seen = 0, set()
    for row in read(base / "authored_controls.jsonl"):
        exact = scalar(row["reference"]) == scalar(row["candidate"])
        native = env["compare_answers"](row["reference"], "Final Answer: " + row["candidate"], dataset)[2]
        if exact != row["equal"] or exact != row["exact"] or native != row["native"]:
            raise ValueError("Authored control score changed")
        checked += 1
    for attempt in read(base / "attempt_projection.jsonl"):
        key = (attempt["model"], attempt["repetition"], attempt["case_id"])
        if key in seen:
            raise ValueError("Duplicate projected response")
        seen.add(key)
        row, case = expected[key], cases[attempt["case_id"]]
        if attempt["status"] != "returned" or attempt["at_output_cap"]:
            continue
        final = attempt["final_scalar"]
        if final != row["final_scalar"]:
            raise ValueError("Final scalar projection changed")
        if case["domain"] == "math":
            prediction = attempt["native_extracted"]
            native = False if prediction is None else normalized_comparison(env, case["reference"], prediction)[0]
            if native != row["native_full_accept"]:
                raise ValueError("Native extracted-scalar credit changed")
        if final is None:
            continue
        value = scalar(final)
        if case["domain"] == "finance":
            if any(row[k] != v for k, v in financial_scores(case, value).items()):
                raise ValueError("Financial endpoint changed")
        else:
            if (value == scalar(case["reference"])) != row["exact_reference_equal"]:
                raise ValueError("Exact reference agreement changed")
            for label, omit in (("native_shared", ()), ("without_both_shared", ("intpart", "digits"))):
                if normalized_comparison(env, case["reference"], final, omit)[0] != row[label]:
                    raise ValueError("Shared-scalar endpoint changed")
    if len(seen) != 96 or len(expected) != 96:
        raise ValueError("Projected attempt denominator changed")
    return {"status": "PASS", "authored_controls": checked, "attempts": len(seen),
            "scope": "fixed extracted-scalar score replay; full-response extraction and semantic truth not certified"}


if __name__ == "__main__":
    print(json.dumps(replay(ROOT / "artifacts/grader-comparison-v1")))
