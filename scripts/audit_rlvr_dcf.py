"""Executive summary: recompute DCF labels from only prompt-visible operands."""
import hashlib
import json
import re
from statistics import median
from decimal import Decimal
from pathlib import Path


SOURCE = Path("literature/pdfs/financial-rlvr-10k-6cfa9a71.jsonl")
EXPECTED_SHA256 = "86968a146a09e2ba1b19aac3a5ca2bec7e878358341a7972fddeb4b8cd7754af"
PATTERN = re.compile(r"FCF_1=\$([\d,.]+), Discount Rate r=([\d.]+)%, Growth Rate g=([\d.]+)%")


def main():
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if source_hash != EXPECTED_SHA256:
        raise ValueError(f"Dataset hash mismatch: {source_hash}")
    counts = {"ordinary_dcf_rows": 0, "parsed_valid_rows": 0, "would_miss_advertised_abs_1e_minus_4": 0,
              "relative_difference_over_0_1_percent": 0, "relative_difference_over_1_percent": 0,
              "gold_within_rounded_input_interval": 0}
    examples = []
    interval_widths = []
    for line in SOURCE.open():
        row = json.loads(line)
        if row["domain"] != "DCF Valuation" or row["is_edge_case"]:
            continue
        counts["ordinary_dcf_rows"] += 1
        match = PATTERN.search(row["prompt"])
        if match is None:
            continue
        cash, rate, growth = [Decimal(value.replace(",", "")) for value in match.groups()]
        if rate <= growth:
            continue
        counts["parsed_valid_rows"] += 1
        visible = cash / (rate / 100 - growth / 100)
        gold = Decimal(str(row["ground_truth"]))
        # If both displayed rates are rounded to a tenth of a percentage point,
        # their difference can shift by 0.1 percentage points in either direction.
        delta = rate - growth
        low = cash / ((delta + Decimal("0.1")) / 100)
        high = cash / ((delta - Decimal("0.1")) / 100)
        if low - Decimal("0.00005") <= gold <= high + Decimal("0.00005"):
            counts["gold_within_rounded_input_interval"] += 1
        interval_widths.append(float((high - low) / visible))
        difference = abs(visible - gold)
        if difference > Decimal("0.0001"):
            counts["would_miss_advertised_abs_1e_minus_4"] += 1
            if len(examples) < 5:
                examples.append({"id": row["id"], "prompt": row["prompt"],
                                 "visible_formula_result": str(visible), "stored_gold": str(gold)})
        if difference / abs(visible) > Decimal("0.001"):
            counts["relative_difference_over_0_1_percent"] += 1
        if difference / abs(visible) > Decimal("0.01"):
            counts["relative_difference_over_1_percent"] += 1
    output = {"dataset": "coslinedev/financial-rlvr-10k-enterprise",
              "revision": "6cfa9a71e777026ba7242fbbb96c11c7dece5011",
              "source_sha256": source_hash, "counts": counts, "examples": examples,
              "median_relative_admissible_interval_width": median(interval_widths),
              "scope": "Advertised tolerance applied analytically; verifier code and real model reward not run"}
    destination = Path("outputs/reward-contract/rlvr-dcf-audit.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
