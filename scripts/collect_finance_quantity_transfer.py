#!/usr/bin/env python3
"""Executive summary: preflight locally or collect an explicitly authorized, frozen paired study."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from finance_quantity_transfer.freeze import verify_freeze
from finance_quantity_transfer.protocol import OUT, rows
from finance_quantity_transfer.runner import authored_case, preflight, run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    local = sub.add_parser("preflight")
    local.add_argument("--allow-paid-calls", action="store_true")
    local.add_argument("--output", type=Path, default=OUT / "authored-paid-preflight")
    local.add_argument("--ledger", type=Path, default=OUT / "spend_ledger.jsonl")
    collect = sub.add_parser("collect")
    collect.add_argument("--packet", type=Path, required=True)
    collect.add_argument("--freeze", type=Path, required=True)
    collect.add_argument("--allow-paid-calls", action="store_true", required=True)
    collect.add_argument("--output", type=Path, default=OUT / "collection")
    collect.add_argument("--ledger", type=Path, default=OUT / "spend_ledger.jsonl")
    args = parser.parse_args()
    if args.command == "preflight":
        result = run([authored_case()], args.output, args.ledger) if args.allow_paid_calls else preflight()
    else:
        frozen = json.loads(args.freeze.read_text())
        verify_freeze(frozen, args.packet)
        result = run(rows(args.packet), args.output, args.ledger, frozen)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
