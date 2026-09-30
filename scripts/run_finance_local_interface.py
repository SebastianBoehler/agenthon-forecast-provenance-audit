"""Executive summary: collect each frozen local model once with explicit failure records."""
import argparse
import json
from datetime import datetime, timezone

from finance_document_local.manifest import digest, rows, verify
from finance_document_local.protocol import CONDITIONS, MODELS, OUT
from finance_document_local.runtime import generate, load


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model_key', choices=MODELS)
    args = parser.parse_args()
    path = OUT / ('responses_' + args.model_key + '.jsonl')
    if path.exists():
        raise ValueError('One-shot ledger exists; selected cases cannot be retried')
    frozen = verify(model_key=args.model_key)
    model, tokenizer = load(args.model_key)
    selection = rows(OUT / 'selection.jsonl')
    audits = {(r['case_id'], r['condition']): r for r in rows(OUT / 'token_audit.jsonl')
              if r['model_key'] == args.model_key}
    conditions = list(CONDITIONS)
    with path.open('x') as stream:
        completed = 0
        for index, case in enumerate(selection):
            rotation = index % len(conditions)
            for condition in conditions[rotation:] + conditions[:rotation]:
                messages = [{'role': 'system', 'content': CONDITIONS[condition]},
                            {'role': 'user', 'content': case['prompt']}]
                record = {'model_key': args.model_key, 'condition': condition,
                          'case_id': case['case_id'], 'source': case['source'],
                          'started_utc': datetime.now(timezone.utc).isoformat(),
                          'collection_index': completed + 1}
                try:
                    result = generate(args.model_key, model, tokenizer, messages)
                    expected = audits[case['case_id'], condition]
                    for key in ['prompt_tokens', 'prompt_token_ids_sha256', 'rendered_prompt_sha256']:
                        if result[key] != expected[key]:
                            raise ValueError(f'Collected prompt differs from token freeze: {key}')
                    record.update(result)
                except Exception as exc:
                    record.update({'text': '', 'runtime_ok': False, 'token_audit_ok': False,
                                   'error': f'{type(exc).__name__}: {exc}',
                                   'finish_reason': 'error'})
                record['completed_utc'] = datetime.now(timezone.utc).isoformat()
                stream.write(json.dumps(record, ensure_ascii=False) + '\n')
                stream.flush()
                completed += 1
                if completed % 8 == 0:
                    print(json.dumps({'model_key': args.model_key, 'completed': completed,
                                      'scheduled': 128}), flush=True)
    receipt = {'executive_summary': 'One attempt per frozen case and condition; failures retained.',
               'model_key': args.model_key, 'attempts': completed, 'scheduled': 128,
               'response_sha256': digest(path), 'freeze_sha256': digest(OUT / 'freeze.json'),
               'selection_sha256': frozen['selection_sha256'],
               'completed_utc': datetime.now(timezone.utc).isoformat()}
    with (OUT / ('receipt_' + args.model_key + '.json')).open('x') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    main()
