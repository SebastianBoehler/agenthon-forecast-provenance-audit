"""Executive summary: verify semantic reward interventions and optimizer blindness."""
import json
from pathlib import Path

from finance_adaptation.adapter import FinanceAdapter, rewards

ROOT = Path(__file__).resolve().parents[1]


def prepared_rows():
    path = ROOT / 'outputs/finance-adaptation-v1/train.jsonl'
    return [json.loads(line) for line in path.read_text().splitlines()]


def test_repaired_integer_reward_does_not_credit_small_fraction():
    row = next(r for r in prepared_rows() if r['family'] == 'cr_eq_gordon')
    target = row['repaired_objective_targets'][0]
    from decimal import Decimal
    text = f'FINAL: {Decimal(target) + Decimal(".001")} currency'
    result = rewards(row, text, 'stop')
    assert not result['repaired_reward']
    assert not result['financial_valid']


def test_passing_family_objectives_preserve_the_same_window():
    from decimal import Decimal
    for row in prepared_rows():
        if row['family'] not in ('eq_gordon', 'corp_wacc'):
            continue
        for delta in ('-.0051', '-.005', '0', '.005', '.0051'):
            value = Decimal(row['source_gold']) + Decimal(delta)
            result = rewards(row, f'FINAL: {value} {row["unit"]}', 'stop')
            assert result['source_reward'] == result['repaired_reward']


def test_source_optimizer_cannot_receive_financial_oracle_feedback(tmp_path):
    row = next(r for r in prepared_rows() if r['family'] == 'deriv_binomial_call')

    class FixedClient:
        def call(self, messages, **kwargs):
            assert row['prompt'] == messages[1]['content']
            return {'text': f'FINAL: {row["source_gold"]} currency', 'finish_reason': 'stop'}

    adapter = FinanceAdapter(FixedClient(), tmp_path, 'source', 0)
    batch = adapter.evaluate([row], {'strategy': 'Calculate.'}, capture_traces=True)
    assert batch.outputs == batch.trajectories
    exposed = json.dumps(batch.outputs)
    for forbidden in ('financial_valid', 'repaired_reward', 'formula', 'admissible_intervals'):
        assert forbidden not in exposed
    assert batch.scores == [1.0]
    assert batch.outputs[0]['Feedback']['target_values'] == [row['source_gold']]


def test_transfer_has_no_released_reward():
    path = ROOT / 'outputs/finance-adaptation-v1/test-transfer.jsonl'
    row = json.loads(path.read_text().splitlines()[0])
    result = rewards(row, f'FINAL: {row["target"]} {row["unit"]}', 'stop')
    assert result['source_reward'] is None
    assert result['financial_valid']
