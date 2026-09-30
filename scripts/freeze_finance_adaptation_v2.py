"""Executive summary: freeze a disclosed logging repair without changing scientific rules."""
import hashlib
import json
import shutil
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'outputs/finance-adaptation-v1'
OUT = ROOT / 'outputs/finance-adaptation-v2'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUT.exists():
        raise ValueError('An execution-repeat directory already exists')
    original = json.loads((OLD / 'freeze.json').read_text())
    for name, checksum in original['frozen_sha256'].items():
        if digest(ROOT / name) != checksum:
            raise ValueError(f'Original frozen file changed: {name}')
    failure = json.loads((OLD / 'execution_failure.json').read_text())
    if failure['status'] != 'interrupted_execution_no_holdouts' or (OLD / 'holdout_responses.jsonl').exists():
        raise ValueError('The first attempt does not match the disclosed interruption')
    calls = [json.loads(line) for line in (OLD / 'api_calls.jsonl').read_text().splitlines()]
    prior = sum(Decimal(row['accounted_usd']) for row in calls)
    if prior != Decimal(failure['accounted_usd']) or len(calls) != failure['api_attempts']:
        raise ValueError('First-attempt accounting differs from the failure record')
    remaining = Decimal('.90') - prior
    required = [ROOT / name for name in (
        'docs/FINANCE_ADAPTATION_EXECUTION_AMENDMENT.md',
        'docs/FINANCE_ADAPTATION_EXECUTION_REVIEW.md',
        'scripts/run_finance_adaptation_v2.py', 'scripts/report_finance_adaptation_v2.py',
        'scripts/freeze_finance_adaptation_v2.py', 'scripts/finance_adaptation/validate_reexecution.py',
        'scripts/finance_adaptation/validate_outputs.py', 'scripts/finance_adaptation/output_support.py',
        'src/finance_adaptation/observed_client.py', 'tests/test_finance_adaptation_logging.py')]
    if any(not path.is_file() for path in required):
        raise ValueError('Execution review or operational implementation is missing')
    OUT.mkdir()
    copies = ['train.jsonl', 'dev.jsonl', 'test-source.jsonl', 'test-transfer.jsonl',
              'preflight.jsonl', 'preparation_manifest.json', 'provider_catalogue.json',
              'dependency_manifest.json', 'independent/benchmark_validation.json',
              'independent/oracle_boundary_checks.json']
    for name in copies:
        target = OUT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OLD / name, target)
    paths = [ROOT / name for name in original['frozen_sha256']]
    paths += [OLD / 'freeze.json', OLD / 'execution_failure.json', OLD / 'api_calls.jsonl',
              OLD / 'format_preflight.jsonl', OLD / 'preflight_result.json']
    paths += list(OLD.glob('*/evaluations.jsonl')) + list(OLD.glob('*/result.json'))
    paths += [OUT / name for name in copies]
    paths += required
    cutoff = datetime.fromisoformat(original['frozen_utc']) + timedelta(hours=3)
    manifest = {
        'executive_summary': 'Prospective operational repeat after a disclosed process-stream failure; unchanged scientific rules.',
        'status': 'frozen_before_reexecution_calls_after_disclosed_interruption',
        'frozen_utc': datetime.now(timezone.utc).isoformat(), 'gepa_version': '0.1.1',
        'shared_cap_usd': str(remaining), 'cumulative_cap_usd': '0.90',
        'prior_attempt_accounted_usd': str(prior),
        'original_start_utc': original['frozen_utc'], 'original_request_cutoff_utc': cutoff.isoformat(),
        'max_metric_calls_per_run': 256, 'maximum_global_api_concurrency': 4,
        'optimizer_seeds': [0, 1],
        'frozen_sha256': {str(path.relative_to(ROOT)): digest(path) for path in sorted(set(paths))}}
    (OUT / 'freeze.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'frozen_utc': manifest['frozen_utc'], 'files': len(manifest['frozen_sha256']),
                      'remaining_cap_usd': str(remaining), 'request_cutoff_utc': cutoff.isoformat()}))


if __name__ == '__main__':
    main()
