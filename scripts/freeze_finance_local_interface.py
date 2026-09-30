"""Executive summary: bind the prospective local pilot before any selected model answer."""
import json
import platform
import sys
from datetime import datetime, timezone
from importlib.metadata import version

from finance_document_local.manifest import digest, rows
from finance_document_local.protocol import MAX_NEW_TOKENS, MODELS, OUT, ROOT, cache
from finance_document_review.native_metrics import verify_native_sources


def main():
    target = OUT / 'freeze.json'
    if target.exists() or list(OUT.glob('responses_*.jsonl')):
        raise ValueError('Preserve the existing freeze or collected answers')
    preparation = json.loads((OUT / 'preparation.json').read_text())
    if preparation['selection_sha256'] != digest(OUT / 'selection.jsonl'):
        raise ValueError('Selected discovery cohort changed')
    files = list((ROOT / 'src/finance_document_local').glob('*.py'))
    files += [ROOT / 'scripts' / name for name in [
        'prepare_finance_local_interface.py', 'probe_finance_local_interface.py',
        'freeze_finance_local_interface.py', 'run_finance_local_interface.py',
        'analyze_finance_local_interface.py']]
    files += [ROOT / 'tests/test_finance_local_interface.py',
              ROOT / 'docs/FINANCE_LOCAL_INTERFACE_PROTOCOL_V1.md',
              ROOT / 'docs/FINANCE_LOCAL_INTERFACE_PRECOLLECTION_REVIEW_V1.md',
              ROOT / 'docs/FINANCE_LOCAL_INTERFACE_READINESS_SUPPLEMENT_V1.md']
    files += [OUT / name for name in ['selection.jsonl', 'token_audit.jsonl', 'preparation.json',
                                     'preflight_driver_environment_deviation.json']]
    files += list((ROOT / 'src/finance_document_review').glob('*.py'))
    files += [ROOT / 'outputs/finance-document-audit-v1/reviewer_a.jsonl',
              ROOT / 'outputs/finance-document-review-v1/pre_target_combined.jsonl',
              ROOT / 'outputs/finance-document-review-v1/pre_target_lock.json',
              ROOT / 'outputs/finance-document-replay-v1/compact_native_annotations.jsonl']
    native = verify_native_sources()
    files += [ROOT / 'outputs/finance-document-native-v1' / name for name in native['sha256']]
    models = {}
    for key in MODELS:
        path = cache(key)
        probe_path = OUT / ('probe_' + key + '.json')
        probe = json.loads(probe_path.read_text())
        if probe['runtime_ok'] is not True or probe['token_audit_ok'] is not True:
            raise ValueError('Native local runtime probe did not pass')
        files.append(probe_path)
        models[key] = {str(p.relative_to(path)): digest(p) for p in path.iterdir() if p.is_file()}
        if not any(name.endswith('.safetensors') for name in models[key]):
            raise ValueError('Pinned checkpoint has no local weights')
    references = {r['case_id']: r for r in rows(
        ROOT / 'outputs/finance-document-review-v1/pre_target_combined.jsonl')}
    selected = rows(OUT / 'selection.jsonl')
    eligible = [r for r in selected if references[r['case_id']]['joint_status'] == 'agreed_determinate_numeric']
    if len(selected) != 32 or len(eligible) != 24:
        raise ValueError('Precollection denominators changed')
    result = {'executive_summary': 'Prospective local discovery pilot after previous document results, not held-out preregistration.',
              'created_utc': datetime.now(timezone.utc).isoformat(),
              'selected_financial_answers_seen': 0, 'scheduled_attempts': 256,
              'selection_sha256': digest(OUT / 'selection.jsonl'),
              'models': MODELS, 'checkpoint_files_sha256': models,
              'files_sha256': {str(p.relative_to(ROOT)): digest(p) for p in sorted(set(files))},
              'locked_eligible_cases': len(eligible), 'outside_reference_cases': 8,
              'locked_source_counts': {s: sum(r['source'] == s for r in eligible) for s in ['finqa', 'tatqa']},
              'runtime': {'python': sys.version, 'platform': platform.platform(),
                          'torch': version('torch'), 'transformers': version('transformers'),
                          'device': 'mps', 'dtype': 'float16', 'mps_cpu_fallback': False,
                          'do_sample': False, 'max_new_tokens': MAX_NEW_TOKENS},
              'quality_exclusion_based_on_toy_answer': False}
    with target.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'status': 'FROZEN', 'scheduled_attempts': 256,
                      'files': len(result['files_sha256']), 'freeze_sha256': digest(target)}))


if __name__ == '__main__':
    main()
