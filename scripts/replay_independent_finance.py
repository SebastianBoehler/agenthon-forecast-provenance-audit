"""Executive summary: verify immutable bank hashes and reproduce native source, exact values and summaries."""

import hashlib
import json

from independent_finance.analysis import assess, summarize
from independent_finance.protocol import ROOT, digest, verified_freeze
from independent_finance.source import generate


def replay(base):
    verified_freeze(base)
    receipt = json.loads((base / "collection_receipt.json").read_text())
    for stem, extension in (("freeze", ".json"), ("analysis", ".json"), ("attempts", ".jsonl")):
        if receipt[stem + "_sha256"] != digest(base / (stem + extension)):
            raise ValueError("Collection receipt changed: " + stem)
    rows = [json.loads(line) for line in (base / "attempts.jsonl").read_text().splitlines()]
    for row in rows:
        question, solution = generate(row["family"], row["seed"])
        if question != row.get("question") or solution != row.get("solution"):
            raise ValueError("Native generated instance changed: " + row["id"])
        for key, text in (("question", question), ("solution", solution)):
            if hashlib.sha256(text.encode()).hexdigest() != row[key + "_sha256"]:
                raise ValueError("Native text checksum changed")
        if row["status"] != "assessed":
            raise ValueError("Replay encountered a nondecision; inspect preserved attempt")
        if any(row[key] != value for key, value in assess(row["family"], question, solution).items()):
            raise ValueError("Reference or compatibility endpoint changed: " + row["id"])
    if summarize(rows) != json.loads((base / "analysis.json").read_text()):
        raise ValueError("Independent-source summary changed")
    return {"status": "PASS", "native_instances": len(rows), "scope": "Current pinned template code and scalar endpoints"}


if __name__ == "__main__":
    print(json.dumps(replay(ROOT / "artifacts/independent-financial-source-v1")))
