"""Executive summary: replay closed transfer attempts without inference or semantic certification."""

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from finance_quantity_analysis.endpoints import arithmetic, candidate, decode, judge, number, raw_evidence, score
from finance_quantity_analysis.provenance import digest, response_usage, rows, verify

ARMS = ('baseline','quantity_reminder')
ENDPOINTS = ('reported_numeric_typed_match','expression_numeric_typed_match','judge_supported')
BOOLEAN_SCORES = ('primary_eligible','schema_valid','reported_numeric_typed_match',
                  'expression_numeric_typed_match','reported_expression_consistent','native_literal_exact')


def write(directory, name, value, jsonl=False):
    with (directory/name).open('x') as f:
        if jsonl:
            for r in value: f.write(json.dumps(r, ensure_ascii=False)+'\n')
        else: json.dump(value, f, ensure_ascii=False, indent=2); f.write('\n')


def check_saved(scored, saved):
    for field in BOOLEAN_SCORES: assert scored[field] == saved[field], field
    assert (scored['schema_error'] is None) == (saved['schema_error'] is None)
    if 'expression_value' in scored:
        x, y = number(scored['expression_value']), number(saved['expression_value'])
        assert abs(x-y) <= max(Fraction(1,10**54),abs(y)/10**54), 'arithmetic precision discrepancy'


def parsed_audit(text, context):
    try: raw = decode(text)
    except (ValueError, TypeError): raw = None
    expression = raw.get('calculation') if isinstance(raw,dict) else None
    supported = False
    try: arithmetic(expression); supported = True
    except (ValueError, TypeError, ArithmeticError, SyntaxError): pass
    audit = raw_evidence(text,context)
    return dict(whole_expression_supported=supported,
                evidence_invalid_paths=audit['invalid_paths'],
                evidence_unavailable=audit['unavailable'], evidence_empty=audit['empty'])



def usage_counts(rs, phase):
    recorded = [r for r in rs if r[phase+'_recorded']]
    usages = [r[phase+'_usage'] for r in recorded]
    costs = []
    for usage in usages:
        try:
            cost=Decimal(str(usage['cost']))
            if not isinstance(usage['cost'],bool) and cost.is_finite() and cost>=0: costs.append(cost)
        except (KeyError,ArithmeticError,ValueError): pass
    token_fields = {}
    for field in ['prompt_tokens','completion_tokens','total_tokens']:
        values=[u[field] for u in usages if type(u.get(field)) is int and u[field]>=0]
        token_fields[field]={'sum_known':sum(values),'records_known':len(values)}
    reasoning=[u['completion_tokens_details'].get('reasoning_tokens') for u in usages
               if isinstance(u.get('completion_tokens_details'),dict)]
    reasoning=[x for x in reasoning if type(x) is int and x>=0]
    return dict(known_cost_usd=str(sum(costs,Decimal(0))),unknown_cost_records=len(usages)-len(costs),
                token_fields=token_fields,reasoning_tokens_known=sum(reasoning),
                reasoning_tokens_records_known=len(reasoning),
                at_output_cap=sum(type(u.get('completion_tokens')) is int and u['completion_tokens']>=1024 for u in usages))


def counts(rs):
    return dict(attempts=len(rs),answer_usage=usage_counts(rs,'answer'),judge_usage=usage_counts(rs,'judge'), provisional_eligible=sum(r['score']['primary_eligible'] for r in rs),
        provisional_ineligible=sum(not r['score']['primary_eligible'] for r in rs),
        answer_recorded=sum(r['answer_recorded'] for r in rs), judge_recorded=sum(r['judge_recorded'] for r in rs),
        judge_collection_status=dict(Counter(r['judge_collection_status'] for r in rs)),
        judge_not_started=sum(not r['judge_recorded'] for r in rs),
        judge_successful_returns=sum(r['judge_recorded'] and not r['judge_runtime_error'] for r in rs),
        strict_schema_valid=sum(r['score']['schema_valid'] for r in rs),
        strict_numeric=sum(r['candidate_status']=='answer' for r in rs),
        candidate_status=dict(Counter(r['candidate_status'] for r in rs)),
        reported_matches=sum(r['score']['reported_numeric_typed_match'] for r in rs),
        expression_matches=sum(r['score']['expression_numeric_typed_match'] for r in rs),
        reported_expression_consistent=sum(r['score']['reported_expression_consistent'] for r in rs),
        native_literal_available=sum(r['score']['native_literal_exact'] is not None for r in rs),
        native_literal_exact=sum(r['score']['native_literal_exact'] is True for r in rs),
        whole_expression_supported=sum(r['answer_audit']['whole_expression_supported'] for r in rs),
        answer_invalid_evidence=sum(bool(r['answer_audit']['evidence_invalid_paths']) for r in rs),
        answer_evidence_unavailable=sum(r['answer_audit']['evidence_unavailable'] for r in rs),
        answer_empty_evidence=sum(r['answer_audit']['evidence_empty'] for r in rs),
        judge_verdict=dict(Counter(r['judge']['effective_verdict'] for r in rs)),
        judge_parse_failure=sum(r['judge_recorded'] and r['judge_error'] is not None for r in rs),
        judge_parse_failure_on_successful_return=sum(r['judge_recorded'] and not r['judge_runtime_error'] and r['judge_error'] is not None for r in rs),
        judge_protocol_violation=sum(r['judge_recorded'] and r['judge']['protocol_violation'] for r in rs),
        judge_invalid_evidence=sum(bool(r['judge_invalid_evidence']) for r in rs),
        judge_evidence_unavailable=sum(r['judge_evidence_unavailable'] for r in rs),
        judge_empty_evidence=sum(r['judge_empty_evidence'] for r in rs),
        judge_empty_operand_checks=sum(r['judge_empty_operand_checks'] for r in rs),
        judge_supported_empty_evidence=sum(r['judge_supported'] and r['judge_empty_evidence'] for r in rs),
        judge_supported_without_numeric_answer=sum(r['judge_supported'] and r['candidate_status']!='answer' for r in rs),
        answer_finish=dict(Counter(r['answer_finish'] for r in rs)),
        judge_finish=dict(Counter(r['judge_finish'] for r in rs)),
        answer_truncated=sum(r['answer_finish']=='length' for r in rs),
        judge_truncated=sum(r['judge_finish']=='length' for r in rs),
        answer_runtime_error=sum(r['answer_runtime_error'] for r in rs),
        judge_runtime_error=sum(r['judge_runtime_error'] for r in rs))


def paired(rs, eligible_only):
    by = {(r['case_id'],r['arm']):r for r in rs}
    cases = sorted({r['case_id'] for r in rs if not eligible_only or r['score']['primary_eligible']})
    result = {'questions':len(cases)}
    for endpoint in ENDPOINTS:
        cells = {str(a)+'->'+str(b):0 for a in (False,True) for b in (False,True)}
        for c in cases:
            vals = [by[c,arm]['judge_supported'] if endpoint=='judge_supported'
                    else by[c,arm]['score'][endpoint] for arm in ARMS]
            cells[str(vals[0])+'->'+str(vals[1])] += 1
        result[endpoint] = cells
    return result


def summary(rs, provenance):
    eligible = [r for r in rs if r['score']['primary_eligible']]
    contingencies = {}
    for endpoint in ENDPOINTS[:2]:
        contingencies[endpoint] = {arm:{str(v):{s:0 for s in ['supported','contradicted','ambiguous','unassessable']}
                                               for v in (False,True)} for arm in ARMS}
        for r in eligible:
            contingencies[endpoint][r['arm']][str(r['score'][endpoint])][r['judge']['effective_verdict']] += 1
    joint = {arm:{str(a)+'/'+str(b):dict.fromkeys(['supported','contradicted','ambiguous','unassessable'],0)
                  for a in (False,True) for b in (False,True)} for arm in ARMS}
    for r in eligible:
        cell='/'.join(str(r['score'][endpoint]) for endpoint in ENDPOINTS[:2])
        joint[r['arm']][cell][r['judge']['effective_verdict']] += 1
    return dict(executive_summary='Closed fixed-panel numerical and same-model proxy accounting; no expert correctness certification.',
        created_utc=datetime.now(timezone.utc).isoformat(), questions=32, planned_answer_attempts=64,
        planned_judge_attempts=64, provisional_reference_kind='AI_technical_readings',
        provisional_eligible_questions=22, unknown_or_ineligible_questions=10,
        all_attempts=counts(rs), by_arm={a:counts([r for r in rs if r['arm']==a]) for a in ARMS},
        by_source_arm={s:{a:counts([r for r in rs if r['arm']==a and r['source']==s]) for a in ARMS}
                       for s in sorted({r['source'] for r in rs})},
        paired_provisional_eligible_22=paired(rs,True), paired_all_32=paired(rs,False),
        judge_vs_numerical_match_only=contingencies,
        judge_by_reported_expression_match_cells=joint, provenance=provenance,
        limitations=['References and the same-model judge are AI technical proxies, not independent expert truth.',
            'Native literal equality has no scaling, tolerance or native evaluator adaptation; it is not FinQA or TAT official accuracy.',
            'Both arms prospectively share pure arithmetic grammar; the earlier assumption-prose confound is not reused.',
            'Numerical comparator enforces typed units but does not certify quantity grounding or currency identity.',
            'All planned attempts remain counted, including ineligible references, abstentions, malformed answers and judge failures.',
            'Judge supported is a same-model diagnostic verdict; contingencies compare it only with numerical match.',
            'Fixed baseline-before-reminder ordering and one model/provider limit causal and cross-family claims.',
            'Compact replay covers numerical/parser accounting, not original evidence pointers, request/source binding or semantics.'])


def compact_record(record):
    # Retain validated accounting flags without model-generated judge rationales.
    r=dict(record)
    r['judge']={k:v for k,v in record['judge'].items() if k!='judgment'}
    return r


def full(study):
    cases = rows(study/'experiment_packet.jsonl')
    assert len(cases)==len({c['case_id'] for c in cases})==32
    assert Counter(c['source'] for c in cases)=={'finqa':16,'tatqa':16}
    assert sum(c['provisional_reference']['eligible'] for c in cases)==22
    collection = study/'collection'
    run = json.loads((collection/'run.json').read_text())
    assert run['state'] in {'complete','stopped'}, 'Wait for collection closure'
    statuses = json.loads((collection/'attempt_status.json').read_text())
    calls = rows(collection/'calls.jsonl')
    provenance = verify(ROOT,study,cases,run,statuses,calls)
    by_call = {(c['case_id'],c['arm'],c['phase']):c for c in calls}
    by_status = {(s['case_id'],s['arm']):s for s in statuses}
    result, portable = [], []
    for case in cases:
        for arm in ARMS:
            status = by_status[case['case_id'],arm]
            answer = by_call.get((case['case_id'],arm,'answer'))
            judged = by_call.get((case['case_id'],arm,'judge'))
            text = answer['text'] if answer else ''
            scored = score(text,case['provisional_reference'],case.get('native_target'))
            if 'scoring' in status: check_saved(scored,status['scoring'])
            a, error = candidate(text)
            j, je = judge(judged['text'] if judged else '',case['original_context'],error)
            if 'quantity_review' in status:
                saved = status['quantity_review']
                assert j==saved and (je is None)==(status['judge_parser_error'] is None)
            judge_audit = raw_evidence(judged['text'] if judged else '',case['original_context'])
            r = dict(case_id=case['case_id'],source=case['source'],arm=arm,score=scored,
                candidate_status=a['status'] if a else 'invalid_or_missing', judge=j,judge_error=je,
                judge_supported=j['effective_verdict']=='supported',
                answer_audit=parsed_audit(text,case['original_context']),judge_invalid_evidence=judge_audit['invalid_paths'],
                judge_evidence_unavailable=judge_audit['unavailable'],judge_empty_evidence=judge_audit['empty'],
                judge_empty_operand_checks=bool(j['judgment'] is not None and j['judgment']['operand_checks']==[]),
                answer_recorded=answer is not None,judge_recorded=judged is not None,
                judge_collection_status=status['judge_status'],
                answer_finish=answer.get('finish_reason') if answer else 'not_recorded',
                judge_finish=judged.get('finish_reason') if judged else 'not_recorded',
                answer_usage=response_usage(answer),judge_usage=response_usage(judged),
                answer_runtime_error=bool(answer and answer.get('error')),
                judge_runtime_error=bool(judged and judged.get('error')))
            result.append(r)
            portable.append(dict(case_id=case['case_id'],source=case['source'],arm=arm,
                provisional_reference=case['provisional_reference'],native_target=case.get('native_target'),
                candidate_text=text,expected_numeric_score=scored,validated_accounting=compact_record(r)))
    assert len(result)==64
    return result,portable,provenance


def replay(path):
    projected = rows(path)
    assert len(projected)==64 and len({(r['case_id'],r['arm']) for r in projected})==64
    assert {r['arm'] for r in projected}==set(ARMS)
    assert len({r['case_id'] for r in projected})==32
    assert sum(r['provisional_reference']['eligible'] for r in projected)==44
    for arm in ARMS: assert Counter(r['source'] for r in projected if r['arm']==arm)=={'finqa':16,'tatqa':16}
    result = []
    for p in projected:
        s = score(p['candidate_text'],p['provisional_reference'],p['native_target'])
        assert s==p['expected_numeric_score']
        r = p['validated_accounting']
        assert r['score']==s and (r['case_id'],r['arm'],r['source'])==(p['case_id'],p['arm'],p['source'])
        result.append(r)
    return result,projected,dict(scope='compact numerical replay; pointer/request/semantic validation not rerun',
                               portable_input_sha256=digest(path))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study-dir',type=Path,default=ROOT/'outputs/finance-quantity-transfer-v1')
    p.add_argument('--portable-input',type=Path)
    p.add_argument('--judge-v2-dir',type=Path)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    args.study_dir=args.study_dir.resolve()
    if args.judge_v2_dir: args.judge_v2_dir=args.judge_v2_dir.resolve()
    started=datetime.now(timezone.utc).isoformat()
    result,portable,provenance=replay(args.portable_input) if args.portable_input else full(args.study_dir)
    input_files=[args.portable_input] if args.portable_input else [args.study_dir/x for x in
        ['experiment_packet.jsonl','experiment_freeze.json','collection/run.json','collection/attempt_status.json','collection/calls.jsonl','spend_ledger.jsonl']]
    inputs={str(f):digest(f) for f in input_files}
    v2_rows=[]
    v2_provenance=None
    if args.portable_input:
        assert args.judge_v2_dir is None, 'Compact mode cannot audit original V2 requests/pointers'
        v2_rows=[p['validated_v2_accounting'] for p in portable if 'validated_v2_accounting' in p]
        assert len(v2_rows) in (0,64)
        for r,p in zip(v2_rows,portable):
            assert r['score']==p['expected_numeric_score']
            assert (r['case_id'],r['arm'])==(p['case_id'],p['arm'])
        v2_provenance={'scope':'Saved validated judge accounting only; context/request checks not rerun'}
    elif args.judge_v2_dir:
        from finance_quantity_analysis.judge_extension import assess
        v2_rows,v2_provenance=assess(ROOT,args.study_dir,args.judge_v2_dir,result)
        for p,r in zip(portable,v2_rows): p['validated_v2_accounting']=compact_record(r)
        extra=args.judge_v2_dir
        for path in [extra/'plan_freeze.json',extra/'collection/run.json',extra/'collection/calls.jsonl',extra/'collection/attempt_status.json']:
            inputs[str(path)]=digest(path)
    output=args.output or args.study_dir/'independent-analysis'
    output.mkdir(parents=True,exist_ok=False)
    write(output,'rows.jsonl',result,True)
    write(output,'portable_numeric_packet.jsonl',portable,True)
    measured=summary(result,provenance)
    if v2_rows:
        write(output,'judge_v2_rows.jsonl',v2_rows,True)
        measured['separate_judge_v2_diagnostic']=summary(v2_rows,v2_provenance)
    write(output,'results.json',measured)
    code=[Path(__file__),*sorted((ROOT/'src/finance_quantity_analysis').glob('*.py'))]
    receipt=dict(executive_summary='Saved-output replay only; original frozen artifacts unchanged.',
        started_utc=started,completed_utc=datetime.now(timezone.utc).isoformat(),inference_performed=False,
        source_contexts_required_for_full_audit=True,
        compact_replay_excludes=['full original contexts','request/source binding','evidence-pointer validation','semantic adjudication'],
        portable_mode=bool(args.portable_input),input_sha256=inputs,code_sha256={str(f.relative_to(ROOT)):digest(f) for f in code},
        output_sha256={f.name:digest(f) for f in output.iterdir()},
        command=' '.join(sys.argv),independent_arithmetic='Exact Fraction AST evaluation with bounded numerical grammar')
    write(output,'receipt.json',receipt)
    print(json.dumps({'output':str(output),'attempts':len(result),'scope':'compact' if args.portable_input else 'full'}))


if __name__=='__main__': main()
