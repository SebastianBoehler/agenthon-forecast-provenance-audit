"""Executive summary: verify the later evidence inventory without rewriting historical records."""
import json
from pathlib import Path

from finance_document_review.model_protocol import ROOT, digest
from finance_document_review.native_metrics import replay_authored_controls
from replay_finance_document_artifact import metrics, rows


def main():
    path = ROOT / 'experiments/finance_document_extension_manifest_v1.json'
    manifest = json.loads(path.read_text())
    for name, sha in manifest['files_sha256'].items():
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Evidence path escapes artifact root')
        if digest(ROOT / relative) != sha:
            raise ValueError(f'Extension evidence changed: {name}')
    graph = ROOT / 'experiments/research_exploration_graph_v1.json'
    if digest(graph) != manifest['historical_graph_sha256']:
        raise ValueError('Historical graph changed')
    old = json.loads(graph.read_text())
    for evidence in old['evidence']:
        if digest(ROOT / evidence['path']) != evidence['sha256']:
            raise ValueError(f'Historical scientific evidence changed: {evidence["path"]}')
    local, excluded = 0, 0
    for name, sha in manifest['external_provenance_sha256'].items():
        original = ROOT / name
        if original.exists():
            if digest(original) != sha:
                raise ValueError(f'Original external-provenance input changed: {name}')
            local += 1
        else:
            excluded += 1
    panel = ROOT / 'outputs/finance-document-models-v1'
    receipt = json.loads((panel / 'interrupted_collection_receipt.json').read_text())
    actual, attempts = rows(panel / 'responses.jsonl'), rows(panel / 'effective_attempts.jsonl')
    assert len(actual) == receipt['actual_api_records'] == 383
    assert attempts[:-1] == actual and len(attempts) == 384
    assert attempts[-1]['actual_api_response'] is False and attempts[-1]['collector_event'] is True
    assert sum(bool(r.get('error')) for r in actual) == 7
    assert receipt['missing_cost_records'] == 8 and receipt['fresh_retries'] == 0
    reference_path = ROOT / 'outputs/finance-document-review-v1/pre_target_combined.jsonl'
    references = {r['case_id']: r for r in rows(reference_path)}
    assert len(references) == 96
    assert sum(r['joint_status'] == 'agreed_determinate_numeric' for r in references.values()) == 62
    compact = ROOT / 'outputs/finance-document-replay-v1'
    targets = {r['case_id']: r['original_annotation'] for r in rows(compact / 'compact_native_annotations.jsonl')}
    result, scored = metrics(attempts, references, targets)
    assert result == json.loads((compact / 'results.json').read_text())
    assert scored == rows(panel / 'paired_scores.jsonl')
    assert result['models']['deepseek-v3.2']['baseline']['aggregate']['locked_matches_all_attempts'] == 25
    assert result['models']['deepseek-v3.2']['quantity_reminder']['aggregate']['locked_matches_all_attempts'] == 26
    controls = replay_authored_controls()
    print(json.dumps({'status': 'PASS', 'extension_files': len(manifest['files_sha256']),
                      'historical_files_unchanged': len(old['evidence']), 'attempts': 384,
                      'actual_api_records': 383, 'censored_events': 1, 'locked_subset': 62,
                      'native_controls': controls, 'external_inputs_verified_locally': local,
                      'external_inputs_excluded_from_copy': excluded,
                      'expert_semantic_or_main_track_certification': False}, indent=2))


if __name__ == '__main__':
    main()
