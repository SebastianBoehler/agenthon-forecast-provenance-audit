"""Executive summary: freeze and collect one fixed-provider GLM arm on the existing panel."""

from collections import Counter
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import time
from urllib.request import Request, urlopen

from grader_comparison.analysis import financial_scores
from grader_comparison.native import load, normalized_comparison
from grader_comparison.protocol import ROOT, OUT, CONFIG, frozen, digest, now, write, jsonl
from grader_comparison.scalars import final_scalar, scalar

DEST = ROOT / 'outputs/glm-final-extension-v1'
MODEL = 'z-ai/glm-4.7-flash'
CAP = Decimal('0.50')
RESERVE = Decimal('0.005')


def request(prompt, sequence):
    ledger = DEST / 'spend_ledger.jsonl'
    previous = [json.loads(x) for x in ledger.read_text().splitlines()] if ledger.exists() else []
    latest = {r['sequence']: r for r in previous}
    if any(r['status'] != 'settled' for r in latest.values()):
        raise ValueError('Unsettled request: no retries or further calls')
    spent = sum((Decimal(str(r['cost_usd'])) for r in latest.values()), Decimal(0))
    if spent + RESERVE > CAP:
        raise ValueError('Study spending cap reached')
    body = {'model': MODEL, 'messages': [{'role': 'system', 'content': CONFIG['system_prompt']},
            {'role': 'user', 'content': prompt}], 'temperature': .2, 'top_k': 40, 'top_p': .95,
            'max_tokens': 1024, 'reasoning': {'enabled': False}, 'stream': False,
            'provider': {'only': ['novita/bf16'], 'allow_fallbacks': False,
                         'require_parameters': True, 'max_price': {'prompt': .08, 'completion': .45}}}
    record = {'sequence': sequence, 'started_utc': now(), 'request': body, 'status': 'pending',
              'reserved_usd': str(RESERVE), 'cost_usd': None}
    def append(value):
        with ledger.open('a') as f:
            f.write(json.dumps(value) + '\n')
    append(record)
    begun = time.perf_counter()
    try:
        req = Request('https://openrouter.ai/api/v1/chat/completions', data=json.dumps(body).encode(),
                      headers={'Authorization': 'Bearer ' + os.environ['OPENROUTER_API_KEY'],
                               'Content-Type': 'application/json'})
        with urlopen(req, timeout=120) as response:
            raw = json.load(response)
        record['raw_response'] = raw
        usage = raw['usage']
        cost = usage.get('cost')
        if cost is None or Decimal(str(cost)) < 0 or Decimal(str(cost)) > RESERVE:
            raise ValueError('Missing or excessive observed charge')
        record['cost_usd'] = cost
        if raw.get('provider') != 'Novita':
            raise ValueError('Unexpected provider')
        choice = raw['choices'][0]
        text = choice['message']['content']
        if not isinstance(text, str) or usage['completion_tokens'] > 1024:
            raise ValueError('Invalid output')
        reasoning = usage.get('completion_tokens_details', {}).get('reasoning_tokens', 0)
        if reasoning or choice['message'].get('reasoning') or choice['message'].get('reasoning_details'):
            raise ValueError('Unexpected reasoning despite disabled request')
        record.update(text=text, at_output_cap=usage['completion_tokens'] == 1024,
                      finish_reason=choice['finish_reason'], status='returned')
    except Exception as exc:
        record.update(status='runtime_nondecision', error=type(exc).__name__ + ': ' + str(exc))
    record.update(completed_utc=now(), elapsed_s=time.perf_counter()-begun)
    write(DEST / f'request-{sequence:03d}.json', record)
    append({'sequence': sequence, 'status': 'settled' if record['cost_usd'] is not None else 'unknown',
            'cost_usd': record['cost_usd'], 'reserved_usd': str(RESERVE), 'completed_utc': now()})
    # Every pending event must be resolved; inspect latest settlement per request.
    if record['status'] != 'returned':
        raise ValueError('Request stopped the arm; retained without retries')
    return record


def collect():
    cohort = frozen()
    DEST.mkdir(exist_ok=False)
    with urlopen('https://openrouter.ai/api/v1/models/z-ai/glm-4.7-flash/endpoints', timeout=30) as f:
        catalogue = json.load(f)
    write(DEST / 'protocol.json', {'frozen_utc': now(), 'model': MODEL, 'route': 'novita/bf16',
          'cohort_calls_before_freeze': 0, 'repetitions': 3, 'scheduled': 48,
          'cohort_sha256': digest(OUT / 'cohort.jsonl'), 'original_freeze_sha256': digest(OUT / 'freeze.json'),
          'script_sha256': digest(Path(__file__)), 'endpoint_catalogue': catalogue,
          'max_output_tokens': 1024, 'source_local_config': CONFIG, 'api_parameter_differences': 'No min_p or repetition penalty requested; hosted defaults apply.', 'study_cap_usd': str(CAP),
          'prior_followup_reserved_cap_usd': 2, 'total_authorization_usd': 10,
          'reason': 'Local GLM load refused by memory guardrail; fixed-provider API extension.',
          'native_template_scope': 'Provider-managed; not independently inspected as in local runs.',
          'interpretation': 'Prospective new arm after inspection of prior panel; exploratory robustness, no family ranking.'})
    jsonl(DEST / 'cohort.jsonl', cohort)
    sequence = 0
    for prompt, target in [('What is 7 + 14?', '21'), ('What is half of 9?', '4.5'), ('What is -3 + 1?', '-2')]:
        r = request(prompt, sequence)
        sequence += 1
        value = final_scalar(r['text'])
        if r['at_output_cap'] or r['finish_reason'] != 'stop' or value is None or scalar(value) != scalar(target):
            raise ValueError('Strict source-free readiness failed; no cohort calls')
    env, _ = load()
    rows, counts = [], {'finance': Counter(), 'math': Counter()}
    for repetition in range(3):
        ordered = sorted(cohort, key=lambda c: hashlib.sha256(f"{repetition}|{c['id']}".encode()).hexdigest())
        for case in ordered:
            r = request(case['prompt'], sequence)
            sequence += 1
            answer = final_scalar(r['text'])
            admitted = not r['at_output_cap'] and r['finish_reason'] == 'stop' and answer is not None
            row = {'model': MODEL, 'case_id': case['id'], 'domain': case['domain'],
                   'repetition': repetition, 'sequence': sequence-1, 'final_scalar': answer,
                   'admitted': admitted, 'at_output_cap': r['at_output_cap'], 'finish_reason': r['finish_reason'],
                   'response_sha256': hashlib.sha256(r['text'].encode()).hexdigest()}
            counter = counts[case['domain']]
            counter['attempted'] += 1
            counter['admitted'] += int(admitted)
            if admitted:
                value = scalar(answer)
                if case['domain'] == 'finance':
                    row.update(financial_scores(case, value))
                    for k in ('released_label_cent', 'complete_contract'):
                        counter[k] += int(row[k])
                    counter['valid_denied'] += int(row['complete_contract'] and not row['released_label_cent'])
                else:
                    equal = value == scalar(case['reference'])
                    native = normalized_comparison(env, case['reference'], answer)[0]
                    row.update(exact=equal, native=native)
                    counter['exact'] += int(equal)
                    counter['native'] += int(native)
                    counter['unequal_credit'] += int(native and not equal)
                    counter['equal_denial'] += int(not native and equal)
            rows.append(row)
            print(json.dumps({'completed': len(rows), 'scheduled': 48}), flush=True)
    jsonl(DEST / 'attempt_projection.jsonl', rows)
    write(DEST / 'analysis.json', {'scheduled': 48, 'counts': counts,
          'scope': 'Same frozen panel and scoring, fixed remote provider; not a capacity comparison.'})


if __name__ == '__main__':
    collect()
