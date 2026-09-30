"""Executive summary: package current paper and follow-ups beside the immutable prior archive.

Preserve history as a nested original ZIP. Include a portable Gemma score replay;
exclude model weights, credentials and original financial-report contexts. Local
document ledgers are inspectable but need separately acquired inputs for replay.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs/answer-contract-research-20260930-document-extension.zip"
BASE_SHA = "b0c28dc488d8ddba89ca336224699bbdd7ad4bdc72bad03e452b631538df0631"
TARGET = ROOT / "outputs/answer-contract-research-20260930-followup-review.zip"
MANIFEST = ROOT / "outputs/submission-iteration-20260930/followup_review_manifest.json"
RECEIPT = ROOT / "outputs/submission-iteration-20260930/followup_review_receipt.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selected_files():
    frozen = json.loads((ROOT / "outputs/model-grading-lmstudio-v2/freeze.json").read_text())
    names = set(frozen["files"])
    local = json.loads((ROOT / "outputs/finance-local-interface-v1/freeze.json").read_text())
    names.update(p for p in local["files_sha256"] if p.startswith(("src/", "scripts/", "tests/", "docs/")))
    for pattern in ("docs/FINANCE_LOCAL_INTERFACE*.md", "docs/MODEL_GRADING_LMSTUDIO*.md"):
        names.update(str(p.relative_to(ROOT)) for p in ROOT.glob(pattern))
    names.update([
        "paper/answer_contract_audit.tex", "pyproject.toml",
        "docs/AGENTHON_SUBMISSION_ITERATION_2026-09-30.md",
        "docs/AGENTHON_ORGANIZER_RESEARCH_LENSES_2026-09-30.md",
        "docs/AGENTHON_INDUSTRY_RESEARCH_LENSES_2026-09-30.md",
        "docs/DEADLINE_EXPERIMENT_PLAN_2026-09-30.md",
        "docs/MAIN_TRACK_RIGOR_AUDIT_2026-09-30.md",
        "docs/SUBMISSION_FORMAT_2026-09-30.md",
        "docs/SUBMISSION_REFERENCE_ADDITIONS_2026-09-30.md",
        "scripts/independent_contract_validation.py",
        "scripts/validate_model_grading_outputs.py",
        "scripts/validate_model_grading_conventions.py",
        "scripts/validate_model_grading_lmstudio.py",
        "scripts/validate_finance_local_interface.py",
        "scripts/diagnose_finance_local_mps.py",
        "scripts/replay_lmstudio_saved_scores.py",
        "scripts/restore_lmstudio_v2_summary.py",
        "scripts/package_submission_followup.py",
    ])
    for folder in ("model-grading-lmstudio-v1", "model-grading-lmstudio-v2", "finance-local-interface-v1"):
        for path in (ROOT / "outputs" / folder).iterdir():
            if path.suffix in (".json", ".jsonl") and path.name != "selection.jsonl":
                names.add(str(path.relative_to(ROOT)))
    return sorted(names)


README = """## Executive summary (read this first)

This local review package contains the current standalone manuscript, current
scientific review/plan, complete Gemma saved-answer evidence and failed local
document-pilot ledgers. The earlier document-extension archive is nested unchanged
under historical/, preserving its older paper, manifests and replay evidence.
The current paper is a later revision; never claim it has the older paper hash.
This package is not a submitted PDF, public release or acceptance receipt.

## Portable numerical replay

Extract this ZIP into an empty directory. From that directory, use a Python
runtime with pandas and mpmath (versions are recorded in the prior archive):

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/replay_lmstudio_saved_scores.py --output gemma_replay.json

The replay checks scientific input bindings, original question identities, raw
native requests/replies, four saved score streams and family aggregates. It
performs no inference or external weight/engine hash checks. Independent full
postflight receipts record those checks on the author's local machine; they are
historical evidence, not a guarantee the reviewer has equivalent caches.

## Separate historical and fresh-inference prerequisites

Extract the nested historical archive into a separate directory and follow its
own README for the original synthetic/document metric replays. Preserve that
directory independently; do not overlay the current paper on its historical
hash-bound paper and then claim its integrity validation passes.

The failed local document pilot is retained for inspection. Its original context
selection, source report contexts, acquired benchmarks and local model/tokenizer
caches are not supplied here. Replaying that full pilot needs the original
acquisition and frozen prerequisites; this ZIP does not certify a portable replay
of it. No full report-context corpus, model weights, local LM Studio preferences,+API key or environment file is included in the follow-up tree.

Fresh inference additionally needs recorded weights, native template, engine and
hardware. The upstream Gemma weight commit is unknown; concrete local bytes were
hashed. The failed V1 launch gate, V2 amendment and summary-path mistake/copy
receipt remain separate. The frozen analyzer still has its documented reporting
path defect; numerical replay reads saved artifacts rather than rerunning it.
"""


def main():
    if digest(BASE) != BASE_SHA:
        raise ValueError("Historical archive identity changed")
    if TARGET.exists() or MANIFEST.exists() or RECEIPT.exists():
        raise FileExistsError("Never replace a previous review package or receipt")
    names = selected_files()
    manifest = {
        "executive_summary": "Current review evidence with unchanged historical archive; portable Gemma numerical replay only.",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "historical_archive_sha256": BASE_SHA,
        "files_sha256": {name: digest(ROOT / name) for name in names},
        "excluded_followup_inputs": ["full financial-report contexts", "local document selection contexts", "model weights and engine binaries", "LM Studio preferences", "credentials and environment files"],
        "cloud_spend_usd": 0,
        "authorized_cloud_cap_usd": 10,
        "standalone_source_compiled": True,
        "rendered_body_pages_verified": False,
        "public_release_or_submission": False,
    }
    MANIFEST.parent.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    with ZipFile(TARGET, "x", compression=ZIP_DEFLATED) as archive:
        archive.write(BASE, "historical/" + BASE.name)
        archive.writestr("README.md", README)
        archive.write(MANIFEST, "followup_review_manifest.json")
        for name in names:
            archive.write(ROOT / name, name)
    with ZipFile(TARGET) as archive:
        assert archive.testzip() is None
        assert hashlib.sha256(archive.read("historical/" + BASE.name)).hexdigest() == BASE_SHA
        for name, expected in manifest["files_sha256"].items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == expected, name
        count = len(archive.namelist())
    receipt = {"executive_summary": "PASS: ZIP member identities and immutable nested archive; replay is checked separately.", "zip_sha256": digest(TARGET), "manifest_sha256": digest(MANIFEST), "entries": count, "hashed_followup_files": len(names), "paper_sha256": digest(ROOT / "paper/answer_contract_audit.tex")}
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
