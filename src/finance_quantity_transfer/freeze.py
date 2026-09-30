"""Executive summary: bind code, approvals, inputs and runtime before financial calls."""

import platform
import sys
from pathlib import Path

from .client import now
from .budget import CONTEXT_LENGTH
from .protocol import FOLLOWUP_CAP, MODEL, OUTPUT_PRICE, PROMPT_PRICE, PROVIDER, ROOT, STUDY_CAP, digest


def file_record(path):
    path = Path(path).resolve()
    return {"path": str(path.relative_to(ROOT)), "sha256": digest(path),
            "bytes": path.stat().st_size}


def source_records():
    paths = sorted((ROOT / "src/finance_quantity_transfer").glob("*.py"))
    paths += [ROOT / "src/finance_document_review/arithmetic.py",
              ROOT / "src/financial_review_io.py",
              ROOT / "scripts/collect_finance_quantity_transfer.py",
              ROOT / "scripts/freeze_finance_quantity_transfer.py",
              ROOT / "scripts/prepare_finance_quantity_transfer.py",
              ROOT / "scripts/prepare_finance_quantity_experiment.py",
              ROOT / "scripts/lock_finance_quantity_references.py",
              ROOT / "scripts/finance_document_audit/joins.py",
              ROOT / "scripts/finance_document_audit/common.py",
              ROOT / "docs/FINANCE_QUANTITY_TRANSFER_EXPERIMENT_V1.md",
              ROOT / "tests/test_finance_quantity_transfer.py"]
    return [file_record(p) for p in paths]


def make_freeze(packet, reference_lock, comparison, semantic_approval):
    metadata = {name: file_record(ROOT / "outputs/finance-quantity-transfer-v1" / name)
                for name in ("provider_catalogue.json", "label_join_freeze.json", "label_join_receipt.json",
                             "reference_a_receipt.json", "reference_b_receipt.json")}
    return {"executive_summary": "Bounded paired transfer study; no calls are authorized by this freeze.",
            "created_utc": now(), "planned_cases": 32, "answer_attempts": 64,
            "quantity_judge_attempts": 64, "reference_kind": "AI_provisional",
            "model": MODEL, "provider": PROVIDER,
            "study_cap_usd": str(STUDY_CAP), "aggregate_cap_usd": str(FOLLOWUP_CAP),
            "initial_actual_usd": "0", "prompt_price_usd_per_token": str(PROMPT_PRICE),
            "output_price_usd_per_token": str(OUTPUT_PRICE),
            "context_byte_framing_output_bound": CONTEXT_LENGTH,
            "python_executable": str(Path(sys.executable).resolve()),
            "python_version": platform.python_version(),
            "source_files": source_records(),
            "inputs": {"experiment_packet": file_record(packet),
                       "reference_joint_lock": file_record(reference_lock),
                       "comparison": file_record(comparison),
                       "semantic_approval": file_record(semantic_approval), **metadata}}


def verify_freeze(frozen, packet):
    expected = file_record(packet)
    if frozen["inputs"]["experiment_packet"] != expected:
        raise ValueError("Experiment packet differs from freeze")
    if frozen["source_files"] != source_records():
        raise ValueError("Source/protocol hashes differ from freeze")
    for record in frozen["inputs"].values():
        if file_record(ROOT / record["path"]) != record:
            raise ValueError("Locked approval/reference provenance differs from freeze")
    if frozen["python_executable"] != str(Path(sys.executable).resolve()) or \
       frozen["python_version"] != platform.python_version():
        raise ValueError("Python runtime differs from freeze")
    if (frozen["planned_cases"], frozen["answer_attempts"], frozen["quantity_judge_attempts"]) != (32, 64, 64):
        raise ValueError("Unexpected study membership")
    if frozen["model"] != MODEL or frozen["provider"] != PROVIDER:
        raise ValueError("Fixed model/provider differs from freeze")
    if frozen["study_cap_usd"] != str(STUDY_CAP) or frozen["aggregate_cap_usd"] != str(FOLLOWUP_CAP):
        raise ValueError("Fixed study caps differ from freeze")
    fixed = {"initial_actual_usd": "0", "reference_kind": "AI_provisional",
             "prompt_price_usd_per_token": str(PROMPT_PRICE),
             "output_price_usd_per_token": str(OUTPUT_PRICE),
             "context_byte_framing_output_bound": CONTEXT_LENGTH}
    if any(frozen[k] != value for k, value in fixed.items()):
        raise ValueError("Fixed measurement/budget metadata differs from freeze")
