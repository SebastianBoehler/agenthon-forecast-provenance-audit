"""Executive summary: hash-bind the finite generator comparison before producing any case."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform

from .source import ROOT, BASE, REVISION, FUNCTIONS, sources

OUT = ROOT / "outputs/independent-financial-source-v1"
FILES = ["docs/INDEPENDENT_FINCHAIN_CODE_PROTOCOL_V1.md", "tests/test_independent_finance.py",
         "scripts/prepare_independent_finance.py", "scripts/run_independent_finance.py",
         "scripts/replay_independent_finance.py"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def freeze():
    target = OUT / "freeze.json"
    if target.exists():
        raise FileExistsError("An existing freeze cannot be replaced")
    sources()  # Verify all source fragment and reconstructed-file hashes without executing functions.
    paths = [ROOT / name for name in FILES]
    paths += sorted((ROOT / "src/independent_finance").glob("*.py"))
    paths += sorted(path for path in BASE.iterdir() if path.is_file() and path.name != "README.md")
    record = {"executive_summary": "Prospective source/code/runtime freeze; no instance generated yet.",
              "frozen_at_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
              "platform": platform.platform(), "code_revision": REVISION, "seeds": list(range(100)),
              "functions": FUNCTIONS, "files": {str(p.relative_to(ROOT)): digest(p) for p in paths},
              "scheduled": 300, "generation": "One random.Random(seed) per native selected function call"}
    write(target, record)
    return record


def verified_freeze(base=OUT):
    record = json.loads((base / "freeze.json").read_text())
    if record["code_revision"] != REVISION or record["seeds"] != list(range(100)):
        raise ValueError("Frozen revision or seed membership changed")
    if record["functions"] != {k: list(v) for k, v in FUNCTIONS.items()} or record["scheduled"] != 300:
        raise ValueError("Frozen function or scheduled denominator changed")
    for name, checksum in record["files"].items():
        if digest(ROOT / name) != checksum:
            raise ValueError("Frozen source or implementation changed: " + name)
    return record
