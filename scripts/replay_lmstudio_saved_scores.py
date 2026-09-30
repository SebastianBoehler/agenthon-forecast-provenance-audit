"""Executive summary: replay Gemma numerical scores without models or external caches.

Check frozen scientific files and all four saved score streams using the separate
independent helpers. This does not recheck external weight/engine hashes, native
tokenization or source semantics; the full postflight receipt covers local hashes.
"""

import argparse
import json
from datetime import datetime, timezone
from fractions import Fraction as F

import validate_model_grading_lmstudio as audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=audit.Path, required=True)
    args = parser.parse_args()
    for path, expected in [
        (audit.OLD / "preflight_freeze.json", audit.EXPECTED["preflight"]),
        (audit.OUT / "freeze.json", audit.EXPECTED["collection"]),
    ]:
        assert audit.digest(path) == expected
        for name, checksum in audit.read(path)["files"].items():
            assert audit.digest(audit.ROOT / name) == checksum, name
    freeze = audit.read(audit.OUT / "freeze.json")
    results = audit.read(audit.OUT / "results.json")
    receipt = audit.read(audit.OUT / "receipt.json")
    selection = audit.rows(audit.ROOT / "outputs/model-grading-v1/selection.jsonl")
    responses = audit.rows(audit.OUT / "responses.jsonl")
    assert len(selection) == len(responses) == receipt["attempts"] == 200
    assert receipt["response_sha256"] == audit.digest(audit.OUT / "responses.jsonl")
    assert results["freeze_sha256"] == audit.EXPECTED["collection"]
    streams = {e: [] for e in ("strict", "numeric", "two_conventions", "numeric_two_conventions")}
    for index, (response, case) in enumerate(zip(responses, selection), 1):
        assert response["collection_index"] == index and response["case_id"] == case["case_id"]
        assert response["model_key"] == audit.MODEL
        assert response["question_hash"] == case["question_hash"]
        assert case["question_hash"] == audit.hashlib.sha256(case["prompt"].encode()).hexdigest()
        assert response["request_body"] == dict(freeze["request_config"], input=case["prompt"])
        assert response["request_sha256"] == audit.body_hash(response["request_body"])
        native = audit.native(response["raw_native_response"], freeze["request_config"]["model"])
        assert all(response[k] == v for k, v in native.items())
        for endpoint in ("strict", "numeric"):
            base = audit.score(response, case, numeric=endpoint == "numeric")
            streams[endpoint].append(base)
            value = F(base["fraction_value"]) if base["fraction_value"] is not None else None
            continuous = value is not None and case["family"] == "deriv_binomial_call" and audit.compatible(value, audit.price(case["prompt"])[1])
            union = dict(base, declared_simple_valid=base["visible_valid"], continuous_valid=bool(continuous))
            union["visible_valid"] = base["visible_valid"] or continuous
            union["decisions"] = base["decisions"] | {"visible_contract": union["visible_valid"]}
            streams["two_conventions" if endpoint == "strict" else "numeric_two_conventions"].append(union)
    names = {"strict": "strict_scored", "numeric": "numeric_scored", "two_conventions": "convention_scored", "numeric_two_conventions": "numeric_convention_scored"}
    for endpoint, rows in streams.items():
        audit.compare(rows, audit.rows(audit.OUT / (names[endpoint] + ".jsonl")), {s["case_id"]: s for s in selection})
        audit.compare_summary(rows, results[endpoint])
        for family, saved in results["families"].items():
            audit.compare_summary([r for r in rows if r["family"] == family], saved[endpoint])
    report = {
        "executive_summary": "PASS: portable scientific-input and 800-score numerical replay; no external model/engine verification.",
        "status": "PASS",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "attempts": 200,
        "scored_records": 800,
        "replay_script_sha256": audit.digest(__file__),
        "external_weight_engine_hashes_rechecked": False,
        "inference_performed": False,
        "semantic_or_trace_certification": False,
        "endpoints": {e: audit.summarize(rows) for e, rows in streams.items()},
    }
    with args.output.open("x") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"status": "PASS", "attempts": 200, "scored_records": 800}))


if __name__ == "__main__":
    main()
