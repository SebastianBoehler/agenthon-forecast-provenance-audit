"""Executive summary: replay saved document scores from compact numeric annotations, without APIs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from finance_document_review.comparison import aggregate, evaluate_response
from finance_document_review.model_protocol import MODELS, ROOT, SYSTEMS, digest
from finance_document_review.reporting import channels, reference_projection

BASE = ROOT / 'outputs/finance-document-replay-v1'


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def metrics(responses, references, targets):
    keys = [(r['model_key'], r['condition'], r['case_id']) for r in responses]
    expected = {(m, a, c) for m in MODELS for a in SYSTEMS for c in references}
    if len(keys) != 384 or len(set(keys)) != 384 or set(keys) != expected:
        raise ValueError('The complete one-attempt384 panel is required')
    scored = [evaluate_response(r, references[r['case_id']], targets[r['case_id']]) for r in responses]
    result = {'executive_summary': 'Saved384-answer replay; numerical/broad-unit proxy, native channels and later precision diagnostic are distinct.',
              'attempts': 384, 'models': {}}
    for model in MODELS:
        result['models'][model] = {}
        for arm in SYSTEMS:
            selected = [r for r in scored if r['model_key'] == model and r['condition'] == arm]
            grouped = {}
            for source in ['finqa', 'tatqa']:
                subset = [r for r in selected if r['source'] == source]
                value = aggregate(subset)
                value['native_channels'] = channels(subset)
                projection = [reference_projection(references[r['case_id']], r['candidate']) for r in subset]
                value['later_precision_diagnostic'] = {
                    'matches': sum(p['matches'] is True for p in projection),
                    'additional_rounded_matches': sum(p['additional_rounded_match'] for p in projection)}
                if source == 'finqa':
                    value['percent_fraction_sensitivity'] = aggregate(subset, 'finqa_percent_fraction_sensitivity')
                grouped[source] = value
            result['models'][model][arm] = {'aggregate': aggregate(selected), 'sources': grouped}
    return result, scored


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true', help='Prepare compact views only from a completed local study')
    args = parser.parse_args()
    panel = ROOT / 'outputs/finance-document-models-v1'
    review = ROOT / 'outputs/finance-document-review-v1'
    if args.prepare:
        if BASE.exists():
            raise ValueError('Preserve existing saved-answer replay package')
        receipt = json.loads((panel / 'interrupted_collection_receipt.json').read_text())
        if digest(panel / 'responses.jsonl') != receipt['response_sha256']:
            raise ValueError('Collection ledger does not match its receipt')
        if digest(panel / 'effective_attempts.jsonl') != receipt['effective_attempts_sha256']:
            raise ValueError('Derived attempt ledger does not match its closure receipt')
        original_path = ROOT / 'outputs/finance-document-audit-v1/source_targets.jsonl'
        unblinding = json.loads((review / 'source_target_unblinding.json').read_text())
        if digest(original_path) != unblinding['source_targets_sha256']:
            raise ValueError('Original selected targets changed')
        compact = []
        for row in rows(original_path):
            fields = ['exe_ans'] if row['source'] == 'finqa' else ['answer', 'answer_type', 'scale']
            compact.append({'case_id': row['case_id'], 'source': row['source'],
                            'original_annotation': {key: row['original_annotation'][key] for key in fields}})
        BASE.mkdir(parents=True)
        (BASE / 'compact_native_annotations.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in compact))
        responses = rows(panel / 'effective_attempts.jsonl')
        references = {r['case_id']: r for r in rows(review / 'pre_target_combined.jsonl')}
        targets = {r['case_id']: r['original_annotation'] for r in compact}
        result, scored = metrics(responses, references, targets)
        original_scores = rows(panel / 'paired_scores.jsonl')
        if scored != original_scores:
            raise AssertionError('Compact native annotations changed any paired score')
        (BASE / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
        paths = [panel / 'responses.jsonl', panel / 'effective_attempts.jsonl',
                 panel / 'interrupted_collection_receipt.json', review / 'pre_target_combined.jsonl',
                 BASE / 'compact_native_annotations.jsonl', BASE / 'results.json',
                 ROOT / 'src/finance_document_review/comparison.py',
                 ROOT / 'src/finance_document_review/reporting.py',
                 ROOT / 'src/finance_document_review/native_metrics.py',
                 ROOT / 'src/finance_document_review/model_protocol.py',
                 ROOT / 'src/finance_document_review/units.py', Path(__file__).resolve()]
        manifest = {'executive_summary': 'Compact annotations retain only the unchanged native numeric fields used by saved scoring. Full corpora, questions/contexts, gold programs and original annotation dictionaries remain outside this package.',
                    'original_target_file_sha256': digest(original_path),
                    'all384_compact_scores_identical': True,
                    'source_content_excluded': True,
                    'files_sha256': {str(p.relative_to(ROOT)): digest(p) for p in paths}}
        (BASE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    manifest = json.loads((BASE / 'manifest.json').read_text())
    for path, sha in manifest['files_sha256'].items():
        if digest(ROOT / path) != sha:
            raise ValueError(f'Replay input changed: {path}')
    references = {r['case_id']: r for r in rows(review / 'pre_target_combined.jsonl')}
    targets = {r['case_id']: r['original_annotation'] for r in rows(BASE / 'compact_native_annotations.jsonl')}
    result, _ = metrics(rows(panel / 'effective_attempts.jsonl'), references, targets)
    if result != json.loads((BASE / 'results.json').read_text()):
        raise AssertionError('Saved-result replay differs')
    print(json.dumps({'status': 'PASS', 'attempts': 384, 'compact_scores_unchanged': True,
                      'saved_aggregate_identical': True, 'fresh_inference': False}))


if __name__ == '__main__':
    main()
