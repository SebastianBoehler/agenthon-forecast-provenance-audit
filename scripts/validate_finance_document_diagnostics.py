"""Executive summary: independently check saved posthoc document diagnostics.

Own conservative recovery, safe AST Decimal arithmetic, exact Fraction matching
and native-normalization calculation. Reuses the independently reviewed TAT
adapter. No inference, annotation-program execution or original-output writes.
"""
import argparse
import ast
import json
import math
import re
import runpy
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from pathlib import Path

import validate_finance_document_final as prior

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/finance-document-diagnostics-v1'
FIELDS = {'status', 'value', 'unit', 'scale', 'calculation', 'evidence'}


def recover(response):
    if response.get('error') or response.get('provider') != 'SiliconFlow' or response.get('collector_event'):
        return None, 'request_provider_or_censored_failure'
    def unique(pairs):
        if len(dict(pairs)) != len(pairs):
            raise ValueError('duplicate key')
        return dict(pairs)
    def reject(_):
        raise ValueError('nonstandard constant')
    try:
        obj = json.loads(response['text'], parse_float=Decimal, object_pairs_hook=unique, parse_constant=reject)
    except (ValueError, TypeError, KeyError):
        return None, 'invalid_single_json_object'
    if not isinstance(obj, dict):
        return None, 'not_json_object'
    if not FIELDS <= obj.keys():
        return None, 'missing_original_fields'
    if not isinstance(obj['unit'], str) or not obj['unit'].strip():
        return None, 'missing_or_nonstring_unit'
    if not isinstance(obj['scale'], str) or obj['scale'] not in ['none', 'thousand', 'million', 'billion']:
        return None, 'invalid_scale'
    v = obj['value']
    if not (type(v) in [int, Decimal] or isinstance(v, str) and re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)', v)):
        return None, 'not_literal_plain_numeric_value'
    d = Decimal(v)
    if not d.is_finite() or not math.isfinite(float(d)):
        return None, 'nonfinite_numeric_value'
    return {**obj, 'status': 'answer', 'value': format(d, 'f')}, None


def execute(expression):
    if not isinstance(expression, str) or not expression.strip() or len(expression) > 2048:
        raise ValueError('expression bounds')
    tree = ast.parse(expression, mode='eval')
    if len(list(ast.walk(tree))) > 256:
        raise ValueError('AST bounds')
    def number(node):
        if isinstance(node, ast.Constant) and type(node.value) in [int, float]:
            v = Decimal(ast.get_source_segment(expression, node).replace('_', ''))
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            v = number(node.operand)
            v = v if isinstance(node.op, ast.UAdd) else -v
        elif isinstance(node, ast.BinOp):
            a, b = number(node.left), number(node.right)
            op = type(node.op)
            if op == ast.Add:
                v = a + b
            elif op == ast.Sub:
                v = a - b
            elif op == ast.Mult:
                v = a * b
            elif op == ast.Div:
                v = a / b
            elif op == ast.Pow and b == b.to_integral_value() and abs(b) <= 32:
                v = a ** int(b)
            else:
                raise ValueError('unsupported operator')
        else:
            raise ValueError('non-arithmetic node')
        if not v.is_finite() or abs(v) > Decimal('1e100'):
            raise ValueError('value bounds')
        return v
    with localcontext() as ctx:
        ctx.prec = 60
        return number(tree.body)


def supported(expression):
    try:
        return execute(expression)
    except (ArithmeticError, ValueError, SyntaxError, RecursionError):
        return None


def normal(value, scale):
    # Pinned primary normalization: numeric conversion round4, round2, scale, format4.
    factor = {'': 1, 'thousand': 1000, 'million': 10**6, 'billion': 10**9, 'percent': .01}[scale]
    return ['%.4f' % (round(round(float(value), 4), 2) * factor)]


def controls(primary):
    base = dict(status='numeric_answer', value='12.34', unit='USD', scale='none', calculation='2+3', evidence=[])
    cases = []
    def check(name, body, wanted, error=None):
        response = {'text': body, 'provider': 'SiliconFlow'}
        c, e = recover(response)
        pc, pe = primary['recover'](response, {'parse_error': 'authored'})
        assert c == pc and e == pe['error'] and (c is not None) == wanted
        if error:
            assert e == error
        cases.append({'id': name, 'text': body, 'recovered': wanted, 'error': e, 'status': 'PASS'})
    for name, changes in [('plain', {}), ('int', {'value': 12}), ('float', {'value': 12.34}),
                          ('mistagged_boolean_status', {'status': 'non_numeric_answer'}), ('extra', {'unused': 8})]:
        check(name, json.dumps({**base, **changes}), True)
    check('JSON exponent numeric', json.dumps(base).replace('"12.34"', '1.234e1'), True)
    for name, value in [('bool', True), ('null', None), ('yes', 'yes'), ('decorated', '12.34%'),
                        ('string_exponent', '1e2'), ('comma', '1,234'), ('nonfinite', 'NaN')]:
        check(name, json.dumps({**base, 'value': value}), False, 'not_literal_plain_numeric_value')
    for field in ['status', 'unit', 'evidence']:
        check('missing_' + field, json.dumps({k: v for k, v in base.items() if k != field}), False, 'missing_original_fields')
    for name, body in [('duplicate', json.dumps(base)[:-1] + ',"value":"3"}'),
                       ('nested_duplicate', json.dumps({**base, 'evidence': []}).replace('[]', '[{"x":1,"x":2}]')),
                       ('two_objects', json.dumps(base) + '{}'), ('markdown', '```' + json.dumps(base) + '```'),
                       ('prose', 'Answer: ' + json.dumps(base)), ('nonstandard', json.dumps(base).replace('"12.34"', 'NaN'))]:
        check(name, body, False, 'invalid_single_json_object')
    check('invalid_scale', json.dumps({**base, 'scale': 'trillion'}), False, 'invalid_scale')
    for expression, wanted in [('1+2', True), ('1/3', True), ('2**-3', True), ('1+2=3', False),
                               ('Assume annual; 1+2', False), ('x+2', False), ('round(1/3)', False),
                               ('1<2', False), ('1/0', False), ('2**33', False), ('True+1', False)]:
        actual = supported(expression)
        try:
            frozen = primary['calculate'](expression)
        except (ValueError, SyntaxError, ArithmeticError, RecursionError):
            frozen = None
        assert actual == frozen and (actual is not None) == wanted
        cases.append({'id': 'arithmetic', 'expression': expression, 'supported': wanted, 'status': 'PASS'})
    return cases


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    primary = runpy.run_path(str(OUT / 'diagnose.py'))  # Definitions only; never invoke its writer.
    controls_result = controls(primary)
    hashes = {}
    for name in ['protocol_freeze.json', 'implementation_freeze.json']:
        for path, expected in prior.read(OUT / name)['files_sha256'].items():
            assert prior.digest(ROOT / path) == expected, path
            hashes[path] = expected
    assert 'src/finance_document_review/arithmetic.py' not in hashes
    arithmetic_hash = prior.digest(ROOT / 'src/finance_document_review/arithmetic.py')
    frozen_controls = prior.read(OUT / 'authored_controls.json')
    assert frozen_controls['count'] == len(frozen_controls['controls']) == 33
    assert all(c['status'] == 'PASS' for c in frozen_controls['controls'])
    responses = prior.lines(prior.PANEL / 'effective_attempts.jsonl')
    rows = prior.lines(OUT / 'rows.jsonl')
    strict = prior.lines(prior.PANEL / 'paired_scores.jsonl')
    refs = {r['case_id']: r for r in prior.lines(prior.REVIEW / 'pre_target_combined.jsonl')}
    targets = {r['case_id']: r['original_annotation'] for r in prior.lines(prior.REPLAY / 'compact_native_annotations.jsonl')}
    def key(r):
        return r['model_key'], r['condition'], r['case_id']
    assert len(rows) == len(responses) == len(strict) == 384
    assert len({key(r) for r in rows}) == 384
    assert {key(r) for r in rows} == {(m, a, c) for m in prior.MODELS for a in prior.SYSTEMS for c in refs}
    supported_eligible = collapse_supported = 0
    transitions = Counter()
    for i, (response, row, s) in enumerate(zip(responses, rows, strict), 1):
        assert key(response) == key(row) == key(s) and row['effective_ledger_line'] == i
        ref, annotation = refs[row['case_id']], targets[row['case_id']]
        assert row['joint_status'] == ref['joint_status'] and row['source'] == ref['source']
        assert row['original_strict'] == {'numeric_answer': s['candidate'] is not None and s['candidate']['status'] == 'answer',
            'parse_error': s['parse_error'], 'locked_comparator': s['locked_comparator'], 'native_or_adapted': s['native_or_adapted']}
        c, error = recover(response)
        assert c == row['recovered_candidate'] and error == row['recovery']['error']
        match, _ = prior.matches(ref, c)
        assert match == row['recovered_locked']['matches']
        assert prior.native(ref['source'], annotation, c) == row['recovered_native']
        execution = None if c is None else supported(c['calculation'])
        a = row['arithmetic']
        assert (execution is not None) == a['supported']
        if execution is None:
            continue
        assert execution == Decimal(a['executed_value'])
        assert (execution == Decimal(c['value'])) == a['reported_value_exact_agreement']
        changed = {**c, 'value': format(execution, 'f')}
        executed_match, _ = prior.matches(ref, changed)
        assert executed_match == a['locked_comparator']['matches']
        assert prior.native(ref['source'], annotation, changed) == a['native_or_adapted']
        if ref['joint_status'] == prior.ELIGIBLE:
            supported_eligible += 1
            transitions[str((match, executed_match))] += 1
        if ref['source'] == 'tatqa' and a['native_or_adapted']['eligible']:
            collapse_supported += 1
            scale = a['native_or_adapted']['native_prediction_scale']
            equal = normal(c['value'], scale) == normal(changed['value'], scale)
            assert equal == a['tatqa_primary_normalization_equal']
    saved = prior.read(OUT / 'results.json')
    assert primary['summary'](rows) == saved['all']
    for model in prior.MODELS:
        assert primary['paired'](rows, model) == saved['paired_reminder'][model]
        for arm in prior.SYSTEMS:
            subset = [r for r in rows if r['model_key'] == model and r['condition'] == arm]
            assert len(subset) == 96 and primary['summary'](subset) == saved['models'][model][arm]['all']
            for source in ['finqa', 'tatqa']:
                ss = [r for r in subset if r['source'] == source]
                assert len(ss) == 48 and primary['summary'](ss) == saved['models'][model][arm]['sources'][source]
    assert transitions == saved['all']['reported_to_executed_locked_transitions_supported']
    receipt = {'executive_summary': 'PASS independent384-row recovery/arithmetic/native-normalization checks; posthoc evidence and incomplete initial dependency binding remain explicit.',
        'status': 'PASS', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'validator_sha256': prior.digest(__file__),
        'attempts': 384, 'supported_expressions': 179, 'supported_eligible_attempts': supported_eligible,
        'supported_tatqa_normalization_attempts': collapse_supported, 'transitions': dict(transitions),
        'independent_authored_controls': controls_result, 'saved_control_records': 33,
        'input_hashes': hashes, 'rows_sha256': prior.digest(OUT / 'rows.jsonl'), 'results_sha256': prior.digest(OUT / 'results.json'),
        'arithmetic_present_hash_verified_after_results': arithmetic_hash, 'arithmetic_in_initial_diagnostic_freeze': False,
        'independence': 'Own conservative JSON recovery and AST Decimal60 calculation; prior independent Fraction matcher; independent float normalization, shared hash-pinned native TAT adapter. Primary summaries replayed from independently validated rows.',
        'new_inference': False, 'semantic_certification': False}
    with args.output.open('x') as stream:
        stream.write(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: receipt[k] for k in ['status', 'attempts', 'supported_expressions', 'supported_eligible_attempts', 'supported_tatqa_normalization_attempts', 'transitions']}))


if __name__ == '__main__':
    main()
