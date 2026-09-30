"""Executive summary: prospectively add a small Llama arm without changing the frozen panel."""

import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time

from grader_comparison.local import api, metadata
from grader_comparison.protocol import ROOT, OUT, CONFIG, frozen, digest, now, write, jsonl
from grader_comparison.scalars import final_scalar, scalar

DEST = ROOT / 'outputs/llama-final-extension-v2'
NATIVE_CONFIG = {k: v for k, v in CONFIG.items() if k != 'reasoning'}
MODEL = {'key': 'llama-3.2-3b-instruct', 'instance': 'final-llama',
         'checkpoint': '/Volumes/Sebastian-NVMe/LM Studio/lmstudio-community/Llama-3.2-3B-Instruct-GGUF/Llama-3.2-3B-Instruct-Q4_K_M.gguf'}


def attempt(model, prompt, loaded):
    body = dict(NATIVE_CONFIG, model=model['instance'], input=prompt)
    record = {'started_utc': now(), 'request': body, 'status': 'runtime_nondecision'}
    started = time.perf_counter()
    try:
        _, live = metadata(model)
        if live != loaded:
            raise ValueError('Native load settings changed')
        raw = api('/api/v1/chat', body)
        record['raw_response'] = raw
        stats = raw['stats']
        tokens = [stats[k] for k in ('input_tokens', 'total_output_tokens', 'reasoning_output_tokens')]
        if any(type(t) is not int or t < 0 for t in tokens):
            raise ValueError('Invalid native token accounting')
        if not tokens[0] or tokens[0]+1024 > 4096 or tokens[1] > 1024 or tokens[2]:
            raise ValueError('Native budget or reasoning violation')
        if raw.get('model_instance_id') != model['instance'] or len(raw['output']) != 1:
            raise ValueError('Unexpected model or output blocks')
        message = raw['output'][0]
        if message['type'] != 'message' or not isinstance(message['content'], str):
            raise ValueError('Unexpected message')
        record.update(status='returned', text=message['content'], stats=stats,
                      at_output_cap=tokens[1] == 1024)
    except Exception as exc:
        record['error'] = type(exc).__name__ + ': ' + str(exc)
    record.update(completed_utc=now(), elapsed_s=time.perf_counter()-started)
    return record


def main():
    cohort = frozen()
    info, config = metadata(MODEL)
    DEST.mkdir(exist_ok=False)
    write(DEST / 'protocol.json', {'frozen_utc': now(), 'model': info, 'loaded_config': config,
          'checkpoint_sha256': digest(MODEL['checkpoint']), 'platform': platform.platform(),
          'cli_version': subprocess.check_output(['lms', '--version'], text=True).strip(),
          'script_sha256': digest(Path(__file__)), 'request_config': NATIVE_CONFIG,
          'amendment': 'Llama exposes no reasoning selector; omit it after three HTTP400 probes, before any cohort collection.',
          'failed_stage_protocol_sha256': digest(ROOT / 'outputs/llama-final-extension-v1/protocol.json'),
          'failed_stage_source_sha256': digest(ROOT / 'outputs/llama-final-extension-v1/frozen_collector.py'),
          'cohort_sha256': digest(OUT / 'cohort.jsonl'), 'scheduled': 48, 'repetitions': 3,
          'cohort_calls_before_freeze': 0, 'seed': None, 'paid_inference_usd': 0,
          'scope': 'Prospective exploratory extension after earlier results; native templates, no family ranking.'})
    jsonl(DEST / 'cohort.jsonl', cohort)
    probes = []
    for prompt, expected in [('What is 7 + 14?', '21'), ('What is half of 9?', '4.5'), ('What is -3 + 1?', '-2')]:
        record = attempt(MODEL, prompt, config)
        value = final_scalar(record.get('text', ''))
        record['probe_pass'] = (record['status'] == 'returned' and not record['at_output_cap']
                                and value is not None and scalar(value) == scalar(expected))
        probes.append(record)
    write(DEST / 'probes.json', probes)
    if not all(r['probe_pass'] for r in probes):
        raise ValueError('Strict readiness failed; no cohort calls')
    count = 0
    for repetition in range(3):
        for case in sorted(cohort, key=lambda c: hashlib.sha256(f"{repetition}|{c['id']}".encode()).hexdigest()):
            record = attempt(MODEL, case['prompt'], config)
            record.update(case_id=case['id'], model='llama', repetition=repetition)
            write(DEST / f'attempt-{count:03d}.json', record)
            count += 1
            print(json.dumps({'completed': count, 'scheduled': 48}), flush=True)
            if record['status'] != 'returned':
                raise ValueError('Runtime failure retained; no retries or further calls')
    write(DEST / 'collection_receipt.json', {'completed_utc': now(), 'recorded': count, 'scheduled': 48,
          'files': {p.name: digest(p) for p in DEST.glob('*.json')}})


if __name__ == '__main__':
    main()
