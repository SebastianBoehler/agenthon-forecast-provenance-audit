"""Executive summary: prepare reviewable adaptation splits without freezing or inference."""
import json
from datetime import datetime, timezone

from finance_adaptation.benchmark import build_benchmark
from model_grading.protocol import ROOT, digest, write_json

DESTINATION = ROOT / 'outputs/finance-adaptation-v1'


def main():
    DESTINATION.mkdir(parents=True, exist_ok=True)
    if any(DESTINATION.glob('*.jsonl')) or (DESTINATION / 'preparation_manifest.json').exists():
        raise FileExistsError('Prepared splits already exist; do not overwrite them')
    partitions, metadata = build_benchmark()
    paths = []
    for partition, rows in partitions.items():
        path = DESTINATION / f'{partition}.jsonl'
        path.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows))
        paths.append(path)
    protocol = ROOT / 'docs/FINANCE_ADAPTATION_PROTOCOL_V1.md'
    files = [*paths, protocol, ROOT / 'scripts/prepare_finance_adaptation.py']
    files += sorted((ROOT / 'src/finance_adaptation').glob('*.py'))
    files += sorted((ROOT / 'src/answer_contract').glob('*.py'))
    files.append(ROOT / 'src/model_grading/protocol.py')
    write_json(DESTINATION / 'preparation_manifest.json', {
        'status': 'prepared_unfrozen_pending_independent_review',
        'prepared_at_utc': datetime.now(timezone.utc).isoformat(), **metadata,
        'prepared_sha256': {str(path.relative_to(ROOT)): digest(path) for path in files},
        'prior_selection_sha256': digest(ROOT / 'outputs/model-grading-v1/selection.jsonl'),
    })
    print(json.dumps({'status': 'prepared_unfrozen', **metadata}))


if __name__ == '__main__':
    main()
