"""Executive summary: build a new local review ZIP only after closed results and numerical replay exist."""

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from semantic_transfer_package_policy import ANALYSIS, BASE_NAME, BASE_SHA, PAPER, README, digest, file_check, observed_spend, selected_files

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "outputs/answer-contract-research-20260930-semantic-transfer-review.zip"
ITERATION = ROOT / "outputs/submission-iteration-20260930"
MANIFEST = ITERATION / "semantic_transfer_review_manifest.json"
RECEIPT = ITERATION / "semantic_transfer_review_receipt.json"
MANUSCRIPT_CHECK = "outputs/submission-iteration-20260930/semantic_transfer_manuscript_check.json"
STYLE_SHA = "c3fc2894e83d2517ca18b66741d6c595986d97957dc08ec08bb2125a7ec4555a"


def read(path):
    return json.loads((ROOT / path).read_text())


def finality():
    states = {}
    for folder in ("finance-quantity-transfer-v1", "finance-quantity-judge-v2"):
        run = read(f"outputs/{folder}/collection/run.json")
        if run["state"] not in {"complete", "stopped"} or not run.get("completed_utc"):
            raise ValueError("Do not package a moving collection")
        states[folder] = run["state"]
    manuscript = read(MANUSCRIPT_CHECK)
    if manuscript["paper_sha256"] != digest(ROOT / PAPER) or manuscript["native_compile_success"] is not True:
        raise ValueError("Current-paper native compilation receipt required")
    if manuscript["embedded_official_style_sha256"] != STYLE_SHA or manuscript["rendered_pages_verified"] is not False:
        raise ValueError("Official-style identity/page-count scope differs from the declared receipt")
    for receipt_path in (f"{ANALYSIS}/receipt.json", f"{ANALYSIS}/portable-replay/receipt.json"):
        receipt = read(receipt_path)
        if receipt["inference_performed"] is not False or not receipt.get("completed_utc"):
            raise ValueError("Completed no-inference analysis/replay receipt required")
        for name, expected in receipt["code_sha256"].items():
            if digest(ROOT / name) != expected:
                raise ValueError("Analysis/replay code changed after receipt")
        parent = (ROOT / receipt_path).parent
        for name, expected in receipt["output_sha256"].items():
            if digest(parent / name) != expected:
                raise ValueError("Analysis/replay output changed after receipt")
    if read(f"{ANALYSIS}/receipt.json")["portable_mode"] is not False:
        raise ValueError("The original full local analysis receipt is required")
    replay_receipt = read(f"{ANALYSIS}/portable-replay/receipt.json")
    if replay_receipt["portable_mode"] is not True:
        raise ValueError("Separate projected numerical replay receipt required")
    for path, expected in replay_receipt["input_sha256"].items():
        input_path = Path(path)
        if not input_path.is_absolute():
            input_path = ROOT / input_path
        if digest(input_path) != expected:
            raise ValueError("Projected numerical replay input changed")
    return states


def main():
    if any(path.exists() for path in (TARGET, MANIFEST, RECEIPT)):
        raise FileExistsError("Never replace prior archives/manifests/receipts")
    base = ROOT / BASE_NAME
    if digest(base) != BASE_SHA:
        raise ValueError("Immutable prior followup archive hash changed")
    states = finality()
    names = selected_files()
    inventory = {name: file_check(ROOT, name) for name in names}
    for frozen_path, field in [("outputs/finance-quantity-transfer-v1/experiment_freeze.json", "source_files"),
                               ("outputs/finance-quantity-judge-v2/plan_freeze.json", "source_files"),
                               ("outputs/finance-quantity-judge-v2/plan_freeze.json", "unchanged_v1_sources")]:
        for record in read(frozen_path)[field]:
            if digest(ROOT / record["path"]) != record["sha256"]:
                raise ValueError("Frozen V1/V2 code/protocol changed")
    ledger_path = "outputs/finance-quantity-transfer-v1/spend_ledger.jsonl"
    events = [json.loads(line) for line in (ROOT / ledger_path).read_text().splitlines() if line.strip()]
    accounting = observed_spend(events)
    if not accounting["observed_cost_complete"] and "stopped" not in states.values():
        raise ValueError("Unknown billing requires an explicitly stopped execution")
    v2_status = read("outputs/finance-quantity-judge-v2/collection/attempt_status.json")
    if len(v2_status) != 64 or len({(x["case_id"], x["arm"]) for x in v2_status}) != 64:
        raise ValueError("All 64 planned V2 judge records must remain present")
    status_counts = Counter(x["judge_status"] for x in v2_status)
    if set(status_counts) - {"recorded", "attempted", "not_started"}:
        raise ValueError("Unknown V2 attempt status")
    original, replayed = read(f"{ANALYSIS}/results.json"), read(f"{ANALYSIS}/portable-replay/results.json")
    for key in ("questions", "planned_answer_attempts", "planned_judge_attempts", "provisional_eligible_questions",
                "all_attempts", "by_arm", "by_source_arm", "paired_provisional_eligible_22", "paired_all_32",
                "judge_vs_numerical_match_only", "judge_by_reported_expression_match_cells"):
        if original[key] != replayed[key]:
            raise ValueError("Saved projected numerical replay disagrees: " + key)
    if original.get("separate_judge_v2_diagnostic", {}).get("by_arm") != \
       replayed.get("separate_judge_v2_diagnostic", {}).get("by_arm"):
        raise ValueError("Saved V2 accounting differs in projected replay")
    manifest = {
        "executive_summary": "Local review evidence and compact numerical replay; contexts and full prompt/semantic replay omitted.",
        "created_utc": datetime.now(timezone.utc).isoformat(), "paper_sha256": inventory[PAPER]["sha256"],
        "historical_archive": {"path": BASE_NAME, "sha256": BASE_SHA, "nested_unchanged": True},
        "files": inventory, "execution_states": states, "accounting": accounting,
        "v2_attempt_denominator": {"planned_judges": 64, "status_counts": dict(status_counts),
            "interpretation": "All planned cases retained, including stopped/failed and not-started attempts; no complete V2 claim."},
        "manuscript_check": {"receipt": MANUSCRIPT_CHECK, "sha256": inventory[MANUSCRIPT_CHECK]["sha256"],
            "native_compile_success": True, "embedded_official_style_sha256": STYLE_SHA,
            "rendered_pages_verified": False, "nine_page_compliance_claimed": False},
        "portable_replay_scope": "Saved numeric/schema/typed-unit/expression/native-literal endpoints and saved proxy-accounting flags only; no inference.",
        "semantic_review_scope": "Inspectable AI technical readings under assumptions; no expert truth certification or full semantic replay.",
        "input_omissions": ["full original report contexts", "question/experiment/review packets",
            "source_targets and original native annotation/program fields", "private outcome join key",
            "raw request bodies and raw provider responses", "credentials/environment/cache/model weights"],
        "omission_boundary": "New iteration tree only; historical ZIP is nested byte-for-byte under its own documented scope.",
        "source_free_numerical_replay": True, "full_prompt_replay": False, "full_semantic_replay": False,
        "expert_adjudication": False, "public_release_or_submission": False,
    }
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    # Recheck every identity immediately before archival; reject moving inputs.
    if any(digest(ROOT / name) != record["sha256"] for name, record in inventory.items()):
        raise ValueError("Whitelisted input changed during packaging")
    ITERATION.mkdir(parents=True, exist_ok=True)
    with ZipFile(TARGET, "x", compression=ZIP_DEFLATED) as archive:
        archive.write(base, "historical/" + base.name)
        archive.writestr("README.md", (ROOT / README).read_bytes())
        archive.writestr("semantic_transfer_review_manifest.json", manifest_bytes)
        for name in names:
            archive.write(ROOT / name, name)
    with ZipFile(TARGET) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP integrity failure; retained failed archive")
        if hashlib.sha256(archive.read("historical/" + base.name)).hexdigest() != BASE_SHA:
            raise ValueError("Nested historical identity mismatch; retained failed archive")
        for name, expected in inventory.items():
            if hashlib.sha256(archive.read(name)).hexdigest() != expected["sha256"]:
                raise ValueError("Archived input changed; retained failed archive: " + name)
        entries = len(archive.namelist())
    with MANIFEST.open("xb") as stream:
        stream.write(manifest_bytes)
    receipt = {"executive_summary": "PASS: whitelist identities and unchanged historical ZIP; saved projected numerical replay checked separately.",
               "created_utc": datetime.now(timezone.utc).isoformat(), "zip_sha256": digest(TARGET),
               "manifest_sha256": digest(MANIFEST), "paper_sha256": inventory[PAPER]["sha256"],
               "entries": entries, "hashed_current_files": len(names), "accounting": accounting,
               "inference_performed": False, "full_semantic_or_prompt_replay": False}
    with RECEIPT.open("x") as stream:
        json.dump(receipt, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
