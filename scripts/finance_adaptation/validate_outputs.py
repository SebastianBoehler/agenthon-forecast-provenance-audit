"""Executive summary: independently rescore the completed frozen adaptation pilot.

Read-only inputs, exact prereview Fraction references, a separate final-line parser,
and reconstructed assigned-only reflection prompts. No API or primary oracle calls.
Run after all six72-case holdouts and four optimizer result files are complete.
"""
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal as D
from fractions import Fraction as F
from pathlib import Path

from output_support import (DATA, ROOT, digest, feedback, literals, read,
                            reflection_prompt, reflection_template, score,
                            summarize, verify_freeze)

LABELS = ('seed', 'manual', 'source-0', 'source-1', 'repaired-0', 'repaired-1')


def check_api(calls, actors, evaluations, questions, wrapper, route, freeze):
    prices = json.loads((DATA / 'provider_catalogue.json').read_text())['pricing']
    lookup = {r['tag']: r for r in calls if not r['tag'].endswith(':reflection')}
    assert len(lookup) == sum(not r['tag'].endswith(':reflection') for r in calls)
    expected_tags = set()
    for tag, record in actors.items():
        if record['finish_reason'] == 'candidate_too_long':
            assert len(record['strategy'].encode()) > 2000 and not record['text']
            continue
        assert len(record['strategy'].encode()) <= 2000
        expected_tags.add(tag)
        api = lookup[tag]
        messages = [{'role': 'system', 'content': wrapper['PREFIX'] + record['strategy'] + wrapper['FORMAT']},
                    {'role': 'user', 'content': questions[record['case_id']]['prompt']}]
        assert api['request_body']['messages'] == messages, tag
        assert api['text'] == record['text'] and api['finish_reason'] == record['finish_reason']
    assert expected_tags == set(lookup)
    ids = [r['index'] for r in calls]
    assert set(ids) == set(range(1, len(ids) + 1)) and len(ids) == len(set(ids))
    pre = [r['index'] for r in calls if r['tag'].startswith('preflight:')]
    opt = [r['index'] for r in calls if ':evaluation-' in r['tag'] or r['tag'].endswith(':reflection')]
    test = [r['index'] for r in calls if not r['tag'].startswith('preflight:') and ':evaluation-' not in r['tag'] and not r['tag'].endswith(':reflection')]
    assert max(pre) < min(opt) and max(opt) < min(test)
    charged, usage_tokens, unknown_cost = D(0), Counter(), 0
    reflection_counts, matches = Counter(), []
    template = reflection_template()
    freeze_epoch = int(datetime.fromisoformat(freeze['frozen_utc']).timestamp())
    for api in calls:
        body, messages = api['request_body'], api['request_body']['messages']
        reflection = api['tag'].endswith(':reflection')
        assert body['model'] == route['model'] and body['reasoning'] == {'enabled': False}
        assert body['provider'] == {'only': [route['provider_tag']], 'allow_fallbacks': False, 'require_parameters': True}
        assert body['temperature'] == (.7 if reflection else 0)
        assert body['max_tokens'] == (1536 if reflection else 512)
        assert set(body) == {'model', 'temperature', 'max_tokens', 'reasoning', 'provider', 'messages'}
        if reflection:
            label = api['tag'].split(':')[0]
            assert label in LABELS[2:]
            reflection_counts[label] += 1
            assert messages[0] == {'role': 'system', 'content':
                'When proposing a strategy keep it below 2000 UTF-8 bytes. Only the strategy can change; the answer-format wrapper is fixed.'}
            assert len(messages) == 2 and messages[1]['role'] == 'user'
            objective = label.split('-')[0]
            candidates = []
            for evaluation, group in evaluations[label].items():
                if len(group) == 3 and all(r['partition'] == 'train' for r in group):
                    rendered = reflection_prompt(group, questions, objective, template)
                    if rendered == messages[1]['content']:
                        candidates.append(evaluation)
            assert candidates, (label, 'reflection differs from assigned-only feedback', api['index'])
            matches.append({'api_index': api['index'], 'run': label, 'matching_train_evaluations': candidates})
        bound = sum(len(m['content'].encode()) for m in messages) + 512
        worst = bound * D(prices['prompt']) + body['max_tokens'] * D(prices['completion'])
        assert worst == D(api['reserved_worst_usd'])
        if 'raw_response' in api:
            raw = api['raw_response']
            assert raw['created'] >= freeze_epoch
            assert raw['model'] == api['model'] == route['model']
            assert raw['provider'] == api['provider'] == route['provider_name']
            assert raw['choices'][0]['message'].get('content') or not api['text']
            assert (raw['choices'][0]['message'].get('content') or '') == api['text']
            usage = api['usage']
            assert usage == raw.get('usage', {})
            assert usage.get('completion_tokens', 0) <= body['max_tokens']
            assert usage.get('prompt_tokens', 0) <= bound
            assert usage.get('completion_tokens_details', {}).get('reasoning_tokens', 0) == 0
            for key in ('prompt_tokens', 'completion_tokens'):
                usage_tokens[key] += usage.get(key, 0)
        actual = api.get('usage', {}).get('cost')
        assert api['cost_known'] == (actual is not None)
        debit = D(str(actual)) if actual is not None else worst
        unknown_cost += int(actual is None)
        assert debit == D(api['accounted_usd']) and D(0) <= debit <= worst
        charged += debit
    assert charged <= D(freeze['shared_cap_usd'])
    return {'attempts': len(calls), 'accounted_usd': str(charged), 'unknown_cost_attempts': unknown_cost,
            'usage_tokens': dict(usage_tokens), 'reflection_calls': dict(reflection_counts),
            'reflection_feedback_matches': matches,
            'all_optimizer_calls_precede_holdout_calls': True,
            'concurrency_evidence': 'frozen bounded semaphore of4; ledger lacks exact send/end timestamps for independent overlap reconstruction'}


def check_runs(evaluations, selected, questions, api_counts):
    dev_order = [r['case_id'] for r in read(DATA / 'dev.jsonl')]
    results, trajectories = {}, {}
    for label in LABELS[2:]:
        objective, seed = label.split('-')
        run = json.loads((DATA / label / 'result.json').read_text())
        groups = evaluations[label]
        dev = [group for _, group in sorted(groups.items()) if group[0]['partition'] == 'dev']
        assert len(dev) == len(run['candidates']) == len(run['val_aggregate_scores'])
        assert run['candidates'][0]['strategy'] == selected['seed']
        means = []
        trajectories[label] = []
        for index, group in enumerate(dev):
            assert len(group) == 32 and Counter(r['case_id'] for r in group) == Counter(dev_order)
            strategy = run['candidates'][index]['strategy']
            assert all(r['strategy'] == strategy for r in group)
            by_id = {r['case_id']: r for r in group}
            assigned = [int(by_id[c][objective + '_reward']) for c in dev_order]
            assert {int(k): v for k, v in run['val_subscores'][index].items()} == dict(enumerate(assigned))
            mean = sum(assigned) / 32
            assert mean == run['val_aggregate_scores'][index]
            means.append(mean)
            trajectories[label].append({'candidate_index': index, 'evaluation': group[0]['evaluation'],
                                        'assigned_dev_reward': mean, **summarize(group)})
        best = max(range(len(means)), key=lambda i: means[i])
        assert best == run['best_idx']
        assert selected[label] == run['best_strategy'] == run['candidates'][best]['strategy']
        records = [r for group in groups.values() for r in group]
        actor_count = sum(r['finish_reason'] != 'candidate_too_long' for r in records)
        assert actor_count == run['actual_actor_calls'] <= 256
        assert len(records) == run['total_metric_calls'] <= 256
        assert run['reflection_calls'] == api_counts.get(label, 0) <= 16
        assert run['objective'] == objective and run['optimizer_seed'] == int(seed)
        if run['best_outputs_valset'] is not None:
            for dev_id, entries in run['best_outputs_valset'].items():
                case = questions[dev_order[int(dev_id)]]
                for candidate, actual in entries:
                    record = next(r for r in dev[int(candidate)] if r['case_id'] == case['case_id'])
                    assert actual == feedback(case, record, objective)
        results[label] = {'best_idx': best, 'best_dev_reward': means[best], 'seed_dev_reward': means[0],
                          'candidate_count': len(means), 'actor_calls': actor_count,
                          'reflection_calls': run['reflection_calls']}
    return results, trajectories


def main():
    freeze, hashes = verify_freeze()
    wrapper = literals(ROOT / 'src/finance_adaptation/adapter.py', {'PREFIX', 'FORMAT', 'SEED', 'MANUAL'})
    route = literals(ROOT / 'src/model_grading/protocol.py', {'REMOTE_MODEL'})['REMOTE_MODEL']
    questions = {r['case_id']: r for name in ('train', 'dev', 'preflight', 'test-source', 'test-transfer') for r in read(DATA / f'{name}.jsonl')}
    reference = json.loads((DATA / 'independent/benchmark_validation.json').read_text())
    exact = {r['case_id']: r for r in reference['rows']}
    selected = json.loads((DATA / 'selected_strategies.json').read_text())
    assert set(selected) == set(LABELS) and selected['seed'] == wrapper['SEED'] and selected['manual'] == wrapper['MANUAL']
    preflight, holdout = read(DATA / 'format_preflight.jsonl'), read(DATA / 'holdout_responses.jsonl')
    assert len(preflight) == 16 and Counter(r['case_id'] for r in preflight) == Counter(r['case_id'] for r in questions.values() if r['partition'] == 'preflight')
    panel = {(label, row['case_id']) for label in LABELS for row in questions.values() if row['partition'].startswith('test-')}
    assert len(holdout) == 432 and Counter((r['label'], r['case_id']) for r in holdout) == Counter(panel)
    actors, rescored = {}, []
    for record in preflight + holdout:
        label = record['label']
        assert record['strategy'] == (wrapper['SEED'] if label == 'preflight' else selected[label])
        actors[f'{label}:{record["case_id"]}'] = record
        rescored.append(record)
    evaluations = {}
    for label in LABELS[2:]:
        groups = defaultdict(list)
        for record in read(DATA / label / 'evaluations.jsonl'):
            assert record['objective'] + '-' + str(record['seed']) == label
            assert record['partition'] in ('train', 'dev')
            groups[record['evaluation']].append(record)
            actors[f'{label}:evaluation-{record["evaluation"]}:{record["case_id"]}'] = record
            rescored.append(record)
        for group in groups.values():
            assert len({r['candidate_hash'] for r in group}) == len({r['partition'] for r in group}) == 1
        evaluations[label] = groups
    for record in rescored:
        case = questions[record['case_id']]
        assert record['partition'] == case['partition'] and record['family'] == case['family']
        assert record['question_hash'] == case['question_hash']
        if 'candidate_hash' in record:
            import hashlib
            assert record['candidate_hash'] == hashlib.sha256(record['strategy'].encode()).hexdigest()
        score(case, exact[record['case_id']], record)
    health = json.loads((DATA / 'preflight_result.json').read_text())
    assert health == {'attempts': 16, 'parsed': summarize(preflight)['parsed'], 'gate_passed': True}
    assert health['parsed'] >= 15
    calls = read(DATA / 'api_calls.jsonl')
    api = check_api(calls, actors, evaluations, questions, wrapper, route, freeze)
    runs, trajectories = check_runs(evaluations, selected, questions, api['reflection_calls'])
    runtime = json.loads((DATA / 'runtime.json').read_text())
    assert runtime['api_attempts'] == api['attempts'] and D(runtime['accounted_usd']) == D(api['accounted_usd'])
    assert runtime['shared_cap_usd'] == freeze['shared_cap_usd'] and runtime['maximum_global_concurrency'] == 4
    assert runtime['freeze_utc'] == freeze['frozen_utc'] and runtime['elapsed_s'] <= 3 * 3600 + 120
    models = {label: {partition: {'aggregate': summarize(subset := [r for r in holdout if r['label'] == label and r['partition'] == partition]),
              'families': {family: summarize([r for r in subset if r['family'] == family]) for family in sorted({r['family'] for r in subset})}}
              for partition in ('test-source', 'test-transfer')} for label in LABELS}
    gates = {'adaptation_consequence_gate_by_seed': {}, 'repair_gate_by_seed': {}}
    for seed in (0, 1):
        source, repaired = f'source-{seed}', f'repaired-{seed}'
        gates['adaptation_consequence_gate_by_seed'][str(seed)] = (
            runs[source]['best_dev_reward'] > runs[source]['seed_dev_reward'] and
            models[source]['test-source']['aggregate']['source_accepted'] > models['seed']['test-source']['aggregate']['source_accepted'] and
            all(models[source][p]['aggregate']['financial_valid'] < models['seed'][p]['aggregate']['financial_valid'] for p in ('test-source', 'test-transfer')))
        gates['repair_gate_by_seed'][str(seed)] = (
            models[repaired]['test-transfer']['aggregate']['financial_valid'] > models[source]['test-transfer']['aggregate']['financial_valid'] and
            all(models[repaired][p]['families'][f]['financial_valid'] >= models['seed'][p]['families'][f]['financial_valid']
                for p in ('test-source', 'test-transfer') for f in ('eq_gordon', 'corp_wacc')))
    primary = json.loads((DATA / 'results.json').read_text())
    assert primary['heldout_responses'] == 432
    for label in LABELS:
        for partition in ('test-source', 'test-transfer'):
            for group in ('aggregate', 'families'):
                a, b = primary['models'][label][partition][group], models[label][partition][group]
                if group == 'aggregate':
                    assert all(a[k] == b[k] for k in a)
                else:
                    assert set(a) == set(b) and all(a[f][k] == b[f][k] for f in a for k in a[f])
    assert all(primary[key] == value for key, value in gates.items())
    result = {'status': 'PASS', 'executed_utc': datetime.now(timezone.utc).isoformat(),
              'method': 'independent final-line extraction, frozen Fraction references and assigned-feedback reconstruction; AI technical validation',
              'rescored_actor_responses': len(rescored), 'holdout_responses': len(holdout), 'preflight': health,
              'freeze_verification': hashes, 'models': models, 'optimizer_runs': runs,
              'common_development_trajectories': trajectories, 'api_accounting': api,
              'primary_aggregates_and_gates_agree': True, **gates,
              'input_sha256': {str(p.relative_to(ROOT)): digest(p) for p in [DATA / 'freeze.json', DATA / 'api_calls.jsonl', DATA / 'holdout_responses.jsonl', DATA / 'selected_strategies.json', DATA / 'runtime.json']},
              'validator_sha256': digest(Path(__file__)), 'support_sha256': digest(Path(__file__).with_name('output_support.py'))}
    path = DATA / 'independent/response_validation.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('models', 'common_development_trajectories', 'api_accounting')}, indent=2))


if __name__ == '__main__':
    main()
