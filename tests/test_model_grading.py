"""Executive summary: check units, half ties, strict extraction, and complete-panel accounting."""
from decimal import Decimal as D

import pytest

from answer_contract.types import Case
from model_grading.protocol import parse_final
from model_grading.scoring import evaluate, score_one


def test_units_and_strict_final_extraction():
    assert parse_final('Work\nFINAL: 8.5100 percent', 'corp_wacc') == (D('8.5100'), None)
    assert parse_final('FINAL: 0.0851 currency', 'corp_wacc')[1] == 'wrong_unit'
    assert parse_final('FINAL: 31.00 currency', 'cr_eq_gordon') == (D(31), None)
    assert parse_final('FINAL: 31 currency\nMore text', 'cr_eq_gordon')[1]
    assert parse_final('FINAL: 31 currency\nFINAL: 30 currency', 'cr_eq_gordon')[1]
    assert parse_final('Previously FINAL: 31\nFINAL: 31 currency', 'cr_eq_gordon')[1]
    assert parse_final('FINAL: 1,23 currency', 'eq_gordon')[1]
    assert parse_final('FINAL: 1e99999999999999999999 currency', 'eq_gordon')[1] == 'invalid_decimal'


def test_integer_half_tie_and_source_false_rejection():
    case = Case('cosimo', 'cr_eq_gordon', 'x', 'q', D('30.94'), D('30.94'),
                D(1), True, D(29))
    response = {'model_key': 'm', 'text': 'FINAL: 31.00 currency', 'finish_reason': 'stop'}
    row = score_one(response, case)
    assert row['visible_valid'] and not row['decisions']['source_abs_0.005']
    assert row['decisions']['integer_and_source_half']
    tie = Case('cosimo', 'cr_eq_gordon', 't', 'q', D('30.5'), D('30.5'), D(1), True, D(29))
    assert tie.accepts(D(30)) and tie.accepts(D(31)) and not tie.accepts(D('30.5'))
    response['finish_reason'] = 'length'
    assert score_one(response, case)['parse_error'] == 'length'


def test_duplicate_or_missing_attempts_fail_panel_validation():
    selection = [{'case_id': 'x'}]
    with pytest.raises(ValueError, match='full frozen'):
        evaluate(selection, [], ['m'])
    with pytest.raises(ValueError, match='full frozen'):
        evaluate(selection, [{'model_key': 'm', 'case_id': 'x'}] * 2, ['m'])
