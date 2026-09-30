"""Executive summary: exercise pairing, randomization, blinding, and key-file safety."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from provenance_audit.blind import StudyInputError, load_cases, write_blinded_packets
from provenance_audit.cli import main


def records(pair_count: int = 6) -> list[dict[str, object]]:
    result = []
    for index in range(pair_count):
        for provenance in ("derived", "answer_first"):
            result.append({
                "case_id": f"case-{index}-{provenance}",
                "pair_id": f"pair-{index}",
                "provenance": provenance,
                "context": {"card": f"card-{index}", "evidence": ["dated source"]},
                "forecast": {"draws": [0.1, 0.2, 0.3]},
                "rationale": f"Rationale wording {index} {len(provenance)}-char condition-specific text.",
                "generation_record": {"prompt_hash": f"hash-{index}-{provenance}"},
            })
    return result


class BlindPacketTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.manifest = self.root / "cases.jsonl"
        self._write_records(records())

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _write_records(self, rows: list[dict[str, object]]) -> None:
        self.manifest.write_text(
            "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
        )

    def _run(
        self, reviewers: int = 4, seed: int = 19, suffix: str = "run",
        reviewers_per_pair: int | None = None,
    ) -> tuple[Path, Path]:
        packet_dir = self.root / f"packets-{suffix}"
        key_path = self.root / f"restricted-{suffix}" / "key.json"
        cases = load_cases(self.manifest)
        count = write_blinded_packets(
            cases, packet_dir=packet_dir, key_path=key_path, reviewers=reviewers, seed=seed,
            reviewers_per_pair=reviewers_per_pair,
        )
        self.assertEqual(count, len({case.pair_id for case in cases}))
        return packet_dir, key_path

    def test_rejects_unmatched_context_and_forecast(self) -> None:
        rows = records()
        rows[1]["context"] = {"different": True}
        self._write_records(rows)
        with self.assertRaisesRegex(StudyInputError, "identical context and forecast"):
            load_cases(self.manifest)

    def test_rejects_duplicate_ids_and_incomplete_pairs(self) -> None:
        rows = records()
        rows[1]["case_id"] = rows[0]["case_id"]
        self._write_records(rows)
        with self.assertRaisesRegex(StudyInputError, "duplicate case_id"):
            load_cases(self.manifest)

        rows = records()
        rows.pop()
        self._write_records(rows)
        with self.assertRaisesRegex(StudyInputError, "exactly one case per provenance"):
            load_cases(self.manifest)

    def test_packets_hide_ids_labels_and_generation_records(self) -> None:
        packet_dir, key_path = self._run()
        key = json.loads(key_path.read_text(encoding="utf-8"))
        self.assertEqual(key["seed"], 19)
        self.assertEqual(key["reviewers"], 4)
        self.assertEqual(len(key["assignments"]), 24)

        key_tokens = {row["case_token"] for row in key["assignments"]}
        seen_tokens: set[str] = set()
        for packet in sorted(packet_dir.glob("reviewer-*/cases.jsonl")):
            rows = [json.loads(line) for line in packet.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows), 6)
            self.assertEqual(len({row["case_token"] for row in rows}), 6)
            for row in rows:
                self.assertEqual(set(row), {"case_token", "context", "forecast", "rationale"})
                self.assertNotIn("pair_id", row["context"])
                self.assertNotIn("answer_first", row["rationale"])
                self.assertNotIn("derived", row["rationale"])
                seen_tokens.add(row["case_token"])
        self.assertEqual(seen_tokens, key_tokens)
        self.assertEqual(os.stat(key_path).st_mode & 0o777, 0o600)

    def test_pair_assignments_are_counterbalanced(self) -> None:
        packet_dir, key_path = self._run(reviewers=5)
        key = json.loads(key_path.read_text(encoding="utf-8"))
        packets = {
            path.parent.name: [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            for path in packet_dir.glob("reviewer-*/cases.jsonl")
        }
        for pair_id in {row["pair_id"] for row in key["assignments"]}:
            labels = []
            for reviewer, rows in packets.items():
                tokens = {row["case_token"] for row in rows}
                assignment = next(
                    item for item in key["assignments"]
                    if item["reviewer"] == reviewer and item["case_token"] in tokens
                    and item["pair_id"] == pair_id
                )
                labels.append(assignment["provenance"])
            self.assertLessEqual(abs(labels.count("derived") - labels.count("answer_first")), 1)

    def test_seed_reproduces_packet_and_key_bytes(self) -> None:
        first_dir, first_key = self._run(suffix="first")
        second_dir, second_key = self._run(suffix="second")
        self.assertEqual(first_key.read_bytes(), second_key.read_bytes())
        for reviewer in range(1, 5):
            first = first_dir / f"reviewer-{reviewer:02d}" / "cases.jsonl"
            second = second_dir / f"reviewer-{reviewer:02d}" / "cases.jsonl"
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_refuses_key_inside_packet_directory_and_existing_outputs(self) -> None:
        cases = load_cases(self.manifest)
        packet_dir = self.root / "packets"
        with self.assertRaisesRegex(StudyInputError, "stored outside"):
            write_blinded_packets(
                cases, packet_dir=packet_dir, key_path=packet_dir / "key.json", reviewers=2, seed=1
            )
        packet_dir.mkdir()
        with self.assertRaisesRegex(StudyInputError, "must not already exist"):
            write_blinded_packets(
                cases, packet_dir=packet_dir, key_path=self.root / "key.json", reviewers=2, seed=1
            )

    def test_requires_multiple_reviewers(self) -> None:
        cases = load_cases(self.manifest)
        with self.assertRaisesRegex(StudyInputError, "at least two reviewers"):
            write_blinded_packets(
                cases, packet_dir=self.root / "packets", key_path=self.root / "key.json",
                reviewers=1, seed=1,
            )

    def test_incomplete_blocks_scale_without_overloading_reviewers(self) -> None:
        self._write_records(records(pair_count=60))
        packet_dir, key_path = self._run(
            reviewers=12, reviewers_per_pair=6, suffix="incomplete-blocks"
        )
        key = json.loads(key_path.read_text(encoding="utf-8"))
        assignments = key["assignments"]
        self.assertEqual(len(assignments), 60 * 6)
        by_pair: dict[str, list[dict[str, str]]] = {}
        by_reviewer: dict[str, list[dict[str, str]]] = {}
        for item in assignments:
            by_pair.setdefault(item["pair_id"], []).append(item)
            by_reviewer.setdefault(item["reviewer"], []).append(item)
        for rows in by_pair.values():
            self.assertEqual(len(rows), 6)
            self.assertEqual([row["provenance"] for row in rows].count("derived"), 3)
            self.assertEqual([row["provenance"] for row in rows].count("answer_first"), 3)
        self.assertEqual({len(rows) for rows in by_reviewer.values()}, {30})
        for reviewer, rows in by_reviewer.items():
            self.assertEqual(len({row["pair_id"] for row in rows}), len(rows))
            packet = packet_dir / reviewer / "cases.jsonl"
            self.assertEqual(len(packet.read_text(encoding="utf-8").splitlines()), 30)

    def test_odd_incomplete_blocks_balance_workload_and_conditions(self) -> None:
        packet_dir, key_path = self._run(
            reviewers=5, reviewers_per_pair=3, suffix="odd-incomplete-blocks"
        )
        key = json.loads(key_path.read_text(encoding="utf-8"))
        by_pair: dict[str, list[dict[str, str]]] = {}
        by_reviewer: dict[str, list[dict[str, str]]] = {}
        for item in key["assignments"]:
            by_pair.setdefault(item["pair_id"], []).append(item)
            by_reviewer.setdefault(item["reviewer"], []).append(item)
        for rows in by_pair.values():
            conditions = [row["provenance"] for row in rows]
            self.assertEqual(len(rows), 3)
            self.assertLessEqual(abs(conditions.count("derived") - conditions.count("answer_first")), 1)
        self.assertLessEqual(max(map(len, by_reviewer.values())) - min(map(len, by_reviewer.values())), 1)
        for reviewer in by_reviewer:
            packet = packet_dir / reviewer / "cases.jsonl"
            self.assertEqual(len(packet.read_text(encoding="utf-8").splitlines()), len(by_reviewer[reviewer]))

    def test_cli_reports_incomplete_block_allocation(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            result = main([
                "blind", "--input", str(self.manifest),
                "--packet-dir", str(self.root / "cli-packets"),
                "--key-out", str(self.root / "cli-restricted" / "key.json"),
                "--reviewers", "4", "--reviewers-per-pair", "2", "--seed", "7",
            ])
        self.assertEqual(result, 0)
        self.assertIn("each pair was assigned to 2 reviewers", output.getvalue())


if __name__ == "__main__":
    unittest.main()
