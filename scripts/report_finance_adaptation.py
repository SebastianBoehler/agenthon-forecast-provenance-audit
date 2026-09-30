"""Executive summary: report complete heldouts and common-question GEPA trajectories."""
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from finance_adaptation.adapter import rewards
from model_grading.protocol import read_jsonl, write_json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/finance-adaptation-v1'
LABELS = ('seed', 'manual', 'source-0', 'source-1', 'repaired-0', 'repaired-1')


def summarize(rows):
    return {'attempts': len(rows), 'parsed': sum(r['value'] is not None for r in rows),
            'financial_valid': sum(r['financial_valid'] for r in rows),
            'source_accepted': (sum(bool(r['source_reward']) for r in rows)
                                if rows and rows[0]['partition'] != 'test-transfer' else None),
            'rounding_violations': sum(r['family'] == 'cr_eq_gordon' and
                                       r['value'] is not None and '.' in r['value'] and
                                       float(r['value']) != int(float(r['value'])) for r in rows),
            'wrong_quantity_source_credited': sum(r['family'] == 'deriv_binomial_call' and
                                                  bool(r['source_reward']) and
                                                  not r['financial_valid'] for r in rows)}


def main():
    selected = json.loads((OUT / 'selected_strategies.json').read_text())
    questions = {r['case_id']: r for name in ('test-source', 'test-transfer')
                 for r in read_jsonl(OUT / f'{name}.jsonl')}
    rows = read_jsonl(OUT / 'holdout_responses.jsonl')
    keys = [(r['label'], r['case_id']) for r in rows]
    if len(keys) != len(set(keys)) or set(keys) != {(l, c) for l in LABELS for c in questions}:
        raise ValueError('Holdout panel is incomplete or has duplicate/unexpected attempts')
    for row in rows:
        case = questions[row['case_id']]
        if row['question_hash'] != case['question_hash'] or row['strategy'] != selected[row['label']]:
            raise ValueError('A holdout answer does not match the frozen question/selected strategy')
        recalculated = rewards(case, row['text'], row['finish_reason'])
        if any(row[k] != v for k, v in recalculated.items()):
            raise ValueError('Saved holdout scoring differs from recalculation')
    results = {}
    for label in LABELS:
        results[label] = {}
        for partition in ('test-source', 'test-transfer'):
            subset = [r for r in rows if r['label'] == label and r['partition'] == partition]
            results[label][partition] = {'aggregate': summarize(subset),
                                         'families': {f: summarize([r for r in subset if r['family'] == f])
                                                      for f in sorted({r['family'] for r in subset})}}
    development = {r['case_id'] for r in read_jsonl(OUT / 'dev.jsonl')}
    trajectories, runs = {}, {}
    for label in LABELS[2:]:
        run = json.loads((OUT / label / 'result.json').read_text())
        runs[label] = {k: run[k] for k in ('best_idx', 'best_strategy', 'actual_actor_calls',
                                          'reflection_calls', 'elapsed_s', 'val_aggregate_scores')}
        groups = defaultdict(list)
        for row in read_jsonl(OUT / label / 'evaluations.jsonl'):
            if row['partition'] == 'dev':
                groups[row['evaluation']].append(row)
        trajectories[label] = []
        for evaluation, subset in sorted(groups.items()):
            if len(subset) != len(development) or {r['case_id'] for r in subset} != development:
                raise ValueError('A development trajectory is not the common full question set')
            trajectories[label].append({'evaluation': evaluation,
                                         'candidate_hash': subset[0]['candidate_hash'],
                                         **summarize(subset),
                                         'repaired_accepted': sum(r['repaired_reward'] for r in subset)})
    consequence, repair = {}, {}
    for seed in (0, 1):
        source = f'source-{seed}'
        consequence[str(seed)] = (
            max(runs[source]['val_aggregate_scores']) > runs[source]['val_aggregate_scores'][0] and
            results[source]['test-source']['aggregate']['source_accepted'] >
            results['seed']['test-source']['aggregate']['source_accepted'] and
            all(results[source][p]['aggregate']['financial_valid'] <
                results['seed'][p]['aggregate']['financial_valid']
                for p in ('test-source', 'test-transfer')))
        repaired = f'repaired-{seed}'
        repair[str(seed)] = (
            results[repaired]['test-transfer']['aggregate']['financial_valid'] >
            results[source]['test-transfer']['aggregate']['financial_valid'] and
            all(results[repaired][p]['families'][f]['financial_valid'] >=
                results['seed'][p]['families'][f]['financial_valid']
                for p in ('test-source', 'test-transfer') for f in ('eq_gordon', 'corp_wacc')))
    runtime = json.loads((OUT / 'runtime.json').read_text())
    report = {'executive_summary': 'Finite paired-objective prompt adaptation; not weight training.',
              'status': 'executed_complete_holdout', 'questions': len(questions),
              'heldout_responses': len(rows), 'models': results, 'optimizer_runs': runs,
              'common_development_trajectories': trajectories,
              'adaptation_consequence_gate_by_seed': consequence,
              'repair_gate_by_seed': repair, 'runtime': runtime,
              'input_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in (OUT / 'freeze.json', OUT / 'holdout_responses.jsonl',
                                         OUT / 'selected_strategies.json', OUT / 'runtime.json')}}
    write_json(OUT / 'results.json', report)
    lines = ['## Executive summary (read this first)', '',
             'The frozen GEPA pilot is complete. These are prompt-adaptation results for one',
             'actor/provider on 48 fresh released questions and24 researcher-authored questions.',
             'No model weights changed; template/family selection limits generalization.', '',
             '| Strategy | Source parsed/48 | Source financially valid/48 | Released credits/48 | Transfer parsed/24 | Transfer financially valid/24 |',
             '|---|---:|---:|---:|---:|---:|']
    for label in LABELS:
        source = results[label]['test-source']['aggregate']
        transfer = results[label]['test-transfer']['aggregate']
        values = [source['parsed'], source['financial_valid'], source['source_accepted'],
                  transfer['parsed'], transfer['financial_valid']]
        lines.append('| ' + label + ' | ' + ' | '.join(map(str, values)) + ' |')
    lines += ['', f'Adaptation consequence gate by optimizer seed: `{consequence}`.',
              f'Repair gate by optimizer seed: `{repair}`.', '',
              f'Accounted API cost: ${runtime["accounted_usd"]}; calls: {runtime["api_attempts"]}.',
              'All failed attempts remain in denominators. Transfer has no released target;',
              'its released-label reward is undefined. The original800-answer study is unchanged.',
              'The independent evaluation reports numerical validity, not trace certification.',
              'See the prospective protocol and independent validation for assumptions and gates.', '',
              'Full development trajectories, per-family counts, selected prompts and raw API',
              'records are retained under outputs/finance-adaptation-v1. Both development',
              'objectives retain the exact source-label cent window on the two passing controls.']
    (ROOT / 'docs/FINANCE_ADAPTATION_RESULTS_V1.md').write_text('\n'.join(lines) + '\n')
    print(json.dumps({'status': report['status'], 'heldout_responses': len(rows),
                      'consequence_gate': consequence, 'repair_gate': repair}))


if __name__ == '__main__':
    main()
