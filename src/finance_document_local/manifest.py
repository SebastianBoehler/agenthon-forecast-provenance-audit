"""Executive summary: verify frozen files without rewriting scientific inputs."""
import hashlib
import json
from pathlib import Path

from finance_document_local.protocol import OUT, ROOT, cache


def digest(path):
    sha = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            sha.update(block)
    return sha.hexdigest()


def rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines()]


def verify(*, model_key=None):
    frozen = json.loads((OUT / 'freeze.json').read_text())
    for name, expected in frozen['files_sha256'].items():
        if digest(ROOT / name) != expected:
            raise ValueError(f'Frozen local-pilot file changed: {name}')
    if model_key is not None:
        for name, expected in frozen['checkpoint_files_sha256'][model_key].items():
            if digest(cache(model_key) / name) != expected:
                raise ValueError(f'Pinned checkpoint file changed: {model_key}/{name}')
    return frozen
