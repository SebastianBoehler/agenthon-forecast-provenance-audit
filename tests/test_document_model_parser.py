"""Executive summary: preserve ambiguous/invalid JSON and nonnumeric task types in scoring."""
import json

from finance_document_review.model_protocol import parse_answer


def answer(**changes):
    row = {"status": "answer", "value": "98.27", "unit": "percent", "scale": "none",
           "calculation": "(198.27-100)/100*100", "evidence": ["table row 1"]}
    row.update(changes)
    return json.dumps(row)


def test_no_format_repair_or_unit_value_coercion():
    assert parse_answer(answer())[1] is None
    assert parse_answer("```json\n" + answer() + "\n```")[1] == "invalid_json"
    assert parse_answer(answer(value=98.27))[1] == "missing_value_or_unit"
    assert parse_answer(answer(value="NaN"))[1] == "nonfinite_value"
    assert parse_answer(answer(status=[]))[1] == "invalid_field_types"
    assert parse_answer(answer(unit="", value="0.9827"))[1] == "missing_value_or_unit"


def test_duplicate_fields_abstention_and_yes_no_remain_distinct():
    duplicate = answer().replace('"value": "98.27"', '"value": "98.27", "value": "0.9827"')
    assert parse_answer(duplicate)[1] == "invalid_json"
    assert parse_answer(answer(status="insufficient_information", value=None))[1] is None
    assert parse_answer(answer(status="insufficient_information", value="0"))[1] == "nonempty_abstention"
    assert parse_answer(answer(status="non_numeric_answer", value="no", unit="boolean"))[1] is None
    assert parse_answer(answer(status="non_numeric_answer", value=[], unit="boolean"))[1] == "invalid_non_numeric_answer"
