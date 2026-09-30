"""Executive summary: pinned TAT-QA scores and adapted, unit-blind FinQA scalars.

No selected annotations are loaded here. FinQA does not score program equivalence.
TAT-QA preserves its separate answer and scale channels, including normalization.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from threading import RLock
from types import ModuleType

_ROOT = Path(__file__).resolve().parents[2]
_BASE = _ROOT / "outputs/finance-document-native-v1"
_HASHES = {
    "finqa/code/evaluate/evaluate.py": "845cd131cab843eceff256cf6d392978cc470a7da4a80107beb56027fdca5c13",
    "finqa/LICENSE": "92c0e67bd762c15c07ba60de09558338315a8ebf99aac4f51f487179809ac087",
    "finqa/README.md": "eb86779cfed6f0a253913761d8e4fabe032a29d9fcf2944e56c23bf007064605",
    "tatqa/tatqa_metric.py": "2aeeac479f89f8c76300af1cc0e8d098eb86af84bc386b38b6ab4af484a6dea8",
    "tatqa/tatqa_utils.py": "a84bb2f960737cf0a53733637a674cc4b20ef030a2be6a4b21dc2c4356f415ec",
    "tatqa/LICENSE": "46e27ffbc49c3fd44a9595c2213f8a5f4319a81b53238e49ce1eec39e7e25662",
    "tatqa/README.md": "85c398173d771a2531abea5b81f3696914296642da2af78c2c34545715c14d5f",
}
_DECIMAL = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$")
_SCALES = {"none", "thousand", "million", "billion"}
_NATIVE_SCALES = {"", "thousand", "million", "billion", "percent"}
_MODULES: dict[str, ModuleType] = {}
_LOCK = RLock()


def _read_verified(relative: str) -> bytes:
    path = _BASE / relative
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise RuntimeError(f"Missing pinned native source: {path}") from exc
    if hashlib.sha256(data).hexdigest() != _HASHES[relative]:
        raise RuntimeError(f"Pinned native source hash mismatch: {path}")
    return data


def verify_native_sources() -> dict:
    """Verify all seven pinned code/notice files; never download a replacement."""
    for relative in _HASHES:
        _read_verified(relative)
    return {"files_verified": len(_HASHES), "sha256": dict(_HASHES)}


def _execute_module(relative: str, name: str) -> ModuleType:
    module = ModuleType(name)
    module.__file__ = str(_BASE / relative)
    try:
        exec(compile(_read_verified(relative), module.__file__, "exec"), module.__dict__)
    except ImportError as exc:
        raise RuntimeError(f"Pinned native evaluator dependency unavailable: {exc}") from exc
    return module


def _load_official(source: str) -> ModuleType:
    """Execute inspected, hash-verified code only; no annotation expression eval."""
    with _LOCK:
        verify_native_sources()  # Also recheck files when a module is cached.
        if source not in _MODULES:
            if source == "finqa":
                module = _execute_module("finqa/code/evaluate/evaluate.py", "_pinned_finqa")
            elif source == "tatqa":
                utils = _execute_module("tatqa/tatqa_utils.py", "_pinned_tatqa_utils")
                previous = sys.modules.get("tatqa_utils")
                sys.modules["tatqa_utils"] = utils
                try:
                    module = _execute_module("tatqa/tatqa_metric.py", "_pinned_tatqa_metric")
                finally:
                    if previous is None:
                        sys.modules.pop("tatqa_utils", None)
                    else:
                        sys.modules["tatqa_utils"] = previous
            else:
                raise ValueError(f"Unknown native source: {source}")
            _MODULES[source] = module
        return _MODULES[source]


def _number(value, name: str, *, decimal_string: bool = False) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError(f"{name} must be a finite number")
    if decimal_string and (not isinstance(value, str) or not _DECIMAL.fullmatch(value)):
        raise ValueError(f"{name} must be a plain decimal string")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not result.is_finite() or not math.isfinite(float(result)):
        raise ValueError(f"{name} must be finite in the native float runtime")
    return result


def _candidate(candidate: dict) -> tuple:
    if not isinstance(candidate, dict) or not {"value", "unit", "scale"} <= candidate.keys():
        raise ValueError("Candidate requires value, unit and scale fields")
    unit, scale, value = candidate["unit"], candidate["scale"], candidate["value"]
    if (not isinstance(unit, str) or not unit.strip() or
            not isinstance(scale, str) or scale not in _SCALES):
        raise ValueError("Candidate requires a nonempty unit and a declared scale")
    status = candidate.get("status", "answer")
    if not isinstance(status, str) or status not in {"answer", "non_numeric_answer", "insufficient_information"}:
        raise ValueError("Unsupported candidate status")
    if status == "insufficient_information":
        if value is not None:
            raise ValueError("An abstention must have null value")
    elif status == "non_numeric_answer":
        if not isinstance(value, str) or value not in {"yes", "no"} or unit != "boolean" or scale != "none":
            raise ValueError("Non-numeric candidates require yes/no, boolean, none")
    else:
        _number(value, "Candidate value", decimal_string=True)
    return value, unit, scale, status


def score_finqa_scalar(annotation: dict, candidate: dict) -> dict:
    """Adapt the literal execution result endpoint; ignore unit/scale metadata.

    Official eval_program rounds numeric execution to five decimals, followed by
    exact equality to the unchanged exe_ans. No DSL/program score is available.
    """
    verify_native_sources()
    if not isinstance(annotation, dict) or "exe_ans" not in annotation:
        raise ValueError("FinQA annotation requires its native exe_ans")
    gold = annotation["exe_ans"]
    if isinstance(gold, str):
        if gold not in {"yes", "no"}:
            raise ValueError("FinQA string exe_ans must be native yes/no")
    else:
        _number(gold, "FinQA exe_ans")
    value, unit, scale, status = _candidate(candidate)
    executed = round(float(value), 5) if status == "answer" else value
    correct = status != "insufficient_information" and executed == gold
    return {"execution_answer_correct": bool(correct), "execution_answer": executed,
            "endpoint": "adapted_literal_execution_answer", "program_equivalence": None,
            "unit_ignored": unit, "scale_ignored": scale}


def score_tatqa(annotation: dict, candidate: dict) -> dict:
    """Call the pinned TaTQAEmAndF1 on arithmetic/count native annotations.

    Percent and percentage_points both serialize as native percent; the native
    answer/scale scores do not distinguish those independent semantic units.
    """
    if not isinstance(annotation, dict) or not {"answer_type", "answer", "scale"} <= annotation.keys():
        raise ValueError("TAT-QA requires native answer_type, answer and scale")
    answer_type, gold_scale = annotation["answer_type"], annotation["scale"]
    if (not isinstance(answer_type, str) or answer_type not in {"arithmetic", "count"} or
            not isinstance(gold_scale, str) or gold_scale not in _NATIVE_SCALES):
        raise ValueError("Only arithmetic/count with a native TAT-QA scale are supported")
    gold = _number(annotation["answer"], "TAT-QA answer")
    if answer_type == "count" and gold != gold.to_integral_value():
        raise ValueError("TAT-QA count annotation must be integral")
    value, unit, scale, status = _candidate(candidate)
    if status == "non_numeric_answer":
        raise ValueError("TAT-QA arithmetic/count does not accept a boolean answer")
    if unit in {"percent", "percentage_points"}:
        if scale != "none":
            raise ValueError("Percentage units cannot also have a monetary scale")
        native_scale = "percent"
    else:
        native_scale = "" if scale == "none" else scale
    metric = _load_official("tatqa").TaTQAEmAndF1()
    metric(dict(annotation), value, pred_scale=native_scale)
    exact_match, f1, scale_score, _ = metric.get_overall_metric()
    return {"answer_em": float(exact_match), "answer_f1": float(f1),
            "scale_score": float(scale_score), "native_prediction_scale": native_scale,
            "semantic_unit_not_checked": unit, "endpoint": "pinned_TaTQAEmAndF1"}


def replay_authored_controls() -> dict:
    """Replay fixed, researcher-authored fixtures; never read selected annotations."""
    receipt = json.loads((_BASE / "authored_controls.json").read_text())
    official_count = 0
    for case in receipt["cases"]:
        scorer = score_finqa_scalar if case["source"] == "finqa" else score_tatqa
        actual = scorer(case["annotation"], case["candidate"])
        if any(actual.get(key) != value for key, value in case["expected"].items()):
            raise AssertionError(f"Authored control failed: {case['id']}")
        if "authored_candidate_program" in case:
            official = _load_official("finqa")
            invalid, result = official.eval_program(
                official.program_tokenization(case["authored_candidate_program"]), [])
            endpoint = invalid == 0 and result == case["annotation"]["exe_ans"]
            if endpoint != actual["execution_answer_correct"] or result != actual["execution_answer"]:
                raise AssertionError(f"Official FinQA endpoint disagreement: {case['id']}")
            official_count += 1
    for case in receipt["schema_rejections"]:
        scorer = score_finqa_scalar if case["source"] == "finqa" else score_tatqa
        try:
            scorer(case["annotation"], case["candidate"])
        except ValueError:
            continue
        raise AssertionError(f"Invalid schema was accepted: {case['id']}")
    return {"status": "PASS", "authored_cases": len(receipt["cases"]),
            "official_finqa_comparisons": official_count,
            "schema_rejections": len(receipt["schema_rejections"]),
            "selected_cases_read": 0}
