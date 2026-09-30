"""Executive summary: validate the disclosed V2 execution using unchanged V1 math.

Read-only frozen inputs and interrupted ledgers; no API calls or primary oracle
imports. Verify the original cutoff and cumulative budget before invoking the
unchanged independent output validator with only its input directory rebound.
"""
import ast
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal as D
from pathlib import Path

import output_support as support
import validate_outputs as original

ROOT = support.ROOT
OLD = ROOT / 'outputs/finance-adaptation-v1'
OUT = ROOT / 'outputs/finance-adaptation-v2'
START = '2026-09-29T20:33:58.526883+00:00'
CUTOFF = '2026-09-29T23:33:58.526883+00:00'
OLD_LEDGER = 'ca6d73475cb12c326090dff5488801651a65b3c9fcc8bbb8e0b55c8b2ffec2e1'
SUPPORT = '9c49923e61d1738dd8b27db7f736e42c837aba145e9ef4c50c36bb5c02fb4f69'
VALIDATOR = '879696c44775abc18d673068e87cd202649ff58e3244b0a174a143c08f2e3f55'
COPIES = ('train.jsonl', 'dev.jsonl', 'test-source.jsonl', 'test-transfer.jsonl',
          'preflight.jsonl', 'preparation_manifest.json', 'provider_catalogue.json',
          'dependency_manifest.json', 'independent/benchmark_validation.json',
          'independent/oracle_boundary_checks.json')


def load(path):
    return json.loads(path.read_text())


def optimizer_keywords(path):
    tree = ast.parse(path.read_text())
    call = next(n for n in ast.walk(tree) if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Attribute) and n.func.attr == 'optimize')
    assert not call.args
    return {kw.arg: ast.dump(kw.value) for kw in call.keywords}


def verify_original():
    previous = support.DATA
    support.DATA = OLD
    try:
        frozen, hashes = support.verify_freeze()
    finally:
        support.DATA = previous
    assert frozen['frozen_utc'] == START
    assert support.digest(OLD / 'api_calls.jsonl') == OLD_LEDGER
    assert support.digest(Path(original.__file__)) == VALIDATOR
    assert support.digest(Path(support.__file__)) == SUPPORT
    failure = load(OLD / 'execution_failure.json')
    assert failure['status'] == 'interrupted_execution_no_holdouts'
    assert failure['process_exit_code'] == 120
    assert failure['exception'] == 'ValueError: I/O operation on closed file.'
    assert failure['completed_run_results'] == ['repaired-0/result.json', 'repaired-1/result.json']
    assert not (OLD / 'holdout_responses.jsonl').exists()
    assert not any((OLD / label / 'result.json').exists() for label in ('source-0', 'source-1'))
    calls = support.read(OLD / 'api_calls.jsonl')
    assert len(calls) == failure['api_attempts'] == 459
    assert Counter(r['index'] for r in calls) == Counter(range(1, 460))
    cost = sum((D(r['accounted_usd']) for r in calls), D(0))
    assert cost == D(failure['accounted_usd']) == D('0.089236560')
    reflections = [r for r in calls if r['tag'].endswith(':reflection')]
    assert len(reflections) == failure['reflection_calls'] == 63
    questions = {r['case_id']: r for name in ('train', 'dev', 'preflight', 'test-source', 'test-transfer')
                 for r in support.read(OLD / f'{name}.jsonl')}
    exact = {r['case_id']: r for r in load(OLD / 'independent/benchmark_validation.json')['rows']}
    groups, actor_tags, rows = {}, set(), []
    for label in original.LABELS[2:]:
        groups[label] = defaultdict(list)
        for r in support.read(OLD / label / 'evaluations.jsonl'):
            support.score(questions[r['case_id']], exact[r['case_id']], r)
            rows.append(r)
            groups[label][r['evaluation']].append(r)
            if r['finish_reason'] != 'candidate_too_long':
                actor_tags.add(f'{label}:evaluation-{r["evaluation"]}:{r["case_id"]}')
    assert len(rows) == 503
    assert Counter(r['finish_reason'] for r in rows) == {'stop': 377, 'candidate_too_long': 126}
    preflight = support.read(OLD / 'format_preflight.jsonl')
    assert len(preflight) == 16
    for r in preflight:
        support.score(questions[r['case_id']], exact[r['case_id']], r)
        actor_tags.add(f'preflight:{r["case_id"]}')
    template = support.reflection_template()
    for api in reflections:
        label = api['tag'].split(':')[0]
        assert any(len(g) == 3 and all(r['partition'] == 'train' for r in g)
                   and support.reflection_prompt(g, questions, label.split('-')[0], template)
                   == api['request_body']['messages'][1]['content'] for g in groups[label].values())
    orphan = [r['tag'] for r in calls if not r['tag'].endswith(':reflection') and r['tag'] not in actor_tags]
    assert len(orphan) == 3
    old_kw = optimizer_keywords(ROOT / 'scripts/run_finance_adaptation.py')
    new_kw = optimizer_keywords(ROOT / 'scripts/run_finance_adaptation_v2.py')
    assert new_kw.pop('logger') == ast.dump(ast.Name(id='logger', ctx=ast.Load()))
    assert old_kw == new_kw
    return frozen, {**hashes, 'api_attempts': len(calls), 'accounted_usd': str(cost),
                    'reflection_calls': len(reflections), 'rescored_optimizer_rows': len(rows),
                    'orphan_actor_tags_preserved': orphan, 'holdout_responses': 0,
                    'optimizer_keywords_unchanged_except_logger': True,
                    'partial_ledger_sha256': {str(p.relative_to(ROOT)): support.digest(p)
                        for p in [OLD / 'api_calls.jsonl', OLD / 'execution_failure.json',
                                  *sorted(OLD.glob('*/evaluations.jsonl')), *sorted(OLD.glob('*/result.json'))]}}


def verify_execution_freeze():
    old, evidence = verify_original()
    frozen = load(OUT / 'freeze.json')
    assert frozen['status'] == 'frozen_before_reexecution_calls_after_disclosed_interruption'
    assert frozen['original_start_utc'] == START
    assert frozen['original_request_cutoff_utc'] == CUTOFF
    assert datetime.fromisoformat(CUTOFF) - datetime.fromisoformat(START) == timedelta(hours=3)
    assert START < frozen['frozen_utc'] < CUTOFF
    assert D(frozen['prior_attempt_accounted_usd']) == D(evidence['accounted_usd'])
    assert D(frozen['shared_cap_usd']) == D('0.810763440')
    assert D(frozen['cumulative_cap_usd']) == D('.90')
    assert D(frozen['shared_cap_usd']) + D(evidence['accounted_usd']) == D('.90')
    for key in ('gepa_version', 'max_metric_calls_per_run', 'maximum_global_api_concurrency', 'optimizer_seeds'):
        assert frozen[key] == old[key]
    for name, checksum in frozen['frozen_sha256'].items():
        assert support.digest(ROOT / name) == checksum, name
    for name, checksum in old['frozen_sha256'].items():
        assert frozen['frozen_sha256'][name] == checksum
    required = [OLD / 'freeze.json', OLD / 'api_calls.jsonl', OLD / 'execution_failure.json',
                OLD / 'format_preflight.jsonl', OLD / 'preflight_result.json',
                *OLD.glob('*/evaluations.jsonl'), *OLD.glob('*/result.json'),
                Path(__file__), Path(original.__file__), Path(support.__file__)]
    assert all(str(p.relative_to(ROOT)) in frozen['frozen_sha256'] for p in required)
    for name in COPIES:
        assert support.digest(OUT / name) == support.digest(OLD / name), name
        assert str((OUT / name).relative_to(ROOT)) in frozen['frozen_sha256']
    return frozen, {'original': evidence, 'reexecution_frozen_files': len(frozen['frozen_sha256']),
                    'reexecution_freeze_sha256': support.digest(OUT / 'freeze.json'),
                    'same_152_questions_and_independent_references': True}


def execution_accounting(frozen):
    calls, slots = support.read(OUT / 'api_calls.jsonl'), support.read(OUT / 'egress_slots.jsonl')
    assert Counter(r['tag'] for r in calls) == Counter(r['tag'] for r in slots)
    events = []
    for r in slots:
        entered = datetime.fromisoformat(r['entered_egress_slot_utc'])
        left = datetime.fromisoformat(r['left_egress_slot_utc'])
        assert datetime.fromisoformat(frozen['frozen_utc']) <= entered < left
        assert entered <= datetime.fromisoformat(CUTOFF), r
        events.extend(((entered, 1), (left, -1)))
    active = peak = 0
    for _, delta in sorted(events):
        active += delta
        peak = max(peak, active)
        assert 0 <= active <= 4
    assert active == 0
    runtime = load(OUT / 'runtime.json')
    cost = sum((D(r['accounted_usd']) for r in calls), D(0))
    prior = D(frozen['prior_attempt_accounted_usd'])
    assert cost == D(runtime['accounted_usd']) <= D(frozen['shared_cap_usd'])
    assert D(runtime['prior_attempt_accounted_usd']) == prior
    assert D(runtime['cumulative_accounted_usd']) == cost + prior <= D('.90')
    assert D(runtime['cumulative_cap_usd']) == D('.90')
    assert runtime['original_start_utc'] == START
    assert runtime['status'] == 'executed_prompt_adaptation_after_disclosed_logging_reexecution'
    return {'attempt_accounted_usd': str(cost), 'prior_accounted_usd': str(prior),
            'cumulative_accounted_usd': str(cost + prior), 'cumulative_cap_usd': '0.90',
            'original_request_cutoff_utc': CUTOFF, 'recorded_egress_slots': len(slots),
            'observed_peak_egress_slots': peak,
            'timing_limit': 'Recorded slots bound actual requests, not exact HTTP wire times.',
            'egress_slots_sha256': support.digest(OUT / 'egress_slots.jsonl')}


def main():
    frozen, hashes = verify_execution_freeze()
    accounting = execution_accounting(frozen)
    # Rebind inputs only; preserve original independent parser/math byte-for-byte.
    support.DATA = original.DATA = OUT
    original.verify_freeze = verify_execution_freeze
    original.main()
    path = OUT / 'independent/response_validation.json'
    result = load(path)
    result['execution_amendment_validation'] = accounting
    result['api_accounting']['concurrency_evidence'] = accounting['timing_limit']
    result['api_accounting']['observed_peak_egress_slots'] = accounting['observed_peak_egress_slots']
    result['reexecution_validator_sha256'] = support.digest(Path(__file__))
    result['execution_freeze_verification'] = hashes
    result['completed_validation_utc'] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', **accounting}, indent=2))


if __name__ == '__main__':
    main()
