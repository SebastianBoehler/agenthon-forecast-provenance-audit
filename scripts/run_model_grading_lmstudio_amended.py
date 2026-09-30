"""Executive summary: disclose a launch-gate amendment without changing inference or scoring."""

import argparse
import json
import time

from model_grading.protocol import frozen_selection
from model_grading_lmstudio import (
    OUT as ORIGINAL,
    ROOT,
    MODEL_KEY,
    digest,
    generate,
    normalized,
    now,
    verify,
)

OUT = ROOT / "outputs/model-grading-lmstudio-v2"


def write(name, value):
    with (OUT / name).open("x") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write("\n")


def prepare():
    frozen = verify("preflight_freeze.json")
    readiness = json.loads((ORIGINAL / "preflight.json").read_text())
    if readiness["preflight_freeze_sha256"] != digest(
        ORIGINAL / "preflight_freeze.json"
    ):
        raise ValueError("Original failed readiness identity changed")
    checks = []
    for row in readiness["records"]:
        actual = normalized(row["raw_native_response"])
        if any(row[k] != value for k, value in actual.items()):
            raise ValueError("Original source-free response normalization changed")
        checks.append(
            actual["finish_reason"] == "stop"
            and bool(actual["text"])
            and row["live_loaded_config"] == frozen["loaded_config"]
        )
    if len(checks) != 3 or not all(checks):
        raise ValueError("Amended native-availability readiness failed")
    OUT.mkdir(exist_ok=False)
    write(
        "readiness_assessment.json",
        {
            "executive_summary": "Post-source-free amendment: runtime readiness, with failed strict-format diagnostic.",
            "created_utc": now(),
            "native_availability_passed": True,
            "original_strict_readiness_passed": readiness["passed"],
            "original_strict_passes": sum(r["passed"] for r in readiness["records"]),
            "source_free_generations_reused": 3,
            "new_generations": 0,
            "original_readiness_sha256": digest(ORIGINAL / "preflight.json"),
        },
    )
    additions = [
        "docs/MODEL_GRADING_LMSTUDIO_AMENDMENT_V2.md",
        "docs/MODEL_GRADING_LMSTUDIO_READINESS_REVIEW_V1.md",
        "docs/MODEL_GRADING_LMSTUDIO_GATE_AMENDMENT_REVIEW_V2.md",
        "scripts/run_model_grading_lmstudio_amended.py",
        "outputs/model-grading-lmstudio-v1/preflight_freeze.json",
        "outputs/model-grading-lmstudio-v1/preflight.json",
        "outputs/model-grading-lmstudio-v2/readiness_assessment.json",
    ]
    frozen["files"].update({p: digest(ROOT / p) for p in additions})
    frozen.update(
        {
            "executive_summary": "V2 collection freeze with disclosed source-free launch-gate amendment.",
            "created_utc": now(),
            "original_failed_gate": True,
            "inference_and_scorers_unchanged": True,
        }
    )
    write("freeze.json", frozen)
    print(
        json.dumps(
            {
                "scheduled": 200,
                "freeze_sha256": digest(OUT / "freeze.json"),
                "original_strict_readiness": readiness["passed"],
            }
        )
    )


def collect():
    frozen = json.loads((OUT / "freeze.json").read_text())
    for name, expected in frozen["files"].items():
        if digest(ROOT / name) != expected:
            raise ValueError("V2 frozen input changed: " + name)
    verify("preflight_freeze.json")
    selection = frozen_selection()
    started = time.perf_counter()
    start_utc = now()
    attempts = []
    errors = 0
    stop_reason = "completed"
    with (OUT / "responses.jsonl").open("x") as stream:
        for index, case in enumerate(selection, 1):
            if errors >= 5 or time.perf_counter() - started > 3600:
                stop_reason = (
                    "consecutive_runtime_errors" if errors >= 5 else "wall_time_bound"
                )
                break
            row = generate(case["prompt"])
            row.update(
                {
                    "model_key": MODEL_KEY,
                    "case_id": case["case_id"],
                    "question_hash": case["question_hash"],
                    "collection_index": index,
                }
            )
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            stream.flush()
            attempts.append(row["case_id"])
            errors = errors + 1 if row["finish_reason"] == "runtime_error" else 0
            if index % 10 == 0:
                print(json.dumps({"attempts": index}), flush=True)
    write(
        "receipt.json",
        {
            "executive_summary": "Actual attempted V2 prefix, including all failures.",
            "started_utc": start_utc,
            "completed_utc": now(),
            "attempts": len(attempts),
            "scheduled": len(selection),
            "stop_reason": stop_reason,
            "unattempted_ids": [r["case_id"] for r in selection[len(attempts) :]],
            "freeze_sha256": digest(OUT / "freeze.json"),
            "response_sha256": digest(OUT / "responses.jsonl"),
        },
    )


def analyze():
    import analyze_model_grading_lmstudio as analysis

    # Route the unchanged saved-response analyzer to this explicit new directory.
    analysis.OUT = OUT
    analysis.main()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "collect", "analyze"))
    args = parser.parse_args()
    {"prepare": prepare, "collect": collect, "analyze": analyze}[args.mode]()
