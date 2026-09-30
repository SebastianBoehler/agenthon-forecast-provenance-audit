"""Executive summary: regenerate standalone paper tables and model summaries from saved results."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'paper/answer_contract_audit.tex'
MODELS = {'qwen3-1.7b': 'Qwen3 1.7B', 'qwen3-4b': 'Qwen3 4B',
          'qwen2.5-coder-3b': 'Qwen2.5-Coder 3B',
          'deepseek-v3.2': 'DeepSeek V3.2'}
FAMILIES = {
    'cr_eq_gordon': ('constructed Gordon', 'Explicit output rounding'),
    'deriv_binomial_call': ('binomial call', 'Incorrect financial quantity'),
    'port_capm': ('CAPM', 'Hidden beta precision$^*$'),
    'eq_gordon': ('ordinary Gordon', 'Matched'),
    'corp_wacc': ('WACC', 'Matched'), 'm_corp_wacc': ('MCQ WACC', 'Matched numerically'),
    'tvm_annuity_fv': ('annuity FV', 'Matched'),
    'v_tvm_annuity_fv': ('vignette annuity FV', 'Matched'),
    'tvm_pv_lump': ('lump-sum PV', 'Matched'), 'tvm_eay': ('effective annual rate', 'Matched'),
}


def replace_block(source, name, content):
    pattern = rf'(% BEGIN GENERATED {name}\n).*?(% END GENERATED {name})'
    result, count = re.subn(pattern, lambda m: m[1] + content + '\n' + m[2], source, flags=re.S)
    if count != 1:
        raise ValueError(f'Expected one generated {name} block, found {count}')
    return result


def numbers(row):
    return (f"{row['valid_answer_rejected']}/{row['valid_answer_count']:,}",
            f"{row['source_invalid_rejected_accepted']}/{row['source_rejected_invalid']}")


def reference_blocks(results):
    census = []
    for family, (label, interpretation) in FAMILIES.items():
        row = results['families'][f'cosimo/{family}']
        census.append(f"Cosimo: {label} & {row['rows']:,} & {row['unique_questions']:,} & "
                      f"{row['gold_invalid_exact_contract']:,} & {interpretation}\\\\")
    row = results['families']['rlvr/dcf_terminal']
    census.append(f"RLVR: ordinary DCF & {row['rows']:,} & {row['unique_questions']:,} & "
                  f"{row['gold_invalid_exact_contract']:,} & Hidden rate precision$^*$\\\\")
    keys = ['cosimo/cr_eq_gordon', 'cosimo/deriv_binomial_call']
    comparators = []
    for label, index in [('Original label, $\\pm0.005$', 2),
                         ('Original label, $\\pm0.5$', 3), ('Original label, 5\\%', 7)]:
        rows = [results['comparators'][key][index] for key in keys]
        comparators.append(label + ' & ' + ' & '.join(n for r in rows for n in numbers(r)) + '\\\\')
    formula = [results['repairs'][key][0] for key in keys]
    complete = [results['repairs'][key][1] for key in keys]
    integer = results['simple_integer_baseline']
    comparators.extend([
        'Visible formula only & ' + ' & '.join(n for r in formula for n in numbers(r)) + '\\\\',
        'Integer + original $\\pm0.5$ & ' + ' & '.join(numbers(integer)) + ' & --- & ---\\\\',
        'Complete numeric contract & ' + ' & '.join(n for r in complete for n in numbers(r)) + '\\\\',
    ])
    return {'CENSUS': '\n'.join(census), 'COMPARATORS': '\n'.join(comparators)}


def model_rows(strict, numeric, conventions):
    rows = []
    for family in ['cr_eq_gordon', 'deriv_binomial_call', 'eq_gordon', 'corp_wacc']:
        label = FAMILIES[family][0].capitalize()
        rows.append(f'\\multicolumn{{8}}{{l}}{{\\emph{{{label}: 50 distinct questions}}}}\\\\')
        for key, model in MODELS.items():
            primary = strict['models'][key]['families'][family]
            row = numeric['models'][key]['families'][family]
            policies = row['policies']
            robust = conventions['numeric_models'][key]['families'][family]['visible_valid']
            counts = [primary['parsed_completed'], row['parsed_completed'], row['visible_valid'], robust,
                      policies['source_abs_0.005']['valid_rejected'],
                      policies['source_relative_5pct']['valid_rejected'],
                      policies['source_relative_5pct']['numeric_invalid_accepted']]
            rows.append(model + ' & ' + ' & '.join(str(n) for n in counts) + '\\\\')
    return '\n'.join(rows)


def model_summary(strict, numeric):
    def pairs(results, field):
        return ', '.join(str(results['models'][key]['aggregate'][field]) for key in MODELS)
    deepseek = numeric['models']['deepseek-v3.2']['aggregate']
    cent = deepseek['policies']['source_abs_0.005']['valid_rejected']
    relative = deepseek['policies']['source_relative_5pct']['valid_rejected']
    cost = strict['api_reported_cost_usd']
    primary = strict['models']['deepseek-v3.2']['aggregate']
    small_gordon = numeric['models']['qwen3-1.7b']['families']['cr_eq_gordon']
    deep_gordon = numeric['models']['deepseek-v3.2']['families']['cr_eq_gordon']
    strict_rejected = primary['policies']['source_abs_0.005']['valid_rejected']
    strict_families = strict['models']['deepseek-v3.2']['families']
    denials = {family: row['policies']['source_abs_0.005']['valid_rejected']
               for family, row in strict_families.items()}
    assert sum(denials.values()) == strict_rejected
    return (
        f'The complete panel contains {strict["responses"]} responses to {strict["questions"]} questions. '
        f'In roster order (Qwen3 1.7B, Qwen3 4B, Qwen2.5-Coder 3B, DeepSeek), '
        f'{pairs(strict, "parsed_completed")} of 200 responses meet the strict final-line format, '
        f'and {pairs(strict, "visible_valid")} meet its numerical contract. '
        f'The exploratory extraction recovers {pairs(numeric, "parsed_completed")} final scalars, '
        f'of which {pairs(numeric, "visible_valid")} are numerically valid. '
        f'Table~\\ref{{tab:models}} reports failures and grader disagreement by family. '
        f'Formatting substantially limits model comparisons: the strict endpoint jointly measures '
        f'final-line compliance and numerical validity. Even exploratory recovery misses many 4B '
        f'answers ending in punctuation such as ``dollars.\'\'; an unparsed answer is not a '
        f'demonstrated arithmetic error. These counts cannot rank latent financial ability or '
        f'isolate a causal effect of model size.\n'
        f'For DeepSeek, reconstructed original-label $\\pm0.005$ grading rejects {strict_rejected} of '
        f'{primary["visible_valid"]} numerically valid strict-format answers. '
        f'These are {denials["deriv_binomial_call"]} wrong-quantity and '
        f'{denials["cr_eq_gordon"]} rounding denials; the passing ordinary-Gordon and WACC '
        f'families contribute {denials["eq_gordon"] + denials["corp_wacc"]}. '
        f'Exploratory recovery increases that count to {cent} of '
        f'{deepseek["visible_valid"]} numerically valid recovered answers; widening to 5\\% still rejects '
        f'{relative}. These are paired decisions on unchanged answers, not different inference runs '
        f'or effects of training on repaired data. '
        f'On constructed Gordon, source-cent grading credits '
        f'{small_gordon["policies"]["source_abs_0.005"]["accepted"]}/50 Qwen3 1.7B answers versus '
        f'{deep_gordon["policies"]["source_abs_0.005"]["accepted"]}/50 DeepSeek answers; '
        f'the integer contract instead validates {small_gordon["visible_valid"]}/50 and '
        f'{deep_gordon["visible_valid"]}/50. This reverses their ordering on this family and '
        f'exploratory extraction endpoint, with no response changed. '
        f'The API reported \\${cost:.5f} in usage cost. '
        f'The local models use existing caches; the study does not estimate deployment economics.\n'
        f'DeepSeek\'s only numerical mismatch uses continuous compounding (\\(e^{{0.05}}\\)) '
        f'where the declared reference uses \\(1.05\\). Its final 3.06 agrees with that alternative convention; '
        f'the reference gives \\(64/21\\). The prompt leaves compounding implicit, so this is a '
        f'convention mismatch rather than an unequivocal arithmetic error. The source label 12.95 '
        f'remains incompatible with both call-price conventions.'
    )


def abstract_models(strict):
    primary = strict['models']['deepseek-v3.2']['aggregate']
    strict_rejected = primary['policies']['source_abs_0.005']['valid_rejected']
    return (f'Grading {strict["responses"]} unchanged answers from four models, reconstructed original-label '
            f'cent-level scoring rejects {strict_rejected} of {primary["visible_valid"]} DeepSeek answers '
            f'satisfying the strict final-line and numerical contract.')


def convention_summary(conventions):
    additions = ', '.join(str(conventions['numeric_models'][key]['continuous_only_added']) for key in MODELS)
    source = conventions['source_binomial']
    robust = conventions['strict_models']['deepseek-v3.2']['aggregate']
    denials = robust['policies']['source_abs_0.005']['valid_rejected']
    return (f'Accepting either simple or continuous compounding adds {additions} numerically compatible answers '
            f'in the same roster order. This separately recorded post hoc sensitivity leaves all '
            f'{source["either_invalid"]} source binomial conflicts intact; the {source["both"]} '
            f'source labels compatible with both conventions are zero-price cases. '
            f'Under this union, reconstructed cent-label grading denies {denials} of '
            f'{robust["visible_valid"]} numerically compatible strict-format DeepSeek answers. '
            f'The acceptance set is the union of two cent neighborhoods, not the interval between the prices. '
            f'Textual mentions of exponential discounting are descriptive evidence, not an acceptance prerequisite.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    source = PAPER.read_text()
    results = json.loads((ROOT / 'outputs/answer-contract-v1/results.json').read_text())
    blocks = reference_blocks(results)
    if '% BEGIN GENERATED MODELS' in source:
        directory = ROOT / 'outputs/model-grading-v1'
        strict = json.loads((directory / 'combined_results.json').read_text())
        numeric = json.loads((directory / 'combined_numeric_sensitivity.json').read_text())
        conventions = json.loads((directory / 'convention_sensitivity.json').read_text())
        blocks['MODELS'] = model_rows(strict, numeric, conventions)
        blocks['MODEL_SUMMARY'] = model_summary(strict, numeric)
        blocks['ABSTRACT_MODELS'] = abstract_models(strict)
        blocks['CONVENTIONS'] = convention_summary(conventions)
    rendered = source
    for name, content in blocks.items():
        rendered = replace_block(rendered, name, content)
    if args.check and rendered != source:
        raise ValueError('Paper tables or model summaries differ from saved results')
    if not args.check:
        PAPER.write_text(rendered)
    print('Standalone paper tables and model summaries agree with saved results')


if __name__ == '__main__':
    main()
