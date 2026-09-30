"""Executive summary: collect fixed-provider DeepSeek answers under a one-dollar bound."""
import json
import os
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from decimal import Decimal as D

from model_grading.protocol import (DESTINATION, MAX_TOKENS, REMOTE_MODEL, SYSTEM,
                                    append_record, frozen_selection, read_jsonl,
                                    write_json)

MODEL_KEY = 'deepseek-v3.2'


def answer(row):
    body = {'model': REMOTE_MODEL['model'], 'temperature': 0, 'max_tokens': MAX_TOKENS,
            'reasoning': {'enabled': False},
            'provider': {'only': [REMOTE_MODEL['provider_tag']],
                         'allow_fallbacks': False, 'require_parameters': True},
            'messages': [{'role': 'system', 'content': SYSTEM},
                         {'role': 'user', 'content': row['prompt']}]}
    request = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',
                                     data=json.dumps(body).encode(),
                                     headers={'Authorization': 'Bearer ' + os.environ['OPENROUTER_API_KEY'],
                                              'Content-Type': 'application/json'})
    start = time.perf_counter()
    record = {'model_key': MODEL_KEY, 'case_id': row['case_id'],
              'question_hash': row['question_hash'], 'request_body': body,
              'text': '', 'finish_reason': 'transport_error'}
    try:
        with urllib.request.urlopen(request, timeout=120) as stream:
            raw = json.load(stream)
        record['raw_response'] = raw
        choice = raw['choices'][0]
        record.update({'text': choice['message'].get('content') or '',
                       'finish_reason': choice['finish_reason'], 'usage': raw.get('usage', {}),
                       'model': raw['model'], 'provider': raw.get('provider')})
        if record['provider'] != REMOTE_MODEL['provider_name']:
            raise ValueError('Returned provider does not match the frozen provider')
    except urllib.error.HTTPError as error:
        record['error'] = {'type': 'HTTPError', 'status': error.code}
    except Exception as error:
        record.update({'finish_reason': 'transport_error',
                       'error': {'type': type(error).__name__, 'message': str(error)}})
    record['elapsed_s'] = time.perf_counter() - start
    return record


def main():
    rows = frozen_selection()
    # Public prompts are far below this UTF-8-byte input-token upper bound.
    worst = sum((len(SYSTEM.encode()) + len(r['prompt'].encode()) + 100) *
                D(REMOTE_MODEL['prompt_price_per_token']) + MAX_TOKENS *
                D(REMOTE_MODEL['completion_price_per_token']) for r in rows)
    if worst > 1:
        raise ValueError(f'One-dollar run bound exceeded: {worst}')
    with urllib.request.urlopen('https://openrouter.ai/api/v1/models/deepseek/deepseek-v3.2/endpoints') as stream:
        endpoints = json.load(stream)
    write_json(DESTINATION / 'deepseek-v3.2_catalogue.json', endpoints)
    path = DESTINATION / f'{MODEL_KEY}_responses.jsonl'
    previous = read_jsonl(path) if path.exists() else []
    completed = {r['case_id'] for r in previous}
    if len(completed) != len(previous) or not completed.issubset({r['case_id'] for r in rows}):
        raise ValueError('Existing response ledger has duplicate or unexpected IDs')
    pending = [r for r in rows if r['case_id'] not in completed]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in as_completed([pool.submit(answer, r) for r in pending]):
            record = result.result()
            append_record(path, record)
            completed.add(record['case_id'])
            if len(completed) % 10 == 0:
                print(json.dumps({'model': MODEL_KEY, 'completed': len(completed)}), flush=True)
    responses = read_jsonl(path)
    cost = sum(D(str(r.get('usage', {}).get('cost', 0))) for r in responses)
    print(json.dumps({'attempts': len(responses), 'reported_cost_usd': str(cost),
                      'preflight_worst_case_usd': str(worst)}), flush=True)


if __name__ == '__main__':
    main()
