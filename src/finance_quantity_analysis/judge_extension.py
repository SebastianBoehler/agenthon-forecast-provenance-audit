"""Executive summary: replay V2 as a separate pointer-format diagnostic on V1 answers."""

import json
import platform
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path

from finance_quantity_judge_v2.protocol import SYSTEM
from .endpoints import candidate, judge, raw_evidence
from .provenance import MALFORMED_RULE, MODEL, PROVIDER, budget_audit, digest, digest_bytes, record_check, request_check, response_usage, rows


def assess(root, study, directory, original_rows):
    run=json.loads((directory/'collection/run.json').read_text())
    assert run['state'] in {'complete','stopped'}, 'Wait for V2 closure'
    assert run['mode']=='saved_v1_answers' and run['planned_judges']==64 and run['answer_calls']==0
    frozen=json.loads((directory/'plan_freeze.json').read_text())
    assert run['freeze']==frozen
    assert digest_bytes(SYSTEM.encode())==frozen['system_sha256']
    assert frozen['phase']=='judge_v2' and frozen['financial_judges']==64 and frozen['answer_calls']==0
    assert frozen['authored_preflight_judges']==2 and frozen['selected_v1_outputs_read_by_author'] is False
    assert frozen['model']==MODEL and frozen['provider']==PROVIDER
    assert frozen['study_id']=='finance_quantity_transfer_v1'
    assert frozen['study_cap_usd']=='2' and frozen['aggregate_cap_usd']=='10'
    for record in frozen['source_files']+frozen['unchanged_v1_sources']+frozen['inputs']: record_check(root,record)
    assert frozen['python_version']==platform.python_version()
    assert frozen['python_executable']==str(Path(sys.executable).resolve())
    assert frozen['created_utc'] <= run['started_utc'] <= run['completed_utc']
    for path, expected in run['input_hashes'].items(): assert digest(root/path)==expected,path
    required={str((study/x).relative_to(root)) for x in
              ['collection/run.json','collection/calls.jsonl','experiment_packet.jsonl']}
    assert set(run['input_hashes'])==required
    v1_run=json.loads((study/'collection/run.json').read_text())
    assert v1_run['state']=='complete' and v1_run['completed_utc'] <= run['started_utc']
    cases={c['case_id']:c for c in rows(study/'experiment_packet.jsonl')}
    v1_calls=rows(study/'collection/calls.jsonl')
    answers={(c['case_id'],c['arm']):c for c in v1_calls if c['phase']=='answer'}
    v1_statuses={(s['case_id'],s['arm']):s for s in json.loads((study/'collection/attempt_status.json').read_text())}
    expected=[(r['case_id'],r['arm']) for r in original_rows]
    calls=rows(directory/'collection/calls.jsonl')
    status=json.loads((directory/'collection/attempt_status.json').read_text())
    assert len(status)==64 and [(s['case_id'],s['arm']) for s in status]==expected
    assert [(c['case_id'],c['arm']) for c in calls]==expected[:len(calls)]
    assert len({c['call_id'] for c in calls})==len(calls)
    by_call={(c['case_id'],c['arm']):c for c in calls}
    by_status={(s['case_id'],s['arm']):s for s in status}
    result=[]
    previous_end=None
    for original in original_rows:
        key=original['case_id'],original['arm']
        case=cases[key[0]]
        record=by_call.get(key)
        answer=answers[key]
        _, error=candidate(answer['text'])
        j, je=judge(record['text'] if record else '',case['original_context'],error)
        s=by_status[key]
        if 'quantity_review' in s:
            assert j==s['quantity_review'] and (je is None)==(s['judge_parser_error'] is None)
        if record:
            assert record['phase']=='judge_v2' and record['source']==case['source']
            assert record['target_model']==MODEL and record['target_provider']==PROVIDER
            assert record['call_id']==f'finance_quantity_transfer_v1:{key[0]}:{key[1]}:judge_v2'
            old_error=v1_statuses[key]['scoring']['schema_error']
            payload=dict(question=case['question'],original_context=case['original_context'],
                candidate_text=answer['text'],candidate_parser_valid=old_error is None,
                candidate_parser_error=old_error,
                malformed_candidate_rule=MALFORMED_RULE)
            request_check(record,SYSTEM,payload)
            assert run['started_utc'] <= record['started_utc'] <= record['completed_utc']
            if previous_end: assert record['started_utc'] >= previous_end
            previous_end=record['completed_utc']
            if not record.get('error'):
                raw=record['raw_response']
                assert record['provider']==raw['provider']=='SiliconFlow'
                assert record['returned_model']==raw['model']==MODEL
                assert record['text']==(raw['choices'][0]['message'].get('content') or '')
                assert record['finish_reason']==raw['choices'][0]['finish_reason']
        judgment=j['judgment']
        audit=raw_evidence(record['text'] if record else '',case['original_context'])
        result.append({**original,'judge':j,'judge_error':je,'judge_supported':j['effective_verdict']=='supported',
            'judge_invalid_evidence':audit['invalid_paths'],'judge_recorded':record is not None,
            'judge_evidence_unavailable':audit['unavailable'],'judge_empty_evidence':audit['empty'],
            'judge_empty_operand_checks':bool(judgment is not None and judgment['operand_checks']==[]),
            'judge_collection_status':s['judge_status'],
            'judge_finish':record['finish_reason'] if record else 'not_recorded',
            'judge_runtime_error':bool(record and record.get('error')), 'judge_usage':response_usage(record)})
    ledger=rows(study/'spend_ledger.jsonl')
    budget=budget_audit(ledger,calls,'finance_quantity_transfer_v1')
    closure=budget_audit([e for e in ledger if e['utc']<=run['completed_utc']],calls,'finance_quantity_transfer_v1')
    before=[e for e in ledger if e['utc']<=run['started_utc']]
    before_budget=budget_audit(before,[],'finance_quantity_transfer_v1')
    assert Decimal(before_budget['study_known_usd'])==Decimal(run['spend_before']['study_usd'])
    if run['state']=='complete':
        assert len(calls)==64 and all(s['judge_status']=='recorded' for s in status)
        assert closure['totals_complete'] and not closure['cap_or_sequence_violations']
        assert Decimal(closure['study_known_usd'])==Decimal(run['spend_after']['study_usd'])
        assert Decimal(closure['aggregate_known_usd'])==Decimal(run['spend_after']['aggregate_usd'])
    else:
        assert len(calls)<64 and run['error']['type']=='BudgetStop'
        assert closure['unknown_billing_calls'] or closure['pending_calls'] or closure['cap_or_sequence_violations']
        assert all(s['judge_status']=='not_started' for s in status[len(calls):])
    return result,dict(state=run['state'],answer_calls=0,planned_judge_attempts=64,actual_judge_calls=len(calls),
        status_counts=dict(Counter(s['judge_status'] for s in status)),closed_error=run.get('error'),
        full_panel_complete=run['state']=='complete',no_retries_verified=True,
        pointer_format_amendment_only=True,primary_v1_preserved=True,plan_freeze_sha256=digest(directory/'plan_freeze.json'),
        timing_disclosure=frozen['timing'],selected_outcome_noninspection_is_disclosure_not_access_control=True,
        shared_budget=budget,closure_budget=closure,
        input_sha256={str(p.relative_to(root)):digest(p) for p in [directory/'plan_freeze.json',
            directory/'collection/run.json',directory/'collection/calls.jsonl',directory/'collection/attempt_status.json']})
