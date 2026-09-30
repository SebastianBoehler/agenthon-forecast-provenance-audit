"""Executive summary: run frozen source-versus-repaired GEPA and untouched holdouts."""
import hashlib
import importlib.metadata
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import gepa

from finance_adaptation.adapter import (FORMAT, MANUAL, PREFIX, SEED,
                                       FinanceAdapter, rewards)
from finance_adaptation.client import BudgetClient
from model_grading.protocol import REMOTE_MODEL, append_record, read_jsonl, write_json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/finance-adaptation-v1'


def load_frozen():
    manifest = json.loads((OUT / 'freeze.json').read_text())
    for name, checksum in manifest['frozen_sha256'].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != checksum:
            raise ValueError(f'Frozen adaptation file changed: {name}')
    if importlib.metadata.version('gepa') != '0.1.1':
        raise ValueError('GEPA package version changed')
    dependencies = json.loads((OUT / 'dependency_manifest.json').read_text())
    distribution = importlib.metadata.distribution('gepa')
    for name, checksum in dependencies['source_sha256'].items():
        if hashlib.sha256(distribution.locate_file(name).read_bytes()).hexdigest() != checksum:
            raise ValueError(f'Installed GEPA implementation changed: {name}')
    return manifest


def answer_panel(client, rows, strategy, label):
    def answer(row):
        raw = client.call([{'role': 'system', 'content': PREFIX + strategy + FORMAT},
                           {'role': 'user', 'content': row['prompt']}],
                          tag=f'{label}:{row["case_id"]}')
        return {'label': label, 'case_id': row['case_id'], 'family': row['family'],
                'partition': row['partition'], 'question_hash': row['question_hash'],
                'strategy': strategy, 'text': raw['text'],
                'finish_reason': raw['finish_reason'],
                **rewards(row, raw['text'], raw['finish_reason'])}

    with ThreadPoolExecutor(max_workers=4) as pool:
        for record in pool.map(answer, rows):
            append_record(OUT / ('format_preflight.jsonl' if label == 'preflight'
                                else 'holdout_responses.jsonl'), record)


def optimize_one(client, objective, seed, train, dev):
    directory = OUT / f'{objective}-{seed}'
    directory.mkdir()
    adapter = FinanceAdapter(client, directory, objective, seed)
    start = time.perf_counter()
    result = gepa.optimize(
        seed_candidate={'strategy': SEED}, trainset=train, valset=dev, adapter=adapter,
        reflection_lm=adapter.reflect, seed=seed, max_metric_calls=256,
        reflection_minibatch_size=3, skip_perfect_score=False,
        stop_callbacks=adapter.stop, run_dir=str(directory / 'gepa'),
        cache_evaluation=False, use_merge=False, raise_on_exception=True)
    saved = result.to_dict()
    saved.update(objective=objective, optimizer_seed=seed,
                 actual_actor_calls=adapter.actor_calls,
                 reflection_calls=adapter.reflection_calls,
                 elapsed_s=time.perf_counter() - start,
                 best_strategy=result.best_candidate['strategy'])
    write_json(directory / 'result.json', saved)
    return f'{objective}-{seed}', result.best_candidate['strategy']


def main():
    manifest = load_frozen()
    catalogue = json.loads((OUT / 'provider_catalogue.json').read_text())
    if catalogue['tag'] != REMOTE_MODEL['provider_tag']:
        raise ValueError('Frozen provider differs from the audited model route')
    client = BudgetClient(OUT, catalogue)
    preflight = read_jsonl(OUT / 'preflight.jsonl')
    answer_panel(client, preflight, SEED, 'preflight')
    health = read_jsonl(OUT / 'format_preflight.jsonl')
    parsed = sum(r['value'] is not None for r in health)
    write_json(OUT / 'preflight_result.json', {'attempts': len(health), 'parsed': parsed,
                                              'gate_passed': parsed >= 15})
    if parsed < 15:
        raise RuntimeError('Frozen off-split formatting gate failed; optimization is stopped')
    train, dev = [read_jsonl(OUT / f'{name}.jsonl') for name in ('train', 'dev')]
    # Objectives receive separate adapters and ledgers; shared client limits total egress.
    jobs = [('source', 0), ('source', 1), ('repaired', 0), ('repaired', 1)]
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda job: optimize_one(client, *job, train, dev), jobs))
    strategies = [('seed', SEED), ('manual', MANUAL)] + results
    # Select all final strategies before any held-out answer is collected.
    write_json(OUT / 'selected_strategies.json', dict(strategies))
    holdout = read_jsonl(OUT / 'test-source.jsonl') + read_jsonl(OUT / 'test-transfer.jsonl')
    for label, strategy in strategies:
        answer_panel(client, holdout, strategy, label)
    write_json(OUT / 'runtime.json', {
        'status': 'executed_prompt_adaptation_not_weight_training',
        'freeze_utc': manifest['frozen_utc'], 'gepa_version': '0.1.1',
        'api_attempts': client.counter, 'accounted_usd': str(client.charged),
        'shared_cap_usd': str(client.limit), 'maximum_global_concurrency': 4,
        'elapsed_s': time.monotonic() - client.start})


if __name__ == '__main__':
    main()
