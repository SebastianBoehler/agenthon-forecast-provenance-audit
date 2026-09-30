#!/usr/bin/env python3
"""Executive summary: freeze reviewed source and locked packet/approval identities, without calling models."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from finance_quantity_transfer.freeze import make_freeze


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ["packet", "reference-lock", "comparison", "semantic-approval", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    frozen = make_freeze(args.packet, args.reference_lock, args.comparison, args.semantic_approval)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(frozen, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"freeze": str(args.output), "model_calls": 0, "planned_answers": 64,
                      "planned_judges": 64}, sort_keys=True))


if __name__ == "__main__":
    main()
