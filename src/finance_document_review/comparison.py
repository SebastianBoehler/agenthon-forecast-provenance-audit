"""Executive summary: compare locked numeric/unit readings with unchanged answer metrics.

The locked comparator checks final values and declared units, not semantic truth,
reasoning traces or human-expert adjudication. FinQA scalars are adapted endpoints.
"""
from __future__ import annotations

from decimal import Decimal

from finance_document_review.model_protocol import parse_answer
from finance_document_review.native_metrics import score_finqa_scalar, score_tatqa
from finance_document_review.units import compatible_units, signature


def locked_match(reference: dict, candidate: dict | None) -> dict:
    if reference['joint_status'] != 'agreed_determinate_numeric':
        return {'eligible': False, 'matches': None, 'reason': reference['joint_status']}
    if candidate is None:
        return {'eligible': True, 'matches': False, 'reason': 'parse_or_request_failure'}
    if candidate['status'] != 'answer':
        return {'eligible': True, 'matches': False, 'reason': candidate['status']}
    unit = signature(candidate['unit'], candidate['scale'])
    if not compatible_units(reference['unit_a'], unit):
        return {'eligible': True, 'matches': False, 'reason': 'incompatible_or_unknown_unit',
                'candidate_unit_signature': unit}
    # Compare in the recorded reference unit, including its monetary multiplier.
    value = Decimal(candidate['value']) * Decimal(unit['factor']) / Decimal(reference['unit_a']['factor'])
    targets = [Decimal(v) for v in reference['reference_values']]
    valid = any(abs(value - target) <= max(Decimal('1e-8'), abs(target) * Decimal('1e-7'))
                for target in targets)
    return {'eligible': True, 'matches': valid, 'reason': 'matches' if valid else 'numeric_difference',
            'value_in_reference_units': str(value), 'candidate_unit_signature': unit}


def native_score(source: str, annotation: dict, candidate: dict | None) -> dict:
    if candidate is None:
        return {'eligible': False, 'credited': None, 'reason': 'parse_or_request_failure'}
    try:
        if source == 'finqa':
            scored = score_finqa_scalar(annotation, candidate)
            return {'eligible': True, 'credited': scored['execution_answer_correct'], **scored}
        scored = score_tatqa(annotation, candidate)
        return {'eligible': True, 'credited': scored['answer_em'] == 1, **scored}
    except ValueError as exc:
        return {'eligible': False, 'credited': None, 'reason': 'adapter_ineligible', 'detail': str(exc)}


def percentage_sensitivity(source: str, annotation: dict, candidate: dict | None) -> dict | None:
    if source != 'finqa' or candidate is None:
        return None
    changed = dict(candidate)
    if candidate['status'] == 'answer' and candidate['unit'] in {'percent', 'percentage_points'}:
        changed['value'] = format(Decimal(candidate['value']) / 100, 'f')
    return native_score(source, annotation, changed)


def evaluate_response(response: dict, reference: dict, annotation: dict) -> dict:
    candidate, error = parse_answer(response.get('text', ''))
    failure = response.get('error') or (response.get('provider') != 'SiliconFlow')
    if failure:
        candidate, error = None, 'request_or_provider_failure'
    financial = locked_match(reference, candidate)
    native = native_score(reference['source'], annotation, candidate)
    sensitivity = percentage_sensitivity(reference['source'], annotation, candidate)
    return {'case_id': response['case_id'], 'source': reference['source'],
            'model_key': response['model_key'], 'condition': response['condition'],
            'joint_status': reference['joint_status'], 'finish_reason': response.get('finish_reason'),
            'parse_error': error, 'candidate': candidate, 'locked_comparator': financial,
            'native_or_adapted': native, 'finqa_percent_fraction_sensitivity': sensitivity,
            'semantic_or_trace_certification': False}


def aggregate(rows: list[dict], endpoint: str = 'native_or_adapted') -> dict:
    states, matrix = {}, {}
    eligible_reference = 0
    for row in rows:
        state = row['parse_error'] or row['candidate']['status']
        states[state] = states.get(state, 0) + 1
        f, n = row['locked_comparator'], row[endpoint]
        eligible_reference += int(f['eligible'])
        if f['eligible']:
            if n is None or not n['eligible']:
                key = 'native_ineligible'
            else:
                key = ('match' if f['matches'] else 'mismatch') + ('_credited' if n['credited'] else '_denied')
            matrix[key] = matrix.get(key, 0) + 1
    return {'attempts': len(rows), 'response_states': states, 'locked_reference_cases': eligible_reference,
            'outside_locked_reference': len(rows) - eligible_reference, 'paired_matrix': matrix,
            'locked_matches_all_attempts': sum(r['locked_comparator']['matches'] is True for r in rows),
            'native_credits_all_attempts': sum(r[endpoint] is not None and r[endpoint]['credited'] is True for r in rows),
            'native_ineligible_all_attempts': sum(r[endpoint] is None or not r[endpoint]['eligible'] for r in rows)}
