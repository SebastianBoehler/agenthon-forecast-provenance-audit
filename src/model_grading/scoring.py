"""Executive summary: grade identical model outputs with independent and source-label policies."""
from collections import defaultdict
from decimal import Decimal as D, localcontext

from answer_contract.sources import cosimo_cases
from .protocol import parse_final

POLICIES = ('source_abs_0.005', 'source_abs_0.5', 'source_relative_5pct',
            'integer_and_source_half', 'visible_contract')


def score_one(response: dict, case) -> dict:
    value, error = parse_final(response.get('text', ''), case.family)
    if response['finish_reason'] not in ('stop', 'eos'):
        value, error = None, response['finish_reason']
    validity = value is not None and case.accepts(value)
    decisions = {p: False for p in POLICIES}
    if value is not None:
        decisions['source_abs_0.005'] = abs(value - case.gold) <= D('.005')
        decisions['source_abs_0.5'] = abs(value - case.gold) <= D('.5')
        decisions['source_relative_5pct'] = abs(value - case.gold) <= abs(case.gold) * D('.05')
        decisions['integer_and_source_half'] = (
            value == value.to_integral_value() and decisions['source_abs_0.5'])
        decisions['visible_contract'] = validity
    return {'model_key': response['model_key'], 'case_id': case.case_id,
            'family': case.family, 'value': str(value) if value is not None else None,
            'parse_error': error, 'visible_valid': validity,
            'gold': str(case.gold), 'formula': str(case.formula),
            'decisions': decisions, 'finish_reason': response['finish_reason']}


def summarize(rows: list[dict]) -> dict:
    return {
        'attempts': len(rows), 'parsed_completed': sum(r['value'] is not None for r in rows),
        'visible_valid': sum(r['visible_valid'] for r in rows),
        'failures': {e: sum(r['parse_error'] == e for r in rows)
                     for e in sorted({r['parse_error'] for r in rows if r['parse_error']})},
        'policies': {p: {
            'accepted': sum(r['decisions'][p] for r in rows),
            'valid_rejected': sum(r['visible_valid'] and not r['decisions'][p] for r in rows),
            'numeric_invalid_accepted': sum(r['value'] is not None and not r['visible_valid']
                                            and r['decisions'][p] for r in rows),
            'paired_changes': sum(r['visible_valid'] != r['decisions'][p] for r in rows),
        } for p in POLICIES},
    }


def evaluate(selection: list[dict], responses: list[dict], models: list[str]):
    selected = {r['case_id']: r for r in selection}
    expected = {(m, c) for m in models for c in selected}
    actual = [(r['model_key'], r['case_id']) for r in responses]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise ValueError('Response keys do not equal the full frozen model/question panel')
    with localcontext() as context:
        context.prec = 50
        cases = {c.case_id: c for c in cosimo_cases() if c.case_id in selected}
        for c in cases.values():
            row = selected[c.case_id]
            if row['prompt'] != c.prompt or D(row['formula']) != c.formula:
                raise ValueError('Frozen question or numerical oracle changed')
        scored = []
        for response in responses:
            frozen = selected[response['case_id']]
            if response['question_hash'] != frozen['question_hash']:
                raise ValueError('Response does not refer to its frozen question')
            scored.append(score_one(response, cases[response['case_id']]))
    groups = defaultdict(list)
    for row in scored:
        groups[row['model_key']].append(row)
    results = {'status': 'executed_model_grading_not_training_effect',
               'questions': len(selection), 'responses': len(scored),
               'models': {m: {'aggregate': summarize(groups[m]),
                             'families': {f: summarize([r for r in groups[m] if r['family'] == f])
                                          for f in sorted({r['family'] for r in groups[m]})}}
                          for m in models}}
    return scored, results
