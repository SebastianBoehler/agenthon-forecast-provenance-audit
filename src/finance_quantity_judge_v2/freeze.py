"""Executive summary: freeze the source-free amendment before selected V1 outcomes are inspected."""

import hashlib
import json
import platform
import sys
from pathlib import Path

from finance_quantity_transfer.client import now
from finance_quantity_transfer.freeze import file_record
from finance_quantity_transfer.protocol import ROOT, OUT as V1_OUT, MODEL, PROVIDER, digest
from .protocol import PHASE, SYSTEM


def sources():
    paths = sorted((ROOT / "src/finance_quantity_judge_v2").glob("*.py"))
    paths += [ROOT / "scripts/freeze_finance_quantity_judge_v2.py",
              ROOT / "scripts/collect_finance_quantity_judge_v2.py",
              ROOT / "docs/FINANCE_QUANTITY_JUDGE_POINTER_AMENDMENT_V2.md",
              ROOT / "tests/test_finance_quantity_judge_v2.py"]
    return [file_record(path) for path in paths]


def make_freeze():
    v1_path = V1_OUT / "experiment_freeze.json"
    v1 = json.loads(v1_path.read_text())  # Metadata only; no selected question/output reads.
    for record in v1["source_files"]:
        if file_record(ROOT / record["path"]) != record:
            raise ValueError("Frozen V1 source changed")
    inputs = [v1_path] + [V1_OUT / "authored-paid-preflight" / name
                         for name in ("run.json", "calls.jsonl", "attempt_status.json")]
    return {"executive_summary": "Separate pointer-format diagnostic; V1 remains primary and unchanged.",
            "created_utc": now(), "phase": PHASE, "model": MODEL, "provider": PROVIDER,
            "financial_judges": 64, "authored_preflight_judges": 2, "answer_calls": 0,
            "study_id": "finance_quantity_transfer_v1", "study_cap_usd": "2", "aggregate_cap_usd": "10",
            "system_sha256": hashlib.sha256(SYSTEM.encode()).hexdigest(),
            "timing": "After V1 collection began, based only on two authored pointer failures; not pristine preregistration.",
            "selected_v1_outputs_read_by_author": False,
            "source_files": sources(), "unchanged_v1_sources": v1["source_files"],
            "inputs": [file_record(path) for path in inputs],
            "python_executable": str(Path(sys.executable).resolve()), "python_version": platform.python_version()}


def verify(frozen):
    if frozen["source_files"] != sources():
        raise ValueError("V2 amendment/source hashes changed")
    for record in frozen["unchanged_v1_sources"] + frozen["inputs"]:
        if file_record(ROOT / record["path"]) != record:
            raise ValueError("V1 source or authored/pre-freeze input changed")
    if frozen["python_executable"] != str(Path(sys.executable).resolve()) or frozen["python_version"] != platform.python_version():
        raise ValueError("Frozen runtime changed")
    fixed = {"phase": PHASE, "model": MODEL, "provider": PROVIDER, "financial_judges": 64,
             "authored_preflight_judges": 2, "answer_calls": 0, "study_id": "finance_quantity_transfer_v1",
             "study_cap_usd": "2", "aggregate_cap_usd": "10", "selected_v1_outputs_read_by_author": False,
             "system_sha256": hashlib.sha256(SYSTEM.encode()).hexdigest()}
    if any(frozen[k] != value for k, value in fixed.items()):
        raise ValueError("Frozen fixed scope changed")


def input_hashes(paths):
    return {str(Path(path).resolve().relative_to(ROOT)): digest(Path(path)) for path in paths}
