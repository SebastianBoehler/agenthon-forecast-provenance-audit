"""Executive summary: independently verify saved blind-packet ranking and isolation.

No source answer, financial calculation or model call is used. This checks the
saved eligible metadata, not a second reconstruction of raw-corpus eligibility.
"""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/finance-document-audit-v1'


def read(name):
    return [json.loads(line) for line in (OUT / name).read_text().splitlines()]


def check_context(value):
    forbidden = {'answer', 'exe_ans', 'program', 'program_re', 'gold_inds', 'derivation',
                 'facts', 'mapping', 'mappings', 'answer_type', 'answer_from', 'scale'}
    if isinstance(value, dict):
        assert not forbidden.intersection(value)
        for child in value.values():
            check_context(child)
    elif isinstance(value, list):
        for child in value:
            check_context(child)


def main():
    config = json.loads((ROOT / 'experiments/finance_document_audit_sources_v1.json').read_text())
    pool, selected = read('admitted_pool_metadata.jsonl'), read('selection_metadata.jsonl')
    for row in pool:
        value = [config['selection_salt'], row['source'], row['native_id'], row['question_sha256']]
        encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(',', ':')).encode()
        assert hashlib.sha256(encoded).hexdigest() == row['order_sha256']
    contexts, questions, expected = set(), set(), []
    for source in ('finqa', 'tatqa'):
        groups, count = set(), 0
        rows = sorted((r for r in pool if r['source'] == source),
                      key=lambda r: (r['order_sha256'], r['native_id']))
        for row in rows:
            if count == 48:
                break
            if (row['group_id'] in groups or row['context_sha256'] in contexts or
                    row['question_sha256'] in questions):
                continue
            expected.append(row)
            groups.add(row['group_id'])
            contexts.add(row['context_sha256'])
            questions.add(row['question_sha256'])
            count += 1
        assert count == 48
    assert selected == expected and len(contexts) == len(questions) == 96
    ids = [r['source'] + ':' + r['native_id'] for r in selected]
    sheets = [read(f'reviewer_{name}.jsonl') for name in ('a', 'b')]
    for sheet, reviewer in zip(sheets, ('a', 'b')):
        assert [r['case_id'] for r in sheet] == ids
        for row in sheet:
            assert set(row) == {'case_id', 'reviewer', 'question', 'original_context', 'rubric', 'review_status'}
            assert row['reviewer'] == reviewer and row['review_status'] == 'blank_not_reviewed'
            assert row['rubric'] == {key: '' for key in config['blank_rubric_fields']}
            check_context(row['original_context'])
    assert all({k: v for k, v in a.items() if k != 'reviewer'} ==
               {k: v for k, v in b.items() if k != 'reviewer'} for a, b in zip(*sheets))
    result = {'executive_summary': 'Independent saved-metadata ranking and blind-sheet checks pass; no financial answers evaluated.',
              'status': 'PASS', 'checked_utc': datetime.now(timezone.utc).isoformat(),
              'selected_cases': len(selected), 'source_counts': dict(Counter(r['source'] for r in selected)),
              'blank_reviewers': 2, 'financial_answers_recomputed': 0,
              'boundary': 'Eligible pool provenance is recorded separately; this does not establish expert adjudication.'}
    (OUT / 'independent_preparation_checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
