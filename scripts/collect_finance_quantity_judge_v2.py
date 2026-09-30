#!/usr/bin/env python3
"""Executive summary: execute the separately frozen pointer diagnostic under existing authorization."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from finance_quantity_judge_v2.freeze import input_hashes, verify
from finance_quantity_judge_v2.protocol import OUT
from finance_quantity_judge_v2.runner import authored_jobs, jobs, run
from finance_quantity_transfer.protocol import OUT as V1_OUT, digest, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("authored-preflight", "collect"))
    parser.add_argument("--allow-paid-calls", action="store_true", required=True)
    parser.add_argument("--freeze", type=Path, default=OUT / "plan_freeze.json")
    parser.add_argument("--ledger", type=Path, default=V1_OUT / "spend_ledger.jsonl")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    frozen = json.loads(args.freeze.read_text())
    verify(frozen)  # Verify the plan before selected financial inputs can be accessed.
    authored = args.mode == "authored-preflight"
    source = V1_OUT / ("authored-paid-preflight" if authored else "collection")
    v1_run, calls = source / "run.json", source / "calls.jsonl"
    if json.loads(v1_run.read_text())["state"] != "complete":
        raise ValueError("V1 collection/preflight must be complete; no selective judging")
    inputs = [v1_run, calls]
    if authored:
        items = authored_jobs(rows(calls))
    else:
        packet = V1_OUT / "experiment_packet.jsonl"
        v1_frozen = json.loads((V1_OUT / "experiment_freeze.json").read_text())
        if digest(packet) != v1_frozen["inputs"]["experiment_packet"]["sha256"]:
            raise ValueError("Original V1 experiment packet changed")
        inputs.append(packet)
        items = jobs(rows(packet), rows(calls))
    output = args.output or OUT / ("authored-paid-preflight" if authored else "collection")
    result = run(items, output, args.ledger, frozen, input_hashes(inputs), authored=authored)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
