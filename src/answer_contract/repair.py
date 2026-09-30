"""Executive summary: materialize explicit-contract numerical patches without claiming trace repair."""
from decimal import ROUND_HALF_UP

from .types import Case


def repair_record(case: Case) -> dict:
    answer = case.target.quantize(case.quantum, rounding=ROUND_HALF_UP)
    if not case.accepts(answer):
        raise ValueError(f'Invalid materialized correction: {case.case_id}')
    prompt = case.prompt
    if case.interval:
        prompt += '\nFor this repaired version, treat every displayed numerical input as exact.'
    return {'source': case.source, 'family': case.family, 'id': case.case_id,
            'question': prompt, 'original_numeric_answer': str(case.gold),
            'repaired_numeric_answer': str(answer),
            'contract': 'explicit_exact_inputs_and_requested_output_projection',
            'output_quantum': str(case.quantum),
            'numeric_label_changed': answer != case.gold,
            'input_convention_added': case.interval is not None,
            'original_trace_status': 'not_preserved_or_certified; full trace regeneration required',
            'preference_action': ('replace_chosen_answer_and_regenerate_trace'
                                  if case.chosen is not None and not case.accepts(case.chosen)
                                  else 'no_numerical_chosen_repair_needed'),
            'half_tie_policy': 'half_up; either nearest integer accepted during original audit'}
