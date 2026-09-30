"""Executive summary: repeat the interrupted pilot with isolated per-arm logging.

Scientific rules are unchanged. Preserve V1 and its failed execution; V2 has a
separate prospective freeze, remaining cumulative budget and original cutoff.
"""
import hashlib
import json
import runpy
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import gepa

from finance_adaptation.adapter import FinanceAdapter, MANUAL, SEED
from finance_adaptation.observed_client import ObservedBudgetClient
from model_grading.protocol import read_jsonl, write_json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/finance-adaptation-v2'


class FileLogger:
    """Write each optimizer's messages without changing process-wide streams."""

    def __init__(self, path):
        self.stream = path.open('x')

    def log(self, message):
        self.stream.write(json.dumps(str(message)) + '\n')
        self.stream.flush()

    def close(self):
        self.stream.close()


def optimize_one(client, objective, seed, train, dev):
    directory = OUT / f'{objective}-{seed}'
    directory.mkdir()
    adapter = FinanceAdapter(client, directory, objective, seed)
    logger = FileLogger(directory / 'optimization.log')
    start = time.perf_counter()
    try:
        result = gepa.optimize(
            seed_candidate={'strategy': SEED}, trainset=train, valset=dev, adapter=adapter,
            reflection_lm=adapter.reflect, seed=seed, max_metric_calls=256,
            reflection_minibatch_size=3, skip_perfect_score=False,
            stop_callbacks=adapter.stop, run_dir=str(directory / 'gepa'), logger=logger,
            cache_evaluation=False, use_merge=False, raise_on_exception=True)
    finally:
        logger.close()
    saved = result.to_dict()
    saved.update(objective=objective, optimizer_seed=seed,
                 actual_actor_calls=adapter.actor_calls,
                 reflection_calls=adapter.reflection_calls,
                 elapsed_s=time.perf_counter() - start,
                 best_strategy=result.best_candidate['strategy'])
    write_json(directory / 'result.json', saved)
    return f'{objective}-{seed}', result.best_candidate['strategy']


def main():
    original = runpy.run_path(str(ROOT / 'scripts/run_finance_adaptation.py'))
    original['load_frozen']()
    manifest = json.loads((OUT / 'freeze.json').read_text())
    for name, checksum in manifest['frozen_sha256'].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != checksum:
            raise ValueError(f'Execution-amendment file changed: {name}')
    catalogue = json.loads((OUT / 'provider_catalogue.json').read_text())
    client = ObservedBudgetClient(OUT, catalogue, limit=Decimal(manifest['shared_cap_usd']))
    # Keep the original attempt's three-hour request cutoff, including time lost.
    original_epoch = datetime.fromisoformat(manifest['original_start_utc']).timestamp()
    client.start -= time.time() - original_epoch
    answer_panel = original['answer_panel']
    answer_panel.__globals__['OUT'] = OUT
    answer_panel(client, read_jsonl(OUT / 'preflight.jsonl'), SEED, 'preflight')
    health = read_jsonl(OUT / 'format_preflight.jsonl')
    parsed = sum(r['value'] is not None for r in health)
    write_json(OUT / 'preflight_result.json', {'attempts': len(health), 'parsed': parsed,
                                              'gate_passed': parsed >= 15})
    if parsed < 15:
        raise RuntimeError('Unchanged off-split formatting gate failed; optimization stops')
    train, dev = [read_jsonl(OUT / f'{name}.jsonl') for name in ('train', 'dev')]
    jobs = [('source', 0), ('source', 1), ('repaired', 0), ('repaired', 1)]
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda job: optimize_one(client, *job, train, dev), jobs))
    strategies = [('seed', SEED), ('manual', MANUAL)] + results
    write_json(OUT / 'selected_strategies.json', dict(strategies))
    holdout = read_jsonl(OUT / 'test-source.jsonl') + read_jsonl(OUT / 'test-transfer.jsonl')
    for label, strategy in strategies:
        answer_panel(client, holdout, strategy, label)
    write_json(OUT / 'runtime.json', {
        'status': 'executed_prompt_adaptation_after_disclosed_logging_reexecution',
        'freeze_utc': manifest['frozen_utc'], 'gepa_version': '0.1.1',
        'api_attempts': client.counter, 'accounted_usd': str(client.charged),
        'prior_attempt_accounted_usd': manifest['prior_attempt_accounted_usd'],
        'cumulative_accounted_usd': str(client.charged + Decimal(manifest['prior_attempt_accounted_usd'])),
        'shared_cap_usd': str(client.limit), 'cumulative_cap_usd': '.90',
        'maximum_global_concurrency': 4, 'original_start_utc': manifest['original_start_utc'],
        'elapsed_s': time.monotonic() - client.start})


if __name__ == '__main__':
    main()
