"""Executive summary: independently validate the exploratory Qwen3 4B extension.

Original 600-response outputs are preserved. Separate Fraction-based scores check
the extension and, when available, all 800 combined per-response decisions.
"""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from validate_model_grading_outputs import MODELS, compare_primary, score, sha, summarize

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "outputs/model-grading-v1"
OUT = ROOT / "outputs/model-grading-review"


def read(path):
    return [json.loads(s) for s in path.read_text().splitlines()]


def aggregates(rows, models, families):
    return {m: {"aggregate": summarize([r for r in rows if r["model_key"] == m]),
                "families": {f: summarize([r for r in rows if r["model_key"] == m and r["family"] == f])
                             for f in families}} for m in models}


def main():
    freeze = STUDY / "extension_manifest.json"
    extension = json.loads(freeze.read_text())
    for path, digest in extension["files"].items():
        assert sha((ROOT / path).read_bytes()) == digest, path
    manifest = json.loads((STUDY / "selection_manifest.json").read_text())
    for path, digest in manifest["frozen_sha256"].items():
        assert sha((ROOT / path).read_bytes()) == digest, path
    supplementary = json.loads((STUDY / "numeric_sensitivity_freeze_v2.json").read_text())
    for path, digest in supplementary["files"].items():
        assert sha((ROOT / path).read_bytes()) == digest, path
    assert sha((STUDY / "selection.jsonl").read_bytes()) == extension["selection_sha256"]
    assert set(extension["added_models"]) == {"qwen3-4b"}
    selection = {r["case_id"]: r for r in read(STUDY / "selection.jsonl")}
    families = sorted({r["family"] for r in selection.values()})
    strict, numeric, counts, hashes, runtime_checks, conflicts = [], [], {}, {}, {}, []
    snapshots = OUT / "extension-ledger-snapshots"
    snapshots.mkdir(parents=True, exist_ok=True)
    for model, spec in extension["added_models"].items():
        path = STUDY / f"{model}_responses.jsonl"
        if not path.exists():
            counts[model] = 0
            continue
        raw = path.read_bytes()
        assert not raw or raw.endswith(b"\n"), "Partial append; rerun after it completes"
        hashes[path.name] = sha(raw)
        (snapshots / f"{sha(raw)[:12]}-{path.name}").write_bytes(raw)
        responses = [json.loads(s) for s in raw.decode().splitlines()]
        ids = {r["case_id"] for r in responses}
        assert len(ids) == len(responses) and ids.issubset(selection)
        runtime_path = STUDY / f"{model}_runtime.json"
        runtime = json.loads(runtime_path.read_text())
        assert all(runtime[k] == v for k, v in spec.items())
        assert runtime["system_prompt"] == manifest["system_prompt"]
        assert runtime["selection_sha256"] == extension["selection_sha256"]
        assert runtime["device"] == "mps" and runtime["dtype"] == "float16"
        assert runtime["decoding"] == "greedy" and runtime["max_new_tokens"] == 1024
        runtime_checks[model] = {"recorded_settings_agree": True, "sha256": sha(runtime_path.read_bytes())}
        for response in responses:
            case = selection[response["case_id"]]
            assert response["model_key"] == model and response["model"] == spec["repository"]
            assert response["question_hash"] == case["question_hash"]
            strict.append(score(response, case))
            n = score(response, case, numeric=True)
            numeric.append(n)
            last_raw = next((s.strip() for s in reversed(response["text"].splitlines()) if s.strip()), "")
            last = last_raw.casefold().strip("*")
            payload = last[6:].lstrip() if last.startswith("final:") else ""
            if payload.startswith("$") and payload.endswith(("percent", "%")) and n["unit_state"] == "wrong":
                conflicts.append({"model_key": model, "case_id": case["case_id"], "last_line": last_raw})
        counts[model] = len(responses)
    models = tuple(extension["added_models"])
    strict_aggregate, numeric_aggregate = aggregates(strict, models, families), aggregates(numeric, models, families)
    result = {"status": "complete_extension" if all(v == 200 for v in counts.values()) else "partial_extension_snapshot",
              "executed_utc": datetime.now(timezone.utc).isoformat(),
              "responses_by_model": counts, "models": strict_aggregate,
              "numeric_models": numeric_aggregate,
              "unit_states": {m: dict(Counter(r["unit_state"] for r in numeric if r["model_key"] == m)) for m in models},
              "response_sha256": hashes, "runtime_checks": runtime_checks,
              "extension_freeze_sha256": sha(freeze.read_bytes()),
              "script_sha256": sha(Path(__file__).read_bytes()),
              "independent_scorer_sha256": sha((ROOT / "scripts/validate_model_grading_outputs.py").read_bytes()),
              "contradictory_prefix_suffix_cases": conflicts,
              "primary_comparison": compare_primary(strict, strict_aggregate, prefix="extension_", models=models),
              "numeric_primary_comparison": compare_primary(numeric, numeric_aggregate, numeric=True, prefix="extension_", models=models)}
    if (STUDY / "combined_results.json").exists():
        for mode, added in (("", strict), ("numeric-", numeric)):
            original = read(OUT / f"independent-{mode}response-scores.jsonl")
            assert len(original) == 600
            combined = original + added
            assert len(combined) == 800
            combined_aggregate = aggregates(combined, MODELS + models, families)
            result[mode + "combined_comparison"] = compare_primary(
                combined, combined_aggregate, numeric=bool(mode), prefix="combined_", models=MODELS + models)
        for filename in ("combined_results.json", "combined_numeric_sensitivity.json"):
            combined_result = json.loads((STUDY / filename).read_text())
            assert combined_result["responses"] == 800 and combined_result["questions"] == 200
            for constituent, digest in combined_result["constituent_sha256"].items():
                assert sha((STUDY / constituent).read_bytes()) == digest
    for name, rows in (("extension-scores.jsonl", strict), ("extension-numeric-scores.jsonl", numeric)):
        (OUT / name).write_text("".join(json.dumps(r) + "\n" for r in rows))
    (OUT / "independent-extension-summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "counts": counts, "models": strict_aggregate}, indent=2))


if __name__ == "__main__":
    main()
