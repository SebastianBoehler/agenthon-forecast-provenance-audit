"""Executive summary: preserve a local author-review package and test its portable replays."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'outputs/author-led-submission-final-v2-20260930.zip'
CITATIONS = ROOT / 'outputs/citation-workspace/voice-final-submission-20260930'
HISTORICAL = ROOT / 'outputs/answer-contract-research-20260930-document-extension.zip'
HISTORICAL_SHA = 'b0c28dc488d8ddba89ca336224699bbdd7ad4bdc72bad03e452b631538df0631'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selected():
    names = {'README.md', 'PAPER.md', 'LICENSE', 'pyproject.toml', '.gitignore',
             'docs/REPRODUCIBILITY.md', 'docs/PUBLIC_RELEASE_REVIEW_2026-09-30.md',
             'docs/FINAL_MODEL_EXTENSION_RESULTS_V1.md',
             'scripts/check_public_repository.py', 'scripts/replay_final_extensions.py',
        'paper/answer_contract_voice_draft.tex', 'literature/citations/voice_source_catalog.json',
        'docs/AUTHOR_LED_SUBMISSION_REVIEW_2026-09-30.md',
        'docs/FINAL_SHORT_APPENDIX_REVIEW_2026-09-30.md',
        'docs/APPENDIX_CONVENTIONS_2026-09-30.md', 'docs/FINAL_BASE_HANDOFF_2026-09-30.md',
        'scripts/check_voice_submission.py', 'scripts/package_voice_submission.py',
        'scripts/replay_grader_comparison.py', 'scripts/replay_independent_finance.py',
        'scripts/validate_recursivemas_authored_controls.py',
        'outputs/answer-contract-v1/results.json', 'outputs/answer-contract-v1/manifest.json',
    }
    for folder in ('artifacts/grader-comparison-v1', 'artifacts/independent-financial-source-v1',
                   'artifacts/finchain-source-v1', 'artifacts/recursivemas-scoring-source-v1',
                   'artifacts/history', 'artifacts/financial-audit-summary-v1',
                   'artifacts/final-model-extensions-v1'):
        names.update(str(p.relative_to(ROOT)) for p in (ROOT / folder).rglob('*') if p.is_file())
    for folder in ('src', 'scripts', 'tests'):
        names.update(str(p.relative_to(ROOT)) for p in (ROOT / folder).rglob('*.py')
                     if '__pycache__' not in p.parts)
    names.update(str(p.relative_to(ROOT)) for p in (ROOT / 'experiments').glob('*') if p.is_file())
    names.update(str(p.relative_to(ROOT)) for p in (ROOT / 'docs').glob('*.md'))
    names.update(str(p.relative_to(ROOT)) for p in (ROOT / '.github/workflows').glob('*.yml'))
    freeze = json.loads((ROOT / 'artifacts/independent-financial-source-v1/freeze.json').read_text())
    names.update(freeze['files'])
    return sorted(names)


README = '''## Executive summary (read this first)

This local author-review package contains the completed standalone manuscript,
review notes, a preserved historical research archive, and two tested portable
follow-up replays. It is not a submitted PDF, public release or acceptance receipt.
The original synthetic/document archive is nested unchanged under historical/;
extract it separately and follow its own README. Do not overlay a later paper
onto a historical hash-bound archive and claim its original integrity passes.

From this package's root, Python 3.11 or later and its standard library suffice:

    PYTHONPATH=src python scripts/replay_grader_comparison.py
    PYTHONPATH=src python scripts/replay_independent_finance.py
    python scripts/check_voice_submission.py
    PYTHONPATH=src python scripts/replay_final_extensions.py
    python scripts/check_public_repository.py

The first replay checks 2,548 authored controls and 96 scalar attempt projections.
The second regenerates 300 native FinChain-template questions/solutions and their
scalar checks. The third checks saved census/figure counts and source structure.
The final model replay checks 96 additional GLM/Llama scalar attempts and observed
API usage. The public check verifies history and evidence identities.
None performs model inference or certifies financial semantic truth. Source
licenses/notices remain beside their fragments. Fresh inference and full-response
extraction require separately acquired inputs, recorded weights and runtimes.

The manuscript uses the unchanged embedded NeurIPS style and compiles in Codex's
native editor. Export the current preview after an author page-layout review;
no current submission PDF is included here. The UI tool blocked preview inspection.
Citation review contains exact saved excerpts, claim inventory and retrieval flags;
full source PDFs and extracted full-text page caches are not newly bundled.
All source texts were locally available. Exact-location checks are not semantic
certification. Read the passages and claims before treating them as approved.
'''


def main():
    if TARGET.exists():
        raise FileExistsError('Never replace an earlier author-review package')
    assert digest(HISTORICAL) == HISTORICAL_SHA
    names = selected()
    for name in names:
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or not (ROOT / path).resolve().is_relative_to(ROOT):
            raise ValueError('Unsafe package input: ' + name)
    manifest = {
        'executive_summary': 'Local submission-draft and replay package; author review and PDF export remain.',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'files_sha256': {name: digest(ROOT / name) for name in names},
        'historical_archive_sha256': HISTORICAL_SHA,
        'source_compiled': True, 'rendered_layout_verified': False, 'current_pdf_exported': False,
        'semantic_citation_certification': False, 'public_release_or_submission': False,
    }
    with ZipFile(TARGET, 'x', compression=ZIP_DEFLATED) as archive:
        archive.writestr('PACKAGE.md', README)
        archive.writestr('package_manifest.json', json.dumps(manifest, indent=2) + '\n')
        for name in names:
            archive.write(ROOT / name, name)
        for name in ('summary.json', 'claims.json', 'source_manifest.json', 'excerpt_ledger.jsonl', 'receipt.json'):
            archive.write(CITATIONS / name, 'citation-review/' + name)
        archive.write(HISTORICAL, 'historical/' + HISTORICAL.name)
    with ZipFile(TARGET) as archive, tempfile.TemporaryDirectory(prefix='agenthon-author-review-') as tmp:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(set(archive.namelist())), 'Duplicate package members'
        archive.extractall(tmp)
        base = Path(tmp)
        for name, expected in manifest['files_sha256'].items():
            assert digest(base / name) == expected, name
        assert digest(base / 'historical' / HISTORICAL.name) == HISTORICAL_SHA
        env = dict(os.environ, PYTHONPATH=str(base / 'src'), PYTHONDONTWRITEBYTECODE='1')
        checks = []
        for script in ('replay_grader_comparison.py', 'replay_independent_finance.py', 'replay_final_extensions.py',
                       'check_voice_submission.py', 'check_public_repository.py'):
            run = subprocess.run([sys.executable, 'scripts/' + script], cwd=base, env=env,
                                 text=True, capture_output=True, check=True)
            checks.append(json.loads(run.stdout))
    receipt = {'status': 'PASS', 'zip_sha256': digest(TARGET), 'bytes': TARGET.stat().st_size,
               'hashed_files': len(names), 'clean_extraction_checks': checks, **manifest}
    TARGET.with_suffix('.receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'zip': str(TARGET), 'bytes': TARGET.stat().st_size,
                      'hashed_files': len(names), 'clean_extraction_checks': checks}, indent=2))


if __name__ == '__main__':
    main()
