"""Executive summary: collect both arms and every label-free judge without retries or selective review."""

import hashlib
import json
import os
from pathlib import Path

from .budget import Budget, BudgetStop
from .client import answer, now
from .freeze import source_records
from .protocol import JUDGE, MODEL, PROVIDER, SYSTEMS, body, encode
from .scoring import native_decimal, parse_answer, parse_judge, score, typed_value

STUDY_ID = "finance_quantity_transfer_v1"


def append(path, record):
    with path.open("a", encoding="utf-8") as stream:
        stream.write(encode(record) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def redact_record(record):
    secret = os.environ.get("OPENROUTER_API_KEY", "")
    def clean(value):
        if isinstance(value, str):
            return value.replace(secret, "[REDACTED_API_KEY]") if secret else value
        if isinstance(value, list):
            return [clean(x) for x in value]
        if isinstance(value, dict):
            return {k: "[REDACTED]" if k.lower() in {"authorization", "api_key", "x-api-key"}
                    else clean(v) for k, v in value.items()}
        return value
    return clean(record)


def atomic_json(path, data):
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        stream.write(encode(data) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def validate_cases(cases, expected=32):
    if len(cases) != expected or len({x["case_id"] for x in cases}) != expected:
        raise ValueError(f"Study requires exactly {expected} distinct fixed case IDs")
    fields = {"case_id", "source", "question", "original_context", "provisional_reference"}
    for case in cases:
        if set(case) - fields - {"native_target"} or fields - set(case):
            raise ValueError("Unexpected experiment-packet fields")
        if not all(isinstance(case[k], str) and case[k] for k in ["case_id", "source", "question"]):
            raise ValueError("Case identity/question must be nonempty strings")
        if not isinstance(case["original_context"], dict):
            raise ValueError("Context must be a JSON object")
        ref = case["provisional_reference"]
        if set(ref) != {"eligible", "value", "unit", "scale", "calculation"} or type(ref["eligible"]) is not bool:
            raise ValueError("Provisional reference fields")
        if ref["eligible"]:
            typed_value(ref["value"], ref["unit"], ref["scale"])
            from finance_document_review.arithmetic import calculate
            calculate(ref["calculation"])
        if "native_target" in case:
            if set(case["native_target"]) != {"value"}:
                raise ValueError("Native target is a separate literal numeric value")
            native_decimal(case["native_target"]["value"])


def question_payload(case):
    # Neither native nor provisional targets can enter model or judge prompts.
    return {"question": case["question"], "original_context": case["original_context"]}


def judge_payload(case, saved):
    _, error = parse_answer(saved["text"])
    return {**question_payload(case), "candidate_text": saved["text"],
            "candidate_parser_valid": error is None,
            "candidate_parser_error": error,
            "malformed_candidate_rule": "If candidate_parser_valid is false, verdict must be unassessable; still inspect and record the attempted answer."}


def call_once(case, arm, phase, system, payload, directory, budget):
    identity = {"case_id": case["case_id"], "source": case["source"],
                "arm": arm, "phase": phase, "target_model": MODEL,
                "target_provider": PROVIDER}
    call_id = f"{STUDY_ID}:{case['case_id']}:{arm}:{phase}"
    request = body(system, encode(payload))
    request_hash = hashlib.sha256(encode(request).encode()).hexdigest()
    budget.reserve(call_id, request, {k: v for k, v in identity.items() if k != "source"}
                   | {"request_sha256": request_hash})
    try:
        record = answer(identity, system, encode(payload))
    except Exception as failure:
        # Preserve a censored/local failure, without assuming it was free.
        record = {**identity, "started_utc": now(), "completed_utc": now(),
                  "text": "", "finish_reason": "local_error",
                  "error": {"type": type(failure).__name__},
                  "request_body": request, "request_sha256": request_hash}
    record["call_id"] = call_id
    record = redact_record(record)
    append(directory / "calls.jsonl", record)
    budget.settle(call_id, record)  # Durable observed usage.cost precedes any next call.
    if record.get("provider") != "SiliconFlow" or record.get("returned_model") != MODEL:
        raise BudgetStop("Returned provider/model differs from the fixed route")
    if record.get("finish_reason") in {"provider_mismatch", "transport_error", "local_error"}:
        raise BudgetStop("Transport/route failure; no retries")
    return record


def run(cases, directory, ledger, frozen=None):
    validate_cases(cases, expected=1 if frozen is None else 32)
    if not os.environ.get("OPENROUTER_API_KEY"):
        raise ValueError("OPENROUTER_API_KEY is required before reserving a paid call")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    budget = Budget(ledger, STUDY_ID)
    planned = [{"case_id": case["case_id"], "source": case["source"], "arm": arm,
                "answer_status": "not_started", "judge_status": "not_started",
                "reference_kind": "AI_provisional",
                "primary_eligible": case["provisional_reference"]["eligible"]}
               for case in cases for arm in SYSTEMS]
    metadata = {"executive_summary": "Every planned arm retains its denominator; judgments are same-model proxies.",
                "started_utc": now(), "mode": "authored_paid_preflight" if frozen is None else "financial_study",
                "planned_answer_attempts": len(planned), "planned_judge_attempts": len(planned),
                "initial_actual_usd": "0", "freeze": frozen,
                "source_files": source_records(), "state": "running"}
    atomic_json(directory / "run.json", metadata)
    try:
        for case_index, case in enumerate(cases):
            for arm_index, (arm, system) in enumerate(SYSTEMS.items()):
                index = case_index * len(SYSTEMS) + arm_index
                item = planned[index]
                item["answer_status"] = "attempted"
                atomic_json(directory / "attempt_status.json", planned)
                saved = call_once(case, arm, "answer", system, question_payload(case), directory, budget)
                item["answer_status"] = "recorded"
                item["scoring"] = score(saved["text"], case["provisional_reference"], case.get("native_target"))
                item["judge_status"] = "attempted"
                atomic_json(directory / "attempt_status.json", planned)
                judged = call_once(case, arm, "judge", JUDGE, judge_payload(case, saved), directory, budget)
                _, candidate_error = parse_answer(saved["text"])
                item["quantity_review"], item["judge_parser_error"] = parse_judge(
                    judged["text"], case["original_context"], candidate_error)
                item["judge_status"] = "recorded"
                atomic_json(directory / "attempt_status.json", planned)
        metadata["state"] = "complete"
        metadata["spend"] = budget.totals()
    except Exception as failure:
        metadata.update(state="stopped", error={"type": type(failure).__name__,
                        "reason": str(failure) if isinstance(failure, (BudgetStop, ValueError))
                        else "Local collector failure; inspect preserved records"})
        raise
    finally:
        metadata["completed_utc"] = now()
        atomic_json(directory / "attempt_status.json", planned)
        atomic_json(directory / "run.json", metadata)
    return metadata


def authored_case():
    return {"case_id": "authored_preflight_v1", "source": "authored_only",
            "question": "What is the percent change in costs from year 1 to year 2?",
            "original_context": {"table": [["year", "cost"], ["1", "120"], ["2", "150"]]},
            "provisional_reference": {"eligible": True, "value": "25", "unit": "percent",
                                      "scale": "none", "calculation": "(150-120)/120*100"}}


def preflight():
    case = authored_case()
    validate_cases([case], expected=1)
    value = {"status": "answer", "value": "25", "unit": "percent", "scale": "none",
             "calculation": "(150-120)/120*100", "evidence": ["table[1][1]", "table[2][1]"]}
    from .budget import reservation_usd
    return {"executive_summary": "Authored-only local preflight: no source cases, credentials or API calls.",
            "api_calls": 0, "actual_cost_usd": "0", "case_id": case["case_id"],
            "scoring": score(encode(value), case["provisional_reference"]),
            "answer_reserves_usd": {arm: str(reservation_usd(body(system, encode(question_payload(case)))))
                                    for arm, system in SYSTEMS.items()},
            "source_files": source_records()}
