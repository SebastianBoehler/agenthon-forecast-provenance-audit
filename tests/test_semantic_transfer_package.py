"""Executive summary: test whitelist privacy and exact observed-cost accounting on authored fixtures only."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import package_semantic_transfer_review as package
from semantic_transfer_package_policy import file_check, inspect_json, observed_spend, selected_files


def events(cost="0.00012", identity="authored", study="finance_quantity_transfer_v1"):
    return [{"event": "reserved", "call_id": identity, "study_id": study,
             "request_sha256": "authored-hash", "reserve_usd": "0.001"},
            {"event": "settled", "call_id": identity, "study_id": study,
             "request_sha256": "authored-hash", "cost_usd": cost}]


class PackagePolicyTests(unittest.TestCase):
    def test_whitelist_omits_raw_inputs_but_preserves_preparation_and_projections(self):
        selected = selected_files()
        self.assertEqual(len(selected), len(set(selected)))
        forbidden = {"calls.jsonl", "question_packet.jsonl", "experiment_packet.jsonl", "source_targets.jsonl",
                     "review_packet.jsonl", "private_join_key.jsonl", "question_only_packet.jsonl", "private_case_map.jsonl"}
        self.assertTrue(all(Path(name).name not in forbidden for name in selected))
        self.assertIn("outputs/finance-human-review-v1/blank_review_form.jsonl", selected)
        self.assertIn("outputs/finance-quantity-transfer-v1/independent-analysis/portable_numeric_packet.jsonl", selected)
        self.assertIn("paper/answer_contract_audit.tex", selected)

    def test_nested_context_request_and_credential_payloads_are_rejected(self):
        for value in [{"original_context": {}}, {"table": [["authored"]]}, {"request_body": {}},
                      {"nested": [{"api_key": "authored-key"}]},
                      {"candidate_text": json.dumps({"question": "authored question"})}]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                inspect_json(value)
        inspect_json({"candidate_text": json.dumps({"value": "25", "calculation": "(150-120)/120*100"}),
                      "native_target": {"value": 25}, "requested_quantity": "relative change"})

    def test_file_checks_reject_secret_echo_and_symlink(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "safe.json").write_text('{"value":"25"}\n')
            self.assertEqual(file_check(root, "safe.json")["bytes"], 15)
            (root / "secret.json").write_text('{"value":"authored-only-secret"}')
            with patch.dict(os.environ, OPENROUTER_API_KEY="authored-only-secret"), self.assertRaises(ValueError):
                file_check(root, "secret.json")
            (root / "link.json").symlink_to(root / "safe.json")
            with self.assertRaises(ValueError):
                file_check(root, "link.json")

    def test_observed_spend_uses_decimal_settlements_and_all_ledger_calls(self):
        result = observed_spend(events() + events("0.00023", identity="second", study="authored_other_study"))
        self.assertEqual(result["actual_aggregate_observed_usd"], "0.00035")
        self.assertEqual(result["study_observed_usd"], "0.00012")
        self.assertEqual(result["settled_calls"], 2)
        self.assertTrue(result["observed_cost_complete"])

    def test_closed_unknown_billing_retains_reserve_without_claiming_actual_total(self):
        fixture = events() + events(None, identity="failed")
        fixture[-1].update(cost_error="Missing usage.cost", error={"type": "HTTPError", "status": 502})
        result = observed_spend(fixture)
        self.assertEqual(result["known_observed_subtotal_usd"], "0.00012")
        self.assertFalse(result["observed_cost_complete"])
        self.assertIsNone(result["actual_aggregate_observed_usd"])
        self.assertIsNone(result["study_observed_usd"])
        self.assertEqual(result["unknown_cost_calls"], 1)
        self.assertIsNone(result["unknown_billing"][0]["cost_usd"])
        self.assertEqual(result["unknown_billing_reserved_usd"], "0.001")
        self.assertEqual(result["accounted_worst_under_fixed_request_prices_usd"], "0.00112")
        with self.assertRaises(ValueError):
            observed_spend(fixture + events(identity="prohibited_next_call"))

    def test_invalid_unsettled_duplicate_and_identity_errors_fail(self):
        invalid = [events(value) for value in [True, "NaN", "-1", "0.01"]]
        invalid += [events()[:1], events() + events()]
        mismatch = events()
        mismatch[1]["request_sha256"] = "changed"
        invalid.append(mismatch)
        for fixture in invalid:
            with self.subTest(fixture=fixture), self.assertRaises((ValueError, ArithmeticError)):
                observed_spend(fixture)

    def test_finality_rejects_a_moving_authored_collection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "outputs/finance-quantity-transfer-v1/collection/run.json"
            path.parent.mkdir(parents=True)
            path.write_text('{"state":"running"}')
            with patch.object(package, "ROOT", root), self.assertRaisesRegex(ValueError, "moving"):
                package.finality()

    def test_finality_requires_current_paper_and_successful_native_receipt(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for folder in ("finance-quantity-transfer-v1", "finance-quantity-judge-v2"):
                path = root / f"outputs/{folder}/collection/run.json"
                path.parent.mkdir(parents=True)
                path.write_text('{"state":"complete","completed_utc":"authored-time"}')
            paper = root / package.PAPER
            paper.parent.mkdir(parents=True)
            paper.write_text("authored manuscript")
            check = root / package.MANUSCRIPT_CHECK
            check.parent.mkdir(parents=True)
            for record in [{"paper_sha256": "stale", "native_compile_success": True},
                           {"paper_sha256": package.digest(paper), "native_compile_success": False}]:
                check.write_text(json.dumps(record))
                with patch.object(package, "ROOT", root), self.assertRaisesRegex(ValueError, "Current-paper"):
                    package.finality()


if __name__ == "__main__":
    unittest.main()
