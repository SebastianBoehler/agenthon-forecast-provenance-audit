"""Executive summary: load hash-checked pinned upstream definitions; isolate normalization ablations."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load():
    path = ROOT / "scripts/validate_recursivemas_authored_controls.py"
    spec = importlib.util.spec_from_file_location("pinned_recursive_controls", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.BASE = ROOT / "artifacts/recursivemas-scoring-source-v1"
    _, fragments, source = module.inspect_snapshots()
    return module.build_environment(fragments, source)


def normalized_comparison(env, reference, prediction, omit=()):
    strategies = [("intpart", "normalize_int_from_first_number"),
                  ("latex_text", "normalize_latex_text_string"),
                  ("nospace", "normalize_raw_no_space"),
                  ("digits", "normalize_answer_string")]
    for name, function in strategies:
        if name in omit:
            continue
        left, right = env[function](reference), env[function](prediction)
        if left and right and left == right:
            return True, name
    return False, None
