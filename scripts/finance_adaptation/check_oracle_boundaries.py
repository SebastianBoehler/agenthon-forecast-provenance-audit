"""Executive summary: exercise the actual oracle API on independently specified edges.

These synthetic cases test software behavior; they are not experimental questions
or empirical observations. The separate Fraction validator imports no primary code.
No inference, benchmark mutation or upstream generator execution occurs here.
"""
import hashlib
import json
import sys
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))

from answer_contract.types import Case
from finance_adaptation.adapter import rewards
from finance_adaptation.benchmark import admissible_values, grade_numeric
from model_grading.protocol import parse_final


def main():
    # D0=1, growth=0%, return=8% gives exactly12.5 under the Gordon model.
    case = Case('synthetic_test', 'cr_eq_gordon', 'synthetic-half-tie', '',
                D('12.50'), D('12.5'), D('1'), True, D('0'))
    allowed = admissible_values(case)
    assert set(map(D, allowed)) == {D(12), D(13)}
    whole = {'family': 'cr_eq_gordon', 'admissible_values': allowed,
             'admissible_intervals': [], 'source_gold': '12.50',
             'repaired_objective_targets': allowed}
    for candidate in ('12', '13'):
        result = rewards(whole, f'FINAL: {candidate}.0000 currency', 'stop')
        assert result['financial_valid'] and result['repaired_reward']
        assert not result['source_reward']
    for candidate in ('11', '14', '12.004', '12.5'):
        assert not grade_numeric(whole, D(candidate))
        assert not rewards(whole, f'FINAL: {candidate} currency', 'stop')['repaired_reward']
    rate = {'family': 'corp_wacc', 'admissible_values': [],
            'admissible_intervals': [['7.24499999999999999999', '7.25500000000000000001']],
            'source_gold': '7.25', 'repaired_objective_targets': ['7.25']}
    for candidate in ('7.245', '7.25', '7.255'):
        result = rewards(rate, f'FINAL: {candidate} percent', 'stop')
        assert result['financial_valid'] and result['source_reward'] == result['repaired_reward']
    for candidate in ('0.0725', '7.244999', '7.255001', 'NaN', 'Infinity'):
        assert not grade_numeric(rate, D(candidate))
    for text in ('FINAL: 7.2500 currency', 'FINAL: $7.2500 percent',
                 'FINAL: 7.2500 %', 'FINAL: 7.2500 percent.',
                 'FINAL: 7.2500 percent\nextra', 'FINAL: 1 percent\nFINAL: 7.2500 percent'):
        assert parse_final(text, 'corp_wacc')[0] is None
    for finish in ('length', 'transport_error'):
        result = rewards(rate, 'FINAL: 7.2500 percent', finish)
        assert result['value'] is None and not result['financial_valid']
    result = {'status': 'PASS', 'synthetic_case_count': 2,
              'checks': ['both half-tie integers', 'fractional integer rejection',
                         'inclusive cent boundaries', 'percentage-point scale',
                         'unit and marker failures', 'nonfinite rejection', 'failed finish'],
              'method': 'actual primary API called with independently specified synthetic cases; no inference',
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    path = ROOT / 'outputs/finance-adaptation-v1/independent/oracle_boundary_checks.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
