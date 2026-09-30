"""Executive summary: freeze 200 distinct public questions before observing model answers."""
import json
import platform
from collections import defaultdict
from datetime import datetime, timezone
from decimal import localcontext
from pathlib import Path

from answer_contract.sources import SOURCES, cosimo_cases
from model_grading.protocol import (DESTINATION, FAMILIES, LOCAL_MODELS, MAX_TOKENS,
                                    REMOTE_MODEL, ROOT, SAMPLE_SALT, SYSTEM, digest,
                                    question_hash, write_json)


def main():
    DESTINATION.mkdir(parents=True, exist_ok=True)
    manifest_path = DESTINATION / 'selection_manifest.json'
    if manifest_path.exists():
        raise FileExistsError('Selection is already frozen; do not overwrite it')
    with localcontext() as context:
        context.prec = 50
        grouped = defaultdict(dict)
        for case in sorted(cosimo_cases(), key=lambda c: c.case_id):
            if case.family in FAMILIES:
                grouped[case.family].setdefault(case.prompt, case)
        selection = []
        for family in FAMILIES:
            ranked = sorted(grouped[family].values(),
                            key=lambda c: question_hash(SAMPLE_SALT + c.prompt))
            for case in ranked[:50]:
                selection.append({
                    'case_id': case.case_id, 'family': family, 'prompt': case.prompt,
                    'question_hash': question_hash(case.prompt),
                    'gold': str(case.gold), 'formula': str(case.formula),
                    'target': str(case.target), 'quantum': str(case.quantum),
                    'requested_rounding': case.requested_rounding,
                })
    path = DESTINATION / 'selection.jsonl'
    path.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in selection))
    protocol = ROOT / 'docs/MODEL_GRADING_PROTOCOL_V1.md'
    frozen = [path, protocol, ROOT / 'scripts/prepare_model_grading.py']
    frozen += sorted((ROOT / 'scripts').glob('*model_grading*.py'))
    frozen += sorted((ROOT / 'src/model_grading').glob('*.py'))
    frozen += sorted((ROOT / 'src/answer_contract').glob('*.py'))
    write_json(manifest_path, {
        'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(), 'source': SOURCES['cosimo'],
        'selection_rule': 'deduplicate prompt; smallest case ID; salted SHA256 order; first 50/family',
        'selection_salt': SAMPLE_SALT,
        'family_unique_populations': {f: len(grouped[f]) for f in FAMILIES},
        'questions': 200, 'system_prompt': SYSTEM, 'local_models': LOCAL_MODELS,
        'remote_model': REMOTE_MODEL, 'max_new_tokens': MAX_TOKENS,
        'frozen_sha256': {str(p.relative_to(ROOT)): digest(p) for p in frozen},
    })
    print(json.dumps({'questions': len(selection), 'selection_sha256': digest(path)}))


if __name__ == '__main__':
    main()
