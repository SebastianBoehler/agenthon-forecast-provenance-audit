"""Executive summary: independently verify prospective splits and finance targets.

All financial calculations use exact Fraction arithmetic. No primary benchmark,
formula, selection, oracle, parser, optimizer or upstream generator is imported.
This is AI-assisted technical validation, not expert human semantic adjudication.
"""
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal as D
from fractions import Fraction as F
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'outputs/finance-adaptation-v1'
OUT = DATA / 'independent'
FAMILIES = ('cr_eq_gordon', 'deriv_binomial_call', 'eq_gordon', 'corp_wacc')
COUNTS = {'train': 8, 'dev': 8, 'test-source': 12, 'preflight': 4}
SALT = 'finance-adaptation-v1-20260929'
SOURCE_SHA = 'afa7e9241e0f06df090916e289a8e39d7fc9c4245c3b21c0c0f1188edafb0abb'
PRIOR_SHA = '75c5b694db2d9a174e089c594e3f756867e0f840f12ac4634e5dc20173acf0cc'
ORIGINAL_CHECKPOINT = '51c753e90ce0bff459c88d4580275eb847b1dab5f73ee088ff1696ceafa5712a'
N = r'([0-9][0-9,]*(?:\.[0-9]+)?)'
EPSILON, GUARD = F(1, 10**42), F(1, 10**20)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_text(value):
    return hashlib.sha256(value.encode()).hexdigest()


def read(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def extract(pattern, text):
    match = re.search(pattern, text)
    assert match, (pattern, text)
    return tuple(F(x.replace(',', '')) for x in match.groups())


def source_operands(family, prompt):
    if family in ('cr_eq_gordon', 'eq_gordon'):
        pattern = rf'D0 = \${N}, growth g = {N}%, required return r = {N}%'
    elif family == 'deriv_binomial_call':
        pattern = rf'S0={N}, u={N}, d={N}, K={N}, rf={N}%'
    else:
        pattern = (rf'market equity {N}, market debt {N}, cost of equity {N}%, '
                   rf'cost of debt {N}%, and a marginal tax rate {N}%')
    return extract(pattern, prompt)


def transfer_operands(row):
    q, family = row['prompt'], row['family']
    if family in ('cr_eq_gordon', 'eq_gordon'):
        assert 'annual' in q and ('paid' in q or 'completed dividend payment' in q)
        assert 'next' in q or 'Gordon' in q
        assert ('whole currency unit' in q) == (family == 'cr_eq_gordon')
        return tuple(F(x) for x in re.findall(N, q.split('Round to the nearest')[0]))
    if family == 'corp_wacc':
        assert 'market' in q and ('deductible' in q or 'tax shield' in q)
        assert 'percentage points' in q and '0.01' in q
        values = re.findall(N, q)
        assert values[-1] == '0.01'
        return tuple(F(x) for x in values[:-1])
    assert 'European' in q and ('no dividends' in q or 'non-dividend-paying' in q)
    assert 'one period' in q or 'one step' in q
    assert '0.01 currency' in q
    index = int(row['template_id'].rsplit(':', 1)[-1])
    if index == 1:
        s = extract(rf'currently costs {N} currency', q)[0]
        s1, u, s2, d = extract(rf'either {N} times {N} or {N} times {N}', q)
        k, r = extract(rf'strike is {N} currency.*?effective {N}%', q)
        assert s == s1 == s2 and extract(rf'gross factor 1 \+ {N}/100', q)[0] == r
    elif index == 2:
        s, u, d, k = extract(rf'priced at {N} currency.*?multiplier of {N}.*?multiplier of {N}.*?end for {N} currency', q)
        r = extract(rf'effective risk-free rate for this one step is {N}%', q)[0]
        assert 'not a continuously compounded rate' in q
    else:
        s, u, d, k, r = extract(rf'trades for {N} currency.*?factors are {N} and {N}.*?expiry is {N} currency.*?earn exactly {N}%', q)
        assert extract(rf'becomes 1 \+ {N}/100', q)[0] == r
    return s, u, d, k, r


def formula(family, values):
    if family in ('cr_eq_gordon', 'eq_gordon'):
        dividend, growth, rate = values
        assert dividend > 0 and rate > growth
        return dividend * (100 + growth) / (rate - growth), {}
    if family == 'corp_wacc':
        equity, debt, re_, rd, tax = values
        assert equity > 0 and debt > 0 and 0 <= tax <= 100
        value = (equity * re_ + debt * rd * (1 - tax / 100)) / (equity + debt)
        assert min(re_, rd * (1 - tax / 100)) <= value <= max(re_, rd * (1 - tax / 100))
        return value, {'weights_sum_to_one': True, 'unit': 'percentage points'}
    spot, up, down, strike, rate = values
    gross = 1 + rate / 100
    assert spot > 0 and down < gross < up
    su, sd = spot * up, spot * down
    cu, cd = max(su - strike, F(0)), max(sd - strike, F(0))
    delta = (cu - cd) / (su - sd)
    bond = (cu - delta * su) / gross
    value = delta * spot + bond
    q = (gross - down) / (up - down)
    assert delta * su + bond * gross == cu and delta * sd + bond * gross == cd
    assert value == (q * cu + (1 - q) * cd) / gross
    assert max(spot - strike / gross, 0) <= value <= spot
    return value, {'replication_and_expectation_agree': True, 'financing_debt': str(-bond)}


def nearest(value, quantum):
    scaled = value / quantum
    lower = scaled.numerator // scaled.denominator
    return quantum * (lower + int(scaled - lower >= F(1, 2)))


def check_row(row):
    family, whole = row['family'], row['family'] == 'cr_eq_gordon'
    values = (transfer_operands(row) if row['partition'] == 'test-transfer'
              else source_operands(family, row['prompt']))
    assert values == tuple(F(x) for x in row['operands']), row['case_id']
    assert hash_text(row['prompt']) == row['question_hash']
    normalized = tuple(format(D(x).normalize(), 'f') for x in row['operands'])
    assert hash_text(json.dumps(normalized)) == row['operand_hash']
    value, identities = formula(family, values)
    assert abs(F(row['formula']) - value) <= EPSILON, row['case_id']
    assert row['requested_rounding'] == whole and F(row['quantum']) == (1 if whole else F(1, 100))
    assert row['unit'] == ('percent' if family == 'corp_wacc' else 'currency')
    assert row['semantics'] == 'exact_displayed_inputs; effective_single_period_binomial_rate'
    target, tie = (nearest(value, F(1)), value.denominator == 2) if whole else (value, False)
    assert abs(F(row['target']) - target) <= EPSILON
    allowed = {target, target - 1} if tie else {target}
    if whole:
        assert set(map(F, row['admissible_values'])) == allowed and not row['admissible_intervals']
    else:
        assert not row['admissible_values'] and len(row['admissible_intervals']) == 1
        low, high = map(F, row['admissible_intervals'][0])
        assert abs(low - (value - F(1, 200) - GUARD)) <= EPSILON
        assert abs(high - (value + F(1, 200) + GUARD)) <= EPSILON
    gold_valid = None
    if 'source_gold' in row:
        gold = F(row['source_gold'])
        gold_valid = gold in allowed if whole else abs(gold - value) <= F(1, 200) + GUARD
    passing = 'source_gold' in row and family in ('eq_gordon', 'corp_wacc')
    repaired = set(map(F, row['repaired_objective_targets']))
    expected = {F(row['source_gold'])} if passing else (allowed if whole else {nearest(value, F(1, 100))})
    assert repaired == expected and (not passing or gold_valid)
    return {'case_id': row['case_id'], 'partition': row['partition'], 'family': family,
            'formula': str(value), 'target': str(target), 'operands': list(map(str, values)),
            'half_tie': tie, 'source_gold_valid': gold_valid, 'identities': identities}


def main():
    source = ROOT / 'literature/pdfs/cosimo-cfa-level-i.parquet'
    prior_path = ROOT / 'outputs/model-grading-v1/selection.jsonl'
    assert sha(source) == SOURCE_SHA and sha(prior_path) == PRIOR_SHA
    original = ROOT / 'outputs/model-grading-review/independent-response-summary.json'
    assert sha(original) == ORIGINAL_CHECKPOINT
    rows = {name: read(DATA / f'{name}.jsonl') for name in (*COUNTS, 'test-transfer')}
    for name, count in (*COUNTS.items(), ('test-transfer', 6)):
        assert Counter(r['family'] for r in rows[name]) == {f: count for f in FAMILIES}
        assert all(r['partition'] == name for r in rows[name])
    public = [r for r in pd.read_parquet(source).to_dict('records') if r['metadata']['generator'] in FAMILIES]
    by_id = {r['id']: r for r in public}
    prior = read(prior_path)
    seen_q = {hash_text(r['prompt']) for r in prior}
    seen_v = {source_operands(r['family'], r['prompt']) for r in prior}
    conflicts, unique_counts = [], {}
    for family in FAMILIES:
        grouped, labels = {}, defaultdict(set)
        for row in sorted(public, key=lambda r: r['id']):
            if row['metadata']['generator'] == family:
                grouped.setdefault(row['question'], row)
                labels[row['question']].add(row['answer'])
        unique_counts[family] = len(grouped)
        conflicts.extend(q for q, labels_ in labels.items() if len(labels_) > 1)
        selected = []
        for row in sorted(grouped.values(), key=lambda r: (hash_text(SALT + r['question']), r['id'])):
            qhash, values = hash_text(row['question']), source_operands(family, row['question'])
            if qhash not in seen_q and values not in seen_v:
                seen_q.add(qhash)
                seen_v.add(values)
                selected.append(row['id'])
                if len(selected) == sum(COUNTS.values()):
                    break
        actual = [r['case_id'] for name in COUNTS for r in rows[name] if r['family'] == family]
        assert selected == actual, family
    manifest = json.loads((DATA / 'preparation_manifest.json').read_text())
    assert unique_counts == manifest['source_unique_prompts'] and not conflicts
    all_source_values = {source_operands(r['metadata']['generator'], r['question']) for r in public}
    all_rows = [r for subset in rows.values() for r in subset]
    assert len({r['question_hash'] for r in all_rows}) == len({r['operand_hash'] for r in all_rows}) == 152
    assert not {r['question_hash'] for r in all_rows} & {r['question_hash'] for r in prior}
    assert not {tuple(map(F, r['operands'])) for r in all_rows} & {source_operands(r['family'], r['prompt']) for r in prior}
    checks = []
    for row in all_rows:
        if row['partition'] == 'test-transfer':
            assert 'source_gold' not in row and row['provenance']['kind'] == 'researcher_authored'
            assert tuple(map(F, row['operands'])) not in all_source_values | seen_v
        else:
            public_row = by_id[row['case_id']]
            assert row['prompt'] == public_row['question']
            tokens = re.findall(r'-?[0-9][0-9,]*(?:\.[0-9]+)?', public_row['answer'])
            assert len(tokens) == 1 and F(tokens[0].replace(',', '')) == F(row['source_gold'])
        checks.append(check_row(row))
    template_counts = Counter(r['template_id'] for r in rows['test-transfer'])
    assert len(template_counts) == 12 and set(template_counts.values()) == {2}
    OUT.mkdir(exist_ok=True)
    result = {'status': 'PASS', 'executed_utc': datetime.now(timezone.utc).isoformat(),
              'method': 'independent direct-parquet selection and exact Fraction calculations; AI technical review only',
              'cases': len(checks), 'partition_counts': {k: len(v) for k, v in rows.items()},
              'unique_source_prompts': unique_counts, 'duplicate_label_conflicts': 0,
              'prompt_and_operand_overlap': 0, 'transfer_source_operand_overlap': 0,
              'half_ties': sum(r['half_tie'] for r in checks),
              'source_invalid_by_partition_family': {name: dict(Counter(r['family'] for r in checks if r['partition'] == name and r['source_gold_valid'] is False)) for name in COUNTS},
              'template_counts': dict(template_counts), 'rows': checks,
              'input_sha256': {str((DATA / f'{name}.jsonl').relative_to(ROOT)): sha(DATA / f'{name}.jsonl') for name in rows},
              'source_sha256': sha(source), 'prior_selection_sha256': sha(prior_path),
              'original600_checkpoint_sha256': sha(original), 'script_sha256': sha(Path(__file__)),
              'preparation_manifest_sha256': sha(DATA / 'preparation_manifest.json')}
    (OUT / 'benchmark_validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
