"""Executive summary: retain the original panel and separately score the frozen size extension."""
import copy
import json
from collections import defaultdict
from decimal import localcontext

from answer_contract.sources import cosimo_cases
from model_grading.numeric_sensitivity import numeric_score
from model_grading.protocol import DESTINATION, digest, frozen_selection, read_jsonl, write_json
from model_grading.scoring import evaluate, summarize


def jsonl(path, rows):
    path.write_text(''.join(json.dumps(row) + '\n' for row in rows))


def combine(original_name, extension_name, target_name):
    original = json.loads((DESTINATION / original_name).read_text())
    added = json.loads((DESTINATION / extension_name).read_text())
    if set(original['models']) & set(added['models']):
        raise ValueError('Combined analysis must not replace an original model')
    result = copy.deepcopy(original)
    result['models'].update(added['models'])
    result['responses'] += added['responses']
    result['roster_extension'] = 'post-original-response within-family size comparison'
    result['constituent_sha256'] = {name: digest(DESTINATION / name)
                                    for name in [original_name, extension_name]}
    write_json(DESTINATION / target_name, result)


def main():
    freeze_path = DESTINATION / 'extension_manifest.json'
    manifest = json.loads(freeze_path.read_text())
    for name, expected in manifest['files'].items():
        if digest(DESTINATION.parents[1] / name) != expected:
            raise ValueError(f'Extension changed after freeze: {name}')
    supplementary = json.loads((DESTINATION / 'numeric_sensitivity_freeze_v2.json').read_text())
    for name, expected in supplementary['files'].items():
        if digest(DESTINATION.parents[1] / name) != expected:
            raise ValueError(f'Supplementary implementation changed: {name}')
    selection = frozen_selection()
    models = list(manifest['added_models'])
    paths = [DESTINATION / f'{model}_responses.jsonl' for model in models]
    responses = [r for p in paths for r in read_jsonl(p)]
    scored, results = evaluate(selection, responses, models)
    results['extension_manifest_sha256'] = digest(freeze_path)
    results['response_sha256'] = {p.name: digest(p) for p in paths}
    write_json(DESTINATION / 'extension_results.json', results)
    jsonl(DESTINATION / 'extension_scored.jsonl', scored)
    with localcontext() as context:
        context.prec = 50
        cases = {c.case_id: c for c in cosimo_cases() if c.case_id in {r['case_id'] for r in selection}}
        numeric = [numeric_score(r, cases[r['case_id']]) for r in responses]
    groups = defaultdict(list)
    for row in numeric:
        groups[row['model_key']].append(row)
    sensitivity = {'status': 'exploratory_numeric_extraction_for_roster_extension',
                   'questions': len(selection), 'responses': len(responses),
                   'extension_manifest_sha256': digest(freeze_path),
                   'models': {model: {
                       'aggregate': summarize(groups[model]),
                       'unit_states': {u: sum(r['unit_state'] == u for r in groups[model])
                                       for u in ['explicit', 'placeholder', 'absent', 'wrong']},
                       'families': {family: summarize([r for r in groups[model] if r['family'] == family])
                                    for family in sorted({r['family'] for r in groups[model]})},
                   } for model in models}}
    write_json(DESTINATION / 'extension_numeric_sensitivity.json', sensitivity)
    jsonl(DESTINATION / 'extension_numeric_scored.jsonl', numeric)
    combine('results.json', 'extension_results.json', 'combined_results.json')
    combine('numeric_sensitivity.json', 'extension_numeric_sensitivity.json',
            'combined_numeric_sensitivity.json')
    jsonl(DESTINATION / 'combined_scored.jsonl', read_jsonl(DESTINATION / 'scored.jsonl') + scored)
    jsonl(DESTINATION / 'combined_numeric_scored.jsonl',
          read_jsonl(DESTINATION / 'numeric_scored.jsonl') + numeric)
    print('Original 600 responses retained; combined four-model panel contains 800 responses')


if __name__ == '__main__':
    main()
