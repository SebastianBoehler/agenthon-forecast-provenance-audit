"""Executive summary: preserve strict grading and report a marked exploratory numeric-only analysis."""
import json
from collections import defaultdict
from decimal import localcontext

from answer_contract.sources import cosimo_cases
from model_grading.numeric_sensitivity import numeric_score
from model_grading.protocol import (DESTINATION, LOCAL_MODELS, digest, frozen_selection,
                                    read_jsonl, write_json)
from model_grading.scoring import summarize


def main():
    freeze_path = DESTINATION / 'numeric_sensitivity_freeze_v2.json'
    freeze = json.loads(freeze_path.read_text())
    for name, expected_hash in freeze['files'].items():
        if digest(DESTINATION.parents[1] / name) != expected_hash:
            raise ValueError(f'Supplementary implementation changed after correction: {name}')
    selection = frozen_selection()
    selected = {r['case_id']: r for r in selection}
    models = list(LOCAL_MODELS) + ['deepseek-v3.2']
    responses = [r for m in models for r in read_jsonl(DESTINATION / f'{m}_responses.jsonl')]
    keys = [(r['model_key'], r['case_id']) for r in responses]
    if len(keys) != len(set(keys)) or set(keys) != {(m, c) for m in models for c in selected}:
        raise ValueError('Sensitivity requires the same complete frozen model panel')
    with localcontext() as context:
        context.prec = 50
        cases = {c.case_id: c for c in cosimo_cases() if c.case_id in selected}
        records = [numeric_score(r, cases[r['case_id']]) for r in responses]
    groups = defaultdict(list)
    for r in records:
        groups[r['model_key']].append(r)
    results = {'status': 'exploratory_numeric_final_line_sensitivity_after_format_failures',
               'no_answer_regeneration': True, 'no_unit_conversion': True,
               'questions': 200, 'responses': len(records),
               'strict_results_sha256': digest(DESTINATION / 'results.json'),
               'supplementary_freeze_sha256': digest(freeze_path),
               'amendment_sha256': digest(DESTINATION.parents[1] / 'docs/MODEL_GRADING_AMENDMENT_NUMERIC.md'),
               'models': {m: {
                   'aggregate': summarize(groups[m]),
                   'unit_states': {u: sum(r['unit_state'] == u for r in groups[m])
                                   for u in ('explicit', 'placeholder', 'absent', 'wrong')},
                   'families': {f: summarize([r for r in groups[m] if r['family'] == f])
                                for f in sorted({r['family'] for r in groups[m]})},
               } for m in models}}
    write_json(DESTINATION / 'numeric_sensitivity.json', results)
    (DESTINATION / 'numeric_scored.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in records))
    print(json.dumps({m: results['models'][m]['aggregate'] for m in models}, indent=2))


if __name__ == '__main__':
    main()
