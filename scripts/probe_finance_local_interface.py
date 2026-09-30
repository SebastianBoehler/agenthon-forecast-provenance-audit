"""Executive summary: preserve a source-free runtime probe before financial collection."""
import argparse
import json
from datetime import datetime, timezone

from finance_document_local.protocol import CONDITIONS, MODELS, OUT
from finance_document_local.runtime import generate, load
from finance_document_local.scoring import candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model_key', choices=MODELS)
    args = parser.parse_args()
    path = OUT / ('probe_' + args.model_key + '.json')
    if path.exists():
        raise ValueError('Preserve the one-shot toy probe')
    model, tokenizer = load(args.model_key)
    messages = [{'role': 'system', 'content': CONDITIONS['compact_baseline']},
                {'role': 'user', 'content': json.dumps({
                    'question': 'How many items are three groups of seven items?',
                    'original_context': 'There are three groups, each containing seven items.'})}]
    result = generate(args.model_key, model, tokenizer, messages, max_new_tokens=64)
    parsed, error = candidate(result['text'], 'compact_baseline')
    result.update({'executive_summary': 'Toy diagnostics are not a model-quality exclusion gate.',
                   'model_key': args.model_key, 'checkpoint': MODELS[args.model_key],
                   'created_utc': datetime.now(timezone.utc).isoformat(),
                   'authored_messages': messages, 'candidate': parsed, 'parse_error': error,
                   'selected_financial_answers_seen': 0})
    with path.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({k: result[k] for k in ['model_key', 'elapsed_seconds',
                     'completion_tokens', 'finish_reason', 'parse_error', 'runtime_ok']}))


if __name__ == '__main__':
    main()
