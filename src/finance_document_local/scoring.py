"""Executive summary: keep requested-schema compliance and status sensitivity separate."""
import json

from finance_document_review.comparison import locked_match, native_score
from finance_document_review.model_protocol import parse_answer
from finance_document_review.reporting import reference_projection


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON field')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f'Nonstandard JSON constant: {value}')


def candidate(text, condition, *, normalize_status=False):
    try:
        obj = json.loads(text, object_pairs_hook=unique_object,
                         parse_constant=reject_constant)
    except (ValueError, TypeError):
        return None, 'invalid_json'
    fields = {'status', 'value', 'unit', 'scale'}
    compact = condition.startswith('compact_')
    if not compact:
        fields |= {'calculation', 'evidence'}
    if not isinstance(obj, dict) or set(obj) != fields:
        return None, 'invalid_fields'
    # Scoring adapter only: these absent trace fields are never certified/executed.
    normalized = dict(obj, calculation='', evidence=[]) if compact else dict(obj)
    if (normalize_status and isinstance(normalized['status'], str)
            and isinstance(normalized['value'], str)):
        if normalized['value'] not in {'yes', 'no'}:
            normalized['status'] = 'answer'
    return parse_answer(json.dumps(normalized))


def score(response, reference, annotation):
    failed = (response.get('error') is not None or response.get('runtime_ok') is not True
              or response.get('token_audit_ok') is not True)
    if failed:
        strict, recovered = None, None
        error = recovery_error = 'runtime_or_token_validation_failure'
    else:
        strict, error = candidate(response['text'], response['condition'])
        recovered, recovery_error = candidate(
            response['text'], response['condition'], normalize_status=True)
    return {
        'model_key': response['model_key'], 'condition': response['condition'],
        'case_id': response['case_id'], 'source': reference['source'],
        'strict_candidate': strict, 'strict_parse_error': error,
        'status_only_candidate': recovered, 'status_only_parse_error': recovery_error,
        'strict_locked': locked_match(reference, strict),
        'status_only_locked': locked_match(reference, recovered),
        'strict_native': native_score(reference['source'], annotation, strict),
        'strict_projected_reference': reference_projection(reference, strict),
        'semantic_or_trace_certification': False,
    }
