"""Executive summary: disclose precision sensitivity and separate native answer/scale channels.

This later reporting diagnostic leaves the prospective strict comparator unchanged.
Matching an independently rounded reference is not certification of financial truth.
"""
from decimal import Decimal, ROUND_HALF_EVEN, localcontext

from finance_document_review.comparison import locked_match


def reference_projection(reference: dict, candidate: dict | None) -> dict:
    match = locked_match(reference, candidate)
    if not match['eligible'] or candidate is None or candidate['status'] != 'answer':
        return {'matches': match['matches'], 'additional_rounded_match': False}
    value = match.get('value_in_reference_units')
    if value is None:
        return {'matches': False, 'additional_rounded_match': False}
    factor = Decimal(reference['unit_a']['factor'])
    proportion = reference['unit_a']['dimension'] in {'proportion', 'percentage_points'}
    # Source-specific fixed precision is declared from inspected code, never fitted per gold.
    quantum = Decimal('.01') if reference['source'] == 'tatqa' else Decimal('.00001')
    if reference['source'] == 'finqa' and proportion:
        quantum = Decimal('.00001') / (factor if proportion else Decimal(1))
        if reference['unit_a']['dimension'] == 'percentage_points':
            quantum = Decimal('.001')
    # Count integrality remains the original unrounded endpoint.
    if reference['unit_a']['dimension'] == 'count':
        return {'matches': match['matches'], 'additional_rounded_match': False}
    with localcontext() as context:
        context.prec = 70
        projected = [(Decimal(v) / quantum).quantize(Decimal(1), rounding=ROUND_HALF_EVEN) * quantum
                     for v in reference['reference_values']]
        rounded = any(abs(Decimal(value) - v) <= max(Decimal('1e-8'), abs(v) * Decimal('1e-7'))
                      for v in projected)
    return {'matches': bool(match['matches'] or rounded),
            'additional_rounded_match': bool(rounded and not match['matches']),
            'quantum_in_reference_unit': str(quantum), 'projection_rule': 'decimal_half_even'}


def channels(rows: list[dict]) -> dict:
    scored = [r['native_or_adapted'] for r in rows if r['native_or_adapted']['eligible']]
    numeric = [r for r in scored if 'answer_em' in r]
    return {'attempts': len(rows), 'native_eligible': len(scored),
            'tatqa_answer_em_sum': sum(r['answer_em'] for r in numeric),
            'tatqa_answer_f1_sum': sum(r['answer_f1'] for r in numeric),
            'tatqa_scale_correct': sum(r['scale_score'] == 1 for r in numeric),
            'tatqa_answer_and_scale_correct': sum(r['answer_em'] == r['scale_score'] == 1 for r in numeric)}
