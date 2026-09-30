"""Executive summary: hash-check pinned public releases and fail on unparsed selected rows."""
import ast
import hashlib
import json
from decimal import Decimal as D
from pathlib import Path

import pandas as pd

from .formulas import FORMULAS, numeric_answer, operands
from .types import Case

SOURCES = {
    'rlvr': {
        'dataset': 'coslinedev/financial-rlvr-10k-enterprise',
        'revision': '6cfa9a71e777026ba7242fbbb96c11c7dece5011',
        'path': 'literature/pdfs/financial-rlvr-10k-6cfa9a71.jsonl',
        'sha256': '86968a146a09e2ba1b19aac3a5ca2bec7e878358341a7972fddeb4b8cd7754af',
        'url': 'https://huggingface.co/datasets/coslinedev/financial-rlvr-10k-enterprise/resolve/6cfa9a71e777026ba7242fbbb96c11c7dece5011/financial_rlvr_10k_enterprise_verified.jsonl',
        'license': 'MIT',
    },
    'cosimo': {
        'dataset': 'btech-software/cosimo-cfa-frm-71k',
        'revision': '42244d29c6b9912683213a08d1a9c5b0373b381b',
        'path': 'literature/pdfs/cosimo-cfa-level-i.parquet',
        'sha256': 'afa7e9241e0f06df090916e289a8e39d7fc9c4245c3b21c0c0f1188edafb0abb',
        'url': 'https://huggingface.co/datasets/btech-software/cosimo-cfa-frm-71k/resolve/42244d29c6b9912683213a08d1a9c5b0373b381b/data/cfa_level_i-00000-of-00001.parquet',
        'license': 'MIT',
    },
}


def checked_path(name: str) -> Path:
    spec = SOURCES[name]
    path = Path(spec['path'])
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != spec['sha256']:
        raise ValueError(f'{name} source hash mismatch: {digest}')
    return path


def cosimo_cases() -> list[Case]:
    frame = pd.read_parquet(checked_path('cosimo'))
    result = []
    for row in frame.itertuples():
        family = row.metadata['generator']
        if family not in FORMULAS:
            continue
        formula, mutation, independent = FORMULAS[family](row.question)
        pair = row.preference_pair
        if not row.verified or not row.verification['answer_matches_recomputation']:
            raise ValueError(f'Unverified source row: {row.id}')
        requested = family == 'cr_eq_gordon'
        if requested and 'nearest whole unit' not in row.question:
            raise ValueError(f'Missing expected instruction: {row.id}')
        interval = None
        if family == 'port_capm':
            rf_, market, beta = operands(r'rf = ([\d.]+)%, E\(Rm\) = ([\d.]+)%, β = (\d+(?:\.\d+)?)', row.question)
            corners = [rf_ + (beta + shift) * (market - rf_)
                       for shift in [D('-.005'), D('.005')]]
            interval = min(corners), max(corners)
        result.append(Case('cosimo', family, row.id, row.question,
                           numeric_answer(row.answer), formula,
                           D(1) if requested else D('.01'), requested, mutation,
                           numeric_answer(pair['chosen']['answer']) if pair else None,
                           numeric_answer(pair['rejected']['answer']) if pair else None,
                           interval=interval, independent_formula=independent))
    if len(result) != len(FORMULAS) * 1000:
        raise ValueError(f'Unexpected selected Cosimo denominator: {len(result)}')
    return result


def literal_dcf(code: str) -> D:
    tree = ast.parse(code)
    matches = [node for node in tree.body if isinstance(node, ast.Assign)
               and isinstance(node.targets[0], ast.Tuple)
               and [item.id for item in node.targets[0].elts] == ['fcf', 'r', 'g']]
    if len(matches) != 1 or not isinstance(matches[0].value, ast.Tuple):
        raise ValueError('Unsupported source DCF operand assignment')
    values = [D(ast.get_source_segment(code, item)) for item in matches[0].value.elts]
    cash, rate, growth = values
    return cash / (rate - growth)


def rlvr_cases() -> list[Case]:
    result = []
    for line in checked_path('rlvr').open():
        row = json.loads(line)
        if row['domain'] != 'DCF Valuation' or row['is_edge_case']:
            continue
        cash, rate, growth = operands(
            r'FCF_1=\$([-\d,.]+), Discount Rate r=([-\d.]+)%, Growth Rate g=([-\d.]+)%',
            row['prompt'])
        delta = (rate - growth) / 100
        if delta <= D('.001'):
            raise ValueError('Nonfinite rounded-input interval')
        interval = cash / (delta + D('.001')), cash / (delta - D('.001'))
        result.append(Case('rlvr', 'dcf_terminal', row['id'], row['prompt'],
                           D(str(row['ground_truth'])), cash / delta, D('.0001'),
                           False, cash / (rate / 100), interval=interval,
                           hidden_formula=literal_dcf(row['code_solution'])))
    if len(result) != 2655:
        raise ValueError(f'Unexpected RLVR denominator: {len(result)}')
    return result
