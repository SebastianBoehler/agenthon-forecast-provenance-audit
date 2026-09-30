"""Executive summary: rescore saved model answers using separate exact-rational calculations.

This does not import the primary parser, scoring code or financial oracle. Active
ledgers are snapshotted and explicitly reported as partial until all 600 keys exist.
"""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from fractions import Fraction as F
from pathlib import Path

from independent_contract_validation import exact_value, valid

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "outputs/model-grading-v1"
OUT = ROOT / "outputs/model-grading-review"
POLICIES = ("source_abs_0.005", "source_abs_0.5", "source_relative_5pct",
            "integer_and_source_half", "visible_contract")
MODELS = ("qwen3-1.7b", "qwen2.5-coder-3b", "deepseek-v3.2")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def decimal_grammar(token):
    unsigned = token[1:] if token[:1] in ("+", "-") else token
    parts = unsigned.lower().split("e")
    if len(parts) > 2:
        return False
    if len(parts) == 2:
        exp = parts[1][1:] if parts[1][:1] in ("+", "-") else parts[1]
        if not exp.isdecimal():
            return False
    base = parts[0].split(".")
    if len(base) > 2 or (len(base) == 2 and not base[1].isdecimal()):
        return False
    digits = base[0].split(",")
    if not all(d.isdecimal() for d in digits):
        return False
    return len(digits) == 1 or (1 <= len(digits[0]) <= 3 and all(len(d) == 3 for d in digits[1:]))


def extract(text, family, finish):
    lines = [s.strip() for s in text.splitlines() if s.strip()]
    reason, number = None, None
    if text.casefold().count("final:") != 1 or not lines:
        reason = "missing_or_nonfinal_marker"
    else:
        tokens = lines[-1].split(" ")
        if len(tokens) != 3 or tokens[0].casefold() != "final:" or not decimal_grammar(tokens[1]) or tokens[2].casefold() not in {"currency", "percent"}:
            reason = "invalid_final_format"
        elif tokens[2].casefold() != ("percent" if family == "corp_wacc" else "currency"):
            reason = "wrong_unit"
        else:
            try:
                number = Decimal(tokens[1].replace(",", ""))
                if not number.is_finite():
                    number, reason = None, "nonfinite_answer"
            except InvalidOperation:
                reason = "invalid_decimal"
    if finish not in ("stop", "eos"):
        return None, finish
    return F(number) if number is not None else None, reason


def extract_numeric(text, family, finish):
    lines = [s.strip() for s in text.splitlines() if s.strip()]
    value, reason, state = None, None, None
    if text.casefold().count("final:") != 1 or not lines:
        reason = "missing_or_nonfinal_marker"
    else:
        body = lines[-1].strip("*")
        if not body.casefold().startswith("final:"):
            reason = "invalid_numeric_final_line"
        else:
            body = body[6:].lstrip()
            dollar = body.startswith("$")
            body = body[1:] if dollar else body
            end = 0
            while end < len(body) and (body[end].isdecimal() or body[end] in "+-.,eE"):
                end += 1
            scalar, suffix = body[:end], body[end:].lstrip().casefold()
            allowed = {"currency", "percent", "%", "usd", "dollar", "dollars", "<unit>", ""}
            if not decimal_grammar(scalar) or suffix not in allowed:
                reason = "invalid_numeric_final_line"
            else:
                percent = suffix in {"percent", "%"}
                currency = dollar or suffix in {"currency", "usd", "dollar", "dollars"}
                wrong = (currency if family == "corp_wacc" else percent)
                if wrong:
                    reason, state = "wrong_explicit_unit", "wrong"
                else:
                    state = "explicit" if currency or percent else "placeholder" if suffix else "absent"
                    try:
                        number = Decimal(scalar.replace(",", ""))
                        value = F(number) if number.is_finite() else None
                        if value is None:
                            reason, state = "nonfinite_answer", None
                    except InvalidOperation:
                        reason, state = "invalid_decimal", None
    if finish not in ("stop", "eos"):
        value, reason = None, finish
    return value, reason, state


def score(response, selected, numeric=False):
    formula, _ = exact_value(selected["family"], selected["prompt"])
    if numeric:
        value, error, units = extract_numeric(response["text"], selected["family"], response["finish_reason"])
    else:
        value, error = extract(response["text"], selected["family"], response["finish_reason"])
    gold = F(selected["gold"])
    correct = value is not None and valid(value, formula, selected["requested_rounding"])
    decisions = dict.fromkeys(POLICIES, False)
    if value is not None:
        gap = abs(value - gold)
        decisions["source_abs_0.005"] = gap <= F(1, 200)
        decisions["source_abs_0.5"] = gap <= F(1, 2)
        decisions["source_relative_5pct"] = gap <= abs(gold) / 20
        decisions["integer_and_source_half"] = value.denominator == 1 and gap <= F(1, 2)
        decisions["visible_contract"] = correct
    result = {"model_key": response["model_key"], "case_id": response["case_id"],
            "family": selected["family"], "fraction_value": str(value) if value is not None else None,
            "parse_error": error, "visible_valid": correct, "decisions": decisions,
            "finish_reason": response["finish_reason"]}
    if numeric:
        result["unit_state"] = units
    return result


def summarize(rows):
    result = {"attempts": len(rows), "parsed_completed": sum(r["fraction_value"] is not None for r in rows),
              "visible_valid": sum(r["visible_valid"] for r in rows),
              "failures": dict(Counter(r["parse_error"] for r in rows if r["parse_error"])), "policies": {}}
    for policy in POLICIES:
        accepted = sum(r["decisions"][policy] for r in rows)
        both = sum(r["visible_valid"] and r["decisions"][policy] for r in rows)
        oracle_only = sum(r["visible_valid"] and not r["decisions"][policy] for r in rows)
        source_only = sum(not r["visible_valid"] and r["decisions"][policy] for r in rows)
        result["policies"][policy] = {"accepted": accepted, "valid_rejected": oracle_only,
                                      "numeric_invalid_accepted": source_only,
                                      "paired_changes": oracle_only + source_only,
                                      "four_cells": {"both": both, "oracle_only": oracle_only,
                                                     "source_only": source_only,
                                                     "neither": len(rows) - both - oracle_only - source_only}}
    return result


def compare_primary(rows, aggregates, numeric=False, prefix="", models=MODELS):
    path = STUDY / (prefix + ("numeric_scored.jsonl" if numeric else "scored.jsonl"))
    if not path.exists():
        return {"status": "primary scoring artifact not yet available"}
    primary_raw = path.read_bytes()
    primary_rows = list(map(json.loads, primary_raw.decode().splitlines()))
    primary = {(r["model_key"], r["case_id"]): r for r in primary_rows}
    assert len(primary) == len(primary_rows), "Duplicate primary scoring keys"
    assert set(primary) == {(r["model_key"], r["case_id"]) for r in rows}
    for row in rows:
        other = primary[(row["model_key"], row["case_id"])]
        assert row["parse_error"] == other["parse_error"], row["case_id"]
        expected = F(other["value"]) if other["value"] is not None else None
        actual = F(row["fraction_value"]) if row["fraction_value"] is not None else None
        assert actual == expected, row["case_id"]
        assert row["decisions"] == other["decisions"], row["case_id"]
        assert row["visible_valid"] == other["visible_valid"], row["case_id"]
        if numeric:
            assert row["unit_state"] == other["unit_state"], row["case_id"]
    results_path = STUDY / (prefix + ("numeric_sensitivity.json" if numeric else "results.json"))
    results = json.loads(results_path.read_text())
    for model in models:
        if numeric:
            for unit in ("explicit", "placeholder", "absent", "wrong"):
                assert sum(r["model_key"] == model and r["unit_state"] == unit for r in rows) == results["models"][model]["unit_states"][unit]
        for level in ("aggregate", "families"):
            if level == "aggregate":
                groups = [(aggregates[model][level], results["models"][model][level])]
            else:
                groups = [(v, results["models"][model][level][f]) for f, v in aggregates[model][level].items()]
            for independent, original in groups:
                for key in ("attempts", "parsed_completed", "visible_valid", "failures"):
                    assert independent[key] == original[key], (model, key)
                for policy in POLICIES:
                    for key, value in original["policies"][policy].items():
                        assert independent["policies"][policy][key] == value, (model, policy, key)
    return {"status": "all decisions, values, errors and aggregates agree", "rows": len(rows),
            "scored_sha256": sha(primary_raw), "results_sha256": sha(results_path.read_bytes())}


def main():
    manifest = json.loads((STUDY / "selection_manifest.json").read_text())
    for path, digest in manifest["frozen_sha256"].items():
        assert sha((ROOT / path).read_bytes()) == digest, path
    selection = [json.loads(s) for s in (STUDY / "selection.jsonl").read_text().splitlines()]
    selected = {r["case_id"]: r for r in selection}
    assert len(selected) == len({r["prompt"] for r in selection}) == 200
    snapshots = OUT / "ledger-snapshots"
    snapshots.mkdir(parents=True, exist_ok=True)
    original_freeze = STUDY / "numeric_sensitivity_freeze.json"
    for path, digest in json.loads(original_freeze.read_text())["sha256"].items():
        original = STUDY / "sensitivity-original" / Path(path).name if path.endswith(".py") else ROOT / path
        assert sha(original.read_bytes()) == digest, str(original)
    correction_freeze = STUDY / "numeric_sensitivity_freeze_v2.json"
    correction = json.loads(correction_freeze.read_text())
    assert sha(original_freeze.read_bytes()) == correction["original_freeze_sha256"]
    for path, digest in correction["files"].items():
        assert sha((ROOT / path).read_bytes()) == digest, path
    scored, numeric_scored, hashes, counts, conflicts, metadata = [], [], {}, {}, [], {}
    for model in MODELS:
        path = STUDY / f"{model}_responses.jsonl"
        if not path.exists():
            counts[model] = 0
            continue
        raw = path.read_bytes()
        assert not raw or raw.endswith(b"\n"), "Partial write; rerun after append completes"
        digest = sha(raw)
        (snapshots / f"{digest[:12]}-{path.name}").write_bytes(raw)
        hashes[path.name] = digest
        responses = [json.loads(s) for s in raw.decode().splitlines()]
        ids = {r["case_id"] for r in responses}
        assert len(ids) == len(responses) and ids.issubset(selected)
        if model in manifest["local_models"]:
            runtime_path = STUDY / f"{model}_runtime.json"
            runtime = json.loads(runtime_path.read_text())
            spec = manifest["local_models"][model]
            assert all(runtime[k] == v for k, v in spec.items())
            assert runtime["device"] == "mps" and runtime["dtype"] == "float16"
            assert runtime["decoding"] == "greedy" and runtime["max_new_tokens"] == 1024
            assert runtime["system_prompt"] == manifest["system_prompt"]
            assert runtime["selection_sha256"] == sha((STUDY / "selection.jsonl").read_bytes())
            metadata[model] = {"runtime_sha256": sha(runtime_path.read_bytes()),
                               "recorded_settings_agree": True}
        else:
            metadata[model] = {"returned_models": dict(Counter(r.get("model") for r in responses)),
                               "returned_providers": dict(Counter(r.get("provider") for r in responses)),
                               "finish_reasons": dict(Counter(r["finish_reason"] for r in responses))}
        for row in responses:
            question = selected[row["case_id"]]
            assert row["model_key"] == model and row["question_hash"] == question["question_hash"]
            if model in manifest["local_models"]:
                assert row["model"] == manifest["local_models"][model]["repository"]
            if model == "deepseek-v3.2":
                body = row["request_body"]
                assert body["messages"] == [{"role": "system", "content": manifest["system_prompt"]}, {"role": "user", "content": question["prompt"]}]
                assert body["provider"]["only"] == ["siliconflow/fp8"] and not body["provider"]["allow_fallbacks"]
                assert body["temperature"] == 0 and body["max_tokens"] == 1024
                assert body["reasoning"] == {"enabled": False}
                if row["finish_reason"] == "stop":
                    assert row["provider"] == "SiliconFlow" and row["model"] == "deepseek/deepseek-v3.2"
            scored.append(score(row, question))
            numeric_scored.append(score(row, question, numeric=True))
            last_raw = next((s.strip() for s in reversed(row["text"].splitlines()) if s.strip()), "")
            last = last_raw.casefold().strip("*")
            payload = last[6:].lstrip() if last.startswith("final:") else ""
            _, unit_error, _ = extract_numeric(row["text"], question["family"], "stop")
            if payload.startswith("$") and payload.endswith(("percent", "%")) and unit_error == "wrong_explicit_unit":
                conflicts.append({"model_key": model, "case_id": row["case_id"], "last_line": last_raw})
        counts[model] = len(responses)
    aggregates = {m: {"aggregate": summarize([r for r in scored if r["model_key"] == m]),
                      "families": {f: summarize([r for r in scored if r["model_key"] == m and r["family"] == f])
                                   for f in sorted({s["family"] for s in selection})}} for m in MODELS}
    numeric_aggregates = {m: {"aggregate": summarize([r for r in numeric_scored if r["model_key"] == m]),
                              "unit_states": dict(Counter(r["unit_state"] for r in numeric_scored if r["model_key"] == m)),
                              "families": {f: summarize([r for r in numeric_scored if r["model_key"] == m and r["family"] == f])
                                           for f in sorted({s["family"] for s in selection})}} for m in MODELS}
    result = {"status": "complete" if all(v == 200 for v in counts.values()) else "partial_live_snapshot",
              "executed_utc": datetime.now(timezone.utc).isoformat(),
              "responses_by_model": counts, "models": aggregates, "response_snapshot_sha256": hashes,
              "script_sha256": sha(Path(__file__).read_bytes()),
              "independent_calculator_sha256": sha((ROOT / "scripts/independent_contract_validation.py").read_bytes()),
              "selection_sha256": sha((STUDY / "selection.jsonl").read_bytes()),
              "collection_metadata_validation": metadata,
              "primary_comparison": compare_primary(scored, aggregates),
              "numeric_sensitivity_models": numeric_aggregates,
              "contradictory_prefix_suffix_cases": conflicts,
              "numeric_original_freeze_sha256": sha(original_freeze.read_bytes()),
              "numeric_corrected_freeze_sha256": sha(correction_freeze.read_bytes()),
              "numeric_primary_comparison": compare_primary(numeric_scored, numeric_aggregates, numeric=True)}
    (OUT / "independent-response-scores.jsonl").write_text("".join(json.dumps(r) + "\n" for r in scored))
    (OUT / "independent-response-summary.json").write_text(json.dumps(result, indent=2) + "\n")
    (OUT / "independent-numeric-response-scores.jsonl").write_text("".join(json.dumps(r) + "\n" for r in numeric_scored))
    print(json.dumps({"status": result["status"], "counts": counts,
                      "aggregates": {m: v["aggregate"] for m, v in aggregates.items()}}, indent=2))


if __name__ == "__main__":
    main()
