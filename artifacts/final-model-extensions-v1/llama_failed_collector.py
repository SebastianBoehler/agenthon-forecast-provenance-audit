"""Executive summary: prospectively add a small Llama arm without changing the frozen panel."""

import hashlib
import json
from pathlib import Path
import platform
import subprocess

from grader_comparison.local import attempt, metadata
from grader_comparison.protocol import ROOT, OUT, CONFIG, frozen, digest, now, write, jsonl
from grader_comparison.scalars import final_scalar, scalar

DEST = ROOT / 'outputs/llama-final-extension-v1'
MODEL = {'key': 'llama-3.2-3b-instruct', 'instance': 'final-llama',
         'checkpoint': '/Volumes/Sebastian-NVMe/LM Studio/lmstudio-community/Llama-3.2-3B-Instruct-GGUF/Llama-3.2-3B-Instruct-Q4_K_M.gguf'}


def main():
    cohort = frozen()
    info, config = metadata(MODEL)
    DEST.mkdir(exist_ok=False)
    write(DEST / 'protocol.json', {'frozen_utc': now(), 'model': info, 'loaded_config': config,
          'checkpoint_sha256': digest(MODEL['checkpoint']), 'platform': platform.platform(),
          'cli_version': subprocess.check_output(['lms', '--version'], text=True).strip(),
          'script_sha256': digest(Path(__file__)), 'request_config': CONFIG,
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
