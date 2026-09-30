"""Executive summary: judge every saved V1 answer once, preserving labels and primary outcomes separately."""

import os
from pathlib import Path

from finance_quantity_transfer.budget import Budget, BudgetStop
from finance_quantity_transfer.client import now
from finance_quantity_transfer.protocol import SYSTEMS
from finance_quantity_transfer.runner import STUDY_ID, atomic_json, authored_case, call_once, judge_payload
from finance_quantity_transfer.scoring import parse_answer, parse_judge
from .protocol import PHASE, SYSTEM


def jobs(packet, calls, expected_cases=32):
    # Read labels neither for admission nor judging; reduce rows to question/context fields.
    fields = ("case_id", "source", "question", "original_context")
    contexts = [{key: row[key] for key in fields} for row in packet]
    if len(contexts) != expected_cases or len({x["case_id"] for x in contexts}) != expected_cases:
        raise ValueError("Fixed distinct question coverage required")
    answers = {}
    for record in calls:
        if record["phase"] != "answer":
            continue
        key = record["case_id"], record["arm"]
        if key in answers or not isinstance(record.get("text"), str):
            raise ValueError("Duplicate or missing saved answer text")
        answers[key] = {"text": record["text"]}
    wanted = {(row["case_id"], arm) for row in contexts for arm in SYSTEMS}
    if set(answers) != wanted:
        raise ValueError("Exactly all fixed V1 answer attempts must be present")
    return [{"case": row, "arm": arm, "saved": answers[row["case_id"], arm]}
            for row in contexts for arm in SYSTEMS]


def authored_jobs(calls):
    return jobs([authored_case()], calls, expected_cases=1)


def run(items, directory, ledger, frozen, inputs, authored=False):
    expected = 2 if authored else 64
    keys = {(x["case"]["case_id"], x["arm"]) for x in items}
    if len(items) != expected or len(keys) != expected:
        raise ValueError("Fixed complete judge coverage required")
    if not os.environ.get("OPENROUTER_API_KEY"):
        raise ValueError("OPENROUTER_API_KEY is required before reserving a paid call")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    budget = Budget(ledger, STUDY_ID)  # Same $2 study and $10 aggregate accounting.
    status = [{"case_id": x["case"]["case_id"], "arm": x["arm"], "judge_status": "not_started"} for x in items]
    metadata = {"executive_summary": "Pointer-format diagnostic on unchanged saved candidates; same-model proxy.",
                "started_utc": now(), "state": "running", "planned_judges": expected, "answer_calls": 0,
                "mode": "authored_preflight" if authored else "saved_v1_answers", "freeze": frozen,
                "input_hashes": inputs, "spend_before": budget.totals()}
    atomic_json(directory / "run.json", metadata)
    try:
        for index, item in enumerate(items):
            status[index]["judge_status"] = "attempted"
            atomic_json(directory / "attempt_status.json", status)
            saved = call_once(item["case"], item["arm"], PHASE, SYSTEM,
                              judge_payload(item["case"], item["saved"]), directory, budget)
            _, candidate_error = parse_answer(item["saved"]["text"])
            review, error = parse_judge(saved["text"], item["case"]["original_context"], candidate_error)
            status[index].update(judge_status="recorded", quantity_review=review, judge_parser_error=error)
            atomic_json(directory / "attempt_status.json", status)
        metadata.update(state="complete", spend_after=budget.totals())
    except Exception as failure:
        metadata.update(state="stopped", error={"type": type(failure).__name__,
                        "reason": str(failure) if isinstance(failure, (ValueError, BudgetStop)) else "Local collector failure"})
        raise
    finally:
        metadata["completed_utc"] = now()
        atomic_json(directory / "attempt_status.json", status)
        atomic_json(directory / "run.json", metadata)
    return metadata
