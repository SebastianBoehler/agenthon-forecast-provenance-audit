"""Executive summary: record one greedy local answer per frozen public question, without retries."""
import argparse
import json
import os
import platform
import time
from pathlib import Path

os.environ['USE_TF'] = '0'
os.environ['USE_FLAX'] = '0'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ['HF_HUB_OFFLINE'] = '1'

import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

from model_grading.protocol import (DESTINATION, LOCAL_MODELS, MAX_TOKENS, SYSTEM,
                                    append_record, digest, frozen_selection,
                                    read_jsonl, write_json)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('model', choices=LOCAL_MODELS)
    args = parser.parse_args()
    selection = frozen_selection()
    spec = LOCAL_MODELS[args.model]
    cache = (Path.home() / '.cache/huggingface/hub' /
             ('models--' + spec['repository'].replace('/', '--')) /
             'snapshots' / spec['revision'])
    if not cache.exists() or not torch.backends.mps.is_available():
        raise RuntimeError('Required pinned model cache or MPS device is unavailable')
    hashes = {p.name: digest(p) for p in sorted(cache.iterdir()) if p.is_file()}
    tokenizer = AutoTokenizer.from_pretrained(cache, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(cache, local_files_only=True,
                                               dtype=torch.float16).to('mps')
    model.eval()
    model.generation_config.temperature = None
    model.generation_config.top_p = None
    model.generation_config.top_k = None
    metadata = {'model_key': args.model, **spec, 'file_sha256': hashes,
                'torch': torch.__version__, 'transformers': transformers.__version__,
                'python': platform.python_version(), 'device': 'mps', 'dtype': 'float16',
                'decoding': 'greedy', 'max_new_tokens': MAX_TOKENS,
                'system_prompt': SYSTEM,
                'selection_sha256': digest(DESTINATION / 'selection.jsonl')}
    write_json(DESTINATION / f'{args.model}_runtime.json', metadata)
    path = DESTINATION / f'{args.model}_responses.jsonl'
    previous = read_jsonl(path) if path.exists() else []
    completed = {r['case_id'] for r in previous}
    if len(completed) != len(previous) or not completed.issubset({r['case_id'] for r in selection}):
        raise ValueError('Existing response ledger has duplicate or unexpected IDs')
    for row in selection:
        if row['case_id'] in completed:
            continue
        started = time.perf_counter()
        record = {'model_key': args.model, 'case_id': row['case_id'],
                  'question_hash': row['question_hash'], 'model': spec['repository'],
                  'text': '', 'finish_reason': 'runtime_error'}
        try:
            messages = [{'role': 'system', 'content': SYSTEM},
                        {'role': 'user', 'content': row['prompt']}]
            options = {'enable_thinking': False} if spec.get('thinking') is False else {}
            prompt = tokenizer.apply_chat_template(messages, tokenize=False,
                                                    add_generation_prompt=True, **options)
            encoded = tokenizer(prompt, return_tensors='pt').to('mps')
            with torch.inference_mode():
                output = model.generate(**encoded, max_new_tokens=MAX_TOKENS,
                                        do_sample=False, pad_token_id=tokenizer.eos_token_id)
            torch.mps.synchronize()
            tokens = output[0, encoded.input_ids.shape[1]:].tolist()
            record.update({'text': tokenizer.decode(tokens, skip_special_tokens=True),
                           'prompt_tokens': encoded.input_ids.shape[1],
                           'generated_tokens': tokens, 'completion_tokens': len(tokens),
                           'finish_reason': 'eos' if tokens[-1] == tokenizer.eos_token_id else 'length'})
        except Exception as error:
            record['error'] = type(error).__name__ + ': ' + str(error)
        record['elapsed_s'] = time.perf_counter() - started
        append_record(path, record)
        completed.add(row['case_id'])
        if len(completed) % 10 == 0:
            print(json.dumps({'model': args.model, 'completed': len(completed)}), flush=True)


if __name__ == '__main__':
    main()
