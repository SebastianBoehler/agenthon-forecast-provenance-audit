"""Executive summary: replay posthoc diagnostic rows using compact unchanged native fields."""
from __future__ import annotations

import importlib.util
import json

from finance_document_review.model_protocol import MODELS, ROOT, SYSTEMS
from replay_finance_document_artifact import rows
from validate_finance_document_extension import main as verify_extension


def main():
    # This later saved-score replay does not alter the full-input frozen protocol.
    verify_extension()
    output = ROOT / 'outputs/finance-document-diagnostics-v1'
    spec = importlib.util.spec_from_file_location('document_diagnostics', output / 'diagnose.py')
    diagnostic = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(diagnostic)
    panel = ROOT / 'outputs/finance-document-models-v1'
    responses = rows(panel / 'effective_attempts.jsonl')
    references = {r['case_id']: r for r in rows(
        ROOT / 'outputs/finance-document-review-v1/pre_target_combined.jsonl')}
    annotations = {r['case_id']: r['original_annotation'] for r in rows(
        ROOT / 'outputs/finance-document-replay-v1/compact_native_annotations.jsonl')}
    strict = {diagnostic.key(r): r for r in rows(panel / 'paired_scores.jsonl')}
    expected = {(m, arm, case) for m in MODELS for arm in SYSTEMS for case in references}
    keys = [diagnostic.key(r) for r in responses]
    if len(keys) != 384 or len(set(keys)) != 384 or set(keys) != expected:
        raise ValueError('Missing, duplicated or unexpected attempt identity')
    if set(annotations) != set(references) or set(strict) != expected:
        raise ValueError('Compact annotation or strict score identities differ')
    replayed = []
    for index, response in enumerate(responses, 1):
        original = strict[diagnostic.key(response)]
        reference = references[response['case_id']]
        annotation = annotations[response['case_id']]
        candidate, recovery = diagnostic.recover(response, original)
        financial = diagnostic.locked_match(reference, candidate)
        native = diagnostic.native_score(reference['source'], annotation, candidate)
        expression = diagnostic.arithmetic(candidate, reference, annotation)
        replayed.append({
            'case_id': response['case_id'], 'source': reference['source'],
            'model_key': response['model_key'], 'condition': response['condition'],
            'effective_ledger_line': index, 'joint_status': reference['joint_status'],
            'original_strict': {
                'numeric_answer': original['candidate'] is not None and
                                  original['candidate']['status'] == 'answer',
                'parse_error': original['parse_error'],
                'locked_comparator': original['locked_comparator'],
                'native_or_adapted': original['native_or_adapted']},
            'recovered_candidate': candidate, 'recovery': recovery,
            'recovered_locked': financial, 'recovered_native': native,
            'reported_exact_reference_after_frozen_conversion':
                diagnostic.exact_reference(financial, reference),
            'arithmetic': expression, 'semantic_or_trace_certification': False})
    serialized = '\n'.join(json.dumps(r, ensure_ascii=False, default=str)
                           for r in replayed) + '\n'
    if serialized != (output / 'rows.jsonl').read_text():
        raise AssertionError('Any compact diagnostic row differs from full-input analysis')
    saved = json.loads((output / 'results.json').read_text())
    if diagnostic.summary(replayed) != saved['all']:
        raise AssertionError('Compact diagnostic aggregate differs')
    if {m: diagnostic.paired(replayed, m) for m in MODELS} != saved['paired_reminder']:
        raise AssertionError('Compact diagnostic paired counts differ')
    models = {}
    for model in MODELS:
        models[model] = {}
        for arm in SYSTEMS:
            selected = [r for r in replayed if r['model_key'] == model and r['condition'] == arm]
            models[model][arm] = {'all': diagnostic.summary(selected), 'sources': {
                source: diagnostic.summary([r for r in selected if r['source'] == source])
                for source in ('finqa', 'tatqa')}}
    if models != saved['models']:
        raise AssertionError('Compact diagnostic source/condition aggregates differ')
    print(json.dumps({'status': 'PASS', 'attempts': 384,
                      'compact_diagnostic_rows_byte_identical': True,
                      'all_aggregate_counts_identical': True, 'new_inference_calls': 0,
                      'original_full_input_protocol_replaced': False,
                      'expert_semantic_certification': False}))


if __name__ == '__main__':
    main()
