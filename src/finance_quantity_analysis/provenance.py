"""Executive summary: verify frozen requests, routes and every spend-ledger event offline."""

import hashlib
import json
import platform
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path

from finance_quantity_transfer.protocol import JUDGE, SYSTEMS

MODEL, PROVIDER = 'deepseek/deepseek-v3.2', 'siliconflow/fp8'
PRICE_IN, PRICE_OUT = Decimal('0.000000259'), Decimal('0.00000042')
MALFORMED_RULE = 'If candidate_parser_valid is false, verdict must be unassessable; still inspect and record the attempted answer.'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def record_check(root, record):
    path = root / record['path']
    assert digest(path) == record['sha256'] and path.stat().st_size == record['bytes'], record['path']


def budget_audit(events, calls, study_id):
    reserved, settled, pending = {}, {}, set()
    total, study, unknown = Decimal(0), Decimal(0), []
    violations = []
    for index, event in enumerate(events):
        identity = event['call_id']
        if event['event'] == 'reserved':
            assert identity not in reserved and not pending
            reserve = Decimal(event['reserve_usd'])
            assert reserve.is_finite() and reserve >= 0
            if unknown: violations.append('reservation_after_unknown_billing')
            if total + reserve > 10: violations.append('aggregate_reservation_cap')
            if event['study_id'] == study_id and study + reserve > 2:
                violations.append('study_reservation_cap')
            reserved[identity] = event
            pending.add(identity)
        else:
            assert event['event'] == 'settled' and identity in pending and identity not in settled
            pending.remove(identity)
            settled[identity] = event
            reserve = reserved[identity]
            assert event['study_id'] == reserve['study_id']
            assert event['request_sha256'] == reserve['request_sha256']
            assert reserve['utc'] <= event['utc']
            if event['cost_usd'] is None:
                unknown.append(identity)
                continue
            cost = Decimal(event['cost_usd'])
            assert cost.is_finite() and cost >= 0
            total += cost
            if event['study_id'] == study_id: study += cost
            if cost > Decimal(reserve['reserve_usd']): violations.append('cost_above_reservation')
            if total > 10 or study > 2: violations.append('observed_cost_above_cap')
    call_cost, call_unknown = Decimal(0), []
    for c in calls:
        identity = c['call_id']
        assert identity in reserved
        reserve = reserved[identity]
        for field in ['case_id','arm','phase','target_model','target_provider','request_sha256']:
            assert c[field] == reserve[field], (identity, field)
        body = c['request_body']
        reserve_expected = PRICE_IN * (len(json.dumps(body, ensure_ascii=False).encode()) + 256) + PRICE_OUT * body['max_tokens']
        assert reserve_expected == Decimal(reserve['reserve_usd'])
        if identity not in settled:
            call_unknown.append(identity)
            continue
        settlement = settled[identity]
        usage = c.get('usage')
        if not isinstance(usage, dict) or 'cost' not in usage:
            usage = c.get('raw_response', {}).get('usage', {})
        value = usage.get('cost') if isinstance(usage, dict) else None
        valid = value is not None and not isinstance(value, bool)
        try:
            cost = Decimal(str(value)) if valid else None
            valid = valid and cost.is_finite() and cost >= 0
        except (ArithmeticError, ValueError):
            valid = False
        assert (settlement['cost_usd'] is not None) == bool(valid)
        if valid:
            assert cost == Decimal(settlement['cost_usd'])
            call_cost += cost
        else:
            call_unknown.append(identity)
        for saved, field in [('provider','returned_provider'),('returned_model','returned_model'),('finish_reason','finish_reason')]:
            assert c.get(saved) == settlement.get(field)
    unresolved=set(unknown)|pending
    unresolved_reserve=sum((Decimal(reserved[k]['reserve_usd']) for k in unresolved),Decimal(0))
    return dict(ledger_events=len(events), reserved_calls=len(reserved), settled_calls=len(settled),
                pending_calls=sorted(pending), unknown_billing_calls=unknown,
                study_known_usd=str(study), aggregate_known_usd=str(total),
                collection_known_usd=str(call_cost), collection_unknown_billing=call_unknown,
                cap_or_sequence_violations=violations,
                totals_complete=not pending and not unknown,observed_cost_complete=not unresolved,
                full_observed_aggregate_usd=str(total) if not unresolved else None,
                unresolved_reserved_usd=str(unresolved_reserve),conditional_accounted_aggregate_usd=str(total+unresolved_reserve),
                conditional_bound_assumption='Unknown charges do not exceed their reservations; not an observed billing total.')




def response_usage(record):
    if not record:
        return {}
    usage = record.get('usage')
    if not isinstance(usage, dict) or 'cost' not in usage:
        usage = record.get('raw_response', {}).get('usage', {})
    return usage if isinstance(usage, dict) else {}


def request_check(record, system, user):
    body = record['request_body']
    assert digest_bytes(encode(body).encode()) == record['request_sha256']
    expected = {'model':MODEL,'temperature':0,'max_tokens':1024,'reasoning':{'enabled':False},
        'response_format':{'type':'json_object'},'provider':{'only':[PROVIDER],'allow_fallbacks':False,
        'require_parameters':True,'max_price':{'prompt':0.259,'completion':0.42}},
        'messages':[{'role':'system','content':system},{'role':'user','content':encode(user)}]}
    assert body == expected


def verify(root, out, cases, run, statuses, calls):
    assert run['state'] in {'complete','stopped'}, 'Do not analyze a moving collection'
    assert run['mode'] == 'financial_study'
    frozen = run['freeze']
    assert frozen == json.loads((out/'experiment_freeze.json').read_text())
    assert frozen['planned_cases'] == 32 and frozen['answer_attempts'] == frozen['quantity_judge_attempts'] == 64
    assert frozen['model'] == MODEL and frozen['provider'] == PROVIDER
    assert frozen['study_cap_usd'] == '2' and frozen['aggregate_cap_usd'] == '10'
    assert frozen['initial_actual_usd'] == '0'
    assert Decimal(frozen['prompt_price_usd_per_token']) == PRICE_IN
    assert Decimal(frozen['output_price_usd_per_token']) == PRICE_OUT
    for record in frozen['source_files'] + list(frozen['inputs'].values()): record_check(root, record)
    assert run['source_files'] == frozen['source_files']
    assert frozen['python_version'] == platform.python_version()
    assert frozen['python_executable'] == str(Path(sys.executable).resolve())
    assert run['started_utc'] >= frozen['created_utc']
    assert run['planned_answer_attempts'] == run['planned_judge_attempts'] == 64
    expected = [(c['case_id'], arm, phase) for c in cases for arm in SYSTEMS for phase in ['answer','judge']]
    planned = [(c['case_id'], arm) for c in cases for arm in SYSTEMS]
    assert len(statuses) == 64 and [(s['case_id'], s['arm']) for s in statuses] == planned
    identities = [(c['case_id'], c['arm'], c['phase']) for c in calls]
    assert len(set(identities)) == len(calls) and identities == expected[:len(calls)]
    assert len({c['call_id'] for c in calls}) == len(calls)
    status_lookup = {(s['case_id'], s['arm']): s for s in statuses}
    case_lookup = {c['case_id']: c for c in cases}
    call_lookup = {(c['case_id'],c['arm'],c['phase']): c for c in calls}
    route_missing, runtime_errors = [], []
    previous_end = None
    for c in calls:
        identity = (c['case_id'],c['arm'],c['phase'])
        case = case_lookup[c['case_id']]
        assert c['source'] == case['source'] and c['target_model'] == MODEL and c['target_provider'] == PROVIDER
        assert c['call_id'] == f"finance_quantity_transfer_v1:{c['case_id']}:{c['arm']}:{c['phase']}"
        body = c['request_body']
        assert digest_bytes(encode(body).encode()) == c['request_sha256']
        user = json.loads(body['messages'][1]['content'])
        base = {'question':case['question'], 'original_context':case['original_context']}
        system = SYSTEMS[c['arm']] if c['phase'] == 'answer' else JUDGE
        if c['phase'] == 'judge':
            answer = call_lookup[(c['case_id'],c['arm'],'answer')]
            error = status_lookup[(c['case_id'],c['arm'])]['scoring']['schema_error']
            base.update(candidate_text=answer['text'], candidate_parser_valid=error is None,
                        candidate_parser_error=error,
                        malformed_candidate_rule=MALFORMED_RULE)
        assert user == base
        request_check(c, system, base)
        assert c['started_utc'] >= run['started_utc'] and c['completed_utc'] >= c['started_utc']
        if previous_end: assert c['started_utc'] >= previous_end
        previous_end = c['completed_utc']
        if c.get('error'): runtime_errors.append(c['call_id'])
        if c.get('provider') != 'SiliconFlow' or c.get('returned_model') != MODEL:
            route_missing.append(c['call_id'])
            assert c.get('error') or c.get('finish_reason') in {'provider_mismatch','transport_error','local_error'}
        raw = c.get('raw_response', {})
        if raw.get('choices') and not c.get('error'):
            assert c['text'] == (raw['choices'][0]['message'].get('content') or '')
            assert c['finish_reason'] == raw['choices'][0]['finish_reason']
            assert c.get('provider') == raw.get('provider') and c.get('returned_model') == raw.get('model')
    if run['state'] == 'complete':
        assert len(calls) == 128 and not route_missing and not runtime_errors
        assert all(s['answer_status'] == s['judge_status'] == 'recorded' for s in statuses)
    ledger = rows(out/'spend_ledger.jsonl')
    audit = budget_audit(ledger, calls, 'finance_quantity_transfer_v1')
    closure = budget_audit([e for e in ledger if e['utc'] <= run['completed_utc']],
                          calls, 'finance_quantity_transfer_v1')
    if run['state'] == 'complete':
        assert closure['totals_complete'] and not closure['cap_or_sequence_violations']
        assert Decimal(run['spend']['study_usd']) == Decimal(closure['study_known_usd'])
        assert Decimal(run['spend']['aggregate_usd']) == Decimal(closure['aggregate_known_usd'])
    audit['v1_closure_totals'] = closure
    return dict(freeze_source_files=len(frozen['source_files']), freeze_inputs=len(frozen['inputs']),
                runtime_identity_match=True, state=run['state'], request_count=len(calls),
                phase_counts=dict(Counter(c['phase'] for c in calls)), route_unverified=route_missing,
                runtime_error_calls=runtime_errors, budget=audit)


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()
