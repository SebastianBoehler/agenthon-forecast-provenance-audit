"""Executive summary: pin, hash and write local audit artifacts without overwriting."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "experiments/finance_document_audit_sources_v1.json"
PROTOCOL = ROOT / "docs/FINANCE_DOCUMENT_AUDIT_PROTOCOL_V1.md"
SCRIPTS = Path(__file__).resolve().parent
OUT = ROOT / "outputs/finance-document-audit-v1"
FREEZE = OUT / "protocol_freeze_v1a.json"
INITIAL_FREEZE = OUT / "protocol_freeze_v1.json"


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_json(path: Path) -> object:
    return json.loads(path.read_text())


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as stream:
        for row in rows:
            stream.write(canonical(row).decode() + "\n")


def frozen_inputs() -> dict[str, str]:
    paths = [CONFIG, PROTOCOL, *sorted(SCRIPTS.glob("*.py"))]
    return {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in paths}


def require_freeze() -> dict:
    freeze = read_json(FREEZE)
    if freeze["files_sha256"] != frozen_inputs():
        raise ValueError("Frozen code/protocol changed: preserve V1 and declare a prospective amendment.")
    if freeze["selection_occurred_before_freeze"] is not False:
        raise ValueError("Invalid prospective freeze declaration")
    return freeze


def freeze_protocol() -> None:
    if (OUT / "raw").exists():
        raise ValueError("Raw corpus directory already exists; initial prospective freeze refused")
    write_json(FREEZE, {
        "executive_summary": "Eligibility, sampling and blank review rubric frozen before corpus download or inspection.",
        "created_utc": timestamp(), "files_sha256": frozen_inputs(),
        "config_sha256": digest(CONFIG.read_bytes()),
        "corpus_opened_or_selected_before_freeze": False,
        "selection_occurred_before_freeze": False,
        "status": "prospective_protocol_frozen_no_cases_selected"
    })


def freeze_amendment() -> None:
    if any((OUT / name).exists() for name in ("selection_metadata.jsonl", "reviewer_a.jsonl", "selection_manifest.json")):
        raise ValueError("Cases already selected; prospective amendment refused")
    initial = read_json(INITIAL_FREEZE)
    history = OUT / "protocol-history/v1"
    if digest((history / "protocol_freeze_v1.json").read_bytes()) != digest(INITIAL_FREEZE.read_bytes()):
        raise ValueError("Initial freeze was not preserved")
    for path, expected in initial["files_sha256"].items():
        if digest((history / path).read_bytes()) != expected:
            raise ValueError("Initial frozen code/config/protocol bytes were not preserved")
    write_json(FREEZE, {
        "executive_summary": "Prospective V1a identity-join amendment after schema inspection, before selecting any cases.",
        "created_utc": timestamp(), "files_sha256": frozen_inputs(),
        "config_sha256": digest(CONFIG.read_bytes()),
        "initial_freeze_sha256": digest(INITIAL_FREEZE.read_bytes()),
        "initial_freeze_utc": initial["created_utc"],
        "selection_occurred_before_freeze": False,
        "schema_inspection_before_amendment": True,
        "amendment": "TAT-QA native UIDs changed; join only unique exact question/context hashes, exclude unmatched identities without inspecting answer values.",
        "status": "prospective_amendment_frozen_no_cases_selected"
    })


def require_text(value: object, description: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing/nontext {description}")
    return value


def require_table(value: object, description: str) -> list:
    if not isinstance(value, list) or not value or any(
        not isinstance(row, list) or not row or any(not isinstance(v, str) for v in row)
        for row in value
    ):
        raise ValueError(f"Invalid {description}: expected nonempty string-cell table")
    return value
