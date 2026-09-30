#!/usr/bin/env python3
"""Executive summary: replay authored controls through pinned public scoring code.

Only inspected pure definitions and the native post-generation scoring statements
run. No model, dataset, network, torch import or complete inference CLI is invoked.
These post-inspection controls do not measure published benchmark-score effects.
"""

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import textwrap
from typing import List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs/recursivemas-code-review-v1"
REVISION = "cbfcaab56c9a8f660a9be598750b4ff3cd762056"
MANIFEST_SHA = "d95f51db4caace8fbcd69c3aab7ed82a07de6d0b171b90d8be8d930b78a88978"
HELPERS = {
    "_dataset_key", "_ensure_text", "_is_gsm8k_dataset", "_is_math500_dataset",
    "_is_aime_dataset", "is_choice_dataset", "extract_boxed_answer",
    "extract_pred_answer", "extract_gold_answer", "normalize_answer_string",
    "normalize_raw_no_space", "_replace_text_macros", "normalize_latex_text_string",
    "_replace_simple_fractions", "normalize_int_from_first_number", "compare_answers",
}
CONTROLS = [
    ("identity", "12", "12", True, "equal numeric identity"),
    ("integer_mismatch", "12", "13", False, "unequal integer negative control"),
    ("decimal_mismatch", "1.2", "1.8", True, "unequal nonintegers"),
    ("fraction_mismatch", r"\frac{1}{2}", r"\frac{4}{5}", True, "unequal fractions"),
    ("sign_mismatch", "-1", "+1", True, "opposite signs; MATH500 only"),
    ("negative_decimal_mismatch", "-1.2", "-1.8", True, "unequal negative decimals"),
    ("unit_diagnostic", "12 dollars", "12 years", True, "unit-blind diagnostic"),
    ("empty_final", "12", "", False, "empty final answer negative control"),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inspect_snapshots():
    raw = (BASE / "source_manifest.json").read_bytes()
    if sha(raw) != MANIFEST_SHA:
        raise ValueError("Source manifest checksum mismatch")
    manifest = json.loads(raw)
    if manifest["revision"] != REVISION:
        raise ValueError("Unexpected source revision")
    entries = {entry["path"]: entry for entry in manifest["sources"]}
    fragments = {}
    for entry in entries.values():
        for part in entry["fragments"]:
            path = (BASE / part["file"]).resolve()
            if BASE.resolve() not in path.parents:
                raise ValueError("Source fragment escapes artifact directory")
            data = path.read_bytes()
            if sha(data) != part["sha256"]:
                raise ValueError(f"Source fragment checksum mismatch: {path.name}")
            if len(data.splitlines()) != part["last_line"] - part["first_line"] + 1:
                raise ValueError(f"Source fragment line count mismatch: {path.name}")
            fragments[path.name] = data.decode()
    answer = entries["inference/inference_utils/answer_utils.py"]
    complete = "".join(fragments[Path(p["file"]).name] for p in answer["fragments"])
    if sha(complete.encode()) != answer["sha256"]:
        raise ValueError("Complete comparator reconstruction checksum mismatch")
    return entries, fragments, complete


def definitions(source, names, constant_names):
    nodes = []
    for node in ast.parse(source).body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            nodes.append(node)
        elif isinstance(node, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id in constant_names for t in node.targets):
                ast.literal_eval(node.value)
                nodes.append(node)
    found = {node.name for node in nodes if isinstance(node, ast.FunctionDef)}
    if found != names:
        raise ValueError(f"Missing inspected definitions: {names - found}")
    if any(isinstance(n, (ast.Import, ast.ImportFrom)) for node in nodes for n in ast.walk(node)):
        raise ValueError("Imports are excluded from control replay")
    return nodes


def build_environment(fragments, answer_source):
    env = {"re": re, "Optional": Optional, "Tuple": Tuple, "List": List}
    nodes = definitions(answer_source, HELPERS,
                        {"_GSM8K_KEYS", "_MATH500_KEYS", "_AIME_KEYS", "_MEDQA_KEYS", "_GPQA_KEYS"})
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "<pinned-pure-comparator>", "exec"), env)
    route = {"Optional": Optional, "Tuple": Tuple}
    nodes = definitions(fragments["lcb_utils_001_114.py.txt"],
                        {"_dataset_key", "is_lcb_dataset", "is_mbppplus_dataset", "is_code_eval_dataset"},
                        {"_LCB_KEYS", "_MBPPPLUS_KEYS"})
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "<pinned-dataset-predicates>", "exec"), route)
    exec(compile(fragments["inference_mas_165_187.py.txt"], "<pinned-resolver>", "exec"), route)
    dataset_name, config = route["resolve_dataset"]("math500")
    if dataset_name != "HuggingFaceH4/MATH-500" or config is not None:
        raise ValueError("Unexpected native MATH500 route")
    if route["is_code_eval_dataset"](dataset_name):
        raise ValueError("MATH500 unexpectedly enters code-test scoring")
    native = textwrap.dedent(fragments["inference_mas_3079_3088.py.txt"])
    harness = ("def native_scoring_block(gold_answers, outputs, dataset_name):\n"
               "    total = len(gold_answers)\n    correct_count = 0\n"
               + textwrap.indent(native, "    ")
               + "    return correct_count, eval_rows_math\n")
    exec(compile(harness, "<unchanged-native-postgeneration-statements>", "exec"), env)
    return env, dataset_name


def validate():
    entries, fragments, source = inspect_snapshots()
    env, dataset_name = build_environment(fragments, source)
    rows = []
    for alias in [dataset_name, "math500", "math-500"]:
        golds = [c[1] for c in CONTROLS]
        outputs = [f"Final Answer: {c[2]}" for c in CONTROLS]
        count, scored = env["native_scoring_block"](golds, outputs, alias)
        if count != sum(c[3] for c in CONTROLS):
            raise ValueError("Native scoring count disagrees with authored expectation")
        for control, generated, result in zip(CONTROLS, outputs, scored):
            helper = env["compare_answers"](control[1], generated, alias)
            if result != helper or result[2] is not control[3]:
                raise ValueError(f"Helper/native-block mismatch: {control[0]}")
            rows.append({"id": control[0], "dataset_name": alias, "gold_authored": control[1],
                         "output_authored": generated, "purpose": control[4],
                         "accepted": result[2], "gold_key": result[3], "prediction_key": result[4]})
    return {"status": "PASS", "revision": REVISION, "manifest_sha256": MANIFEST_SHA,
            "script_sha256": sha(Path(__file__).read_bytes()), "source_file_count": len(entries),
            "fragment_count": len(fragments), "authored_control_count": len(CONTROLS),
            "dataset_alias_count": 3, "native_block_checks": len(rows),
            "canonical_native_count": 6, "canonical_authored_denominator": 8,
            "rows": rows, "scope": "post-inspection MATH500 authored controls only; static dispatch plus isolated native scoring block",
            "not_measured": ["complete CLI execution", "model behavior", "real benchmark scores", "historical paper evaluator", "financial label correctness"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a new receipt; an existing file is never overwritten")
    args = parser.parse_args()
    result = validate()
    if args.output:
        result["validated_utc"] = datetime.now(timezone.utc).isoformat()
        with args.output.open("x") as handle:
            handle.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["status", "source_file_count", "fragment_count", "authored_control_count", "native_block_checks"]}))


if __name__ == "__main__":
    main()
