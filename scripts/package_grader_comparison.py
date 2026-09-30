"""Executive summary: publish a scalar replay projection without original questions, contexts or weights."""

from collections import Counter
import json
from pathlib import Path

from grader_comparison.analysis import analyze
from grader_comparison.protocol import ROOT, OUT, digest, jsonl, read, write, now
from grader_comparison.scalars import final_scalar
from grader_comparison.native import load


def main():
    report = analyze()
    if report["recorded_attempts"] != 96 or any(c["unattempted"] for c in report["counts"].values()):
        raise ValueError("Collection is not complete")
    destination = ROOT / "artifacts/grader-comparison-v1"
    destination.mkdir(exist_ok=False)
    cohort = read(OUT / "cohort.jsonl")
    env, _ = load()
    projections = []
    for row in cohort:
        fields = {k: v for k, v in row.items() if k not in ("prompt", "original_prompt")}
        fields["prompt_sha256"] = __import__("hashlib").sha256(row["prompt"].encode()).hexdigest()
        projections.append(fields)
    jsonl(destination / "cohort_projection.jsonl", projections)
    attempts = []
    for name in ("gemma", "qwen"):
        for path in sorted((OUT / name).glob("attempt-*.json")):
            raw = json.loads(path.read_text())
            # Keep only generated scalar extractions, not possibly copied question/solution prose.
            text = raw.get("text", "")
            attempts.append({"model": name, "repetition": raw["repetition"], "case_id": raw["case_id"],
                             "status": raw["status"], "at_output_cap": raw.get("at_output_cap"),
                             "final_scalar": final_scalar(text),
                             "native_extracted": env["extract_pred_answer"](text) if raw["status"] == "returned" else None,
                             "stats": raw.get("stats"), "elapsed_s": raw["elapsed_s"],
                             "saved_raw_record_sha256": digest(path),
                             "generated_text_sha256": __import__("hashlib").sha256(text.encode()).hexdigest()})
    jsonl(destination / "attempt_projection.jsonl", attempts)
    jsonl(destination / "authored_controls.jsonl", read(OUT / "authored_controls.jsonl"))
    # Fix the name of the historical salted ordering digest in the prospective projection.
    census = []
    for row in read(OUT / "reference_census.jsonl"):
        row["salted_problem_order_sha256"] = row.pop("problem_sha256")
        if not row["eligible"]:
            row.pop("reference")
        census.append(row)
    jsonl(destination / "reference_census_projection.jsonl", census)
    for name in ("freeze.json", "census_summary.json", "analysis.json"):
        (destination / name).write_bytes((OUT / name).read_bytes())
    (destination / "math_source_manifest.json").write_bytes((OUT / "source/source_manifest.json").read_bytes())
    for name in ("gemma", "qwen"):
        freeze = json.loads((OUT / name / "model_freeze.json").read_text())
        freeze["checkpoint_path"] = Path(freeze["checkpoint_path"]).name
        write(destination / f"{name}_model_freeze_projection.json", freeze)
    write(destination / "qwen_precollection_amendment.json", json.loads((OUT / "qwen/precollection_amendment.json").read_text()))
    values = {r["reference"] for r in read(OUT / "authored_controls.jsonl")}
    from fractions import Fraction
    from grader_comparison.scalars import scalar
    value_count = len({scalar(v) for v in values})
    pair_count = len({(scalar(r["reference"]), scalar(r["candidate"])) for r in read(OUT / "authored_controls.jsonl")})
    write(destination / "manifest.json", {"executive_summary": "Scalar replay projection; not source-question, full-response or expert-semantic reconstruction.",
          "packaged_utc": now(), "distinct_reference_values": value_count, "distinct_numeric_control_pairs": pair_count,
          "files": {p.name: digest(p) for p in destination.iterdir() if p.is_file()},
          "scope": "Values, extracted scalars, original-response hashes and fixed paired score replay. Full response/extraction replay requires local originals.",
          "omitted": ["original question/solution corpora", "request prompts", "generated explanatory prose", "model weights"],
          "historical_census_name_correction": "problem_sha256 was a salted selection-order digest, now explicitly named salted_problem_order_sha256"})
    print(json.dumps({"artifact": str(destination), "attempts": len(attempts),
                      "distinct_reference_values": value_count, "distinct_numeric_pairs": pair_count}))


if __name__ == "__main__":
    main()
