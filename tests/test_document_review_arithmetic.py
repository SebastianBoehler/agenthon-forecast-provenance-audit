"""Executive summary: verify decimal arithmetic and reject executable annotation expressions."""
from decimal import Decimal

import pytest

from finance_document_review.arithmetic import calculate


def test_decimal_sign_and_percentage_semantics_are_preserved():
    assert calculate("0.1 + 0.2") == Decimal("0.3")
    assert calculate("(-110 - 158) / 158 * 100") < Decimal("-100")
    assert calculate("(198.27 - 100) / 100") == Decimal("0.9827")
    assert calculate("(198.27 - 100) / 100 * 100") == Decimal("98.27")
    assert calculate("1 + 1 + 1") == Decimal(3)


@pytest.mark.parametrize("expression", [
    "__import__('os').getcwd()", "open('source_targets.jsonl').read()",
    "value + 1", "[1, 2][0]", "True + 1", "2 ** 999999", "1 // 2", "1 % 2",
])
def test_annotation_text_cannot_execute_or_change_operator_semantics(expression):
    with pytest.raises(ValueError):
        calculate(expression)
