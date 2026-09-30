"""Executive summary: generate once with pinned local FP16 models on Apple MPS."""
import os
import time

os.environ['USE_TF'] = '0'
os.environ['USE_FLAX'] = '0'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from finance_document_local.protocol import MAX_NEW_TOKENS, MODELS, cache
from finance_document_local.tokenization import check_budget, encode


def load(model_key):
    if not torch.backends.mps.is_available():
        raise RuntimeError('Frozen pilot requires Apple MPS')
    if os.environ.get('PYTORCH_ENABLE_MPS_FALLBACK') == '1':
        raise RuntimeError('CPU fallback would change the frozen backend')
    path = cache(model_key)
    tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        path, local_files_only=True, torch_dtype=torch.float16).to('mps').eval()
    if any(p.device.type != 'mps' or p.dtype != torch.float16
           for p in model.parameters()):
        raise RuntimeError('Model parameters do not match FP16 MPS')
    return model, tokenizer


def generate(model_key, model, tokenizer, messages, *, max_new_tokens=MAX_NEW_TOKENS):
    encoded, audit = encode(tokenizer, messages, MODELS[model_key]['template_options'])
    check_budget(audit['prompt_tokens'], model.config.max_position_embeddings)
    encoded = {key: value.to('mps') for key, value in encoded.items()}
    eos = model.generation_config.eos_token_id
    eos_ids = eos if isinstance(eos, list) else [eos]
    if not eos_ids or any(v is None for v in eos_ids):
        raise RuntimeError('Native generation has no EOS token')
    pad = model.generation_config.pad_token_id
    torch.mps.synchronize()
    start = time.monotonic()
    with torch.inference_mode():
        output = model.generate(**encoded, do_sample=False,
                                max_new_tokens=max_new_tokens,
                                pad_token_id=pad if pad is not None else eos_ids[0])
    torch.mps.synchronize()
    elapsed = time.monotonic() - start
    ids = output[0, audit['prompt_tokens']:].tolist()
    stopped = bool(ids and ids[-1] in eos_ids)
    return {'text': tokenizer.decode(ids, skip_special_tokens=True),
            'generated_token_ids': ids, 'completion_tokens': len(ids),
            'finish_reason': 'eos' if stopped else 'length',
            'max_new_tokens': max_new_tokens, 'elapsed_seconds': elapsed,
            'runtime_ok': True, 'token_audit_ok': True,
            'device': 'mps', 'dtype': 'float16', 'do_sample': False,
            'eos_token_ids': eos_ids, 'error': None, **audit}
