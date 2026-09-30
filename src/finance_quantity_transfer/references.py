"""Executive summary: validate and compare provisional AI references before label unblinding."""

import ast
from decimal import Decimal

from financial_review_io import review_record
from finance_document_review.arithmetic import calculate
from .protocol import SCALES, UNITS

FIELDS = set('case_id status requested_quantity entity time_scope assumptions operand_bindings unit scale currency expression value alternatives evidence_paths rationale'.split())
STATUSES = {'determinate', 'conditional', 'ambiguous', 'insufficient_information', 'non_numeric'}


def validate(record, packet):
    result = review_record(record, packet, FIELDS, STATUSES, 'case_id')
    if record['unit'] not in UNITS or record['scale'] not in SCALES:
        raise ValueError('Unknown unit/scale')
    if record['currency'] is not None and not isinstance(record['currency'], str):
        raise ValueError('Invalid currency')
    expression = record['expression']
    if expression is None:
        if record['value'] is not None or record['status'] == 'determinate':
            raise ValueError('Missing determinate expression or value without expression')
    else:
        if not isinstance(record['value'], str) or calculate(expression) != Decimal(record['value']):
            raise ValueError('Expression/value disagreement')
        literals = {ast.get_source_segment(expression, node) for node in ast.walk(ast.parse(expression, mode='eval')) if isinstance(node, ast.Constant)}
        bound_magnitudes = {abs(Decimal(b['literal'])) for b in record['operand_bindings']}
        if not {abs(Decimal(x)) for x in literals} <= bound_magnitudes:
            raise ValueError('Primary expression has an unbound numerical literal')
    if not isinstance(record['alternatives'], list):
        raise ValueError('Invalid alternatives')
    for alternative in record['alternatives']:
        if set(alternative) != {'expression','unit','scale','interpretation'}:
            raise ValueError('Invalid alternative schema')
        if alternative['unit'] not in UNITS or alternative['scale'] not in SCALES:
            raise ValueError('Invalid alternative unit/scale')
        if not isinstance(alternative['interpretation'], str) or not alternative['interpretation']:
            raise ValueError('Missing alternative interpretation')
        if alternative['expression'] is not None:
            calculate(alternative['expression'])
    return result


def compare(a, b):
    determinate = a['status'] == b['status'] == 'determinate'
    unit_agreement = a['unit'] == b['unit'] and a['unit'] != 'unknown'
    currency_conflict = a['currency'] and b['currency'] and a['currency'] != b['currency']
    numeric = False
    if a['value'] is not None and b['value'] is not None:
        x = Decimal(a['value']) * SCALES[a['scale']]
        y = Decimal(b['value']) * SCALES[b['scale']]
        numeric = abs(x-y) <= max(Decimal('1e-10'), abs(x)*Decimal('1e-10'))
    return dict(case_id=a['case_id'], a_status=a['status'], b_status=b['status'],
        numeric_agreement=numeric, unit_agreement=unit_agreement,
        currency_conflict=bool(currency_conflict),
        provisional_numeric_candidate=bool(determinate and unit_agreement and numeric and not currency_conflict),
        a_quantity=a['requested_quantity'], b_quantity=b['requested_quantity'],
        a_time=a['time_scope'], b_time=b['time_scope'])
