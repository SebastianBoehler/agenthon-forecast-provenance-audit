"""Executive summary: independently replay the completed saved Gemma V2 panel.

No model, server, upstream solution or primary scoring/parser imports. Reuse
separate Fraction extraction/formulas and 100-digit replicating-portfolio math.
Verify both freezes, raw requests, native accounting and all four score streams.
Write only a new independent receipt; never replace scientific outputs.
"""
import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from fractions import Fraction as F
from pathlib import Path

from independent_contract_validation import exact_value
from validate_model_grading_outputs import score, summarize
from validate_model_grading_conventions import price, compatible

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'outputs/model-grading-lmstudio-v1'
OUT = ROOT / 'outputs/model-grading-lmstudio-v2'
MODEL = 'gemma4-e2b-q4km'
EXPECTED = {'preflight': '746b7079e2778e3778a5aa37e4fdb1719e225888ec7bc4ee863245298317325b',
            'collection': '2949178d43af5b3ffef701073f7df92d8fce1c0d33133c783b2d4e805e52d96a'}


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def rows(path):
    raw = Path(path).read_bytes()
    assert raw.endswith(b'\n'), 'Incomplete saved ledger'
    return [json.loads(s) for s in raw.decode().splitlines()]


def utc(value):
    return datetime.fromisoformat(value)


def body_hash(body):
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def native(raw, instance):
    assert raw['model_instance_id'] == instance
    output, stats = raw['output'], raw['stats']
    assert len(output) == 1 and output[0]['type'] == 'message'
    assert isinstance(output[0]['content'], str)
    assert all(type(stats.get(k)) is int and stats[k] >= 0 for k in
               ('input_tokens', 'total_output_tokens', 'reasoning_output_tokens'))
    assert stats['input_tokens'] > 0 and stats['reasoning_output_tokens'] == 0
    assert stats['input_tokens'] + 1024 <= 4096 and stats['total_output_tokens'] <= 1024
    assert not output[0]['content'] or stats['total_output_tokens'] > 0
    return {'text': output[0]['content'],
            'finish_reason': 'length' if stats['total_output_tokens'] == 1024 else 'stop',
            'native_finish_reason': None,
            'finish_reason_origin': 'normally_returned_native_reply_vs_conservative_cap',
            'prompt_tokens': stats['input_tokens'], 'completion_tokens': stats['total_output_tokens']}


def verify_freezes():
    assert digest(OLD / 'preflight_freeze.json') == EXPECTED['preflight']
    assert digest(OUT / 'freeze.json') == EXPECTED['collection']
    a, b = read(OLD / 'preflight_freeze.json'), read(OUT / 'freeze.json')
    hashes = {}
    for frozen in (a, b):
        for name, expected in frozen['files'].items():
            path = ROOT / name
            hashes.setdefault(str(path), digest(path))
            assert hashes[str(path)] == expected, name
        for name, expected in frozen['checkpoint_files'].items():
            if name not in hashes:
                hashes[name] = digest(name)
            assert hashes[name] == expected, name
    assert a['checkpoint_files'] == b['checkpoint_files']
    assert a['request_config'] == b['request_config'] and a['loaded_config'] == b['loaded_config']
    assert all(b['files'][p] == h for p, h in a['files'].items())
    config = b['loaded_config']
    assert config['context_length'] == 4096 and config['parallel'] == 1
    assert config['offload_kv_cache_to_gpu'] is True
    assert not config['speculative_draft_mtp'] and not config['speculative_draft_simple']
    assert not config['speculative_draft_model']
    assert b['full_metal_offload_requested'] is True and b['effective_gpu_layer_ratio_exposed'] is False
    assert b['original_failed_gate'] is True and b['inference_and_scorers_unchanged'] is True
    assert all(not (OLD / p).exists() for p in ('responses.jsonl', 'freeze.json', 'receipt.json'))
    probe, gate = read(OLD / 'preflight.json'), read(OUT / 'readiness_assessment.json')
    assert probe['passed'] is False and sum(r['passed'] for r in probe['records']) == 1
    assert probe['preflight_freeze_sha256'] == EXPECTED['preflight'] and len(probe['records']) == 3
    for r in probe['records']:
        n = native(r['raw_native_response'], b['request_config']['model'])
        assert all(r[k] == v for k, v in n.items()) and n['finish_reason'] == 'stop'
        assert r['live_loaded_config'] == config and r.get('error') is None
        assert r['request_body'] == dict(b['request_config'], input=r['authored_prompt'])
        assert r['request_sha256'] == body_hash(r['request_body'])
    assert gate['native_availability_passed'] is True and gate['original_strict_readiness_passed'] is False
    assert gate['original_strict_passes'] == 1 and gate['source_free_generations_reused'] == 3 and gate['new_generations'] == 0
    assert gate['original_readiness_sha256'] == digest(OLD / 'preflight.json')
    assert utc(a['created_utc']) < utc(probe['completed_utc']) <= utc(gate['created_utc']) <= utc(b['created_utc'])
    return a, b


def compare(ours, saved, selection):
    assert len(ours) == len(saved) == 200
    for r, s in zip(ours, saved):
        for k in ('model_key', 'case_id', 'family', 'parse_error', 'visible_valid', 'decisions', 'finish_reason'):
            assert r[k] == s[k], (r['case_id'], k)
        assert (F(r['fraction_value']) if r['fraction_value'] is not None else None) == (F(s['value']) if s['value'] is not None else None)
        for k in ('unit_state', 'declared_simple_valid', 'continuous_valid'):
            if k in r:
                assert r[k] == s[k], (r['case_id'], k)
        if 'gold' in s:
            chosen = selection[r['case_id']]
            assert F(s['gold']) == F(chosen['gold'])
            assert abs(F(s['formula']) - exact_value(r['family'], chosen['prompt'])[0]) < F(1, 10**35)


def compare_summary(ours, saved):
    current = summarize(ours)
    for k in ('attempts', 'parsed_completed', 'visible_valid', 'failures'):
        assert current[k] == saved[k], k
    for policy, counts in saved['policies'].items():
        assert all(current['policies'][policy][k] == v for k, v in counts.items()), policy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    receipt, results = read(OUT / 'receipt.json'), read(OUT / 'results.json')
    old, freeze = verify_freezes()
    correction = read(OUT / 'summary_path_correction.json')
    assert (OLD / 'results.json').read_bytes() == (OUT / 'results.json').read_bytes()
    assert correction['source_sha256'] == correction['target_sha256'] == digest(OUT / 'results.json')
    assert correction['correction_script_sha256'] == digest(ROOT / 'scripts/restore_lmstudio_v2_summary.py')
    assert correction['original_preserved'] is True and all(correction[k] is False for k in
        ('inference_repeated', 'scoring_changed', 'frozen_code_changed'))
    selection = rows(ROOT / 'outputs/model-grading-v1/selection.jsonl')
    responses = rows(OUT / 'responses.jsonl')
    assert len(selection) == len({s['question_hash'] for s in selection}) == 200
    assert Counter(s['family'] for s in selection) == {'cr_eq_gordon': 50, 'deriv_binomial_call': 50, 'eq_gordon': 50, 'corp_wacc': 50}
    assert receipt['scheduled'] == receipt['attempts'] == len(responses) == 200
    assert receipt['unattempted_ids'] == [] and receipt['stop_reason'] == 'completed'
    assert receipt['freeze_sha256'] == EXPECTED['collection']
    assert receipt['response_sha256'] == digest(OUT / 'responses.jsonl')
    assert results['scheduled'] == results['attempts'] == 200 and results['complete'] is True
    assert results['freeze_sha256'] == EXPECTED['collection']
    previous = utc(receipt['started_utc'])
    assert utc(freeze['created_utc']) <= previous
    streams = {'strict': [], 'numeric': [], 'two_conventions': [], 'numeric_two_conventions': []}
    alternatives, runtime_errors = {}, []
    for i, (r, s) in enumerate(zip(responses, selection), 1):
        assert r['model_key'] == MODEL and r['collection_index'] == i and r['case_id'] == s['case_id']
        assert r['question_hash'] == s['question_hash'] == hashlib.sha256(s['prompt'].encode()).hexdigest()
        assert previous <= utc(r['started_utc']) <= utc(r['completed_utc']) <= utc(receipt['completed_utc'])
        previous = utc(r['completed_utc'])
        assert r['elapsed_s'] >= 0 and utc(r['started_utc']) <= utc(receipt['started_utc']) + timedelta(hours=1)
        assert r['request_body'] == dict(freeze['request_config'], input=s['prompt'])
        assert r['request_sha256'] == body_hash(r['request_body'])
        if r['finish_reason'] == 'runtime_error':
            assert r['text'] == '' and isinstance(r.get('error'), str) and r['error']
            runtime_errors.append(r['case_id'])
        else:
            assert r.get('error') is None and r['live_loaded_config'] == freeze['loaded_config']
            n = native(r['raw_native_response'], freeze['request_config']['model'])
            assert all(r[k] == v for k, v in n.items())
        formula, _ = exact_value(s['family'], s['prompt'])
        assert abs(formula - F(s['formula'])) < F(1, 10**35)
        assert s['requested_rounding'] == (s['family'] == 'cr_eq_gordon')
        if s['family'] == 'deriv_binomial_call':
            _, alternatives[s['case_id']] = price(s['prompt'])
        for endpoint in ('strict', 'numeric'):
            base = score(r, s, numeric=endpoint == 'numeric')
            streams[endpoint].append(base)
            value = F(base['fraction_value']) if base['fraction_value'] is not None else None
            continuous = value is not None and s['family'] == 'deriv_binomial_call' and compatible(value, alternatives[s['case_id']])
            union = dict(base, declared_simple_valid=base['visible_valid'], continuous_valid=bool(continuous))
            union['visible_valid'] = base['visible_valid'] or continuous
            union['decisions'] = base['decisions'] | {'visible_contract': union['visible_valid']}
            streams['two_conventions' if endpoint == 'strict' else 'numeric_two_conventions'].append(union)
    names = {'strict': 'strict_scored', 'numeric': 'numeric_scored', 'two_conventions': 'convention_scored', 'numeric_two_conventions': 'numeric_convention_scored'}
    for endpoint, ours in streams.items():
        compare(ours, rows(OUT / (names[endpoint] + '.jsonl')), {s['case_id']: s for s in selection})
        compare_summary(ours, results[endpoint])
        assert set(results['families']) == {s['family'] for s in selection}
        for family, group in results['families'].items():
            compare_summary([r for r in ours if r['family'] == family], group[endpoint])
    helper_paths = ['scripts/independent_contract_validation.py', 'scripts/validate_model_grading_outputs.py', 'scripts/validate_model_grading_conventions.py']
    notes = []
    selected = {s['case_id']: s for s in selection}
    raw = {r['case_id']: r for r in responses}
    for r in streams['numeric_two_conventions']:
        boundary = r['family'] == 'corp_wacc' and r['visible_valid'] != r['decisions']['source_abs_0.005']
        continuous_only = r['continuous_valid'] and not r['declared_simple_valid']
        if boundary or continuous_only:
            s = selected[r['case_id']]
            notes.append({'case_id': r['case_id'], 'family': r['family'],
                'interpretation': 'continuous-only numeric-compatible call, missing strict unit' if continuous_only else 'rounded-label/computed-reference window difference; label itself passes',
                'raw_last_line': raw[r['case_id']]['text'].splitlines()[-1],
                'question': s['prompt'], 'answer_fraction': r['fraction_value'], 'source_gold': s['gold'],
                'independent_formula_fraction': str(exact_value(s['family'], s['prompt'])[0]),
                'source_abs_0.005_credit': r['decisions']['source_abs_0.005'],
                'continuous_price_100digits': str(alternatives[s['case_id']]) if continuous_only else None})
    report = {'executive_summary': 'PASS: completed 200 saved Gemma attempts across four unchanged scoring endpoints; no inference or semantic/causal certification.',
        'status': 'PASS', 'completed_utc': datetime.now(timezone.utc).isoformat(),
        'validator_sha256': digest(__file__), 'helper_sha256': {p: digest(ROOT / p) for p in helper_paths},
        'freeze_sha256': EXPECTED, 'frozen_scientific_files': {'v1': len(old['files']), 'v2': len(freeze['files'])},
        'external_files_checked': len(freeze['checkpoint_files']), 'attempts': 200,
        'runtime_errors': runtime_errors, 'successful_native_replies': 200 - len(runtime_errors),
        'finish_reasons': dict(Counter(r['finish_reason'] for r in responses)),
        'observed_input_tokens': sum(r.get('prompt_tokens', 0) for r in responses),
        'observed_output_tokens': sum(r.get('completion_tokens', 0) for r in responses),
        'started_utc': receipt['started_utc'], 'completed_collection_utc': receipt['completed_utc'],
        'original_strict_probe_passes': 1, 'original_runtime_probe_passes': 3,
        'summary_path_correction_sha256': digest(OUT / 'summary_path_correction.json'),
        'source_and_target_summary_bytes_identical': True, 'case_notes': notes,
        'file_sha256': {p.name: digest(p) for p in [OUT/'receipt.json', OUT/'responses.jsonl', OUT/'results.json'] + [OUT/(n+'.jsonl') for n in names.values()]},
        'endpoints': {e: summarize(v) for e, v in streams.items()},
        'source_abs_0.005_denials_by_family': {e: dict(Counter(r['family'] for r in v if r['visible_valid'] and not r['decisions']['source_abs_0.005'])) for e, v in streams.items()},
        'scope': 'Own saved native/request/accounting replay; prior separate Fraction/parser and 100-digit compounding helpers; all four row decisions/errors/values and aggregate/family counts agree. Full engine/model/config file hashes checked. No native token-ID/EOS/full-GPU observation; no source semantics certification.',
        'new_inference': False}
    with args.output.open('x') as stream:
        stream.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'attempts': 200, 'finish_reasons': report['finish_reasons'],
                      'endpoints': {e: {'parsed': v['parsed_completed'], 'valid': v['visible_valid']} for e, v in report['endpoints'].items()}}))


if __name__ == '__main__':
    main()
