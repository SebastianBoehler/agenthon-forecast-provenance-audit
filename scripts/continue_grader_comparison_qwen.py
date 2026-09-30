"""Executive summary: prospectively separate Qwen probe readiness from strict scientific format scoring.

The original gate stopped before cohort collection. This amendment uses the saved
source-free probes only; no probe, prompt or cohort request is retried or replaced.
The frozen final-line parser and all scoring endpoints remain unchanged.
"""

import hashlib
import json
from pathlib import Path
import re

from grader_comparison.local import attempt, metadata
from grader_comparison.protocol import OUT, MODELS, REPEATS, CONFIG, frozen, write, digest, now
from grader_comparison.scalars import scalar


def main():
    cohort = frozen()
    root = OUT / "qwen"
    if list(root.glob("attempt-*.json")):
        raise ValueError("Qwen cohort was already started")
    freeze = json.loads((root / "model_freeze.json").read_text())
    if digest(MODELS["qwen"]["checkpoint"]) != freeze["checkpoint_sha256"]:
        raise ValueError("Model bytes changed")
    _, live = metadata(MODELS["qwen"])
    if live != freeze["loaded_config"] or CONFIG != freeze["request_config"]:
        raise ValueError("Model/request configuration changed")
    probes = json.loads((root / "probes.json").read_text())
    checks = []
    for record, expected in zip(probes, ("21", "4.5", "-2"), strict=True):
        match = re.search(r"Final Answer:\s*([^\n]+)\s*$", record.get("text", ""), re.I)
        passed = (record["status"] == "returned" and not record["at_output_cap"]
                  and match is not None and scalar(match[1]) == scalar(expected))
        checks.append({"original_strict_probe_pass": record["probe_pass"], "readiness_pass": passed})
    if len(checks) != 3 or not all(r["readiness_pass"] for r in checks):
        raise ValueError("Saved source-free readiness evidence insufficient")
    write(root / "precollection_amendment.json", {
        "declared_utc": now(), "cohort_calls_at_amendment": 0,
        "reason": "One correct arithmetic probe placed its final marker inline; scientific strict formatting remains unchanged.",
        "probe_sha256": digest(root / "probes.json"), "checks": checks,
        "original_scientific_freeze_sha256": digest(OUT / "freeze.json"),
        "continuation_script_sha256": digest(Path(__file__)),
        "change_scope": "source-free readiness only; no retries or scientific endpoint changes"})
    completed = 0
    for repetition in range(REPEATS):
        ordered = sorted(cohort, key=lambda c: hashlib.sha256(f"{repetition}|{c['id']}".encode()).hexdigest())
        for case in ordered:
            record = attempt(MODELS["qwen"], case["prompt"], live)
            record.update(case_id=case["id"], model="qwen", repetition=repetition)
            write(root / f"attempt-{repetition}-{completed:03d}.json", record)
            completed += 1
            print(json.dumps({"model": "qwen", "completed": completed, "scheduled": 48,
                              "status": record["status"]}), flush=True)
    write(root / "collection_receipt.json", {"completed_utc": now(), "scheduled": 48,
          "recorded": completed, "files": {p.name: digest(p) for p in root.glob("*.json")}})


if __name__ == "__main__":
    main()
