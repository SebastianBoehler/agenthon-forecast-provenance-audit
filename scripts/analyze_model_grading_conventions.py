"""Executive summary: test implicit binomial compounding without replacing the frozen simple-rate oracle."""
import copy
import json
from collections import defaultdict
from decimal import Decimal as D, localcontext

from answer_contract.formulas import NUM, operands
from answer_contract.sources import cosimo_cases
from model_grading.numeric_sensitivity import numeric_score
from model_grading.protocol import DESTINATION, LOCAL_MODELS, digest, frozen_selection, read_jsonl, write_json
from model_grading.scoring import score_one, summarize


def continuous_price(prompt):
    spot, up, down, strike, rate = operands(
        rf'S0={NUM}, u={NUM}, d={NUM}, K={NUM}, rf={NUM}%', prompt)
    gross = (rate / 100).exp()
    if not down < gross < up:
        return None
    cu, cd = max(spot * up - strike, D(0)), max(spot * down - strike, D(0))
    probability = (gross - down) / (up - down)
    return (probability * cu + (1 - probability) * cd) / gross


def extended_record(record, alternative):
    result = copy.deepcopy(record)
    alt_valid = (alternative is not None and result['value'] is not None and
                 abs(D(result['value']) - alternative) <= D('.005') + D('1e-20'))
    result['declared_simple_valid'] = result['visible_valid']
    result['continuous_valid'] = alt_valid
    result['visible_valid'] = result['visible_valid'] or alt_valid
    result['decisions']['visible_contract'] = result['visible_valid']
    return result


def aggregate(records, models):
    groups = defaultdict(list)
    for record in records:
        groups[record['model_key']].append(record)
    return {model: {'aggregate': summarize(groups[model]),
                    'binomial_compatibility': compatibility(
                        [r for r in groups[model] if r['family'] == 'deriv_binomial_call']),
                    'continuous_only_added': sum(r['continuous_valid'] and not r['declared_simple_valid']
                                                 for r in groups[model]),
                    'families': {family: summarize([r for r in groups[model] if r['family'] == family])
                                 for family in sorted({r['family'] for r in groups[model]})}}
            for model in models}


def compatibility(rows):
    return {'simple_only': sum(r['declared_simple_valid'] and not r['continuous_valid'] for r in rows),
            'continuous_only': sum(r['continuous_valid'] and not r['declared_simple_valid'] for r in rows),
            'both': sum(r['continuous_valid'] and r['declared_simple_valid'] for r in rows),
            'neither_parsed': sum(r['value'] is not None and not r['visible_valid'] for r in rows),
            'unparsed': sum(r['value'] is None for r in rows)}


def main():
    freeze_path = DESTINATION / 'convention_sensitivity_freeze_v2.json'
    freeze = json.loads(freeze_path.read_text())
    for name, expected in freeze['files'].items():
        if digest(DESTINATION.parents[1] / name) != expected:
            raise ValueError(f'Compounding sensitivity changed after freeze: {name}')
    supplementary = json.loads((DESTINATION / 'numeric_sensitivity_freeze_v2.json').read_text())
    for name, expected in supplementary['files'].items():
        if digest(DESTINATION.parents[1] / name) != expected:
            raise ValueError(f'Supplementary parser changed: {name}')
    selection = frozen_selection()
    selected = {r['case_id'] for r in selection}
    models = list(LOCAL_MODELS) + ['deepseek-v3.2', 'qwen3-4b']
    paths = [DESTINATION / f'{model}_responses.jsonl' for model in models]
    responses = [row for path in paths for row in read_jsonl(path)]
    keys = [(r['model_key'], r['case_id']) for r in responses]
    if len(keys) != len(set(keys)) or set(keys) != {(m, c) for m in models for c in selected}:
        raise ValueError('Convention sensitivity requires the complete original-plus-extension panel')
    strict, numeric, source_rows, alternatives = [], [], [], {}
    with localcontext() as context:
        context.prec = 50
        all_cases = list(cosimo_cases())
        cases = {c.case_id: c for c in all_cases if c.case_id in selected}
        for case in all_cases:
            if case.family != 'deriv_binomial_call':
                continue
            alternative = continuous_price(case.prompt)
            alternatives[case.case_id] = alternative
            simple_valid = case.accepts(case.gold)
            alt_valid = (alternative is not None and
                         abs(case.gold - alternative) <= D('.005') + D('1e-20'))
            source_rows.append({'case_id': case.case_id, 'simple_price': str(case.formula),
                                'continuous_price': str(alternative) if alternative is not None else None,
                                'gold': str(case.gold), 'simple_valid': simple_valid,
                                'continuous_valid': alt_valid, 'either_valid': simple_valid or alt_valid})
        for response in responses:
            case = cases[response['case_id']]
            alternative = alternatives.get(case.case_id)
            strict.append(extended_record(score_one(response, case), alternative))
            numeric.append(extended_record(numeric_score(response, case), alternative))
    results = {'executive_summary': 'Posthoc union of two binomial compounding conventions; primary analyses unchanged.',
               'questions': len(selection), 'responses': len(responses),
               'freeze_sha256': digest(freeze_path),
               'response_sha256': {path.name: digest(path) for path in paths},
               'source_binomial': {'rows': len(source_rows),
                   'simple_invalid': sum(not r['simple_valid'] for r in source_rows),
                   'either_invalid': sum(not r['either_valid'] for r in source_rows),
                   'continuous_only_added': sum(r['continuous_valid'] and not r['simple_valid'] for r in source_rows),
                   'simple_only': sum(r['simple_valid'] and not r['continuous_valid'] for r in source_rows),
                   'continuous_only': sum(r['continuous_valid'] and not r['simple_valid'] for r in source_rows),
                   'both': sum(r['continuous_valid'] and r['simple_valid'] for r in source_rows),
                   'continuous_no_arbitrage_failures': sum(r['continuous_price'] is None for r in source_rows)},
               'strict_models': aggregate(strict, models), 'numeric_models': aggregate(numeric, models)}
    write_json(DESTINATION / 'convention_sensitivity.json', results)
    for name, rows in [('convention_source_rows', source_rows), ('convention_strict_scored', strict),
                       ('convention_numeric_scored', numeric)]:
        (DESTINATION / f'{name}.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
    print(json.dumps(results['source_binomial']))
    print(json.dumps({m: r['continuous_only_added'] for m, r in results['numeric_models'].items()}))


if __name__ == '__main__':
    main()
