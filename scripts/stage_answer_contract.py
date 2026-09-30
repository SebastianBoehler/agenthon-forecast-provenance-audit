"""Executive summary: download only pinned public audit inputs and verify every source hash."""
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

from answer_contract.sources import SOURCES


def stage(url: str, destination: Path, digest: str):
    if destination.exists():
        raw = destination.read_bytes()
    else:
        with urlopen(url, timeout=30) as response:
            raw = response.read()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != digest:
        raise ValueError(f'Input hash mismatch for {destination}: {actual}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        destination.write_bytes(raw)
    print(destination, actual)


def main():
    for spec in SOURCES.values():
        stage(spec['url'], Path(spec['path']), spec['sha256'])
    manifest = json.loads(Path('experiments/cosimo_source_manifest.json').read_text())
    for spec in manifest['files']:
        url = spec['url'].replace('https://github.com/', 'https://raw.githubusercontent.com/').replace('/blob/', '/')
        stage(url, Path(spec['local_path']), spec['sha256'])
    destination = Path('literature/pdfs/cosimo-source-manifest.json')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(manifest, indent=2)+'\n')


if __name__ == '__main__':
    main()
