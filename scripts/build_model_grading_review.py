"""Executive summary: prepare anonymous finance prompts with a separate ignored key.

Input is the frozen JSONL ledger containing 200 public source IDs as `case_id`.
This prepares review materials; it never supplies or records human annotations.
"""
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import pandas as pd

from independent_contract_validation import N, SOURCES, answer, exact_value, extract, round_whole

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/model-grading-review"
FAMILIES = ("cr_eq_gordon", "deriv_binomial_call", "eq_gordon", "corp_wacc")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank(row):
    text = "human-review-model-grading-v1:" + row["id"]
    return hashlib.sha256(text.encode()).hexdigest()


def rational(value):
    return {"fraction": str(value), "display": format(float(value), ".12g")}


def cosimo_key(row, role):
    family = row["metadata"]["generator"]
    value, details = exact_value(family, row["question"])
    whole = "nearest whole unit" in row["question"].lower()
    target, tie = round_whole(value) if whole else (value, False)
    key = {"source": "cosimo", "source_id": row["id"], "family": family,
           "role": role, "question": row["question"], "gold": rational(answer(row["answer"])),
           "formula": rational(value), "target": rational(target), "requested_whole": whole,
           "half_tie": tie, "units": "percentage points" if family in {"corp_wacc", "port_capm"} else "currency units",
           "rounding_allowance": "exact integer, either neighboring integer at a half tie" if whole else "0.005 output unit",
           "independent_details": {k: rational(v) if isinstance(v, F) else v for k, v in details.items()}}
    if family == "port_capm":
        key["interpretations"] = ["Displayed inputs exact", "Beta rounded to two decimals; displayed rates fixed"]
    return key


def dcf_key(row):
    cash, rate, growth = extract(rf"FCF_1=\${N}, Discount Rate r={N}%, Growth Rate g={N}%", row["prompt"])
    gap = rate - growth
    assert gap > F(1, 10)
    value = cash * 100 / gap
    return {"source": "rlvr", "source_id": row["id"], "family": "DCF_ordinary",
            "role": "supplementary_ambiguity", "question": row["prompt"], "units": "currency units",
            "gold": rational(F(str(row["ground_truth"]))), "formula": rational(value),
            "target": rational(value), "interpretations": ["Displayed rates exact", "Each displayed rate rounded to 0.1 percentage point"],
            "rounded_rate_interval": [rational(cash * 100 / (gap + F(1, 10))),
                                      rational(cash * 100 / (gap - F(1, 10)))]}


def main(selection):
    dataset = ROOT / "literature/pdfs" / SOURCES["cosimo"][0]
    rlvr = ROOT / "literature/pdfs" / SOURCES["rlvr"][0]
    assert sha(dataset) == SOURCES["cosimo"][1]
    assert sha(rlvr) == SOURCES["rlvr"][1]
    public = pd.read_parquet(dataset).to_dict("records")
    lookup = {r["id"]: r for r in public}
    chosen = [json.loads(line) for line in selection.read_text().splitlines()]
    assert len(chosen) == 200 and len({r["case_id"] for r in chosen}) == 200
    rows = [lookup[r["case_id"]] for r in chosen]
    assert all(item["prompt"] == row["question"] for item, row in zip(chosen, rows))
    keys = []
    for family in FAMILIES:
        pool = [r for r in rows if r["metadata"]["generator"] == family]
        assert len(pool) == 50 and len({r["question"] for r in pool}) == 50
        keys += [cosimo_key(r, "primary_panel") for r in sorted(pool, key=rank)[:2]]
    capm = sorted([r for r in public if r["metadata"]["generator"] == "port_capm"], key=rank)
    keys += [cosimo_key(r, "supplementary_ambiguity") for r in capm[:2]]
    dcf = [json.loads(line) for line in rlvr.read_text().splitlines()]
    dcf = [r for r in dcf if r["domain"] == "DCF Valuation" and not r["is_edge_case"]]
    keys += [dcf_key(r) for r in sorted(dcf, key=rank)[:2]]
    keys.sort(key=lambda r: hashlib.sha256(("review-order-v1:" + r["source_id"]).encode()).hexdigest())
    sections = ["## Executive summary (read this first)", "",
                "Twelve anonymous financial questions for prospective human review. No source labels,",
                "study classifications, verification flags or model identities are shown. Human",
                "annotation is pending. Complete each financial judgment before any candidate responses.", ""]
    blind = []
    for i, key in enumerate(keys, 1):
        rid = f"R{i:02d}"
        key["review_id"] = rid
        blind.append({"review_id": rid, "question": key["question"]})
        sections += [f"## {rid}", "", key["question"], "", "Assumptions: ____________________",
                     "Formula or cash flows: ____________________", "Final value and units: ____________________",
                     "Requested output precision: ____________________", "Input determinacy or conditional interpretations: ____________________",
                     "Disputed conventions or uncertainty: ____________________", "Candidate answer assessment (when supplied): ____________________", ""]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "BLINDED_PACKET.md").write_text("\n".join(sections) + "\n")
    (OUT / "BLINDED_QUESTIONS.jsonl").write_text("".join(json.dumps(r) + "\n" for r in blind))
    (OUT / "ANSWER_KEY.json").write_text(json.dumps({"status": "calculation key; no human annotations", "items": keys}, indent=2) + "\n")
    files = ["BLINDED_PACKET.md", "BLINDED_QUESTIONS.jsonl", "ANSWER_KEY.json", "REVIEW_INSTRUCTIONS.md"]
    manifest = {"status": "prepared; no human review or contact", "selection_sha256": sha(selection),
                "script_sha256": sha(Path(__file__)), "selected_review_source_ids": [k["source_id"] for k in keys],
                "input_hashes": {"cosimo": sha(dataset), "rlvr": sha(rlvr)},
                "packet_hashes": {name: sha(OUT / name) for name in files},
                "primary_panel_items": 8, "supplementary_ambiguity_items": 4}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
