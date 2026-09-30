"""Executive summary: test authored arithmetic, billing stops and complete label-free call coverage."""

import copy
import hashlib
import json
import os
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from finance_quantity_transfer import freeze, runner
from finance_quantity_transfer.budget import Budget, BudgetStop, observed_cost, reservation_usd
from finance_quantity_transfer.protocol import MODEL, SYSTEMS, body, encode
from finance_quantity_transfer.scoring import native_decimal, parse_answer, parse_judge, score


def candidate(**changes):
    return encode({"status": "answer", "value": "25", "unit": "percent", "scale": "none",
                   "calculation": "(150-120)/120*100", "evidence": ["table[1][1]"], **changes})


def judgment(**changes):
    return encode({"verdict": "supported", "requested_quantity": "relative cost change",
                   "operand_checks": [{"literal": "120", "role": "base", "evidence": "table[1][1]"}],
                   "unit_check": "percent, scale none", "reason": "Authored costs rise by 25 percent",
                   "evidence": ["table[1][1]", "table[2][1]"], **changes})


def cases():
    result = []
    for index in range(32):
        case = copy.deepcopy(runner.authored_case())
        case["case_id"] = f"authored_{index}"
        case["native_target"] = {"value": 25.0}
        if index >= 22:
            case["provisional_reference"]["eligible"] = False
        result.append(case)
    return result


class ScoreTests(unittest.TestCase):
    def setUp(self):
        self.ref = runner.authored_case()["provisional_reference"]

    def test_reported_and_expression_endpoints_are_separate(self):
        result = score(candidate(value="99"), self.ref)
        self.assertFalse(result["reported_numeric_typed_match"])
        self.assertTrue(result["expression_numeric_typed_match"])
        self.assertFalse(result["reported_expression_consistent"])
        self.assertTrue(score(candidate(value="25.0025"), self.ref)["reported_numeric_typed_match"])
        self.assertFalse(score(candidate(value="25.0025001"), self.ref)["reported_numeric_typed_match"])

    def test_scale_normalization_preserves_unit_distinctions(self):
        ref = {"eligible": True, "value": "1000", "unit": "currency", "scale": "none"}
        good = score(candidate(value="1", calculation="1", unit="currency", scale="thousand"), ref)
        self.assertTrue(good["reported_numeric_typed_match"])
        self.assertTrue(good["expression_numeric_typed_match"])
        self.assertFalse(score(candidate(unit="percentage_points"), self.ref)["reported_numeric_typed_match"])
        self.assertFalse(score(candidate(scale="million"), self.ref)["schema_valid"])
        zero = {**self.ref, "value": "0"}
        self.assertTrue(score(candidate(value="0.00000001"), zero)["reported_numeric_typed_match"])
        self.assertFalse(score(candidate(value="0.000000011"), zero)["reported_numeric_typed_match"])

    def test_literal_native_scalars_have_no_conversion_or_tolerance(self):
        result = score(candidate(value="0.1", calculation="0.1"), self.ref, {"value": 0.1})
        self.assertTrue(result["native_literal_exact"])
        self.assertFalse(score(candidate(), self.ref, {"value": 0.25})["native_literal_exact"])
        self.assertFalse(score(candidate(value="25.00001"), self.ref, {"value": 25})["native_literal_exact"])
        for value in [True, None, float("nan"), "Infinity", [], {}]:
            with self.subTest(value=value), self.assertRaises((ValueError, ArithmeticError)):
                native_decimal(value)

    def test_strict_grammar_duplicates_and_boolean_coverage(self):
        for text in [candidate(calculation="The result is 25"), candidate(calculation="__import__('os')"),
                     candidate().replace('"status": "answer"', '"status": "answer", "status": "answer"')]:
            self.assertIsNotNone(parse_answer(text)[1])
        boolean = candidate(status="non_numeric_answer", value="yes", unit="boolean", calculation="")
        self.assertTrue(score(boolean, self.ref)["schema_valid"])
        self.assertFalse(score(boolean, self.ref)["reported_numeric_typed_match"])
        abstain = candidate(status="ambiguous", value=None, unit="unknown", calculation="")
        self.assertTrue(score(abstain, self.ref)["schema_valid"])

    def test_judge_pointer_validation_and_malformed_override(self):
        context = runner.authored_case()["original_context"]
        value, error = parse_judge(judgment(), context, "bad answer grammar")
        self.assertIsNone(error)
        self.assertEqual(value["effective_verdict"], "unassessable")
        self.assertTrue(value["protocol_violation"])
        for text in [judgment(evidence=["table[99][1]"]), judgment(evidence=["table[1]"]),
                     judgment(operand_checks=["invalid"]), judgment(extra="invalid")]:
            self.assertIsNotNone(parse_judge(text, context, None)[1])

    def test_requests_exclude_labels_scores_and_arm(self):
        case = cases()[0]
        case["provisional_reference"]["value"] = "123456789"
        case["native_target"]["value"] = 987654321
        payload = runner.judge_payload(case, {"text": "malformed"})
        self.assertFalse(payload["candidate_parser_valid"])
        encoded = encode(payload)
        for forbidden in ["123456789", "987654321", "provisional_reference", "native_target", '"arm"', '"scoring"']:
            self.assertNotIn(forbidden, encoded)
        self.assertEqual(set(runner.question_payload(case)), {"question", "original_context"})


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "ledger.jsonl"
        self.budget = Budget(self.path, "test")
        self.request = body("Authored", "data")

    def tearDown(self):
        self.temp.cleanup()

    def events(self):
        return [json.loads(x) for x in self.path.read_text().splitlines()]

    def test_unknown_or_invalid_cost_is_persisted_and_prevents_resume(self):
        for value in [None, True, "NaN", "Infinity", "-1", "bad"]:
            with self.subTest(value=value):
                self.path.unlink(missing_ok=True)
                self.budget.reserve("one", self.request, {})
                with self.assertRaises(BudgetStop):
                    self.budget.settle("one", {"usage": {"cost": value}})
                self.assertIsNone(self.events()[-1]["cost_usd"])
                with self.assertRaises(BudgetStop):
                    self.budget.reserve("two", self.request, {})

    def test_zero_cost_and_raw_cost_survive_choice_parsing_failure(self):
        self.assertEqual(observed_cost({"raw_response": {"usage": {"cost": "0.00012"}}}), Decimal("0.00012"))
        self.budget.reserve("one", self.request, {})
        self.budget.settle("one", {"raw_response": {"usage": {"cost": 0}}})
        self.assertEqual(self.budget.totals()["study_usd"], "0")
        with self.assertRaises(BudgetStop):
            self.budget.reserve("one", self.request, {})

    def test_pending_and_over_reserve_are_persistent_stops(self):
        reserved = self.budget.reserve("one", self.request, {})
        with self.assertRaises(BudgetStop):
            self.budget.reserve("two", self.request, {})
        with self.assertRaises(BudgetStop):
            self.budget.settle("one", {"usage": {"cost": str(reserved + Decimal("0.01"))}})
        self.assertEqual(self.events()[-1]["cost_usd"], str(reserved + Decimal("0.01")))
        with self.assertRaises(BudgetStop):
            Budget(self.path, "test").reserve("two", self.request, {})

    def test_full_input_reserve_and_fixed_caps(self):
        self.assertGreater(reservation_usd(body("Authored", "é" * 1000)), reservation_usd(self.request))
        with self.assertRaises(BudgetStop):
            reservation_usd(body("Authored", "a" * 163840))
        for total_cap in [2, 11]:
            with self.assertRaises(ValueError):
                Budget(self.path, "test", total_cap=total_cap)
        for study_ids in [["test"], ["a", "b", "c", "d", "e"]]:
            events = []
            for sid in study_ids:
                events += [{"event": "reserved", "call_id": sid, "study_id": sid, "reserve_usd": "1.9999"},
                           {"event": "settled", "call_id": sid, "study_id": sid, "cost_usd": "1.9999"}]
            self.path.write_text("\n".join(map(encode, events)) + "\n")
            with self.assertRaises(BudgetStop):
                self.budget.reserve("next", self.request, {})


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.ledger = self.root / "ledger.jsonl"
        self.calls = []

    def tearDown(self):
        self.temp.cleanup()

    def transport(self, identity, system, user):
        events = [json.loads(x) for x in self.ledger.read_text().splitlines()]
        self.assertEqual(events[-1]["event"], "reserved")
        if len(events) > 1:
            self.assertEqual(events[-2]["event"], "settled")
            self.assertEqual(events[-2]["cost_usd"], "0.000001")
        payload = json.loads(user)
        self.assertNotIn("provisional_reference", payload)
        self.assertNotIn("native_target", payload)
        self.assertNotIn("arm", payload)
        self.calls.append(identity)
        text = judgment() if identity["phase"] == "judge" else candidate()
        if identity["case_id"] == "authored_0" and identity["arm"] == "baseline" and identity["phase"] == "answer":
            text = "malformed"
        request = body(system, user)
        return {**identity, "text": text, "usage": {"cost": "0.000001"}, "provider": "SiliconFlow",
                "returned_model": MODEL, "finish_reason": "stop", "request_body": request,
                "request_sha256": hashlib.sha256(encode(request).encode()).hexdigest()}

    def test_complete_32_case_panel_makes_every_judge_and_retains_denominators(self):
        with patch.dict(os.environ, OPENROUTER_API_KEY="authored-test-key"), patch.object(runner, "answer", self.transport):
            result = runner.run(cases(), self.root / "run", self.ledger, {"authored_fixture": True})
        self.assertEqual(result["state"], "complete")
        self.assertEqual(len(self.calls), 128)
        self.assertEqual(sum(x["phase"] == "judge" for x in self.calls), 64)
        self.assertEqual(sum(x["phase"] == "answer" for x in self.calls), 64)
        status = json.loads((self.root / "run/attempt_status.json").read_text())
        self.assertEqual(len(status), 64)
        self.assertEqual(sum(x["primary_eligible"] for x in status), 44)
        self.assertEqual(status[0]["quantity_review"]["effective_verdict"], "unassessable")
        self.assertTrue(status[0]["quantity_review"]["protocol_violation"])
        self.assertTrue(all(x["judge_status"] == "recorded" for x in status))
        self.assertEqual(Decimal(result["spend"]["study_usd"]), Decimal("0.000128"))

    def test_unknown_first_billing_stops_before_judge_and_preserves_response(self):
        def unknown(*args):
            record = self.transport(*args)
            record.pop("usage")
            return record
        with patch.dict(os.environ, OPENROUTER_API_KEY="authored-test-key"), patch.object(runner, "answer", unknown):
            with self.assertRaises(BudgetStop):
                runner.run(cases(), self.root / "run", self.ledger, {"authored_fixture": True})
        self.assertEqual(len(self.calls), 1)
        self.assertTrue((self.root / "run/calls.jsonl").exists())
        meta = json.loads((self.root / "run/run.json").read_text())
        self.assertEqual(meta["state"], "stopped")
        self.assertEqual(meta["planned_judge_attempts"], 64)

    def test_local_preflight_and_secret_redaction(self):
        with patch.object(runner, "answer", side_effect=AssertionError("No network allowed")):
            self.assertEqual(runner.preflight()["api_calls"], 0)
        with patch.dict(os.environ, OPENROUTER_API_KEY="authored-test-key"):
            cleaned = runner.redact_record({"text": "echo authored-test-key", "nested": {"authorization": "secret"}})
        self.assertNotIn("authored-test-key", encode(cleaned))
        self.assertNotIn('"secret"', encode(cleaned))

    def test_authored_freeze_rejects_input_source_and_price_drift(self):
        metadata = self.root / "outputs/finance-quantity-transfer-v1"
        metadata.mkdir(parents=True)
        paths = [self.root / x for x in ["packet", "lock", "comparison", "approval"]]
        for path in paths:
            path.write_text("authored-only\n")
        for name in ["provider_catalogue.json", "label_join_freeze.json", "label_join_receipt.json",
                     "reference_a_receipt.json", "reference_b_receipt.json"]:
            (metadata / name).write_text("authored metadata\n")
        with patch.object(freeze, "ROOT", self.root), patch.object(freeze, "source_records", return_value=[]):
            frozen = freeze.make_freeze(*paths)
            freeze.verify_freeze(frozen, paths[0])
            tampered = copy.deepcopy(frozen)
            tampered["prompt_price_usd_per_token"] = "0"
            with self.assertRaises(ValueError):
                freeze.verify_freeze(tampered, paths[0])
            paths[0].write_text("changed authored packet")
            with self.assertRaises(ValueError):
                freeze.verify_freeze(frozen, paths[0])


if __name__ == "__main__":
    unittest.main()
