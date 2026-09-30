"""Executive summary: retain fixed denominators and separate numeric from interface changes."""
import json
from collections import Counter
from decimal import Decimal

from finance_document_local.manifest import digest, rows, verify
from finance_document_local.protocol import CONDITIONS, MODELS, OUT, ROOT
from finance_document_local.scoring import score
from finance_document_review.arithmetic import calculate
from finance_document_review.comparison import locked_match, percentage_sensitivity


def executable(row, reference):
    if row['condition'].startswith('compact_'):
        return {'requested': False, 'supported': None}
    answer = row['strict_candidate']
    if answer is None or answer['status'] != 'answer':
        return {'requested': True, 'supported': False, 'reason': 'no_strict_numeric_answer'}
    try:
        value = calculate(answer['calculation'])
    except (ValueError, ArithmeticError, SyntaxError) as exc:
        return {'requested': True, 'supported': False, 'reason': type(exc).__name__}
    executed = dict(answer, value=format(value, 'f'))
    return {'requested': True, 'supported': True, 'value': executed['value'],
            'locked': locked_match(reference, executed),
            'quantity_or_trace_certification': False}


def aggregate(selected):
    states = Counter(r['strict_parse_error'] or r['strict_candidate']['status'] for r in selected)
    return {'attempts': len(selected), 'response_states': dict(states),
            'strict_numeric': sum(r['strict_candidate'] is not None and
                                  r['strict_candidate']['status'] == 'answer' for r in selected),
            'status_only_numeric': sum(r['status_only_candidate'] is not None and
                                       r['status_only_candidate']['status'] == 'answer' for r in selected),
            'locked_eligible': sum(r['strict_locked']['eligible'] for r in selected),
            'strict_locked_matches': sum(r['strict_locked']['matches'] is True for r in selected),
            'status_only_locked_matches': sum(r['status_only_locked']['matches'] is True for r in selected),
            'projected_reference_matches': sum(r['strict_projected_reference']['matches'] is True for r in selected),
            'native_eligible': sum(r['strict_native']['eligible'] for r in selected),
            'native_credits': sum(r['strict_native']['credited'] is True for r in selected),
            'tatqa_answer_em_sum': sum(r['strict_native'].get('answer_em', 0) for r in selected),
            'tatqa_answer_f1_sum': sum(r['strict_native'].get('answer_f1', 0) for r in selected),
            'tatqa_scale_correct': sum(r['strict_native'].get('scale_score') == 1 for r in selected),
            'finqa_percent_fraction_credits': sum(r['finqa_percent_fraction_sensitivity'] is not None
                and r['finqa_percent_fraction_sensitivity']['credited'] is True for r in selected),
            'length_exhausted': sum(r['finish_reason'] == 'length' for r in selected),
            'full_expressions_supported': sum(r['arithmetic']['supported'] is True for r in selected)}


def paired(index, ids, left, right):
    transitions, details = Counter(), []
    for case in ids:
        a, b = index[case, left], index[case, right]
        if not a['strict_locked']['eligible']:
            continue
        before, after = a['strict_locked']['matches'], b['strict_locked']['matches']
        transitions[f'{before}->{after}'] += 1
        if before == after:
            continue
        ac, bc = a['strict_candidate'], b['strict_candidate']
        if ac is None or bc is None or ac['status'] != 'answer' or bc['status'] != 'answer':
            change = 'numeric_availability'
        else:
            numeric = Decimal(ac['value']) != Decimal(bc['value'])
            unit = (ac['unit'], ac['scale']) != (bc['unit'], bc['scale'])
            change = 'mixed' if numeric and unit else ('numeric_value' if numeric else 'unit_scale')
        details.append({'case_id': case, 'before': before, 'after': after,
                        'difference_class': change,
                        'left_candidate': ac, 'right_candidate': bc})
    return {'left': left, 'right': right, 'strict_locked_transitions': dict(transitions),
            'discordances': details}


def main():
    frozen = verify()
    references = {r['case_id']: r for r in rows(
        ROOT / 'outputs/finance-document-review-v1/pre_target_combined.jsonl')}
    annotations = {r['case_id']: r['original_annotation'] for r in rows(
        ROOT / 'outputs/finance-document-replay-v1/compact_native_annotations.jsonl')}
    ids = [r['case_id'] for r in rows(OUT / 'selection.jsonl')]
    responses, receipts = [], {}
    for model in MODELS:
        path = OUT / ('responses_' + model + '.jsonl')
        receipt = json.loads((OUT / ('receipt_' + model + '.json')).read_text())
        if receipt['response_sha256'] != digest(path) or receipt['freeze_sha256'] != digest(OUT / 'freeze.json'):
            raise ValueError('Completed response ledger or freeze identity changed')
        responses.extend(rows(path))
        receipts[model] = receipt
    expected = {(m, c, case) for m in MODELS for c in CONDITIONS for case in ids}
    counts = Counter((r['model_key'], r['condition'], r['case_id']) for r in responses)
    if set(counts) != expected or len(responses) != 256 or any(n != 1 for n in counts.values()):
        raise ValueError('Missing, duplicated or unexpected local attempt')
    scored = []
    for response in responses:
        reference, annotation = references[response['case_id']], annotations[response['case_id']]
        row = score(response, reference, annotation)
        row['finish_reason'] = response['finish_reason']
        row['arithmetic'] = executable(row, reference)
        row['finqa_percent_fraction_sensitivity'] = percentage_sensitivity(
            reference['source'], annotation, row['strict_candidate'])
        scored.append(row)
    result = {'executive_summary': 'Discovery-cohort interface/quantity-reminder comparison, not expert truth or model-size causality.',
              'attempts': len(scored), 'freeze_sha256': digest(OUT / 'freeze.json'),
              'locked_eligible_cases': frozen['locked_eligible_cases'], 'receipts': receipts,
              'models': {}, 'paired': {}}
    for model in MODELS:
        panel = [r for r in scored if r['model_key'] == model]
        index = {(r['case_id'], r['condition']): r for r in panel}
        result['models'][model] = {c: {'all': aggregate([r for r in panel if r['condition'] == c]),
            'sources': {s: aggregate([r for r in panel if r['condition'] == c and r['source'] == s])
                        for s in ('finqa', 'tatqa')}} for c in CONDITIONS}
        comparisons = [('compact_baseline', 'compact_reminder'), ('full_baseline', 'full_reminder'),
                       ('compact_baseline', 'full_baseline'), ('compact_reminder', 'full_reminder')]
        result['paired'][model] = [paired(index, ids, a, b) for a, b in comparisons]
    for name, text in [('scores.jsonl', ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in scored)),
                       ('results.json', json.dumps(result, indent=2) + '\n')]:
        with (OUT / name).open('x') as stream:
            stream.write(text)
    print(json.dumps({'attempts': 256, 'locked_eligible_cases': result['locked_eligible_cases'],
                      'models': {m: {c: result['models'][m][c]['all'] for c in CONDITIONS} for m in MODELS}}, indent=2))


if __name__ == '__main__':
    main()
