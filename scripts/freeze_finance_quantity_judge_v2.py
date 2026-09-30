#!/usr/bin/env python3
"""Executive summary: save a new source-free pointer-amendment freeze without any model call."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from finance_quantity_judge_v2.freeze import make_freeze
from finance_quantity_judge_v2.protocol import OUT
from finance_quantity_transfer.protocol import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT / "plan_freeze.json")
    args = parser.parse_args()
    frozen = make_freeze()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(frozen, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"freeze_sha256": digest(args.output), "model_calls": 0,
                      "financial_judges": 64, "authored_preflight_judges": 2, "answer_calls": 0}))


if __name__ == "__main__":
    main()
