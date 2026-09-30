"""Executive summary: test MPS memory cleanup on authored inputs, preserving the failed panel."""
import argparse
import gc
import json
from datetime import datetime, timezone

from finance_document_local.protocol import CONDITIONS, OUT
from finance_document_local.runtime import generate, load, torch


def memory():
    return {'current_allocated_bytes': torch.mps.current_allocated_memory(),
            'driver_allocated_bytes': torch.mps.driver_allocated_memory()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--empty-cache', action='store_true')
    args = parser.parse_args()
    arm = 'clear_cache' if args.empty_cache else 'unchanged_runtime'
    path = OUT / ('source_free_mps_' + arm + '.json')
    if path.exists():
        raise ValueError('Preserve the existing runtime diagnostic')
    model, tokenizer = load('smollm2-1.7b')
    records = []
    for index in range(6):
        text = 'Inventory observation. ' * (650 + 37 * index)
        messages = [{'role': 'system', 'content': CONDITIONS['full_baseline']},
                    {'role': 'user', 'content': json.dumps({
                        'question': 'How many items are three groups of seven items?',
                        'original_context': text + 'There are three groups, each with seven items.'})}]
        record = {'index': index, 'memory_before': memory(), 'authored_messages': messages}
        try:
            record['generation'] = generate('smollm2-1.7b', model, tokenizer, messages)
        except Exception as exc:
            record['error'] = f'{type(exc).__name__}: {exc}'
        record['memory_after_generation'] = memory()
        if args.empty_cache:
            gc.collect()
            torch.mps.empty_cache()
            torch.mps.synchronize()
        record['memory_after_cleanup'] = memory()
        records.append(record)
        print(json.dumps({'arm': arm, 'index': index, 'memory': record['memory_after_cleanup'],
                          'error': record.get('error')}), flush=True)
        if record.get('error') or record['memory_after_cleanup']['driver_allocated_bytes'] > 10 * 1024**3:
            break
    result = {'executive_summary': 'Source-free runtime diagnostic, not financial performance or a repaired v1 panel.',
              'created_utc': datetime.now(timezone.utc).isoformat(), 'arm': arm,
              'source_free': True, 'selected_financial_retries': 0,
              'attention_implementation': model.config._attn_implementation,
              'planned_source_free_probes': 6, 'completed_probes': len(records),
              'memory_stop_driver_bytes': 10 * 1024**3, 'records': records}
    with path.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    main()
