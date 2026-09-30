"""Executive summary: reconstruct exact Apache-licensed source and load inspected pure functions only."""

import ast
import hashlib
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "artifacts/finchain-source-v1"
REVISION = "9bd2942b85d992844b77094a8b822aa16832703c"
FUNCTIONS = {
    "binomial_call": ("data/templates/financial_markets/option_pricing.py", "template_op_medium1"),
    "wacc": ("data/templates/corporate_finance/wacc.py", "template_easy_wacc"),
    "compound_interest": ("data/templates/investment_analysis/ci.py", "template_ci_simple_calculation")}


def sources():
    manifest = json.loads((BASE / "source_manifest.json").read_text())
    if manifest["revision"] != REVISION:
        raise ValueError("Unexpected FinChain code revision")
    result = {}
    for entry in manifest["sources"]:
        chunks = []
        for part in entry["fragments"]:
            raw = (BASE / part["file"]).read_bytes()
            if hashlib.sha256(raw).hexdigest() != part["sha256"]:
                raise ValueError("Source fragment changed")
            if len(raw.splitlines()) != part["last_line"] - part["first_line"] + 1:
                raise ValueError("Source line interval changed")
            chunks.append(raw)
        complete = b"".join(chunks)
        if hashlib.sha256(complete).hexdigest() != entry["sha256"]:
            raise ValueError("Reconstructed FinChain source changed")
        result[entry["upstream_path"]] = complete.decode()
    return result


def generate(family, seed):
    code = sources()
    path, name = FUNCTIONS[family]
    nodes = ast.parse(code[path]).body
    function = [n for n in nodes if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(function) != 1 or any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(function[0])):
        raise ValueError("Unexpected selected source definition")
    env = {"random": random.Random(seed)}
    for node in nodes + ast.parse(code["data/templates/corporate_finance/misc.py"]).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            key = node.targets[0].id
            if key in ("investor_names", "underlying_assets", "project_names", "companies", "currencies"):
                env[key] = ast.literal_eval(node.value)
    exec(compile(ast.Module(body=function, type_ignores=[]), "<pinned-finchain-selected-template>", "exec"), env)
    question, solution = env[name]()
    if not isinstance(question, str) or not isinstance(solution, str):
        raise ValueError("Native template did not return two strings")
    return question, solution
