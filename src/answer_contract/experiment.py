"""Executive summary: measure explicit grading sensitivity and source preference validity."""
from collections import defaultdict
from decimal import Decimal as D, ROUND_HALF_UP
from statistics import median

from .types import Case

ABSOLUTE = [D(0), D('.0001'), D('.005'), D('.5'), D(1)]
RELATIVE = [D('.001'), D('.01'), D('.05')]


def original_accepts(case: Case, answer: D, kind: str, tolerance: D) -> bool:
    limit = tolerance if kind == 'absolute' else tolerance * abs(case.gold)
    return abs(answer - case.gold) <= limit + D('1e-20')


def summarize(cases: list[Case]) -> dict:
    counts = defaultdict(int)
    unique = {}
    widths = []
    for case in cases:
        unique.setdefault(case.prompt, case)
        counts['rows'] += 1
        counts['gold_invalid_exact_contract'] += not case.accepts(case.gold)
        counts['gold_matches_raw_within_serialization'] += abs(case.gold-case.formula) <= D('.005')+D('1e-20')
        counts['ties'] += case.requested_rounding and abs(case.formula-case.target) == D('.5')
        counts['mutation_answer_collides'] += case.accepts(case.mutation)
        if case.independent_formula is not None:
            counts['independent_identity_checked'] += 1
            if abs(case.independent_formula - case.formula) > D('1e-20'):
                raise ValueError(f'Independent identity fails: {case.case_id}')
        if case.interval:
            low, high = case.interval
            counts['gold_feasible_rounded_inputs'] += low-case.quantum/2 <= case.gold <= high+case.quantum/2
            counts['plus_one_percent_feasible_rounded_inputs'] += low <= case.formula*D('1.01') <= high
            widths.append(float((high-low)/case.formula))
            if case.hidden_formula is not None:
                counts['hidden_formula_matches_gold'] += abs(case.hidden_formula-case.gold) <= D('.00005')+D('1e-20')
        if case.chosen is not None:
            counts['preference_pairs'] += 1
            chosen, rejected = case.accepts(case.chosen), case.accepts(case.rejected)
            state = ('valid' if chosen else 'invalid') + '_chosen_' + ('valid' if rejected else 'invalid') + '_rejected'
            counts[state] += 1
    counts['unique_questions'] = len(unique)
    counts['unique_gold_invalid'] = len({case.prompt for case in cases if not case.accepts(case.gold)})
    result = dict(counts)
    if widths:
        result['median_relative_interval_width'] = median(widths)
    return result


def comparator_rows(cases: list[Case]) -> list[dict]:
    result = []
    for kind, values in [('absolute', ABSOLUTE), ('relative', RELATIVE)]:
        for tolerance in values:
            counts = defaultdict(int)
            for case in cases:
                counts['valid_answer_count'] += 1
                counts['valid_answer_rejected'] += not original_accepts(case, case.target, kind, tolerance)
                if not case.accepts(case.mutation):
                    counts['wrong_formula_count'] += 1
                    counts['wrong_formula_accepted'] += original_accepts(case, case.mutation, kind, tolerance)
                if case.rejected is not None:
                    valid = case.accepts(case.rejected)
                    counts['source_rejected_valid' if valid else 'source_rejected_invalid'] += 1
                    if not valid:
                        counts['source_invalid_rejected_accepted'] += original_accepts(case, case.rejected, kind, tolerance)
            result.append({'kind': kind, 'tolerance': str(tolerance), **counts})
    return result


def repairs(cases: list[Case]) -> list[dict]:
    result = []
    for rounding in [False, True]:
        row = defaultdict(int)
        for case in cases:
            row['valid_answer_count'] += 1
            row['valid_answer_rejected'] += not case.accepts(case.target, rounding)
            if not case.accepts(case.mutation):
                row['wrong_formula_count'] += 1
                row['wrong_formula_accepted'] += case.accepts(case.mutation, rounding)
            if case.rejected is not None and not case.accepts(case.rejected):
                row['source_rejected_invalid'] += 1
                row['source_invalid_rejected_accepted'] += case.accepts(case.rejected, rounding)
        result.append({'repair': 'visible_formula_and_requested_rounding' if rounding else 'visible_formula_only', **row})
    return result


def rounded_error_controls(cases: list[Case]) -> dict:
    counts = defaultdict(int)
    for case in cases:
        if not case.requested_rounding or case.rejected is None:
            continue
        projected = case.rejected.quantize(case.quantum, rounding=ROUND_HALF_UP)
        counts['source_rejected_answers'] += 1
        if case.accepts(projected):
            counts['rounded_error_numerically_valid'] += 1
            continue
        counts['rounded_error_numerically_invalid'] += 1
        counts['integer_format_only_accepted'] += 1
        counts['original_relative_5pct_accepted'] += original_accepts(case, projected, 'relative', D('.05'))
        counts['original_absolute_half_accepted'] += original_accepts(case, projected, 'absolute', D('.5'))
        counts['full_contract_accepted'] += case.accepts(projected)
        counts['integer_filter_plus_half_accepted'] += projected == projected.to_integral_value() and original_accepts(case, projected, 'absolute', D('.5'))
    rows = [case for case in cases if case.requested_rounding]
    counts['integer_filter_plus_half_valid_rejected'] = sum(
        not original_accepts(case, case.target, 'absolute', D('.5')) for case in rows)
    return dict(counts)


def integer_filter_baseline(cases: list[Case]) -> dict:
    counts = defaultdict(int)
    for case in cases:
        if not case.requested_rounding:
            continue
        def accepted(answer):
            return answer == answer.to_integral_value() and original_accepts(case, answer, 'absolute', D('.5'))
        counts['valid_answer_count'] += 1
        counts['valid_answer_rejected'] += not accepted(case.target)
        if case.rejected is not None and not case.accepts(case.rejected):
            counts['source_rejected_invalid'] += 1
            counts['source_invalid_rejected_accepted'] += accepted(case.rejected)
    return dict(counts)


def row_record(case: Case) -> dict:
    return {'source': case.source, 'family': case.family, 'id': case.case_id,
            'prompt_sha256': __import__('hashlib').sha256(case.prompt.encode()).hexdigest(),
            'gold': str(case.gold), 'formula': str(case.formula), 'target': str(case.target),
            'gold_valid': case.accepts(case.gold), 'requested_rounding': case.requested_rounding,
            'chosen_valid': case.accepts(case.chosen) if case.chosen is not None else None,
            'rejected_valid': case.accepts(case.rejected) if case.rejected is not None else None,
            'interval': [str(item) for item in case.interval] if case.interval else None}
