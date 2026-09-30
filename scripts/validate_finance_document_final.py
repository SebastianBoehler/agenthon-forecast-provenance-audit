"""Executive summary: independently rescore the closed384-event document panel.

Own parser and Fraction value/unit/precision arithmetic; pinned native TAT metric
is shared, with independently checked FinQA scalar credits. No API calls or
annotation-program execution. Writes a new receipt only, never frozen artifacts.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction as F
from pathlib import Path

from finance_document_review.model_protocol import SYSTEMS
from finance_document_review.native_metrics import (
    replay_authored_controls, score_finqa_scalar, score_tatqa, verify_native_sources,
)

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / 'outputs/finance-document-models-v1'
REVIEW = ROOT / 'outputs/finance-document-review-v1'
REPLAY = ROOT / 'outputs/finance-document-replay-v1'
MODELS = {'deepseek-v3.2': 'deepseek/deepseek-v3.2', 'qwen3.5-9b': 'qwen/qwen3.5-9b'}
ELIGIBLE = 'agreed_determinate_numeric'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def lines(path):
    return [json.loads(x) for x in Path(path).read_text().splitlines()]


def parse(text):
    def unique(pairs):
        if len(dict(pairs)) != len(pairs):
            raise ValueError('duplicate')
        return dict(pairs)
    try:
        c = json.loads(text, object_pairs_hook=unique)
    except (ValueError, TypeError):
        return None, 'invalid_json'
    if not isinstance(c, dict) or set(c) != {'status', 'value', 'unit', 'scale', 'calculation', 'evidence'}:
        return None, 'invalid_fields'
    if (any(not isinstance(c[k], str) for k in ['status', 'unit', 'scale', 'calculation'])
            or c['status'] not in {'answer', 'non_numeric_answer', 'insufficient_information'}
            or c['scale'] not in {'none', 'thousand', 'million', 'billion'}
            or not isinstance(c['evidence'], list)):
        return None, 'invalid_field_types'
    if c['status'] == 'insufficient_information':
        return (c, None) if c['value'] is None else (None, 'nonempty_abstention')
    if c['status'] == 'non_numeric_answer':
        ok = isinstance(c['value'], str) and c['value'] in ['yes', 'no'] and c['unit'] == 'boolean' and c['scale'] == 'none'
        return (c, None) if ok else (None, 'invalid_non_numeric_answer')
    if not isinstance(c['value'], str) or not c['unit'].strip():
        return None, 'missing_value_or_unit'
    try:
        d = Decimal(c['value'])
    except ArithmeticError:
        return None, 'invalid_decimal'
    return (c, None) if d.is_finite() else (None, 'nonfinite_value')


def unit(c):
    # Reproduce the declared BROAD dimensions, including documented substring limitations.
    s, scale = c['unit'].lower().strip().replace('_', ' '), c['scale']
    if 'percent or percentage' in s.replace('-', ' '):
        return 'ambiguous', None, None
    if 'percentage point' in s:
        dim, factor = 'percentage_points', F(1)
    elif 'percent' in s or s == '%':
        dim, factor = 'proportion', F(1, 100)
    elif any(w in s for w in ['ratio', 'proportion', 'portion', 'dimensionless']):
        dim, factor = 'proportion', F(1)
    elif any(w in s for w in ['usd', 'dollar', 'eur', 'gbp', 'rmb', 'yuan', 'currency', 'monetary', 'cent', '$', '£', '€']):
        dim, factor = 'monetary', F(1, 100) if 'cent' in s else F(1)
    elif any(w in s for w in ['shares', 'years', 'year', 'count']):
        dim, factor = 'count', F(1)
    else:
        return 'boolean' if 'boolean' in s else 'unresolved', None, None
    if dim in ['monetary', 'count']:
        factor *= {'none': 1, 'thousand': 1000, 'million': 10**6, 'billion': 10**9}[scale]
    elif scale != 'none':
        return 'incompatible_scale', None, None
    currency = next((x for x in ['USD', 'EUR', 'GBP', 'RMB'] if re.search(r'\b' + x.lower() + r'\b', s)), None)
    return dim, factor, 'RMB' if 'yuan' in s else currency


def near(value, target):
    return abs(value - target) <= max(F('1e-8'), abs(target) * F('1e-7'))


def matches(ref, c):
    if ref['joint_status'] != ELIGIBLE:
        return None, None
    if c is None or c['status'] != 'answer':
        return False, None
    dim, factor, currency = unit(c)
    r = ref['unit_a']
    if (dim != r['dimension'] or factor is None or r['factor'] is None
            or currency and r['currency'] and currency != r['currency']):
        return False, None
    value = F(c['value']) * factor / F(r['factor'])
    return any(near(value, F(t)) for t in ref['reference_values']), value


def projection(ref, match, value):
    if value is None or ref['unit_a']['dimension'] == 'count':
        return match, False
    quantum = F('.01') if ref['source'] == 'tatqa' else F('.00001')
    if ref['source'] == 'finqa' and ref['unit_a']['dimension'] in ['proportion', 'percentage_points']:
        quantum /= F(ref['unit_a']['factor'])
        if ref['unit_a']['dimension'] == 'percentage_points':
            quantum = F('.001')
    # Python Fraction round is exact nearest-even, independent of primary Decimal implementation.
    rounded = any(near(value, round(F(t) / quantum) * quantum) for t in ref['reference_values'])
    return bool(match or rounded), bool(rounded and not match)


def native(source, annotation, c):
    if c is None:
        return {'eligible': False, 'credited': None, 'reason': 'parse_or_request_failure'}
    try:
        result = (score_finqa_scalar if source == 'finqa' else score_tatqa)(annotation, c)
        credited = result['execution_answer_correct'] if source == 'finqa' else result['answer_em'] == 1
        if source == 'finqa':
            value = round(float(c['value']), 5) if c['status'] == 'answer' else c['value']
            assert credited == (c['status'] != 'insufficient_information' and value == annotation['exe_ans'])
        return {'eligible': True, 'credited': credited, **result}
    except ValueError as exc:
        return {'eligible': False, 'credited': None, 'reason': 'adapter_ineligible', 'detail': str(exc)}


def aggregate(rows, endpoint='native'):
    matrix = Counter()
    for r in rows:
        n = r[endpoint]
        if r['eligible']:
            key = 'native_ineligible' if n is None or not n['eligible'] else (
                ('match' if r['match'] else 'mismatch') + ('_credited' if n['credited'] else '_denied'))
            matrix[key] += 1
    eligible = sum(r['eligible'] for r in rows)
    return {'attempts': len(rows), 'response_states': dict(Counter(r['state'] for r in rows)),
            'locked_reference_cases': eligible, 'outside_locked_reference': len(rows) - eligible,
            'paired_matrix': dict(matrix), 'locked_matches_all_attempts': sum(r['match'] is True for r in rows),
            'native_credits_all_attempts': sum(r[endpoint] is not None and r[endpoint]['credited'] is True for r in rows),
            'native_ineligible_all_attempts': sum(r[endpoint] is None or not r[endpoint]['eligible'] for r in rows)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    freeze_paths = [PANEL / p for p in ['freeze.json', 'analysis_implementation_freeze.json', 'reporting_diagnostic_freeze.json']]
    freeze_paths += [REVIEW / p for p in ['stage_freeze.json', 'pre_target_lock.json', 'comparison_protocol_freeze.json']]
    freeze_paths += [REPLAY / 'manifest.json']
    checked = {}
    for p in freeze_paths:
        for path, sha in read(p)['files_sha256'].items():
            assert digest(ROOT / path) == sha, path
            checked[path] = sha
        checked[str(p.relative_to(ROOT))] = digest(p)
    unblind = read(REVIEW / 'source_target_unblinding.json')
    assert digest(REVIEW / 'pre_target_lock.json') == unblind['pre_target_lock_sha256']
    original_targets = ROOT / 'outputs/finance-document-audit-v1/source_targets.jsonl'
    assert digest(original_targets) == unblind['source_targets_sha256']
    target_rows = lines(original_targets)
    compact = lines(REPLAY / 'compact_native_annotations.jsonl')
    expected_compact = [{'case_id': r['case_id'], 'source': r['source'], 'original_annotation': {
        k: r['original_annotation'][k] for k in (['exe_ans'] if r['source'] == 'finqa' else ['answer', 'answer_type', 'scale'])}}
        for r in target_rows]
    assert compact == expected_compact and len(compact) == 96
    targets = {r['case_id']: r['original_annotation'] for r in compact}
    refs = {r['case_id']: r for r in lines(REVIEW / 'pre_target_combined.jsonl')}
    raw, events = lines(PANEL / 'responses.jsonl'), lines(PANEL / 'effective_attempts.jsonl')
    assert len(raw) == 383 and events[:-1] == raw and len(events) == 384
    assert (PANEL / 'effective_attempts.jsonl').read_bytes().startswith((PANEL / 'responses.jsonl').read_bytes())
    keys = [(r['model_key'], r['condition'], r['case_id']) for r in events]
    assert len(set(keys)) == 384 and set(keys) == {(m, a, c) for m in MODELS for a in SYSTEMS for c in refs}
    last, intent, receipt = events[-1], read(PANEL / 'interruption_intent.json'), read(PANEL / 'interrupted_collection_receipt.json')
    assert all(last[k] == v for k, v in intent['pending_case'].items()) and refs[last['case_id']]['joint_status'] != ELIGIBLE
    assert last['collector_event'] and last['actual_api_response'] is False and not last['text'] and 'raw_response' not in last
    assert last['error']['type'] == 'CensoredUnreturnedAttempt' and last['request_metadata_reconstructed_from_freeze']
    assert last['closure_utc'] == receipt['closure_utc'] == intent['closure_utc']
    assert digest(PANEL / 'responses.jsonl') == receipt['response_sha256'] == intent['raw_ledger_sha256']
    assert digest(PANEL / 'effective_attempts.jsonl') == receipt['effective_attempts_sha256']
    packet = {r['case_id']: r for r in lines(ROOT / 'outputs/finance-document-audit-v1/reviewer_a.jsonl')}
    for r in events:
        p = packet[r['case_id']]
        prompt = json.dumps({'question': p['question'], 'original_context': p['original_context']}, ensure_ascii=False, sort_keys=True)
        body = {'model': MODELS[r['model_key']], 'temperature': 0, 'max_tokens': 1024, 'reasoning': {'enabled': False},
                'response_format': {'type': 'json_object'}, 'provider': {'only': ['siliconflow/fp8'], 'allow_fallbacks': False, 'require_parameters': True},
                'messages': [{'role': 'system', 'content': SYSTEMS[r['condition']]}, {'role': 'user', 'content': prompt}]}
        assert hashlib.sha256(prompt.encode()).hexdigest() == r['prompt_sha256']
        assert hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True).encode()).hexdigest() == r['request_sha256']
        if not r.get('error'):
            assert r['provider'] == r['raw_response']['provider'] == 'SiliconFlow'
            assert r['returned_model'] == r['raw_response']['model'] == MODELS[r['model_key']]
            assert r['usage'] == r['raw_response']['usage'] and r['text'] == r['raw_response']['choices'][0]['message']['content']
    assert sum(bool(r.get('error')) for r in raw) == 7
    known = sum((Decimal(str(r['usage']['cost'])) for r in raw if r.get('usage', {}).get('cost') is not None), Decimal(0))
    assert str(known) == receipt['reported_cost_usd'] == '0.087702416'
    assert sum(r.get('usage', {}).get('cost') is None for r in events) == receipt['missing_cost_records'] == 8
    saved = lines(PANEL / 'paired_scores.jsonl')
    assert len(saved) == 384 and [(s['model_key'], s['condition'], s['case_id']) for s in saved] == keys
    independent = []
    for r, s in zip(events, saved):
        ref = refs[r['case_id']]
        c, error = parse(r['text'])
        if r.get('error') or r.get('provider') != 'SiliconFlow':
            c, error = None, 'request_or_provider_failure'
        match, value = matches(ref, c)
        n = native(ref['source'], targets[r['case_id']], c)
        frac = None
        if ref['source'] == 'finqa' and c is not None:
            changed = dict(c)
            if c['status'] == 'answer' and c['unit'] in ['percent', 'percentage_points']:
                changed['value'] = format(Decimal(c['value']) / 100, 'f')
            frac = native('finqa', targets[r['case_id']], changed)
        assert c == s['candidate'] and error == s['parse_error'], r['case_id']
        assert match == s['locked_comparator']['matches'] and (ref['joint_status'] == ELIGIBLE) == s['locked_comparator']['eligible']
        assert n == s['native_or_adapted'] and frac == s['finqa_percent_fraction_sensitivity']
        assert s['semantic_or_trace_certification'] is False
        projected, additional = projection(ref, match, value)
        independent.append({**r, 'source': ref['source'], 'state': error or c['status'], 'match': match,
                            'eligible': ref['joint_status'] == ELIGIBLE, 'native': n, 'fraction': frac,
                            'projected': projected, 'additional': additional})
    result = read(PANEL / 'results.json')
    assert result == read(REPLAY / 'results.json')
    counts = {}
    for m in MODELS:
        counts[m] = {}
        for arm in SYSTEMS:
            subset = [r for r in independent if r['model_key'] == m and r['condition'] == arm]
            expected = result['models'][m][arm]
            assert aggregate(subset) == expected['aggregate']
            counts[m][arm] = {'strict_numeric_answers': sum(r['state'] == 'answer' for r in subset),
                              'locked_matches': sum(r['match'] is True for r in subset),
                              'later_precision_matches': sum(r['projected'] is True for r in subset)}
            for source in ['finqa', 'tatqa']:
                ss = [r for r in subset if r['source'] == source]
                e = expected['sources'][source]
                assert len(ss) == 48 and aggregate(ss) == {k: e[k] for k in aggregate(ss)}
                assert {'matches': sum(r['projected'] is True for r in ss), 'additional_rounded_matches': sum(r['additional'] for r in ss)} == e['later_precision_diagnostic']
                ns = [r['native'] for r in ss if r['native']['eligible']]
                ts = [n for n in ns if 'answer_em' in n]
                channels = {'attempts': 48, 'native_eligible': len(ns), 'tatqa_answer_em_sum': sum(n['answer_em'] for n in ts),
                            'tatqa_answer_f1_sum': sum(n['answer_f1'] for n in ts), 'tatqa_scale_correct': sum(n['scale_score'] == 1 for n in ts),
                            'tatqa_answer_and_scale_correct': sum(n['answer_em'] == n['scale_score'] == 1 for n in ts)}
                assert channels == e['native_channels']
                if source == 'finqa':
                    assert aggregate(ss, 'fraction') == e['percent_fraction_sensitivity']
    report = {'executive_summary': 'PASS saved384-event coverage, requests, freeze integrity and independent scalar/precision rescore; no semantic truth certification.',
              'status': 'PASS', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'validator_sha256': digest(__file__),
              'actual_api_records': 383, 'returned_transport_failures': 7, 'censored_attempts': 1, 'planned_attempts': 384,
              'strict_subset_per_arm': 62, 'all_request_hashes_checked': 384, 'reported_panel_cost_usd': str(known),
              'unknown_cost_records': 8, 'counts': counts, 'input_hashes': checked,
              'paired_scores_sha256': digest(PANEL / 'paired_scores.jsonl'), 'results_sha256': digest(PANEL / 'results.json'),
              'native_sources': verify_native_sources(), 'native_authored_controls': replay_authored_controls(),
              'independence': 'Own JSON validation and exact Fraction comparisons/projections; shared hash-verified native TAT adapter, independently checked FinQA scalar credits; locked references reused.',
              'fresh_inference': False, 'human_adjudication': False, 'semantic_truth_certification': False}
    with args.output.open('x') as stream:
        stream.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'counts': counts, 'receipt': str(args.output)}))


if __name__ == '__main__':
    main()
