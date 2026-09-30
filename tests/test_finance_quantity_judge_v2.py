"""Executive summary: validate the isolated format delta and all saved-answer judge coverage on authored data."""

import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from finance_quantity_judge_v2 import runner as v2
from finance_quantity_judge_v2.protocol import FORMAT, PHASE, SYSTEM
from finance_quantity_transfer import runner as v1
from finance_quantity_transfer.protocol import JUDGE, MODEL, SYSTEMS, body, encode
from finance_quantity_transfer.scoring import location


def authored_packet(count=32):
    result = []
    for i in range(count):
        row = copy.deepcopy(v1.authored_case())
        row["case_id"] = f"authored_v2_{i}"
        row["native_target"] = {"value": "DO_NOT_SEND_NATIVE"}
        row["provisional_reference"]["value"] = "DO_NOT_SEND_REFERENCE"
        result.append(row)
    return result


def saved_answers(packet):
    text = encode({"status": "answer", "value": "25", "unit": "percent", "scale": "none",
                   "calculation": "(150-120)/120*100", "evidence": ["table: cost 120"]})
    return [{"case_id": row["case_id"], "arm": arm, "phase": "answer", "text": text}
            for row in packet for arm in SYSTEMS]


class PointerAmendmentTests(unittest.TestCase):
    def test_only_appended_format_changes_system_and_all_formats_exist(self):
        self.assertEqual(SYSTEM, JUDGE + FORMAT)
        self.assertEqual(PHASE, "judge_v2")
        context = {"table": [["120"]], "pre_text": ["first"], "post_text": ["last"]}
        for path in ["table[0][0]", "pre_text[0]", "post_text[0]"]:
            self.assertIsInstance(location(context, path), str)
        context = {"table": {"table": [["150"]]}, "paragraphs": [{"text": "costs"}]}
        for path in ["table.table[0][0]", "paragraphs[0].text"]:
            self.assertIsInstance(location(context, path), str)
        self.assertIn("whole table cell or paragraph string", FORMAT)

    def test_all_saved_answers_retained_and_labels_discarded(self):
        packet = authored_packet()
        calls = saved_answers(packet)
        calls[0]["text"] = "malformed"
        items = v2.jobs(packet, calls)
        self.assertEqual(len(items), 64)
        self.assertEqual(items[0]["saved"]["text"], "malformed")
        self.assertNotIn("provisional_reference", items[0]["case"])
        self.assertNotIn("native_target", items[0]["case"])
        for invalid in [calls[:-1], calls + [calls[0]]]:
            with self.assertRaises(ValueError):
                v2.jobs(packet, invalid)

    def test_complete_panel_judges_once_without_answers_or_prompt_label_identity(self):
        packet = authored_packet()
        saved = saved_answers(packet)
        saved[0]["text"] = "malformed"
        items = v2.jobs(packet, saved)
        seen = []
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ledger = root / "ledger.jsonl"
            def transport(identity, system, user):
                events = [json.loads(line) for line in ledger.read_text().splitlines()]
                self.assertEqual(events[-1]["event"], "reserved")
                if len(events) > 1:
                    self.assertEqual(events[-2]["event"], "settled")
                self.assertEqual(system, SYSTEM)
                self.assertEqual(identity["phase"], PHASE)
                payload = json.loads(user)
                for forbidden in ["case_id", "source", "arm", "native_target", "provisional_reference"]:
                    self.assertNotIn(forbidden, payload)
                self.assertNotIn("DO_NOT_SEND", user)
                seen.append(identity)
                result = {"verdict": "supported", "requested_quantity": "relative cost change",
                          "operand_checks": [], "unit_check": "percent", "reason": "Authored arithmetic",
                          "evidence": ["table[1][1]", "table[2][1]"]}
                return {**identity, "text": encode(result), "usage": {"cost": "0.000001"},
                        "provider": "SiliconFlow", "returned_model": MODEL, "finish_reason": "stop",
                        "request_body": body(system, user)}
            with patch.dict(os.environ, OPENROUTER_API_KEY="authored-no-network-key"), patch.object(v1, "answer", transport):
                result = v2.run(items, root / "run", ledger, {"authored_fixture": True}, {"fixture": "authored"})
            self.assertEqual(result["planned_judges"], 64)
            self.assertEqual(result["answer_calls"], 0)
            self.assertEqual(len(seen), 64)
            status = json.loads((root / "run/attempt_status.json").read_text())
            self.assertEqual(status[0]["quantity_review"]["effective_verdict"], "unassessable")
            self.assertTrue(all(x["judge_status"] == "recorded" for x in status))
            reservations = [x for x in map(json.loads, ledger.read_text().splitlines()) if x["event"] == "reserved"]
            self.assertTrue(all(x["study_id"] == v1.STUDY_ID for x in reservations))
            self.assertTrue(all(x["call_id"].endswith(":" + PHASE) for x in reservations))


if __name__ == "__main__":
    unittest.main()
