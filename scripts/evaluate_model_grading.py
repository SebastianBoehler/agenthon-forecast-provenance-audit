"""Executive summary: derive manuscript-ready grading counts from the complete saved panel."""
import json

from model_grading.protocol import (DESTINATION, LOCAL_MODELS, digest, frozen_selection,
                                    read_jsonl, write_json)
from model_grading.scoring import evaluate


def main():
    selection = frozen_selection()
    models = list(LOCAL_MODELS) + ['deepseek-v3.2']
    paths = [DESTINATION / f'{m}_responses.jsonl' for m in models]
    records = [r for path in paths for r in read_jsonl(path)]
    scored, results = evaluate(selection, records, models)
    results['api_reported_cost_usd'] = sum(
        r.get('usage', {}).get('cost', 0) for r in records if r['model_key'] == 'deepseek-v3.2')
    results['response_sha256'] = {p.name: digest(p) for p in paths}
    write_json(DESTINATION / 'results.json', results)
    (DESTINATION / 'scored.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in scored))
    print(json.dumps({m: results['models'][m]['aggregate'] for m in models}, indent=2))


if __name__ == '__main__':
    main()
