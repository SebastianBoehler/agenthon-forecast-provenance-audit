"""Executive summary: replay the frozen document panel without inference or target fitting."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from finance_document_review.comparison import aggregate, evaluate_response
from finance_document_review.model_protocol import MODELS, OUTPUT, ROOT, SYSTEMS, digest
from finance_document_review.native_metrics import verify_native_sources


def read(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def verify(manifest: dict) -> None:
    for name, sha in manifest['files_sha256'].items():
        if digest(ROOT / name) != sha:
            raise ValueError(f'Frozen input changed: {name}')


def main() -> None:
    verify(json.loads((OUTPUT / 'freeze.json').read_text()))
    review = ROOT / 'outputs/finance-document-review-v1'
    verify(json.loads((review / 'pre_target_lock.json').read_text()))
    verify(json.loads((OUTPUT / 'analysis_implementation_freeze.json').read_text()))
    verify_native_sources()
    receipt = json.loads((OUTPUT / 'collection_receipt.json').read_text())
    if receipt['response_sha256'] != digest(OUTPUT / 'responses.jsonl'):
        raise ValueError('Response ledger changed after collection')
    references = {r['case_id']: r for r in read(review / 'pre_target_combined.jsonl')}
    targets_path = ROOT / 'outputs/finance-document-audit-v1/source_targets.jsonl'
    unblinding = json.loads((review / 'source_target_unblinding.json').read_text())
    if digest(targets_path) != unblinding['source_targets_sha256']:
        raise ValueError('Original native targets changed')
    targets = {r['case_id']: r['original_annotation'] for r in read(targets_path)}
    responses = read(OUTPUT / 'responses.jsonl')
    expected = {(key, arm, case) for key in MODELS for arm in SYSTEMS for case in references}
    counts = Counter((r['model_key'], r['condition'], r['case_id']) for r in responses)
    if set(counts) != expected or any(v != 1 for v in counts.values()) or len(responses) != 384:
        raise ValueError('Panel does not cover each frozen case/configuration/condition exactly once')
    scored = [evaluate_response(r, references[r['case_id']], targets[r['case_id']]) for r in responses]
    result = {'executive_summary': 'Paired unchanged-answer replay; locked final-value/unit endpoint is not expert semantic ground truth.',
              'attempts': len(scored), 'source_sha256': {
                  str(p.relative_to(ROOT)): digest(p) for p in [OUTPUT / 'responses.jsonl',
                  review / 'pre_target_combined.jsonl', targets_path,
                  ROOT / 'src/finance_document_review/comparison.py']}, 'models': {}}
    for model in MODELS:
        result['models'][model] = {}
        for arm in SYSTEMS:
            rows = [r for r in scored if r['model_key'] == model and r['condition'] == arm]
            value = {'aggregate': aggregate(rows), 'sources': {}}
            for source in ['finqa', 'tatqa']:
                selected = [r for r in rows if r['source'] == source]
                value['sources'][source] = aggregate(selected)
                if source == 'finqa':
                    value['sources'][source]['percent_fraction_sensitivity'] = aggregate(selected, 'finqa_percent_fraction_sensitivity')
            result['models'][model][arm] = value
    result['paired_reminder_changes'] = {}
    for model in MODELS:
        keyed = {(r['case_id'], r['condition']): r for r in scored if r['model_key'] == model}
        changes = Counter()
        for case in references:
            a, b = [keyed[case, arm]['locked_comparator'] for arm in ['baseline', 'quantity_reminder']]
            if a['eligible']:
                changes[str((a['matches'], b['matches']))] += 1
        result['paired_reminder_changes'][model] = dict(changes)
    (OUTPUT / 'paired_scores.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in scored))
    (OUTPUT / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
