"""Executive summary: separately diagnose numeric final answers after observed unit-format failures."""
import re
from decimal import Decimal as D, InvalidOperation

from .protocol import FINAL
from .scoring import POLICIES

NUMBER = FINAL.pattern.split('FINAL: ')[1].split(' (currency|percent)')[0]
NUMERIC_FINAL = re.compile(
    r'\**Final:\s*(\$?)' + NUMBER +
    r'\s*(currency|percent|%|USD|dollars?|<unit>)?\**', re.IGNORECASE)


def parse_numeric(text: str, family: str):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(re.findall(r'FINAL:', text, re.IGNORECASE)) != 1 or not lines:
        return None, 'missing_or_nonfinal_marker', None
    match = NUMERIC_FINAL.fullmatch(lines[-1])
    if not match:
        return None, 'invalid_numeric_final_line', None
    prefix, scalar, suffix = match.groups()
    suffix = (suffix or '').lower()
    if prefix and suffix in ('percent', '%'):
        return None, 'wrong_explicit_unit', 'wrong'
    stated = ('percent' if suffix in ('percent', '%') else
              'currency' if prefix or suffix in ('currency', 'usd', 'dollar', 'dollars') else None)
    required = 'percent' if family == 'corp_wacc' else 'currency'
    if stated and stated != required:
        return None, 'wrong_explicit_unit', 'wrong'
    try:
        value = D(scalar.replace(',', ''))
    except InvalidOperation:
        return None, 'invalid_decimal', None
    if not value.is_finite():
        return None, 'nonfinite_answer', None
    unit_state = 'explicit' if stated else 'placeholder' if suffix else 'absent'
    return value, None, unit_state


def numeric_score(response: dict, case) -> dict:
    value, error, units = parse_numeric(response.get('text', ''), case.family)
    if response['finish_reason'] not in ('eos', 'stop'):
        value, error = None, response['finish_reason']
    valid = value is not None and case.accepts(value)
    decisions = {p: False for p in POLICIES}
    if value is not None:
        decisions.update({
            'source_abs_0.005': abs(value - case.gold) <= D('.005'),
            'source_abs_0.5': abs(value - case.gold) <= D('.5'),
            'source_relative_5pct': abs(value - case.gold) <= abs(case.gold) * D('.05'),
            'visible_contract': valid,
        })
        decisions['integer_and_source_half'] = (
            value == value.to_integral_value() and decisions['source_abs_0.5'])
    return {'model_key': response['model_key'], 'case_id': case.case_id,
            'family': case.family, 'value': str(value) if value is not None else None,
            'parse_error': error, 'unit_state': units, 'visible_valid': valid,
            'decisions': decisions, 'finish_reason': response['finish_reason']}
