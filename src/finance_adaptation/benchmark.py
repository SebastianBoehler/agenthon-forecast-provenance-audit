"""Executive summary: prepare disjoint questions and keep authored targets source-free."""
import hashlib
import json
from collections import defaultdict
from decimal import Decimal as D, ROUND_HALF_UP, localcontext

from answer_contract.formulas import FORMULAS, NUM, operands
from answer_contract.sources import SOURCES, cosimo_cases
from answer_contract.types import Case
from model_grading.protocol import FAMILIES, frozen_selection, question_hash

from .transfer import INPUTS, transfer_prompt

SALT = 'finance-adaptation-v1-20260929'
COUNTS = {'train': 8, 'dev': 8, 'test-source': 12, 'preflight': 4}
PATTERNS = {
    'gordon': rf'D0 = \${NUM}, growth g = {NUM}%, required return r = {NUM}%',
    'deriv_binomial_call': rf'S0={NUM}, u={NUM}, d={NUM}, K={NUM}, rf={NUM}%',
    'corp_wacc': (rf'market equity {NUM}, market debt {NUM}, cost of equity '
                  rf'{NUM}%, cost of debt {NUM}%, and a marginal tax rate {NUM}%'),
}


def canonical_values(values) -> tuple[str, ...]:
    return tuple(format(D(v).normalize(), 'f') for v in values)


def source_operands(family: str, prompt: str) -> tuple[str, ...]:
    key = 'gordon' if family in ('cr_eq_gordon', 'eq_gordon') else family
    return canonical_values(operands(PATTERNS[key], prompt))


def operand_hash(values) -> str:
    return hashlib.sha256(json.dumps(canonical_values(values)).encode()).hexdigest()


def admissible_values(case: Case) -> list[str]:
    if not case.requested_rounding:
        return []
    values = [case.target]
    if abs(case.formula - case.target) == D('.5'):
        values.append(case.target - 1 if case.target > case.formula else case.target + 1)
    return sorted(str(value) for value in values)


def grade_numeric(row: dict, value: D) -> bool:
    if not value.is_finite():
        return False
    if row['admissible_values']:
        return value in {D(x) for x in row['admissible_values']}
    return any(D(lo) <= value <= D(hi) for lo, hi in row['admissible_intervals'])


def record(case: Case, values, partition: str, template_id: str) -> dict:
    allowed = admissible_values(case)
    tolerance = case.quantum / 2 + D('1e-20')
    row = {
        'case_id': case.case_id, 'family': case.family, 'partition': partition,
        'prompt': case.prompt, 'question_hash': question_hash(case.prompt),
        'operands': canonical_values(values), 'operand_hash': operand_hash(values),
        'formula': str(case.formula), 'target': str(case.target),
        'quantum': str(case.quantum), 'requested_rounding': case.requested_rounding,
        'unit': 'percent' if case.family == 'corp_wacc' else 'currency',
        'template_id': template_id, 'admissible_values': allowed,
        'admissible_intervals': ([] if allowed else
                                [[str(case.formula - tolerance),
                                  str(case.formula + tolerance)]]),
        'semantics': 'exact_displayed_inputs; effective_single_period_binomial_rate',
    }
    if case.source == 'cosimo':
        row['source_gold'] = str(case.gold)
        row['provenance'] = {'kind': 'released_source', 'release': SOURCES['cosimo']}
    else:
        row['provenance'] = {'kind': 'researcher_authored',
                             'target_basis': 'independent_financial_formula'}
    if not grade_numeric(row, case.target):
        raise ValueError(f'Materialized target fails its contract: {case.case_id}')
    if case.source == 'cosimo' and case.family in ('eq_gordon', 'corp_wacc'):
        if not grade_numeric(row, case.gold):
            raise ValueError(f'Passing-family source target is invalid: {case.case_id}')
        row['repaired_objective_targets'] = [str(case.gold)]
    else:
        row['repaired_objective_targets'] = (allowed or
            [str(case.formula.quantize(case.quantum, rounding=ROUND_HALF_UP))])
    return row


def canonical_prompt(family: str, values: tuple[str, ...]) -> str:
    if family in ('cr_eq_gordon', 'eq_gordon'):
        return f'D0 = ${values[0]}, growth g = {values[1]}%, required return r = {values[2]}%'
    if family == 'deriv_binomial_call':
        return (f'S0={values[0]}, u={values[1]}, d={values[2]}, '
                f'K={values[3]}, rf={values[4]}%')
    if family == 'corp_wacc':
        return (f'market equity {values[0]}, market debt {values[1]}, '
                f'cost of equity {values[2]}%, cost of debt {values[3]}%, '
                f'and a marginal tax rate {values[4]}%')
    raise ValueError(f'Unsupported family: {family}')


def build_benchmark() -> tuple[dict[str, list[dict]], dict]:
    with localcontext() as context:
        context.prec = 50
        prior = frozen_selection()
        seen_prompts = {row['question_hash'] for row in prior}
        seen_operands = {operand_hash(source_operands(row['family'], row['prompt']))
                         for row in prior}
        cases = [case for case in cosimo_cases() if case.family in FAMILIES]
        all_source_operands = {operand_hash(source_operands(c.family, c.prompt))
                               for c in cases}
        grouped = defaultdict(dict)
        prompt_groups = defaultdict(list)
        for case in sorted(cases, key=lambda c: c.case_id):
            grouped[case.family].setdefault(case.prompt, case)
            prompt_groups[case.prompt].append(case)
        duplicate_conflicts = [
            {'question_hash': question_hash(prompt),
             'case_ids': [case.case_id for case in duplicates],
             'source_golds': sorted({str(case.gold) for case in duplicates})}
            for prompt, duplicates in prompt_groups.items()
            if len({case.gold for case in duplicates}) > 1]
        result = {name: [] for name in (*COUNTS, 'test-transfer')}
        for family in FAMILIES:
            ranked = sorted(grouped[family].values(),
                            key=lambda c: (question_hash(SALT + c.prompt), c.case_id))
            available = []
            for case in ranked:
                qhash = question_hash(case.prompt)
                values = source_operands(family, case.prompt)
                ohash = operand_hash(values)
                if qhash in seen_prompts or ohash in seen_operands:
                    continue
                seen_prompts.add(qhash)
                seen_operands.add(ohash)
                available.append((case, values))
                if len(available) == sum(COUNTS.values()):
                    break
            if len(available) != sum(COUNTS.values()):
                raise ValueError(f'Insufficient disjoint questions for {family}')
            cursor = 0
            for partition, count in COUNTS.items():
                for case, values in available[cursor:cursor + count]:
                    result[partition].append(record(case, values, partition,
                                                    f'source:{family}'))
                cursor += count
        for family in FAMILIES:
            for index, values in enumerate(INPUTS[family]):
                if operand_hash(values) in all_source_operands | seen_operands:
                    raise ValueError(f'Transfer inputs are not new: {family}/{index}')
                prompt = transfer_prompt(family, values, index // 2)
                if question_hash(prompt) in seen_prompts:
                    raise ValueError('Transfer prompt duplicates an existing question')
                formula, mutation, independent = FORMULAS[family](canonical_prompt(family, values))
                if independent is not None and abs(independent - formula) > D('1e-40'):
                    raise ValueError('Primary finance derivations disagree')
                case = Case('researcher_authored', family, f'transfer-{family}-{index + 1:02d}',
                            prompt, formula, formula,
                            D(1) if family == 'cr_eq_gordon' else D('.01'),
                            family == 'cr_eq_gordon', mutation,
                            independent_formula=independent)
                result['test-transfer'].append(record(case, values, 'test-transfer',
                                                      f'authored:{family}:{index // 2 + 1}'))
                seen_prompts.add(question_hash(prompt))
                seen_operands.add(operand_hash(values))
        return result, {'prior_excluded_questions': len(prior),
                        'source_rows': len(cases),
                        'source_unique_prompts': {family: len(grouped[family]) for family in FAMILIES},
                        'duplicate_prompt_label_conflicts': duplicate_conflicts,
                        'selection_salt': SALT,
                        'selection_rule': 'salted question SHA256, then case ID; '
                                          'exclude prior/all-split prompts and operand tuples',
                        'partition_counts': {name: len(rows) for name, rows in result.items()}}
