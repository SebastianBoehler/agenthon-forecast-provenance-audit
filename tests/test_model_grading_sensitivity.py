"""Executive summary: bound exploratory recovery to one stated final scalar and preserve unit errors."""
from decimal import Decimal as D

from model_grading.numeric_sensitivity import parse_numeric


def test_only_numeric_final_line_recovered():
    assert parse_numeric('Value 30.94\nFINAL: 31', 'cr_eq_gordon') == (D(31), None, 'absent')
    assert parse_numeric('Final: 16 <unit>', 'cr_eq_gordon') == (D(16), None, 'placeholder')
    assert parse_numeric('**FINAL: $31**', 'cr_eq_gordon') == (D(31), None, 'explicit')
    assert parse_numeric('Value 30.94\nAnswer 31', 'cr_eq_gordon')[0] is None
    assert parse_numeric('FINAL: 31 or 32', 'cr_eq_gordon')[0] is None
    assert parse_numeric('FINAL: 1,23', 'cr_eq_gordon')[0] is None
    assert parse_numeric('FINAL: 31\nFINAL: 32', 'cr_eq_gordon')[0] is None


def test_no_silent_rate_conversion_or_unit_repair():
    assert parse_numeric('FINAL: 0.0851', 'corp_wacc') == (D('.0851'), None, 'absent')
    assert parse_numeric('FINAL: $8.51', 'corp_wacc')[1] == 'wrong_explicit_unit'
    assert parse_numeric('FINAL: $8.51 percent', 'corp_wacc')[1] == 'wrong_explicit_unit'
    assert parse_numeric('FINAL: $8.51%', 'corp_wacc')[1] == 'wrong_explicit_unit'
    assert parse_numeric('FINAL: 31 percent', 'cr_eq_gordon')[1] == 'wrong_explicit_unit'
