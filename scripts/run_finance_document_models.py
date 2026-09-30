"""Executive summary: collect the frozen 384-answer panel after blinded review locks, under $1.50."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from decimal import Decimal

from finance_document_review.model_client import answer
from finance_document_review.model_protocol import (
    MODELS, OUTPUT, ROOT, SPENDING_CAP, SYSTEMS, cases, digest, spending_bound,
)


def check_freeze() -> dict:
    freeze = json.loads((OUTPUT / "freeze.json").read_text())
    for path, expected in freeze["files_sha256"].items():
        if digest(ROOT / path) != expected:
            raise ValueError(f"Frozen panel input changed: {path}")
    locks = ROOT / "outputs/finance-document-review-v1/pre_target_lock.json"
    if not locks.exists():
        raise ValueError("Both technical reviews and pre-target adjudication must be locked first")
    lock = json.loads(locks.read_text())
    for path, expected in lock["files_sha256"].items():
        if digest(ROOT / path) != expected:
            raise ValueError(f"Locked review changed: {path}")
    for spec in MODELS.values():
        url = "https://openrouter.ai/api/v1/models/" + spec["model"] + "/endpoints"
        with urllib.request.urlopen(url, timeout=45) as response:
            endpoints = json.load(response)["data"]["endpoints"]
        matches = [row for row in endpoints if row["tag"] == spec["provider_tag"]]
        if len(matches) != 1:
            raise ValueError("Frozen provider is no longer uniquely available")
        endpoint = matches[0]
        if (Decimal(endpoint["pricing"]["prompt"]) != Decimal(spec["prompt_price"])
                or Decimal(endpoint["pricing"]["completion"]) != Decimal(spec["completion_price"])
                or not {"response_format", "reasoning", "temperature", "max_tokens"}
                    <= set(endpoint["supported_parameters"])):
            raise ValueError("Frozen endpoint price or parameter support changed")
    return freeze


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    check_freeze()
    rows = cases()
    bound = spending_bound(rows) + Decimal("0.01")
    if bound > SPENDING_CAP:
        raise ValueError(f"Panel and preflight bound exceeds cap: {bound}")
    path = OUTPUT / ("preflight.jsonl" if args.preflight else "responses.jsonl")
    if path.exists():
        raise ValueError("Existing response ledger; one-attempt panel refuses regeneration")
    jobs = [(model, condition, row) for model in MODELS for condition in SYSTEMS for row in rows]
    if args.preflight:
        toy = {"case_id": "authored_api_preflight", "prompt": json.dumps({
            "question": "What is 7 times 9?", "original_context": {"text": "Count in units."}
        })}
        jobs = [(model, "baseline", toy) for model in MODELS]
    random.Random(20260930).shuffle(jobs)
    costs, missing_costs = Decimal(0), 0
    with path.open("x") as output, ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(answer, model, condition, row) for model, condition, row in jobs]
        for completed, future in enumerate(as_completed(futures), 1):
            result = future.result()
            output.write(json.dumps(result, ensure_ascii=False) + "\n")
            output.flush()
            cost = result.get("usage", {}).get("cost")
            if cost is None:
                missing_costs += 1
            else:
                costs += Decimal(str(cost))
            if completed % 16 == 0 or completed == len(jobs):
                print(json.dumps({"completed": completed, "attempts": len(jobs),
                                  "reported_cost_usd": str(costs),
                                  "missing_cost_records": missing_costs}), flush=True)
    receipt = {"executive_summary": "One attempt per frozen question/configuration/condition; failures retained.",
               "attempts": len(jobs), "response_sha256": digest(path),
               "freeze_sha256": digest(OUTPUT / "freeze.json"),
               "reported_cost_usd": str(costs), "missing_cost_records": missing_costs,
               "conservative_bound_usd": str(bound), "spending_cap_usd": str(SPENDING_CAP),
               "collection_order_seed": 20260930, "preflight": args.preflight}
    name = "preflight_receipt.json" if args.preflight else "collection_receipt.json"
    with (OUTPUT / name).open("x") as output:
        json.dump(receipt, output, indent=2)
        output.write("\n")


if __name__ == "__main__":
    main()
