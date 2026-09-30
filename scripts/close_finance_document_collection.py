"""Executive summary: retain an interrupted attempt without inventing an API response or retry."""
import hashlib
import json
from decimal import Decimal

from finance_document_review.model_protocol import OUTPUT, ROOT, cases, digest, request_body
from replay_finance_document_artifact import metrics, rows


def main():
    intent = json.loads((OUTPUT / 'interruption_intent.json').read_text())
    original = rows(OUTPUT / 'responses.jsonl')
    if digest(OUTPUT / 'responses.jsonl') != intent['raw_ledger_sha256'] or len(original) != 383:
        raise ValueError('Actual API ledger changed after closure')
    path = OUTPUT / 'effective_attempts.jsonl'
    if path.exists():
        raise ValueError('Closure already recorded; do not regenerate')
    pending = intent['pending_case']
    case = next(r for r in cases() if r['case_id'] == pending['case_id'])
    body = request_body(pending['model_key'], pending['condition'], case['prompt'])
    encoded = json.dumps(body, ensure_ascii=False, sort_keys=True).encode()
    event = {**pending, 'prompt_sha256': hashlib.sha256(case['prompt'].encode()).hexdigest(),
             'request_sha256': hashlib.sha256(encoded).hexdigest(), 'text': '',
             'finish_reason': 'collector_interrupted', 'elapsed_s': None,
             'error': {'type': 'CensoredUnreturnedAttempt'},
             'collector_event': True, 'actual_api_response': False,
             'request_metadata_reconstructed_from_freeze': True,
             'closure_utc': intent['closure_utc']}
    attempts = original + [event]
    with path.open('x') as stream:
        stream.write((OUTPUT / 'responses.jsonl').read_text())
        stream.write(json.dumps(event) + '\n')
    report_cost = sum((Decimal(str(r['usage']['cost'])) for r in original
                       if r.get('usage', {}).get('cost') is not None), Decimal(0))
    receipt = {'executive_summary': '383 actual API records and one distinct censored-attempt event; all384 attempts retained.',
               'attempts': 384, 'actual_api_records': 383, 'censored_attempts': 1,
               'request_failures_with_returned_records': sum(bool(r.get('error')) for r in original),
               'response_sha256': digest(OUTPUT / 'responses.jsonl'),
               'effective_attempts_sha256': digest(path),
               'freeze_sha256': digest(OUTPUT / 'freeze.json'),
               'original_runner_completed': False, 'fresh_retries': 0,
               'reported_cost_usd': str(report_cost),
               'missing_cost_records': sum(r.get('usage', {}).get('cost') is None for r in original) + 1,
               'closure_utc': intent['closure_utc']}
    (OUTPUT / 'interrupted_collection_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    review = ROOT / 'outputs/finance-document-review-v1'
    references = {r['case_id']: r for r in rows(review / 'pre_target_combined.jsonl')}
    targets = {r['case_id']: r['original_annotation'] for r in rows(ROOT / 'outputs/finance-document-audit-v1/source_targets.jsonl')}
    result, scored = metrics(attempts, references, targets)
    (OUTPUT / 'paired_scores.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in scored))
    (OUTPUT / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
