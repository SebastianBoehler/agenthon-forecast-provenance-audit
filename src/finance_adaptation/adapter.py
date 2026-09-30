"""Executive summary: isolate GEPA objective feedback from the financial evaluation oracle."""
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal as D

from gepa.core.adapter import EvaluationBatch

from model_grading.protocol import append_record, parse_final, question_hash
from .benchmark import grade_numeric

SEED = 'Read the financial question carefully and calculate the requested answer.'
MANUAL = (
    'Compute the quantity requested, then apply its rounding instruction. For Gordon '
    'growth use next dividend divided by required return minus growth. For a binomial '
    'call use risk-neutral probability ((1+r)-d)/(u-d) and discounted expected positive '
    'payoffs, not the financing debt. For WACC use E/(D+E)*Re + D/(D+E)*Rd*(1-tax), '
    'keeping all rates in consistent units. Round only the final result.'
)
PREFIX = ('Solve the financial question using numbers exactly as displayed. Treat a '
          'quoted one-period binomial rate as effective for that period: gross factor 1+r. '
          'Assume no dividends during the binomial period.\n')
FORMAT = ('\nGive a concise calculation in at most five sentences. End with exactly one '
          'final line, using the literal unit words in these examples: FINAL: 12.3456 currency '
          'or FINAL: 7.2500 percent. Percent means percentage points. Do not use Markdown, '
          'a dollar sign, a percent sign, punctuation after the unit, or text after that line.')
MAX_CANDIDATE_BYTES = 2000


def rewards(row, text, finish_reason):
    value, error = parse_final(text, row['family'])
    if finish_reason != 'stop':
        value, error = None, finish_reason
    financial = value is not None and grade_numeric(row, value)
    source = (None if 'source_gold' not in row else
              value is not None and abs(value - D(row['source_gold'])) <= D('.005'))
    repaired = value is not None and any(
        abs(value - D(t)) <= D('.005') for t in row['repaired_objective_targets'])
    if row['family'] == 'cr_eq_gordon' and value is not None:
        repaired = repaired and value == value.to_integral_value()
    return {'value': str(value) if value is not None else None, 'parse_error': error,
            'financial_valid': financial, 'source_reward': source,
            'repaired_reward': repaired}


class FinanceAdapter:
    propose_new_texts = None

    def __init__(self, client, directory, objective, seed):
        self.client, self.directory = client, directory
        self.objective, self.seed = objective, seed
        self.actor_calls = 0
        self.reflection_calls = 0
        self.evaluations = 0

    def evaluate(self, batch, candidate, capture_traces=False):
        strategy = candidate['strategy']
        self.evaluations += 1
        oversized = len(strategy.encode()) > MAX_CANDIDATE_BYTES
        if not oversized and self.actor_calls + len(batch) > 256:
            raise RuntimeError('Metric-call hard cap would be exceeded')

        def answer(row):
            if oversized:
                raw = {'text': '', 'finish_reason': 'candidate_too_long'}
            else:
                raw = self.client.call(
                    [{'role': 'system', 'content': PREFIX + strategy + FORMAT},
                     {'role': 'user', 'content': row['prompt']}],
                    tag=f'{self.objective}-{self.seed}:evaluation-{self.evaluations}:{row["case_id"]}')
            grade = rewards(row, raw['text'], raw['finish_reason'])
            key = 'source_reward' if self.objective == 'source' else 'repaired_reward'
            if grade[key] is None:
                raise ValueError('Source objective must never evaluate authored transfer')
            record = {'case_id': row['case_id'], 'partition': row['partition'],
                      'family': row['family'], 'question_hash': row['question_hash'],
                      'candidate_hash': question_hash(strategy), 'strategy': strategy,
                      'evaluation': self.evaluations, 'objective': self.objective,
                      'seed': self.seed, 'text': raw['text'],
                      'finish_reason': raw['finish_reason'], **grade}
            target = ([row['source_gold']] if self.objective == 'source' else
                      row['repaired_objective_targets'])
            # Only this assigned-objective view is ever passed to GEPA reflection.
            feedback = {'Inputs': row['prompt'], 'Generated Outputs': raw['text'],
                        'Feedback': {'reward': int(grade[key]), 'target_values': target,
                                     'absolute_tolerance': '0.005',
                                     'integer_required': (self.objective == 'repaired' and
                                                          row['family'] == 'cr_eq_gordon'),
                                     'format_error': grade['parse_error']}}
            return record, feedback, float(grade[key])

        with ThreadPoolExecutor(max_workers=4) as pool:
            evaluated = list(pool.map(answer, batch))
        records, traces, scores = map(list, zip(*evaluated))
        self.actor_calls += 0 if oversized else len(batch)
        for record in records:
            append_record(self.directory / 'evaluations.jsonl', record)
        # GEPA outputs, as well as reflection traces, contain only assigned feedback.
        return EvaluationBatch(traces, scores, traces if capture_traces else None)

    def make_reflective_dataset(self, candidate, eval_batch, components_to_update):
        return {key: eval_batch.trajectories for key in components_to_update}

    def reflect(self, prompt):
        if self.reflection_calls >= 16:
            raise RuntimeError('Reflection hard cap reached')
        self.reflection_calls += 1
        messages = [{'role': 'system', 'content':
                     'When proposing a strategy keep it below 2000 UTF-8 bytes. '
                     'Only the strategy can change; the answer-format wrapper is fixed.'},
                    {'role': 'user', 'content': prompt}]
        result = self.client.call(messages, tag=f'{self.objective}-{self.seed}:reflection',
                                  max_tokens=1536, temperature=.7)
        if result['finish_reason'] != 'stop':
            raise RuntimeError('Reflection did not complete normally')
        return result['text']

    def stop(self, state):
        # Reserve one minibatch before/after pair plus a full32-example dev evaluation.
        return (max(self.actor_calls, state.total_num_evals) > 256 - 38 or
                self.reflection_calls >= 16 or
                state.i >= 40)
