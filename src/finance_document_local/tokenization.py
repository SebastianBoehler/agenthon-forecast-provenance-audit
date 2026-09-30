"""Executive summary: use native chat tokens and verify equivalent explicit tokenization."""
import hashlib
import json

from finance_document_local.protocol import MAX_NEW_TOKENS


def encode(tokenizer, messages, options):
    encoded = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True,
        return_tensors='pt', return_dict=True, **options)
    rendered = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True, **options)
    explicit = tokenizer(rendered, add_special_tokens=False, return_tensors='pt')
    ids = encoded['input_ids'][0].tolist()
    if ids != explicit['input_ids'][0].tolist():
        raise ValueError('Native template and explicitly nonduplicated token IDs differ')
    legacy = tokenizer(rendered, return_tensors='pt')['input_ids'][0].tolist()
    return encoded, {
        'prompt_tokens': len(ids), 'prompt_token_ids_sha256': hashlib.sha256(
            json.dumps(ids, separators=(',', ':')).encode()).hexdigest(),
        'rendered_prompt_sha256': hashlib.sha256(rendered.encode()).hexdigest(),
        'explicit_no_special_tokens_identical': True,
        'legacy_default_add_special_tokens_identical': legacy == ids,
        'legacy_default_prompt_tokens': len(legacy),
        'truncation_requested': False,
    }


def check_budget(count, context_limit):
    if count + MAX_NEW_TOKENS > context_limit:
        raise ValueError('Full context plus completion budget exceeds native context window')
