"""Executive summary: reuse the unchanged local engine for a documented Qwen3 size extension."""
import json

from model_grading.protocol import DESTINATION, LOCAL_MODELS, digest
from run_model_grading_local import main


def extend_roster():
    manifest = json.loads((DESTINATION / 'extension_manifest.json').read_text())
    for name, expected in manifest['files'].items():
        if digest(DESTINATION.parents[1] / name) != expected:
            raise ValueError(f'Roster extension changed after freeze: {name}')
    if digest(DESTINATION / 'selection.jsonl') != manifest['selection_sha256']:
        raise ValueError('Extended roster must use the original frozen panel')
    if set(manifest['added_models']) & set(LOCAL_MODELS):
        raise ValueError('An extension must not replace an original model')
    LOCAL_MODELS.update(manifest['added_models'])


if __name__ == '__main__':
    extend_roster()
    main()
