"""Executive summary: replay unchanged grading and separately specified extraction/convention sensitivities."""

import hashlib
import json
from decimal import Decimal, localcontext

from answer_contract.sources import cosimo_cases
from model_grading.protocol import frozen_selection
from model_grading.scoring import score_one, summarize
from model_grading.numeric_sensitivity import numeric_score
from model_grading_lmstudio import (
    CONFIG,
    MODEL_KEY,
    OUT,
    ROOT,
    digest,
    normalized,
    write,
)
from analyze_model_grading_conventions import continuous_price, extended_record


def main():
    frozen = json.loads((OUT / "freeze.json").read_text())
    for name, checksum in frozen["files"].items():
        if digest(ROOT / name) != checksum:
            raise ValueError("Frozen input changed: " + name)
    receipt = json.loads((OUT / "receipt.json").read_text())
    if receipt["freeze_sha256"] != digest(OUT / "freeze.json") or receipt[
        "response_sha256"
    ] != digest(OUT / "responses.jsonl"):
        raise ValueError("Receipt identity changed")
    records = [
        json.loads(line) for line in (OUT / "responses.jsonl").read_text().splitlines()
    ]
    selection = frozen_selection()
    if receipt["scheduled"] != 200 or receipt["unattempted_ids"] != [
        r["case_id"] for r in selection[len(records) :]
    ]:
        raise ValueError("Scheduled/unattempted accounting changed")
    if len(records) != receipt["attempts"] or [r["case_id"] for r in records] != [
        r["case_id"] for r in selection[: len(records)]
    ]:
        raise ValueError("Attempt ordering or count changed")
    strict = []
    numeric = []
    conventions = []
    numeric_conventions = []
    with localcontext() as context:
        context.prec = 50
        cases = {
            c.case_id: c
            for c in cosimo_cases()
            if c.case_id in {r["case_id"] for r in selection}
        }
        for index, (response, case) in enumerate(zip(records, selection), 1):
            if (
                response["model_key"] != MODEL_KEY
                or response["collection_index"] != index
            ):
                raise ValueError("Model identity or collection index changed")
            if response["started_utc"] < frozen["created_utc"]:
                raise ValueError("Selected request predates collection freeze")
            if response["question_hash"] != case["question_hash"]:
                raise ValueError("Question identity changed")
            request = dict(CONFIG, input=case["prompt"])
            request_hash = hashlib.sha256(
                json.dumps(request, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()
            if (
                response["request_body"] != request
                or response["request_sha256"] != request_hash
            ):
                raise ValueError("Actual native request changed")
            if response["finish_reason"] != "runtime_error":
                if response["live_loaded_config"] != frozen["loaded_config"]:
                    raise ValueError("Native load settings changed")
                for key, value in normalized(response["raw_native_response"]).items():
                    if response[key] != value:
                        raise ValueError("Native normalization changed")
            c = cases[response["case_id"]]
            if c.prompt != case["prompt"] or c.formula != Decimal(case["formula"]):
                raise ValueError("Original question or reference formula changed")
            strict.append(score_one(response, c))
            numeric.append(numeric_score(response, c))
            alternative = (
                continuous_price(c.prompt)
                if c.family == "deriv_binomial_call"
                else None
            )
            conventions.append(extended_record(strict[-1], alternative))
            numeric_conventions.append(extended_record(numeric[-1], alternative))
    result = {
        "executive_summary": "Checkpoint/backend replication, not causal model-family or size effect.",
        "scheduled": len(selection),
        "attempts": len(records),
        "complete": len(records) == 200,
        "freeze_sha256": digest(OUT / "freeze.json"),
        "strict": summarize(strict),
        "numeric": summarize(numeric),
        "two_conventions": summarize(conventions),
        "numeric_two_conventions": summarize(numeric_conventions),
        "families": {
            f: {
                "strict": summarize([r for r in strict if r["family"] == f]),
                "numeric": summarize([r for r in numeric if r["family"] == f]),
                "two_conventions": summarize(
                    [r for r in conventions if r["family"] == f]
                ),
                "numeric_two_conventions": summarize(
                    [r for r in numeric_conventions if r["family"] == f]
                ),
            }
            for f in sorted({r["family"] for r in strict})
        },
    }
    write("results.json", result)
    for name, rows in [
        ("strict_scored", strict),
        ("numeric_scored", numeric),
        ("convention_scored", conventions),
        ("numeric_convention_scored", numeric_conventions),
    ]:
        with (OUT / (name + ".jsonl")).open("x") as stream:
            for row in rows:
                stream.write(json.dumps(row) + "\n")
    print(
        json.dumps(
            {
                k: result[k]
                for k in (
                    "complete",
                    "attempts",
                    "strict",
                    "numeric",
                    "two_conventions",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
