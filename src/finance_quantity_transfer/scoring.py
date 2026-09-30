"""Executive summary: score typed values, safe arithmetic and literal native labels separately."""

import json
import re
from decimal import Decimal

from finance_document_review.arithmetic import calculate

from .protocol import SCALES, UNITS, parse

RTOL, ATOL = Decimal("0.0001"), Decimal("0.00000001")
SCALED_UNITS = {"currency", "currency_per_share", "currency_per_year", "count"}
JUDGE_FIELDS = {"verdict", "requested_quantity", "operand_checks", "unit_check",
                "reason", "evidence"}


def native_decimal(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError("Native value must be a finite decimal-compatible scalar")
    result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError("Nonfinite native value")
    return result


def typed_value(value, unit, scale):
    if unit not in UNITS or unit in {"boolean", "unknown"} or scale not in SCALES:
        raise ValueError("Unrecognized numerical unit/scale")
    if unit not in SCALED_UNITS and scale != "none":
        raise ValueError("Dimensionless/rate/duration unit cannot carry monetary scale")
    if not isinstance(value, str):
        raise ValueError("Numeric value must be a decimal string")
    number = Decimal(value)
    if not number.is_finite():
        raise ValueError("Nonfinite decimal")
    return number * SCALES[scale]


def parse_answer(text):
    answer, error = parse(text)
    if error:
        return None, error
    try:
        status, expression = answer["status"], answer["calculation"]
        if not all(isinstance(x, str) for x in answer["evidence"]):
            raise ValueError("Evidence locations must be strings")
        if status == "answer":
            typed_value(answer["value"], answer["unit"], answer["scale"])
            calculate(expression)
        elif expression.strip():
            raise ValueError("Abstention/Boolean calculation must be empty")
        if status == "non_numeric_answer" and answer["scale"] != "none":
            raise ValueError("Boolean scale must be none")
        return answer, None
    except (ValueError, TypeError, ArithmeticError, SyntaxError) as failure:
        return None, str(failure)


def close(actual, reference):
    return abs(actual - reference) <= max(ATOL, RTOL * abs(reference))


def score(text, reference, native_target=None):
    answer, error = parse_answer(text)
    eligible = reference["eligible"] is True
    result = {"reference_kind": "AI_provisional", "primary_eligible": eligible,
              "schema_valid": error is None, "schema_error": error,
              "reported_numeric_typed_match": False,
              "expression_numeric_typed_match": False,
              "reported_expression_consistent": False,
              "native_literal_exact": None if native_target is None else False}
    if answer is None or answer["status"] != "answer":
        return result
    actual = typed_value(answer["value"], answer["unit"], answer["scale"])
    expression = calculate(answer["calculation"])
    expressed = typed_value(str(expression), answer["unit"], answer["scale"])
    result["expression_value"] = str(expression)
    result["reported_expression_consistent"] = close(actual, expressed)
    if eligible:
        target = typed_value(reference["value"], reference["unit"], reference["scale"])
        same_unit = answer["unit"] == reference["unit"]
        result["reported_numeric_typed_match"] = same_unit and close(actual, target)
        result["expression_numeric_typed_match"] = same_unit and close(expressed, target)
    if native_target is not None:
        # Literal channel: no percent conversion, scaling, tolerance or semantic oracle.
        result["native_literal_exact"] = Decimal(answer["value"]) == native_decimal(native_target["value"])
    return result


def location(context, path):
    if not isinstance(path, str) or not re.fullmatch(
        r"[A-Za-z_][A-Za-z_0-9]*(?:(?:\.[A-Za-z_][A-Za-z_0-9]*)|(?:\[\d+\]))*", path
    ):
        raise ValueError("Invalid context pointer")
    value = context
    for key, index in re.findall(r"([A-Za-z_][A-Za-z_0-9]*)|\[(\d+)\]", path):
        value = value[key] if key else value[int(index)]
    if not isinstance(value, str):
        raise ValueError("Evidence pointer must identify original text/cell")
    return value


def parse_judge(text, context, candidate_error):
    try:
        pairs = json.loads(text, object_pairs_hook=lambda pairs: pairs)
        if not isinstance(pairs, list) or any(not isinstance(x, tuple) for x in pairs):
            raise ValueError("Judge must return one JSON object")
        judgment = dict(pairs)
        if len(judgment) != len(pairs) or set(judgment) != JUDGE_FIELDS:
            raise ValueError("Judge duplicate/missing/extra field")
        # Decode again after duplicate detection; nested objects also require uniqueness.
        def unique(items):
            if len(dict(items)) != len(items):
                raise ValueError("Judge duplicate key")
            return dict(items)
        judgment = json.loads(text, object_pairs_hook=unique,
                              parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Nonfinite JSON")))
        if judgment["verdict"] not in {"supported", "contradicted", "ambiguous", "unassessable"}:
            raise ValueError("Judge verdict")
        if not all(isinstance(judgment[k], str) for k in
                   {"requested_quantity", "unit_check", "reason"}):
            raise ValueError("Judge text field")
        if not isinstance(judgment["operand_checks"], list) or not all(
            isinstance(x, dict) for x in judgment["operand_checks"]
        ):
            raise ValueError("Judge operand_checks")
        if not isinstance(judgment["evidence"], list):
            raise ValueError("Judge evidence")
        for path in judgment["evidence"]:
            location(context, path)
        effective = "unassessable" if candidate_error else judgment["verdict"]
        return {"judgment": judgment, "effective_verdict": effective,
                "candidate_malformed": candidate_error is not None,
                "protocol_violation": bool(candidate_error and judgment["verdict"] != "unassessable")}, None
    except (ValueError, TypeError, KeyError, IndexError) as error:
        return {"judgment": None, "effective_verdict": "unassessable",
                "candidate_malformed": candidate_error is not None,
                "protocol_violation": True}, str(error)
