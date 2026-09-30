"""Executive summary: lock validated reference reviews before comparing or unblinding labels."""

import json
from datetime import datetime, timezone
from pathlib import Path

from financial_review_io import digest, rows
from finance_quantity_transfer.references import compare, validate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'outputs/finance-quantity-transfer-v1'
packet = rows(OUT/'question_packet.jsonl')
reviews = [rows(OUT/f'reference_{name}.jsonl') for name in ['a','b']]
ids = [p['case_id'] for p in packet]
assert len(ids) == len(set(ids)) == 32
for review in reviews:
    assert [r['case_id'] for r in review] == ids
validation = [dict(records=len(review), source_pointers_checked=sum(validate(r,p)['source_pointers_checked'] for r,p in zip(review,packet))) for review in reviews]
files = [OUT/name for name in ['reference_a.jsonl','reference_b.jsonl','reference_a_receipt.json','reference_b_receipt.json','question_packet.jsonl','cohort_freeze.json','reference_stage_freeze.json','derive_reference_b.py']]
files += [ROOT/name for name in ['docs/FINANCE_QUANTITY_TRANSFER_REFERENCE_PROTOCOL_V1.md','src/finance_quantity_transfer/references.py','src/finance_quantity_transfer/protocol.py','src/financial_review_io.py','src/finance_document_review/arithmetic.py','scripts/lock_finance_quantity_references.py']]
lock = dict(created_utc=datetime.now(timezone.utc).isoformat(), validation=validation,
    files_sha256={str(p.relative_to(ROOT)):digest(p) for p in files},
    disclosure='Both question-only AI reviews locked before comparison and before source-target/model-output unblinding. No qualified financial expert has adjudicated them.')
with (OUT/'reference_joint_lock.json').open('x') as stream:
    json.dump(lock,stream,indent=2,sort_keys=True); stream.write('\n')
(OUT/'reference_joint_lock.json').chmod(0o444)
comparisons = [compare(a,b) for a,b in zip(*reviews)]
with (OUT/'reference_comparison.jsonl').open('x') as stream:
    for row in comparisons:
        stream.write(json.dumps(row,sort_keys=True)+'\n')
print(json.dumps(dict(lock_sha256=digest(OUT/'reference_joint_lock.json'), validation=validation,
    provisional_numeric_candidates=sum(r['provisional_numeric_candidate'] for r in comparisons)),indent=2))
