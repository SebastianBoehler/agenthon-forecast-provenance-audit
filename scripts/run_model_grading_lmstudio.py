"""Executive summary: gate source-free readiness, then retain every attempted selected question."""

import argparse
import json
import time
from decimal import Decimal

from model_grading.protocol import frozen_selection, parse_final
from model_grading_lmstudio import (
    OUT,
    ROOT,
    MODEL_KEY,
    PROBES,
    digest,
    generate,
    now,
    verify,
    write,
)


def preflight():
    verify("preflight_freeze.json")
    if (OUT / "preflight.json").exists():
        raise ValueError("Preserve the existing preflight")
    rows = []
    for prompt, family, expected in PROBES:
        row = generate(prompt)
        value, error = parse_final(row["text"], family)
        row.update(
            {
                "authored_prompt": prompt,
                "family": family,
                "expected": expected,
                "parsed": str(value) if value is not None else None,
                "parse_error": error,
                "passed": row["finish_reason"] == "stop"
                and value is not None
                and abs(value - Decimal(expected)) <= Decimal(".0001"),
            }
        )
        rows.append(row)
    result = {
        "executive_summary": "Authored source-free readiness, not financial benchmark evidence.",
        "completed_utc": now(),
        "preflight_freeze_sha256": digest(OUT / "preflight_freeze.json"),
        "passed": all(r["passed"] for r in rows),
        "records": rows,
    }
    write("preflight.json", result)
    print(
        json.dumps(
            {
                "passed": result["passed"],
                "records": [
                    {k: r[k] for k in ("parsed", "parse_error", "passed", "elapsed_s")}
                    for r in rows
                ],
            }
        )
    )


def collect():
    frozen = verify("preflight_freeze.json")
    readiness = json.loads((OUT / "preflight.json").read_text())
    if not readiness["passed"] or readiness["preflight_freeze_sha256"] != digest(
        OUT / "preflight_freeze.json"
    ):
        raise ValueError("Frozen readiness did not pass")
    review = "docs/MODEL_GRADING_GEMMA_PRECOLLECTION_REVIEW_V1.md"
    frozen["files"].update(
        {
            review: digest(ROOT / review),
            "outputs/model-grading-lmstudio-v1/preflight.json": digest(
                OUT / "preflight.json"
            ),
            "outputs/model-grading-lmstudio-v1/preflight_freeze.json": digest(
                OUT / "preflight_freeze.json"
            ),
        }
    )
    frozen.update(
        {
            "executive_summary": "Collection freeze before any selected Gemma answer.",
            "created_utc": now(),
        }
    )
    write("freeze.json", frozen)
    selection = frozen_selection()
    started = time.perf_counter()
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
            "executive_summary": "Actual attempted prefix; unattempted IDs are not answers.",
            "completed_utc": now(),
            "attempts": len(attempts),
            "scheduled": len(selection),
            "stop_reason": stop_reason,
            "unattempted_ids": [r["case_id"] for r in selection[len(attempts) :]],
            "freeze_sha256": digest(OUT / "freeze.json"),
            "response_sha256": digest(OUT / "responses.jsonl"),
        },
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("preflight", "collect"))
    args = parser.parse_args()
    preflight() if args.mode == "preflight" else collect()
