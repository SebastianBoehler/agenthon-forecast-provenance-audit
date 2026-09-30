"""Executive summary: independently validate saved local pilot accounting and scores.

No model loading, generation or network. Own strict/status JSON validation and
Fraction matching reuse earlier independent helpers; native metric is shared.
Writes a new postflight receipt only. Failed attempts never become responses.
"""
import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import validate_finance_document_final as prior
from finance_document_local.manifest import digest, rows, verify
from finance_document_local.protocol import CONDITIONS, MODELS, OUT, ROOT, cache


def parse(text, condition, status_only=False):
    def unique(pairs):
        if len(dict(pairs)) != len(pairs):
            raise ValueError('duplicate')
        return dict(pairs)
    def constant(_):
        raise ValueError('nonstandard')
    try:
        obj = json.loads(text, object_pairs_hook=unique, parse_constant=constant)
    except (ValueError, TypeError):
        return None, 'invalid_json'
    required = {'status', 'value', 'unit', 'scale'}
    compact = condition.startswith('compact_')
    if not compact:
        required |= {'calculation', 'evidence'}
    if not isinstance(obj, dict) or set(obj) != required:
        return None, 'invalid_fields'
    c = {**obj, 'calculation': '', 'evidence': []} if compact else dict(obj)
    if status_only and isinstance(c['status'], str) and isinstance(c['value'], str) and c['value'] not in ['yes', 'no']:
        c['status'] = 'answer'
    return prior.parse(json.dumps(c))


def summary(selected):
    return {'attempts': len(selected), 'response_states': dict(Counter(r['state'] for r in selected)),
        'strict_numeric': sum(r['strict'] is not None and r['strict']['status'] == 'answer' for r in selected),
        'status_only_numeric': sum(r['recovered'] is not None and r['recovered']['status'] == 'answer' for r in selected),
        'locked_eligible': sum(r['eligible'] for r in selected),
        'strict_locked_matches': sum(r['match'] is True for r in selected),
        'status_only_locked_matches': sum(r['recovered_match'] is True for r in selected),
        'projected_reference_matches': sum(r['projected'] is True for r in selected),
        'native_eligible': sum(r['native']['eligible'] for r in selected),
        'native_credits': sum(r['native']['credited'] is True for r in selected),
        'tatqa_answer_em_sum': sum(r['native'].get('answer_em', 0) for r in selected),
        'tatqa_answer_f1_sum': sum(r['native'].get('answer_f1', 0) for r in selected),
        'tatqa_scale_correct': sum(r['native'].get('scale_score') == 1 for r in selected),
        'finqa_percent_fraction_credits': sum(r['fraction'] is not None and r['fraction']['credited'] is True for r in selected),
        'length_exhausted': sum(r['finish_reason'] == 'length' for r in selected),
        'full_expressions_supported': 0}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    frozen = verify()
    for model in MODELS:
        verify(model_key=model)  # Hash every bound checkpoint file; no weight/model loading.
    selection = rows(OUT / 'selection.jsonl')
    ids = [r['case_id'] for r in selection]
    assert len(ids) == len(set(ids)) == 32 and Counter(r['source'] for r in selection) == {'finqa': 16, 'tatqa': 16}
    assert digest(OUT / 'selection.jsonl') == frozen['selection_sha256']
    refs = {r['case_id']: r for r in rows(ROOT / 'outputs/finance-document-review-v1/pre_target_combined.jsonl')}
    ann = {r['case_id']: r['original_annotation'] for r in rows(ROOT / 'outputs/finance-document-replay-v1/compact_native_annotations.jsonl')}
    assert sum(refs[c]['joint_status'] == prior.ELIGIBLE for c in ids) == frozen['locked_eligible_cases'] == 24
    audits = {(r['model_key'], r['condition'], r['case_id']): r for r in rows(OUT / 'token_audit.jsonl')}
    response_rows, ledgers = [], {}
    freeze_time = datetime.fromisoformat(frozen['created_utc'])
    for model in MODELS:
        path = OUT / ('responses_' + model + '.jsonl')
        response = rows(path)
        receipt_path = OUT / ('receipt_' + model + '.json')
        receipt = json.loads(receipt_path.read_text())
        assert receipt['response_sha256'] == digest(path) and receipt['freeze_sha256'] == digest(OUT / 'freeze.json')
        assert receipt['selection_sha256'] == frozen['selection_sha256']
        assert receipt['model_key'] == model and receipt['attempts'] == receipt['scheduled'] == len(response) == 128
        order = []
        for i, case in enumerate(selection):
            conditions = list(CONDITIONS)
            order += [(case['case_id'], c) for c in conditions[i % 4:] + conditions[:i % 4]]
        assert [(r['case_id'], r['condition']) for r in response] == order
        previous = freeze_time
        for i, r in enumerate(response, 1):
            assert r['model_key'] == model and r['collection_index'] == i
            assert r['source'] == refs[r['case_id']]['source']
            start, end = [datetime.fromisoformat(r[k]) for k in ['started_utc', 'completed_utc']]
            assert previous <= start <= end <= datetime.fromisoformat(receipt['completed_utc'])
            previous = end
            if r.get('error') is None:
                assert r['runtime_ok'] is r['token_audit_ok'] is True
                assert r['device'] == 'mps' and r['dtype'] == 'float16' and r['do_sample'] is False
                expected = audits[model, r['condition'], r['case_id']]
                for k in ['prompt_tokens', 'prompt_token_ids_sha256', 'rendered_prompt_sha256']:
                    assert r[k] == expected[k]
                assert r['explicit_no_special_tokens_identical'] is True and r['truncation_requested'] is False
                assert r['prompt_tokens'] + 512 <= expected['context_limit']
                assert r['completion_tokens'] == len(r['generated_token_ids']) <= r['max_new_tokens'] == 512
                eos = bool(r['generated_token_ids'] and r['generated_token_ids'][-1] in r['eos_token_ids'])
                assert r['finish_reason'] == ('eos' if eos else 'length')
                if not eos:
                    assert r['completion_tokens'] == 512
            else:
                assert r['runtime_ok'] is r['token_audit_ok'] is False and r['text'] == '' and r['finish_reason'] == 'error'
                assert 'MPS backend out of memory' in r['error']
                assert 'generated_token_ids' not in r and 'completion_tokens' not in r
        success = [r for r in response if not r.get('error')]
        failed = [r for r in response if r.get('error')]
        ledgers[model] = {'attempts': 128, 'runtime_successful': len(success), 'runtime_failed': len(failed),
            'success_by_source': dict(Counter(r['source'] for r in success)),
            'success_by_condition': {c: sum(r['condition'] == c for r in success) for c in CONDITIONS},
            'finish_reasons': dict(Counter(r['finish_reason'] for r in response)),
            'observed_completion_tokens': sum(r['completion_tokens'] for r in success),
            'successful_generation_seconds': sum(r['elapsed_seconds'] for r in success),
            'started_utc': response[0]['started_utc'], 'completed_utc': response[-1]['completed_utc'],
            'response_sha256': digest(path), 'receipt_sha256': digest(receipt_path),
            'first_failure_collection_index': failed[0]['collection_index'] if failed else None}
        response_rows += response
    assert datetime.fromisoformat(ledgers['qwen3-1.7b']['completed_utc']) <= datetime.fromisoformat(ledgers['smollm2-1.7b']['started_utc'])
    assert len(response_rows) == 256 and len({(r['model_key'], r['condition'], r['case_id']) for r in response_rows}) == 256
    saved_scores = rows(OUT / 'scores.jsonl')
    assert len(saved_scores) == 256
    independent = []
    for response, score in zip(response_rows, saved_scores):
        for k in ['model_key', 'condition', 'case_id', 'finish_reason']:
            assert response[k] == score[k]
        ref, annotation = refs[response['case_id']], ann[response['case_id']]
        c, error = parse(response['text'], response['condition'])
        recovered, re = parse(response['text'], response['condition'], True)
        if response.get('error') is not None or response.get('runtime_ok') is not True or response.get('token_audit_ok') is not True:
            c = recovered = None
            error = re = 'runtime_or_token_validation_failure'
        assert c == score['strict_candidate'] and error == score['strict_parse_error']
        assert recovered == score['status_only_candidate'] and re == score['status_only_parse_error']
        match, value = prior.matches(ref, c)
        recovered_match, _ = prior.matches(ref, recovered)
        assert match == score['strict_locked']['matches'] and recovered_match == score['status_only_locked']['matches']
        native = prior.native(ref['source'], annotation, c)
        assert native == score['strict_native']
        projected, extra = prior.projection(ref, match, value)
        assert projected == score['strict_projected_reference']['matches'] and extra == score['strict_projected_reference']['additional_rounded_match']
        fraction = None
        if ref['source'] == 'finqa' and c is not None:
            assert c['status'] != 'answer'  # Observed strict floor: no invented numeric repairs.
            fraction = prior.native('finqa', annotation, c)
        assert fraction == score['finqa_percent_fraction_sensitivity']
        assert score['semantic_or_trace_certification'] is False
        if response['condition'].startswith('compact_'):
            assert score['arithmetic'] == {'requested': False, 'supported': None}
        else:
            assert score['arithmetic'] == {'requested': True, 'supported': False, 'reason': 'no_strict_numeric_answer'}
        independent.append({**response, 'strict': c, 'recovered': recovered, 'state': error or c['status'],
            'match': match, 'recovered_match': recovered_match, 'projected': projected, 'native': native,
            'fraction': fraction, 'eligible': ref['joint_status'] == prior.ELIGIBLE})
    result = json.loads((OUT / 'results.json').read_text())
    assert result['attempts'] == 256 and result['freeze_sha256'] == digest(OUT / 'freeze.json')
    for model in MODELS:
        index = {(r['case_id'], r['condition']): r for r in independent if r['model_key'] == model}
        for condition in CONDITIONS:
            ss = [r for r in independent if r['model_key'] == model and r['condition'] == condition]
            assert summary(ss) == result['models'][model][condition]['all']
            for source in ['finqa', 'tatqa']:
                assert summary([r for r in ss if r['source'] == source]) == result['models'][model][condition]['sources'][source]
        for p in result['paired'][model]:
            counts = Counter()
            for case in ids:
                a, b = index[case, p['left']], index[case, p['right']]
                if a['eligible']:
                    counts[f"{a['match']}->{b['match']}"] += 1
            assert dict(counts) == p['strict_locked_transitions'] == {'False->False': 24} and p['discordances'] == []
    report = {'executive_summary': 'PASS256 saved attempted records;141 successful generations and115 retained OOM failures. No viable two-family financial comparison or numeric availability effect.',
        'status': 'PASS', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'validator_sha256': digest(__file__),
        'scheduled_attempts': 256, 'successful_generations': sum(r['runtime_successful'] for r in ledgers.values()),
        'failed_runtime_attempts': sum(r['runtime_failed'] for r in ledgers.values()), 'model_accounting': ledgers,
        'strict_numeric_answers': 0, 'strict_locked_matches': 0, 'status_only_locked_matches': 0,
        'status_only_numeric_by_arm': {m: {c: result['models'][m][c]['all']['status_only_numeric'] for c in CONDITIONS} for m in MODELS},
        'fixed_reference_questions': 24, 'freeze_sha256': digest(OUT / 'freeze.json'),
        'frozen_input_count': len(frozen['files_sha256']), 'checkpoint_files_verified': {m: len(v) for m, v in frozen['checkpoint_files_sha256'].items()},
        'scores_sha256': digest(OUT / 'scores.jsonl'), 'results_sha256': digest(OUT / 'results.json'),
        'prior_independent_helper_sha256': digest(Path(prior.__file__)),
        'scope': 'Own standard-JSON schema/status parsing and prior independent Fraction matching/projection; shared hash-pinned native adapter. Full frozen files/checkpoint hashes, ledgers, identities, order, timing, flags, audit IDs and token counters checked. No model loading/generation/network.',
        'new_inference': False, 'semantic_truth_certification': False}
    with args.output.open('x') as stream:
        stream.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'successful_generations': report['successful_generations'],
                     'failed_runtime_attempts': report['failed_runtime_attempts'], 'model_accounting': ledgers}))


if __name__ == '__main__':
    main()
