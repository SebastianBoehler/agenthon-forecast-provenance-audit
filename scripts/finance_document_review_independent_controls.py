"""Executive summary: exercise frozen endpoint boundaries with authored rational controls.

No model calls, selected annotations, corpus programs or blind-review changes.
Passing controls confirm observed scoring behavior, including explicitly retained
dimensional gaps; they do not certify the comparator as semantic ground truth.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

from finance_document_review.comparison import locked_match, native_score, percentage_sensitivity
from finance_document_review.native_metrics import verify_native_sources
from finance_document_review.units import signature

ROOT = Path(__file__).resolve().parents[1]


def number(value: Fraction | str | int) -> str:
    fraction = value if isinstance(value, Fraction) else Fraction(value)
    with localcontext() as ctx:
        ctx.prec = 50
        return format(Decimal(fraction.numerator) / Decimal(fraction.denominator), 'f')


def candidate(value: str, unit: str, scale: str = 'none') -> dict:
    return {'status': 'answer', 'value': value, 'unit': unit, 'scale': scale,
            'calculation': '', 'evidence': []}


def control(name, exact, reference_unit, answer, source, annotation,
            expected_locked, expected_native, expected_scale, explanation,
            dimensional_match=True):
    return {'id': name, 'reference': {
        'joint_status': 'agreed_determinate_numeric', 'unit_a': signature(reference_unit),
        'reference_values': [number(exact)]}, 'candidate': answer, 'source': source,
        'annotation': annotation, 'expected_locked_match': expected_locked,
        'expected_native_credit': expected_native, 'expected_scale_score': expected_scale,
        'independent_dimensional_match': dimensional_match, 'interpretation': explanation}


def fixtures() -> list[dict]:
    third = Fraction(100, 3)
    tat_percent = {'answer_type': 'arithmetic', 'answer': 33.33, 'scale': 'percent'}
    return [
        control('exact_percent', third, 'percent', candidate(number(third), 'percent'),
                'tatqa', tat_percent, True, True, 1,
                'Unrounded exact rational target; native normalization rounds to two decimals.'),
        control('source_rounded_percent', third, 'percent', candidate('33.33', 'percent'),
                'tatqa', tat_percent, False, True, 1,
                'Native-rounded credit with locked-unrounded mismatch is a precision convention, '
                'not an unconditional arithmetic error.'),
        control('equivalent_fraction', third, 'percent', candidate(number(Fraction(1, 3)), 'ratio'),
                'tatqa', tat_percent, True, True, 0,
                'Equivalent ratio passes both value channels but fails native scale accuracy.'),
        control('factor100_percent_error', third, 'percent', candidate('0.33333333', 'percent'),
                'tatqa', tat_percent, False, False, 1,
                'Correct scale label alone does not guarantee correct answer magnitude.'),
        control('monetary_rescaling', 1, 'thousand USD', candidate('1000', 'USD'),
                'tatqa', {'answer_type': 'arithmetic', 'answer': 1, 'scale': 'thousand'},
                True, True, 0, 'Equal economic amount; native answer EM and scale diverge.'),
        control('wrong_currency', 1, 'million USD', candidate('1', 'EUR', 'million'),
                'tatqa', {'answer_type': 'arithmetic', 'answer': 1, 'scale': 'million'},
                False, True, 1, 'Native answer/scale do not check currency identity.', False),
        control('duration_vs_shares', Fraction(5, 2), 'years', candidate('2.5', 'shares'),
                'finqa', {'exe_ans': 2.5}, True, True, None,
                'Frozen unit signature collapses duration and share count into count.', False),
        control('per_share_vs_total', Fraction(36, 100), 'USD per share', candidate('0.36', 'USD'),
                'finqa', {'exe_ans': 0.36}, True, True, None,
                'Frozen monetary signature does not retain the per-share denominator.', False),
        control('percentage_point_vs_percent', Fraction(15, 4), 'percentage points',
                candidate('3.75', 'percent'), 'tatqa',
                {'answer_type': 'arithmetic', 'answer': 3.75, 'scale': 'percent'},
                False, True, 1, 'Native percent scale conflates relative percent and points.', False),
        control('finqa_literal_vs_fraction', third, 'percent', candidate(number(third), 'percent'),
                'finqa', {'exe_ans': 0.33333}, True, False, None,
                'Literal JSON scalar differs from FinQA fraction execution convention; '
                'declared percent-as-fraction sensitivity should credit the answer.'),
        control('finqa_rounded_native_percent', Fraction('472.7') / Fraction('635.6') * 100,
                'percent', candidate('74.371', 'percent'), 'finqa', {'exe_ans': 0.74371},
                False, False, None, 'FinQA five-decimal fraction projection becomes 74.371 '
                'percent; sensitivity credits it although the unrounded comparator does not.'),
        control('cents_to_dollars', 44, 'cents per ordinary share', candidate('0.44', 'USD per share'),
                'finqa', {'exe_ans': 44}, True, False, None,
                'Valid dimensional rescaling is not part of literal FinQA scalar adaptation.'),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sources = verify_native_sources()
    rows = fixtures()
    for row in rows:
        match = locked_match(row['reference'], row['candidate'])
        native = native_score(row['source'], row['annotation'], row['candidate'])
        sensitivity = percentage_sensitivity(row['source'], row['annotation'], row['candidate'])
        assert match['matches'] == row['expected_locked_match'], row['id']
        assert native['credited'] == row['expected_native_credit'], row['id']
        if row['expected_scale_score'] is not None:
            assert native['scale_score'] == row['expected_scale_score'], row['id']
        if row['id'] in {'finqa_literal_vs_fraction', 'finqa_rounded_native_percent'}:
            assert sensitivity['credited'], row['id']
        row.update(locked_result=match, native_result=native, percentage_sensitivity=sensitivity)
    paths = ['src/finance_document_review/comparison.py',
             'src/finance_document_review/native_metrics.py',
             'src/finance_document_review/units.py',
             'scripts/finance_document_review_independent_controls.py']
    receipt = {'executive_summary': 'Authored endpoint controls pass; two broad-unit '
               'dimensional gaps and source-rounding differences remain disclosed.',
               'status': 'PASS_EXPECTED_FROZEN_BEHAVIOR', 'created_utc': datetime.now(timezone.utc).isoformat(),
               'controls': len(rows), 'selected_annotations_read': 0, 'model_calls': 0,
               'reference_arithmetic': 'Independent Fraction literals, Decimal precision 50.',
               'sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
               'native_source_integrity': sources, 'cases': rows}
    with args.output.open('x') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'status': receipt['status'], 'controls': len(rows), 'output': str(args.output)}))


if __name__ == '__main__':
    main()
