"""Executive summary: generate a bounded study report from complete saved-answer analyses."""
import json
from pathlib import Path

from model_grading.protocol import DESTINATION, digest, read_jsonl

ROOT = Path(__file__).resolve().parents[1]
MODELS = {'qwen3-1.7b': 'Qwen3 1.7B', 'qwen3-4b': 'Qwen3 4B',
          'qwen2.5-coder-3b': 'Qwen2.5-Coder 3B', 'deepseek-v3.2': 'DeepSeek V3.2'}
FAMILIES = {'cr_eq_gordon': 'Whole-unit Gordon', 'deriv_binomial_call': 'Binomial call',
            'eq_gordon': 'Ordinary Gordon', 'corp_wacc': 'WACC'}


def table(header, rows):
    return '\n'.join(['| ' + ' | '.join(header) + ' |',
                      '| ' + ' | '.join(['---'] * len(header)) + ' |'] +
                     ['| ' + ' | '.join(map(str, row)) + ' |' for row in rows])


def paired(rows):
    by_model = {m: {r['case_id']: r for r in rows if r['model_key'] == m}
                for m in ['qwen3-1.7b', 'qwen3-4b']}
    if set(by_model['qwen3-1.7b']) != set(by_model['qwen3-4b']):
        raise ValueError('Within-family comparison requires identical question IDs')
    pairs = [(r['visible_valid'], by_model['qwen3-4b'][key]['visible_valid'])
             for key, r in by_model['qwen3-1.7b'].items()]
    return [sum(a and b for a, b in pairs), sum(a and not b for a, b in pairs),
            sum(b and not a for a, b in pairs), sum(not a and not b for a, b in pairs)]


def main():
    strict = json.loads((DESTINATION / 'combined_results.json').read_text())
    numeric = json.loads((DESTINATION / 'combined_numeric_sensitivity.json').read_text())
    conventions = json.loads((DESTINATION / 'convention_sensitivity.json').read_text())
    if any(r['responses'] != 800 or r['questions'] != 200 for r in [strict, numeric, conventions]):
        raise ValueError('Report requires the complete four-model panel')
    summaries = []
    for model, label in MODELS.items():
        p = strict['models'][model]['aggregate']
        n = numeric['models'][model]['aggregate']
        c = conventions['numeric_models'][model]['aggregate']
        summaries.append([label, p['parsed_completed'], p['visible_valid'],
                          n['parsed_completed'], n['visible_valid'], c['visible_valid']])
    text = ['## Executive summary (read this first)', '',
            'Executed 800 responses to the same 200 distinct public questions: four models, 50 questions per family. '
            'The original three-model 600-response panel is preserved separately from the later 4B extension. '
            'This measures grading of saved model answers, not training effects. Strict final-line parsing, '
            'post hoc numeric extraction and post hoc compounding sensitivity are distinct endpoints.', '',
            f"Reported API usage cost: ${strict['api_reported_cost_usd']:.9f}; the additional local run uses cached weights.", '',
            '## Completion and declared numerical validity', '',
            'Every cell has the same 200-question denominator. Strict is the declared final-line endpoint, '
            'not complete compliance with all system instructions. Numeric recovery may lack an explicit unit. '
            'The last column broadens only binomial validity to either simple or continuous compounding.', '',
            table(['Model', 'Strict parsed', 'Strict valid', 'Numeric parsed', 'Numeric valid (1+r)',
                   'Numeric valid (either convention)'], summaries), '',
            '## Grading unchanged recovered numbers', '',
            'All cells are counts among the same 50 questions per model/family, including failures in the denominator. '
            '“Denied” counts declared-contract-valid numbers rejected by an original-label comparator; '
            '“credited” counts parsed numbers outside that contract accepted by it. '
            'They are paired numerical decisions, not separate generations. Here the binomial reference remains 1+r.', '']
    rows = []
    for family, family_label in FAMILIES.items():
        for model, label in MODELS.items():
            row = numeric['models'][model]['families'][family]
            policies = row['policies']
            counts = [policies[p][field] for p in ['source_abs_0.005', 'source_abs_0.5', 'source_relative_5pct']
                      for field in ['valid_rejected', 'numeric_invalid_accepted']]
            rows.append([label, family_label, *counts])
    small = numeric['models']['qwen3-1.7b']['families']['cr_eq_gordon']
    deep = numeric['models']['deepseek-v3.2']['families']['cr_eq_gordon']
    text += [f"Constructed-Gordon source-cent credits are {small['policies']['source_abs_0.005']['accepted']}/50 "
             f"for Qwen3 1.7B versus {deep['policies']['source_abs_0.005']['accepted']}/50 for DeepSeek; "
             f"visible integer-contract validity is {small['visible_valid']}/50 versus {deep['visible_valid']}/50. "
             'Changing only the grader reverses their ordering on this family under the exploratory numeric endpoint. '
             'This is not a general model ranking.', '']
    text += [table(['Model', 'Family', 'Cent denied', 'Cent credited', 'Half denied', 'Half credited',
                    '5% denied', '5% credited'], rows), '', '## Cheap rounding baseline', '',
             'Only constructed Gordon has a meaningful integer-plus-original-half-unit baseline. '
             'Other-family mechanical JSON values are not interpreted.', '']
    rows = []
    for model, label in MODELS.items():
        row = numeric['models'][model]['families']['cr_eq_gordon']
        p = row['policies']
        rows.append([label, row['visible_valid'], p['source_abs_0.5']['numeric_invalid_accepted'],
                     p['integer_and_source_half']['numeric_invalid_accepted'],
                     p['integer_and_source_half']['valid_rejected']])
    text += [table(['Model', 'Valid recovered', 'Half: invalid credited', 'Integer+half: invalid credited',
                    'Integer+half: valid denied'], rows), '', '## Paired Qwen3 checkpoint comparison', '',
             'Counts use all 200 shared question IDs. This controls prompt, model generation, precision, runtime and decoding; '
             'it does not identify a causal parameter-count effect because checkpoints/training differ.', '']
    rows = []
    for endpoint, filename in [('Strict', 'combined_scored.jsonl'), ('Numeric', 'combined_numeric_scored.jsonl'),
                               ('Numeric, either convention', 'convention_numeric_scored.jsonl')]:
        rows.append([endpoint, *paired(read_jsonl(DESTINATION / filename))])
    text += [table(['Endpoint', 'Both valid', '1.7B only valid', '4B only valid', 'Neither valid'], rows), '',
             '## Convention robustness and limits', '',
             f"Among all 1,000 source binomial labels, {conventions['source_binomial']['either_invalid']} remain invalid "
             'under both checked conventions. The source generator computes financing debt; coincident numerical '
             'values do not certify that formula. The convention sensitivity is a union of two cent neighborhoods, '
             'not the interval between their prices. Literal reasoning keywords are not a gate for this test.', '',
             'The original compounding-sensitivity timing claim was corrected in a separate note: its first freeze '
             'followed 14 Coder binomial responses and preceded all 4B responses. The endpoint remains explicitly post hoc. '
             'Neither the size extension nor numerical recovery is retrospectively preregistered.', '',
             'Family selection is purposive; repeated templates prevent treating the census as independent population samples. '
             'No fine-tuning, executable upstream reward, general-validator accuracy, human expert review or causal model ranking '
             'is claimed. Final-answer compatibility does not certify a reasoning trace. A 12-item anonymous human-review '
             'packet is prepared but its sheet remains blank.', '', '## Input analysis hashes', '']
    text += [f'- `{name}`: `{digest(DESTINATION / name)}`' for name in
             ['results.json', 'numeric_sensitivity.json', 'extension_results.json',
              'combined_results.json', 'combined_numeric_sensitivity.json', 'convention_sensitivity.json']]
    path = ROOT / 'docs/MODEL_GRADING_RESULTS_V1.md'
    path.write_text('\n'.join(text) + '\n')
    print(path)


if __name__ == '__main__':
    main()
