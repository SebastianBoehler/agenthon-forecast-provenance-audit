"""Executive summary: freeze a small paired local study before generating any cohort answers."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/grader-comparison-v1"
SYSTEM = ("Solve the question. You may briefly explain the calculation in at most five lines. "
          "End with exactly one final line: Final Answer: <scalar>. "
          "The scalar must be a signed integer, finite decimal, or fraction p/q. "
          "Do not write units, commas, Markdown, or a symbolic expression on that line. "
          "Respect requested rounding. Otherwise retain at least four decimal places for "
          "financial amounts. Financial rates use percentage points, for example 7.25 for 7.25%.")
CONFIG = {"system_prompt": SYSTEM, "temperature": 0.2, "top_k": 40, "top_p": 0.95,
          "min_p": 0, "repeat_penalty": 1, "max_output_tokens": 1024,
          "reasoning": "off", "integrations": [], "store": False, "stream": False}
MODELS = {
    "gemma": {"key": "google/gemma-4-e2b", "instance": "final-gemma",
              "checkpoint": "/Volumes/Sebastian-NVMe/LM Studio/lmstudio-community/gemma-4-E2B-it-GGUF/gemma-4-E2B-it-Q4_K_M.gguf"},
    "qwen": {"key": "qwen/qwen3.5-9b", "instance": "final-qwen",
             "checkpoint": "/Volumes/Sebastian-NVMe/LM Studio/lmstudio-community/Qwen3.5-9B-GGUF/Qwen3.5-9B-Q4_K_M.gguf"}}
REPEATS = 3


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def write(path, value):
    with Path(path).open("x") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write("\n")


def jsonl(path, rows):
    with Path(path).open("x") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")


def read(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines()]


def frozen():
    receipt = json.loads((OUT / "freeze.json").read_text())
    for path, checksum in receipt["files"].items():
        if digest(ROOT / path) != checksum:
            raise ValueError("Frozen study input changed: " + path)
    return read(OUT / "cohort.jsonl")
