"""Executive summary: join unchanged source labels only after locked question-only references."""

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from financial_review_io import digest, rows

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'outputs/finance-quantity-transfer-v1'
OLD = ROOT/'outputs/finance-document-audit-v1'


def write(name, value, jsonl=False):
    with (OUT/name).open('x') as stream:
        if jsonl:
            for record in value:
                stream.write(json.dumps(record,ensure_ascii=False,sort_keys=True)+'\n')
        else:
            json.dump(value,stream,indent=2,sort_keys=True); stream.write('\n')


def main():
    lock = json.loads((OUT/'reference_joint_lock.json').read_text())
    for name, expected in lock['files_sha256'].items():
        if digest(ROOT/name) != expected:
            raise ValueError('Locked reference input changed: '+name)
    approval = json.loads((OUT/'reference_semantic_comparison.json').read_text())
    if approval['reference_joint_lock_sha256'] != digest(OUT/'reference_joint_lock.json'):
        raise ValueError('Semantic comparison does not bind this reference lock')
    packet, refs = rows(OUT/'question_packet.jsonl'), rows(OUT/'reference_a.jsonl')
    comparisons = rows(OUT/'reference_comparison.jsonl')
    approved = set(approval['approved_numeric_candidate_ids'])
    if approved != {r['case_id'] for r in comparisons if r['provisional_numeric_candidate']}:
        raise ValueError('Unexplained candidate filtering')
    freeze_inputs = ['scripts/prepare_finance_quantity_experiment.py',
        'outputs/finance-quantity-transfer-v1/reference_joint_lock.json',
        'outputs/finance-quantity-transfer-v1/reference_semantic_comparison.json',
        'outputs/finance-quantity-transfer-v1/reference_comparison.jsonl',
        'scripts/finance_document_audit/joins.py','scripts/finance_document_audit/common.py',
        'outputs/finance-document-audit-v1/ingestion_manifest.json']
    write('label_join_freeze.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),
        files_sha256={p:digest(ROOT/p) for p in freeze_inputs}, source_target_fields_read=False))
    ingestion = json.loads((OLD/'ingestion_manifest.json').read_text())
    for artifact in ingestion['artifacts']:
        if digest(ROOT/artifact['path']) != artifact['sha256']:
            raise ValueError('Pinned financial source changed')
    sys.path.insert(0,str(ROOT/'scripts/finance_document_audit'))
    from joins import exact_question_context_join
    finqa = {r['id']:r for r in json.loads((OLD/'raw/finqa/dataset/test.json').read_text())}
    tat_raw = json.loads((OLD/'raw/tatqa/dataset_raw/tatqa_dataset_test.json').read_text())
    tat_gold = json.loads((OLD/'raw/tatqa/dataset_raw/tatqa_dataset_test_gold.json').read_text())
    tat, join = exact_question_context_join(tat_raw,tat_gold)
    source_targets, experiment = [], []
    for row, reference in zip(packet,refs):
        assert row['case_id'] == reference['case_id']
        source, uid = row['case_id'].split(':',1)
        annotation = finqa[uid]['qa'] if source == 'finqa' else tat[uid]
        native = annotation['exe_ans' if source == 'finqa' else 'answer']
        source_targets.append(dict(case_id=row['case_id'],source=source,original_annotation=annotation))
        experiment.append({**row,'provisional_reference':dict(eligible=row['case_id'] in approved,
            value=reference['value'],unit=reference['unit'],scale=reference['scale'],calculation=reference['expression']),
            'native_target':{'value':native}})
    write('source_targets.jsonl',source_targets,True)
    write('experiment_packet.jsonl',experiment,True)
    write('label_join_receipt.json',dict(completed_utc=datetime.now(timezone.utc).isoformat(),
        reference_joint_lock_sha256=digest(OUT/'reference_joint_lock.json'),
        label_join_freeze_sha256=digest(OUT/'label_join_freeze.json'), cases=32,
        provisional_reference_cases=len(approved), tat_original_input_join=join,
        source_targets_sha256=digest(OUT/'source_targets.jsonl'),experiment_packet_sha256=digest(OUT/'experiment_packet.jsonl'),
        disclosure='Native labels unchanged and excluded from model requests. Exact native numeric representation is a diagnostic, not official FinQA program accuracy or TAT-QA EM/F1. References remain AI provisional; ten cases retain unresolved interpretations.'))
    print(json.dumps({'cases':32,'provisional_reference_cases':len(approved),'packet_sha256':digest(OUT/'experiment_packet.jsonl')}))


if __name__ == '__main__':
    main()
