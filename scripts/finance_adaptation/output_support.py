"""Executive summary: independently parse saved answers and reconstruct assigned feedback.

Financial references are the frozen prereview's exact Fraction values. No primary
oracle, parser, optimizer, or financial implementation is imported or executed.
"""
import ast
import hashlib
import importlib.metadata
import json
import re
from collections import Counter
from decimal import Decimal as D, InvalidOperation
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'outputs/finance-adaptation-v1'
FINAL = re.compile(r'FINAL: ([+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][+-]?\d+)?) (currency|percent)', re.I)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return [json.loads(x) for x in path.read_text().splitlines()]


def literals(path, names):
    return {node.targets[0].id: ast.literal_eval(node.value)
            for node in ast.parse(path.read_text()).body
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id in names}


def verify_freeze():
    assert digest(DATA / 'freeze.json') == '2b4728f21b4890b6bdf9ebb33dd89c9b83c105d6de021beb3435343e4bdddd24'
    freeze = json.loads((DATA / 'freeze.json').read_text())
    assert len(freeze['frozen_sha256']) == 34
    for name, checksum in freeze['frozen_sha256'].items():
        assert digest(ROOT / name) == checksum, name
    dependencies = json.loads((DATA / 'dependency_manifest.json').read_text())
    assert len(dependencies['source_sha256']) == 81
    distribution = importlib.metadata.distribution('gepa')
    assert distribution.version == dependencies['gepa_version'] == freeze['gepa_version'] == '0.1.1'
    for name, checksum in dependencies['source_sha256'].items():
        assert digest(distribution.locate_file(name)) == checksum, name
    return freeze, {'frozen_files': len(freeze['frozen_sha256']),
                    'gepa_source_files': len(dependencies['source_sha256']),
                    'freeze_sha256': digest(DATA / 'freeze.json')}


def parse(text, family, finish):
    lines = [s.strip() for s in text.splitlines() if s.strip()]
    if len(re.findall('FINAL:', text, re.I)) != 1 or not lines:
        value, error = None, 'missing_or_nonfinal_marker'
    else:
        match = FINAL.fullmatch(lines[-1])
        if match is None:
            value, error = None, 'invalid_final_format'
        elif match[2].lower() != ('percent' if family == 'corp_wacc' else 'currency'):
            value, error = None, 'wrong_unit'
        else:
            try:
                value = D(match[1].replace(',', ''))
                error = None if value.is_finite() else 'nonfinite_answer'
                if error:
                    value = None
            except InvalidOperation:
                value, error = None, 'invalid_decimal'
    return (value, error) if finish == 'stop' else (None, finish)


def score(row, exact, record):
    value, error = parse(record['text'], row['family'], record['finish_reason'])
    financial = source = repaired = False
    if value is not None:
        candidate, formula = F(value), F(exact['formula'])
        if row['family'] == 'cr_eq_gordon':
            financial = candidate.denominator == 1 and abs(candidate - formula) <= F(1, 2)
        else:
            financial = abs(candidate - formula) <= F(1, 200) + F(1, 10**20)
        if 'source_gold' in row:
            source = abs(candidate - F(row['source_gold'])) <= F(1, 200)
        repaired = any(abs(candidate - F(x)) <= F(1, 200) for x in row['repaired_objective_targets'])
        if row['family'] == 'cr_eq_gordon':
            repaired = repaired and candidate.denominator == 1
    result = {'value': str(value) if value is not None else None, 'parse_error': error,
              'financial_valid': financial,
              'source_reward': source if 'source_gold' in row else None,
              'repaired_reward': repaired}
    for key, actual in result.items():
        assert record[key] == actual, (row['case_id'], key, record[key], actual)
    if row['family'] in ('eq_gordon', 'corp_wacc') and 'source_gold' in row:
        assert source == repaired
    return result


def summarize(rows):
    return {'attempts': len(rows), 'parsed': sum(r['value'] is not None for r in rows),
            'financial_valid': sum(r['financial_valid'] for r in rows),
            'source_accepted': sum(bool(r['source_reward']) for r in rows) if rows and rows[0]['source_reward'] is not None else None,
            'repaired_accepted': sum(r['repaired_reward'] for r in rows),
            'rounding_violations': sum(r['family'] == 'cr_eq_gordon' and r['value'] is not None and F(r['value']).denominator != 1 for r in rows),
            'wrong_quantity_source_credited': sum(r['family'] == 'deriv_binomial_call' and bool(r['source_reward']) and not r['financial_valid'] for r in rows),
            'parse_errors': dict(Counter(r['parse_error'] for r in rows if r['parse_error']))}


def feedback(row, record, objective):
    return {'Inputs': row['prompt'], 'Generated Outputs': record['text'],
            'Feedback': {'reward': int(record[objective + '_reward']),
                         'target_values': [row['source_gold']] if objective == 'source' else row['repaired_objective_targets'],
                         'absolute_tolerance': '0.005',
                         'integer_required': objective == 'repaired' and row['family'] == 'cr_eq_gordon',
                         'format_error': record['parse_error']}}


def render(value, level=3):
    if isinstance(value, dict):
        return ''.join('#' * level + ' ' + k + '\n' + render(v, min(level + 1, 6)) for k, v in value.items())
    if isinstance(value, list):
        return ''.join('#' * level + f' Item {i + 1}\n' + render(v, min(level + 1, 6)) for i, v in enumerate(value))
    return str(value).strip() + '\n\n'


def reflection_template():
    distribution = importlib.metadata.distribution('gepa')
    path = distribution.locate_file('gepa/strategies/instruction_proposal.py')
    cls = next(n for n in ast.parse(path.read_text()).body if isinstance(n, ast.ClassDef))
    node = next(n for n in cls.body if isinstance(n, ast.Assign) and n.targets[0].id == 'default_prompt_template')
    return ast.literal_eval(node.value)


def reflection_prompt(records, questions, objective, template):
    samples = [feedback(questions[r['case_id']], r, objective) for r in records]
    side = '\n\n'.join(f'# Example {i + 1}\n' + ''.join('## ' + k + '\n' + render(v) for k, v in sample.items()) for i, sample in enumerate(samples))
    return template.replace('<curr_param>', records[0]['strategy']).replace('<side_info>', side)
