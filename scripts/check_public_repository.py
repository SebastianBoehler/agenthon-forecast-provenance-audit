"""Executive summary: verify portable-bank and history identities before a public release."""

import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SECRET = re.compile(rb'sk-or-v1-[A-Za-z0-9]{32,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')


def contained(base, relative):
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError('Unsafe manifest path')
    resolved = (base / path).resolve()
    if not resolved.is_relative_to(base.resolve()) or not resolved.is_file():
        raise ValueError('Missing or escaping manifest file: ' + relative)
    return resolved


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check(root=ROOT):
    checked = 0
    for name in ('grader-comparison-v1', 'independent-financial-source-v1', 'financial-audit-summary-v1', 'final-model-extensions-v1'):
        base = root / 'artifacts' / name
        manifest = json.loads((base / 'manifest.json').read_text())
        for relative, expected in manifest['files'].items():
            raw = contained(base, relative).read_bytes()
            if sha(raw) != expected:
                raise ValueError('Evidence identity changed: ' + relative)
            checked += 1
    history = root / 'artifacts/history'
    manifest = json.loads((history / 'retired-branches-manifest.json').read_text())
    archive = history / 'retired-branches-20260930.zip'
    if sha(archive.read_bytes()) != manifest['archive_sha256']:
        raise ValueError('Retired archive identity changed')
    with ZipFile(archive) as z:
        if z.testzip() is not None or len(z.namelist()) != len(set(z.namelist())):
            raise ValueError('Invalid or duplicate archive members')
        if set(z.namelist()) != set(manifest['files']) | {'manifest.json'}:
            raise ValueError('Unexpected retired archive inventory')
        for relative, expected in manifest['files'].items():
            if Path(relative).is_absolute() or '..' in Path(relative).parts:
                raise ValueError('Unsafe archived path')
            raw = z.read(relative)
            if sha(raw) != expected or SECRET.search(raw):
                raise ValueError('Retired archive content check failed: ' + relative)
            checked += 1
    for folder in ('src', 'scripts', 'docs', 'experiments', 'paper', 'artifacts', 'literature/citations', '.github'):
        for path in (root / folder).rglob('*'):
            if path.is_file() and path.suffix in ('.py', '.md', '.json', '.jsonl', '.tex', '.txt', '.yml'):
                if SECRET.search(path.read_bytes()):
                    raise ValueError('Credential-pattern match: ' + str(path.relative_to(root)))
    for name in ('README.md', 'PAPER.md', 'docs/REPRODUCIBILITY.md'):
        path = root / name
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in link and not (path.parent / link.split('#')[0]).exists():
                raise ValueError('Broken entry-point link: ' + link)
    if 'MIT License' not in (root / 'LICENSE').read_text():
        raise ValueError('Author license missing')
    return {'status': 'PASS', 'identity_checked_files': checked,
            'retired_files': len(manifest['files']),
            'scope': 'Declared bank/history identities, entry-point links and limited credential patterns; not semantic certification.'}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
