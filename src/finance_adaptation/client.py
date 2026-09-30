"""Executive summary: record fixed-provider calls under a shared, reserved dollar cap."""
import json
import os
import threading
import time
import urllib.error
import urllib.request
from decimal import Decimal as D

from model_grading.protocol import REMOTE_MODEL, append_record


class BudgetClient:
    def __init__(self, directory, catalogue, limit=D('.90')):
        self.path = directory / 'api_calls.jsonl'
        self.lock = threading.Lock()
        self.charged = D(0)
        self.reserved = D(0)
        self.limit = limit
        self.counter = 0
        self.start = time.monotonic()
        self.gate = threading.BoundedSemaphore(4)
        self.prices = {k: D(catalogue['pricing'][k]) for k in ('prompt', 'completion')}
        if self.path.exists():
            raise ValueError('A new run cannot overwrite an existing API ledger')

    def call(self, messages, *, tag, max_tokens=512, temperature=0):
        input_bound = sum(len(m['content'].encode()) for m in messages) + 512
        worst = (input_bound * self.prices['prompt'] +
                 max_tokens * self.prices['completion'])
        with self.lock:
            if time.monotonic() - self.start > 3 * 3600:
                raise RuntimeError('Three-hour pilot limit reached before request')
            if self.charged + self.reserved + worst > self.limit:
                raise RuntimeError('Shared API spending cap reached before request')
            self.reserved += worst
            self.counter += 1
            index = self.counter
        body = {'model': REMOTE_MODEL['model'], 'temperature': temperature,
                'max_tokens': max_tokens, 'reasoning': {'enabled': False},
                'provider': {'only': [REMOTE_MODEL['provider_tag']],
                             'allow_fallbacks': False, 'require_parameters': True},
                'messages': messages}
        request = urllib.request.Request(
            'https://openrouter.ai/api/v1/chat/completions', data=json.dumps(body).encode(),
            headers={'Authorization': 'Bearer ' + os.environ['OPENROUTER_API_KEY'],
                     'Content-Type': 'application/json'})
        start = time.perf_counter()
        record = {'index': index, 'tag': tag, 'request_body': body, 'text': '',
                  'finish_reason': 'transport_error', 'reserved_worst_usd': str(worst)}
        try:
            with self.gate:
                if time.monotonic() - self.start > 3 * 3600:
                    raise RuntimeError('Three-hour pilot limit reached while waiting for egress')
                with urllib.request.urlopen(request, timeout=120) as stream:
                    raw = json.load(stream)
            record['raw_response'] = raw
            choice = raw['choices'][0]
            record.update(text=choice['message'].get('content') or '',
                          finish_reason=choice['finish_reason'], usage=raw.get('usage', {}),
                          model=raw['model'], provider=raw.get('provider'))
            if record['provider'] != REMOTE_MODEL['provider_name']:
                raise ValueError('Returned provider differs from the pinned route')
            if record['model'] != REMOTE_MODEL['model']:
                raise ValueError('Returned model identifier differs from the pinned route')
        except urllib.error.HTTPError as error:
            record['error'] = {'type': 'HTTPError', 'status': error.code}
        except Exception as error:
            record.update(finish_reason='transport_error',
                          error={'type': type(error).__name__, 'message': str(error)})
        actual = record.get('usage', {}).get('cost')
        debit = D(str(actual)) if actual is not None else worst
        record.update(elapsed_s=time.perf_counter() - start, accounted_usd=str(debit),
                      cost_known=actual is not None)
        with self.lock:
            self.reserved -= worst
            self.charged += debit
            append_record(self.path, record)
            print(json.dumps({'api_attempts': self.counter, 'accounted_usd': str(self.charged),
                              'latest_tag': tag}), flush=True)
        if debit > worst or self.charged > self.limit:
            raise RuntimeError('Observed billing exceeds the conservative spending reservation')
        return record
