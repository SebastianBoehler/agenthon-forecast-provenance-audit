"""Executive summary: audit visible rounding instructions against Cosimo labels."""
import hashlib
import json
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import pandas as pd


SOURCE = Path("literature/pdfs/cosimo-cfa-level-i.parquet")
EXPECTED_SHA256 = "afa7e9241e0f06df090916e289a8e39d7fc9c4245c3b21c0c0f1188edafb0abb"
PATTERN = re.compile(r"D0 = \$([\d,.]+), growth g = ([\d.]+)%, required return r = ([\d.]+)%")


def main():
    actual_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if actual_hash != EXPECTED_SHA256:
        raise ValueError(f"Dataset hash mismatch: {actual_hash}")
    frame = pd.read_parquet(SOURCE)
    gordon = frame[frame.metadata.map(lambda meta: meta["generator"] == "cr_eq_gordon")]
    counts = {"total": len(gordon), "requests_whole_unit": 0, "parsed": 0,
              "raw_formula_matches_gold_within_cent": 0, "gold_differs_from_requested_whole_unit": 0,
              "preference_pairs": 0, "chosen_answer_differs_from_requested_whole_unit": 0}
    examples = []
    for row in gordon.itertuples():
        if "nearest whole unit" not in row.question.lower():
            continue
        counts["requests_whole_unit"] += 1
        match = PATTERN.search(row.question)
        if match is None:
            continue
        counts["parsed"] += 1
        dividend, growth, required = [Decimal(raw.replace(",", "")) for raw in match.groups()]
        exact = dividend * (1 + growth / 100) / (required / 100 - growth / 100)
        requested = exact.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        gold = Decimal(row.answer.replace(",", ""))
        if abs(exact - gold) <= Decimal("0.005"):
            counts["raw_formula_matches_gold_within_cent"] += 1
        if row.preference_pair is not None:
            counts["preference_pairs"] += 1
            chosen = Decimal(row.preference_pair["chosen"]["answer"].replace(",", ""))
            if chosen != requested:
                counts["chosen_answer_differs_from_requested_whole_unit"] += 1
        if gold != requested:
            counts["gold_differs_from_requested_whole_unit"] += 1
            if len(examples) < 5:
                examples.append({"id": row.id, "visible_question": row.question,
                                 "stored_gold": str(gold), "prompt_consistent": str(requested)})
    output = {"dataset": "btech-software/cosimo-cfa-frm-71k", "revision": "42244d29c6b9912683213a08d1a9c5b0373b381b",
              "source_sha256": actual_hash, "counts": counts, "examples": examples}
    destination = Path("outputs/reward-contract/cosimo-gordon-audit.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
