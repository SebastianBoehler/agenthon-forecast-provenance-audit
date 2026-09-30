"""Executive summary: parse the packet-builder command and report input errors clearly."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .blind import StudyInputError, load_cases, write_blinded_packets


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="provenance-audit")
    commands = parser.add_subparsers(dest="command", required=True)
    blind = commands.add_parser("blind", help="create blinded reviewer packets and a separate key")
    blind.add_argument("--input", required=True, type=Path, help="JSONL case manifest")
    blind.add_argument("--packet-dir", required=True, type=Path, help="new directory for reviewer packets")
    blind.add_argument("--key-out", required=True, type=Path, help="restricted path for the unblinding key")
    blind.add_argument("--reviewers", required=True, type=int, help="number of independent reviewers (at least 2)")
    blind.add_argument(
        "--reviewers-per-pair", type=int,
        help="reviewers assigned to each pair; default: all reviewers",
    )
    blind.add_argument("--seed", required=True, type=int, help="recorded randomization seed")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        cases = load_cases(args.input)
        count = write_blinded_packets(
            cases,
            packet_dir=args.packet_dir,
            key_path=args.key_out,
            reviewers=args.reviewers,
            seed=args.seed,
            reviewers_per_pair=args.reviewers_per_pair,
        )
    except (StudyInputError, OSError) as exc:
        print(f"provenance-audit: error: {exc}", file=sys.stderr)
        return 2
    pair_reviewers = args.reviewers if args.reviewers_per_pair is None else args.reviewers_per_pair
    print(
        f"Created blinded packets for {args.reviewers} reviewers across {count} matched pairs; "
        f"each pair was assigned to {pair_reviewers} reviewers."
    )
    return 0
