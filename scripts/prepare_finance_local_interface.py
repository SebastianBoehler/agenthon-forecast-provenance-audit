"""Executive summary: select and token-audit a new local pilot before financial responses."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

os.environ['USE_TF'] = '0'
os.environ['USE_FLAX'] = '0'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
from transformers import AutoTokenizer

from finance_document_local.protocol import (
    CASES_PER_SOURCE, CONDITIONS, MODELS, OUT, ROOT, SALT, cache)
from finance_document_local.tokenization import check_budget, encode
from finance_document_review.model_protocol import digest


def main():
    if OUT.exists():
        raise ValueError('Preserve the existing local pilot; never reselect it')
    source = ROOT / 'outputs/finance-document-audit-v1/reviewer_a.jsonl'
    original = [json.loads(line) for line in source.read_text().splitlines()]
    if len(original) != 96 or len({r['case_id'] for r in original}) != 96:
        raise ValueError('Original cohort identity changed')
    def order(row):
        return hashlib.sha256((SALT + '\n' + row['case_id']).encode()).hexdigest()
    selected = []
    for name in ['finqa', 'tatqa']:
        subset = sorted((r for r in original if r['case_id'].startswith(name + ':')), key=order)
        selected.extend({'case_id': r['case_id'], 'source': name, 'order_sha256': order(r),
                         'prompt': json.dumps({'question': r['question'],
                                               'original_context': r['original_context']},
                                              sort_keys=True, ensure_ascii=False)}
                        for r in subset[:CASES_PER_SOURCE])
    audits, tokenizers = [], {}
    for model, spec in MODELS.items():
        path = cache(model)
        tokenizers[model] = {str(p.relative_to(path)): digest(p) for p in path.iterdir()
                             if p.is_file() and p.suffix != '.safetensors'}
        tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
        context = json.loads((path / 'config.json').read_text())['max_position_embeddings']
        for case in selected:
            for condition, system in CONDITIONS.items():
                messages = [{'role': 'system', 'content': system},
                            {'role': 'user', 'content': case['prompt']}]
                _, record = encode(tokenizer, messages, spec['template_options'])
                check_budget(record['prompt_tokens'], context)
                audits.append({'model_key': model, 'case_id': case['case_id'],
                               'condition': condition, 'context_limit': context, **record})
    OUT.mkdir(parents=True)
    for name, records in [('selection.jsonl', selected), ('token_audit.jsonl', audits)]:
        with (OUT / name).open('x') as stream:
            stream.write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in records))
    result = {'executive_summary': 'Pre-financial-response selection and native token audit.',
              'created_utc': datetime.now(timezone.utc).isoformat(), 'cases': len(selected),
              'conditions': len(CONDITIONS), 'planned_attempts': len(audits),
              'selection_sha256': digest(OUT / 'selection.jsonl'),
              'source_packet_sha256': digest(source), 'tokenizer_files_sha256': tokenizers,
              'token_id_checks': len(audits), 'native_explicit_parity': True,
              'legacy_default_path_differences': sum(not r['legacy_default_add_special_tokens_identical'] for r in audits),
              'max_prompt_tokens': max(r['prompt_tokens'] for r in audits),
              'context_truncation': False, 'financial_model_answers_seen': 0}
    (OUT / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['cases', 'planned_attempts', 'token_id_checks',
                                          'legacy_default_path_differences', 'max_prompt_tokens']}))


if __name__ == '__main__':
    main()
