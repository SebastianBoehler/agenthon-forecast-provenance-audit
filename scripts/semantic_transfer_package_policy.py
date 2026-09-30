"""Executive summary: whitelist inspectable iteration evidence and reject private context/request payloads."""

import hashlib
import json
import os
import re
from decimal import Decimal
from pathlib import Path

BASE_NAME = "outputs/answer-contract-research-20260930-followup-review.zip"
BASE_SHA = "dff5d83910965513e4643a5b8ca4ad5db48e8c7e6da292b3341151eb63666246"
PAPER = "paper/answer_contract_audit.tex"
ANALYSIS = "outputs/finance-quantity-transfer-v1/independent-analysis"
README = "docs/SEMANTIC_TRANSFER_REVIEW_PACKAGE_2026-09-30.md"
FORBIDDEN_KEYS = {"original_context", "table", "pre_text", "post_text", "paragraphs", "question",
                  "original_annotation", "request_body", "raw_response", "messages",
                  "authorization", "api_key", "x-api-key", "access_token", "refresh_token", "private_key"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def selected_files():
    names = {PAPER, "pyproject.toml", README,
             "paper/generated/finance_semantic_review.tikz",
             "paper/generated/finance_semantic_review_metadata.json",
             "docs/PAPER_STRENGTHENING_ITERATION_2026-09-30.md",
             "docs/NEURIPS_CHECKLIST_READINESS_2026-09-30.md",
             "docs/CLOSED_STUDY_COMPUTE_ACCOUNTING_2026-09-30.md",
             "docs/SUBMISSION_FORMAT_2026-09-30.md",
             "docs/FINANCE_HUMAN_REVIEW_HANDOFF_V1.md",
             "docs/FINANCE_EXPRESSION_SEMANTIC_REVIEW_PROTOCOL_V1.md",
             "docs/FINANCE_EXPRESSION_SEMANTIC_REVIEW_RESULTS_V1.md",
             "docs/FINANCE_QUANTITY_TRANSFER_COHORT_PROTOCOL_V1.md",
             "docs/FINANCE_QUANTITY_TRANSFER_REFERENCE_PROTOCOL_V1.md",
             "docs/FINANCE_QUANTITY_TRANSFER_EXPERIMENT_V1.md",
             "docs/FINANCE_QUANTITY_TRANSFER_PREINFERENCE_VALIDATION_V1.md",
             "docs/FINANCE_QUANTITY_JUDGE_POINTER_AMENDMENT_V2.md",
             "docs/FINANCE_QUANTITY_JUDGE_SOURCE_NOTE_V1.md",
             "docs/FINANCE_QUANTITY_TRANSFER_INDEPENDENT_RESULTS_V1.md",
             "outputs/submission-iteration-20260930/semantic_transfer_manuscript_check.json",
             "src/financial_review_io.py", "src/finance_document_review/arithmetic.py",
             "scripts/finance_document_audit/common.py", "scripts/finance_document_audit/joins.py",
             "scripts/prepare_finance_expression_review.py", "scripts/validate_finance_expression_review.py",
             "scripts/analyze_finance_expression_review.py", "scripts/render_finance_semantic_figure.py",
             "scripts/prepare_finance_quantity_transfer.py", "scripts/prepare_finance_quantity_experiment.py",
             "scripts/lock_finance_quantity_references.py", "scripts/freeze_finance_quantity_transfer.py",
             "scripts/collect_finance_quantity_transfer.py", "scripts/freeze_finance_quantity_judge_v2.py",
             "scripts/collect_finance_quantity_judge_v2.py", "scripts/analyze_finance_quantity_transfer.py",
             "scripts/prepare_finance_human_review.py",
             "scripts/package_semantic_transfer_review.py", "scripts/semantic_transfer_package_policy.py",
             "tests/test_finance_quantity_transfer.py", "tests/test_finance_quantity_judge_v2.py",
             "tests/test_finance_quantity_analysis.py", "tests/test_semantic_transfer_package.py"}
    for module, files in {
        "finance_quantity_transfer": "__init__ protocol client budget scoring freeze runner references",
        "finance_quantity_judge_v2": "__init__ protocol freeze runner",
        "finance_quantity_analysis": "__init__ endpoints provenance judge_extension",
    }.items():
        names.update(f"src/{module}/{name}.py" for name in files.split())
    for folder, files in {
        "finance-expression-review-v1": "freeze.json joint_review_lock.json review_a.jsonl review_b.jsonl reviewer_a_receipt.json reviewer_b_receipt.json validation_a.json validation_b.json semantic_results.json semantic_analysis_receipt.json",
        "finance-quantity-transfer-v1": "cohort_freeze.json selection_metadata.jsonl cohort_validation.json reference_stage_freeze.json reference_a.jsonl reference_b.jsonl reference_a_receipt.json reference_b_receipt.json reference_comparison.jsonl reference_joint_lock.json reference_semantic_comparison.json preinference_validation.json label_join_freeze.json label_join_receipt.json experiment_freeze.json provider_catalogue.json spend_ledger.jsonl authored-paid-preflight/run.json authored-paid-preflight/attempt_status.json collection/run.json collection/attempt_status.json",
        "finance-quantity-judge-v2": "plan_freeze.json authored-paid-preflight/run.json authored-paid-preflight/attempt_status.json collection/run.json collection/attempt_status.json",
        "finance-human-review-v1": "preparation_receipt.json blank_review_form.jsonl",
    }.items():
        names.update(f"outputs/{folder}/{name}" for name in files.split())
    names.update(f"{ANALYSIS}/{name}" for name in
                 "results.json receipt.json portable_numeric_packet.jsonl portable-replay/results.json portable-replay/receipt.json".split())
    return sorted(names)


def inspect_json(value):
    if isinstance(value, dict):
        if any(str(key).lower() in FORBIDDEN_KEYS for key in value):
            raise ValueError("Private context/request/credential field in whitelisted JSON")
        for child in value.values():
            inspect_json(child)
    elif isinstance(value, list):
        for child in value:
            inspect_json(child)
    elif isinstance(value, str) and value.lstrip().startswith(("{", "[")):
        try:
            nested = json.loads(value)
        except ValueError:
            return
        inspect_json(nested)


def file_check(root, name):
    root = Path(root).resolve()
    path = root / name
    if path.is_symlink() or path.resolve().parent != (root / name).parent.resolve():
        raise ValueError("Package input must not be a symlink")
    if not path.resolve().is_relative_to(root) or not path.is_file():
        raise ValueError("Missing or out-of-root whitelisted input: " + name)
    text = path.read_text(encoding="utf-8")
    secret = os.environ.get("OPENROUTER_API_KEY", "")
    if (secret and secret in text) or re.search(r"\bsk-or-v1-[A-Za-z0-9]{20,}\b", text):
        raise ValueError("Credential-like value found in package input")
    if path.suffix == ".json":
        inspect_json(json.loads(text))
    elif path.suffix == ".jsonl":
        for line in text.splitlines():
            if line.strip():
                inspect_json(json.loads(line))
    return {"sha256": digest(path), "bytes": path.stat().st_size}


def observed_spend(events):
    reservations, settlements = {}, {}
    total = Decimal(0)
    pending, unknown = set(), []
    for event in events:
        identity = event["call_id"]
        if event["event"] == "reserved":
            if identity in reservations or pending or unknown:
                raise ValueError("Duplicate/concurrent unsettled reservation")
            reservations[identity] = event
            pending.add(identity)
        elif event["event"] == "settled":
            if identity not in pending or identity in settlements:
                raise ValueError("Unreserved/duplicate billing settlement")
            reserve = reservations[identity]
            if event["study_id"] != reserve["study_id"] or event["request_sha256"] != reserve["request_sha256"]:
                raise ValueError("Reservation/billing identity mismatch")
            bound = Decimal(str(reserve["reserve_usd"]))
            if not bound.is_finite() or bound < 0:
                raise ValueError("Invalid reservation")
            value = event["cost_usd"]
            if value is None:
                unknown.append({"call_id": identity, "study_id": event["study_id"],
                                "reserved_usd": str(bound), "cost_usd": None,
                                "cost_error": event.get("cost_error"),
                                "finish_reason": event.get("finish_reason"), "error": event.get("error")})
            else:
                if isinstance(value, bool):
                    raise ValueError("Invalid observed billing")
                cost = Decimal(str(value))
                if not cost.is_finite() or cost < 0 or cost > bound:
                    raise ValueError("Invalid observed billing or reservation exceeded")
                total += cost
            settlements[identity] = event
            pending.remove(identity)
        else:
            raise ValueError("Unknown ledger event")
    if pending or set(reservations) != set(settlements) or total > Decimal(10):
        raise ValueError("Incomplete ledger or aggregate cap exceeded")
    study = sum((Decimal(x["cost_usd"]) for x in settlements.values()
                 if x["study_id"] == "finance_quantity_transfer_v1" and x["cost_usd"] is not None), Decimal(0))
    unknown_reserve = sum((Decimal(x["reserved_usd"]) for x in unknown), Decimal(0))
    study_reserve = sum((Decimal(x["reserved_usd"]) for x in unknown
                         if x["study_id"] == "finance_quantity_transfer_v1"), Decimal(0))
    if study + study_reserve > Decimal(2) or total + unknown_reserve > Decimal(10):
        raise ValueError("Study cap exceeded")
    return {"actual_aggregate_observed_usd": None if unknown else str(total),
            "study_observed_usd": None if any(x["study_id"] == "finance_quantity_transfer_v1" for x in unknown) else str(study),
            "known_observed_subtotal_usd": str(total), "study_known_observed_subtotal_usd": str(study),
            "observed_cost_complete": not unknown, "settled_calls": len(settlements),
            "known_cost_calls": len(settlements) - len(unknown), "unknown_cost_calls": len(unknown),
            "unknown_billing": unknown, "unknown_billing_reserved_usd": str(unknown_reserve),
            "accounted_worst_under_fixed_request_prices_usd": str(total + unknown_reserve),
            "reservation_scope": "Declared fixed-price and byte/token reservation accounting only; not observed or reconciled billing.",
            "ledger_events": len(events), "study_cap_usd": "2", "aggregate_cap_usd": "10"}
