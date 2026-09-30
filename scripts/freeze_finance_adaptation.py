"""Executive summary: freeze reviewed data and all new pilot rules before model egress."""
import hashlib
import importlib.metadata
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/finance-adaptation-v1'


def main():
    if (OUT / 'freeze.json').exists() or (OUT / 'api_calls.jsonl').exists():
        raise ValueError('A freeze or model-call ledger already exists')
    validation = json.loads((OUT / 'independent/benchmark_validation.json').read_text())
    if validation['status'] != 'PASS' or validation['cases'] != 152:
        raise ValueError('Independent benchmark review has not passed')
    boundaries = json.loads((OUT / 'independent/oracle_boundary_checks.json').read_text())
    if boundaries['status'] != 'PASS':
        raise ValueError('Independent oracle edge checks have not passed')
    for name, checksum in validation['input_sha256'].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != checksum:
            raise ValueError(f'Question input differs from independent review: {name}')
    paths = [ROOT / 'docs/FINANCE_ADAPTATION_PROTOCOL_V1.md',
             ROOT / 'docs/FINANCE_ADAPTATION_INDEPENDENT_REVIEW.md',
             ROOT / 'experiments/finance_adaptation_requirements.txt',
             ROOT / 'tests/test_finance_adaptation.py']
    paths += list((ROOT / 'src/finance_adaptation').glob('*.py'))
    paths += [ROOT / 'scripts' / name for name in
              ('prepare_finance_adaptation.py', 'run_finance_adaptation.py',
               'freeze_finance_adaptation.py', 'report_finance_adaptation.py')]
    paths += list((ROOT / 'scripts/finance_adaptation').glob('*.py'))
    paths += [OUT / name for name in
              ('train.jsonl', 'dev.jsonl', 'test-source.jsonl', 'test-transfer.jsonl',
               'preflight.jsonl', 'preparation_manifest.json', 'provider_catalogue.json',
               'dependency_manifest.json', 'independent/benchmark_validation.json')]
    paths.append(OUT / 'independent/oracle_boundary_checks.json')
    # The new experiment imports these old modules without changing their original freezes.
    paths += list((ROOT / 'src/answer_contract').glob('*.py'))
    paths += [ROOT / 'src/model_grading/protocol.py',
              ROOT / 'outputs/model-grading-v1/selection.jsonl',
              ROOT / 'outputs/model-grading-v1/selection_manifest.json']
    manifest = {'executive_summary': 'Prospective adaptation freeze after independent technical review.',
                'status': 'frozen_before_any_pilot_model_call',
                'frozen_utc': datetime.now(timezone.utc).isoformat(),
                'gepa_version': importlib.metadata.version('gepa'),
                'shared_cap_usd': '0.90', 'max_metric_calls_per_run': 256,
                'maximum_global_api_concurrency': 4, 'optimizer_seeds': [0, 1],
                'frozen_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in sorted(set(paths))}}
    (OUT / 'freeze.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'frozen_utc': manifest['frozen_utc'],
                      'files': len(manifest['frozen_sha256'])}))


if __name__ == '__main__':
    main()
