"""Executive summary: preserve native LM Studio replies and disclose completion normalization."""

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

from model_grading.protocol import ROOT, SYSTEM, MAX_TOKENS

OUT = ROOT / "outputs/model-grading-lmstudio-v1"
MODEL_KEY = "gemma4-e2b-q4km"
INSTANCE = "audit-gemma4-e2b"
BASE = "http://127.0.0.1:1234"
CONFIG = {
    "model": INSTANCE,
    "system_prompt": SYSTEM,
    "temperature": 0,
    "top_k": 1,
    "top_p": 1,
    "min_p": 0,
    "repeat_penalty": 1,
    "max_output_tokens": MAX_TOKENS,
    "reasoning": "off",
    "integrations": [],
    "store": False,
    "stream": False,
}
PROBES = [
    ("Currency amount: add 7 and 14 currency units.", "eq_gordon", "21"),
    ("Currency amount: what is half of 9 currency units?", "eq_gordon", "4.5"),
    (
        "A rate averages 4% and 8%, with weight 50% for each. What is the rate?",
        "corp_wacc",
        "6",
    ),
]


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    checksum = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(chunk)
    return checksum.hexdigest()


def write(name, value):
    with (OUT / name).open("x") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write("\n")


def api(route, body=None):
    request = Request(
        BASE + route,
        data=None if body is None else json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=120) as response:
        return json.load(response)


def normalized(raw):
    if raw.get("model_instance_id") != INSTANCE:
        raise ValueError("Unexpected model instance")
    output, stats = raw["output"], raw["stats"]
    if len(output) != 1 or output[0].get("type") != "message":
        raise ValueError("Missing message or unexpected reasoning/tool output")
    for field in ("input_tokens", "total_output_tokens", "reasoning_output_tokens"):
        if type(stats.get(field)) is not int or stats[field] < 0:
            raise ValueError("Invalid native token statistics")
    if stats["input_tokens"] == 0:
        raise ValueError("Missing native input-token accounting")
    if (
        stats["reasoning_output_tokens"] != 0
        or stats["total_output_tokens"] > MAX_TOKENS
    ):
        raise ValueError("Reasoning or output-token setting violated")
    if stats["input_tokens"] + MAX_TOKENS > 4096:
        raise ValueError("Native context budget is insufficient")
    text = output[0]["content"]
    if not isinstance(text, str):
        raise ValueError("Invalid returned message text")
    if text and stats["total_output_tokens"] == 0:
        raise ValueError("Nonempty reply has no native output tokens")
    return {
        "text": text,
        "finish_reason": (
            "length" if stats["total_output_tokens"] == MAX_TOKENS else "stop"
        ),
        "native_finish_reason": None,
        "finish_reason_origin": "normally_returned_native_reply_vs_conservative_cap",
        "prompt_tokens": stats["input_tokens"],
        "completion_tokens": stats["total_output_tokens"],
    }


def generate(prompt):
    record = {"text": "", "finish_reason": "runtime_error", "started_utc": now()}
    body = dict(CONFIG, input=prompt)
    serialized = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    record.update(
        {"request_body": body, "request_sha256": hashlib.sha256(serialized).hexdigest()}
    )
    started = time.perf_counter()
    try:
        loaded = [
            i
            for m in api("/api/v1/models")["models"]
            if m["key"] == "google/gemma-4-e2b"
            for i in m["loaded_instances"]
            if i["id"] == INSTANCE
        ]
        if len(loaded) != 1:
            raise ValueError("Required native instance is unavailable")
        record["live_loaded_config"] = loaded[0]["config"]
        frozen = json.loads((OUT / "preflight_freeze.json").read_text())
        if record["live_loaded_config"] != frozen["loaded_config"]:
            raise ValueError("Native load settings changed before the request")
        raw = api("/api/v1/chat", body)
        record["raw_native_response"] = raw
        record.update(normalized(raw))
    except Exception as exc:
        record["error"] = type(exc).__name__ + ": " + str(exc)
    record["elapsed_s"] = time.perf_counter() - started
    record["completed_utc"] = now()
    return record


def verify(name):
    frozen = json.loads((OUT / name).read_text())
    for path, expected in frozen["files"].items():
        if digest(ROOT / path) != expected:
            raise ValueError("Frozen scientific input changed: " + path)
    for path, expected in frozen["checkpoint_files"].items():
        if digest(path) != expected:
            raise ValueError("Frozen checkpoint/configuration changed: " + path)
    if frozen["request_config"] != CONFIG:
        raise ValueError("Frozen native request changed")
    models = api("/api/v1/models")["models"]
    instances = [
        i
        for m in models
        if m["key"] == "google/gemma-4-e2b"
        for i in m["loaded_instances"]
        if i["id"] == INSTANCE
    ]
    if len(instances) != 1 or instances[0]["config"] != frozen["loaded_config"]:
        raise ValueError("Loaded model configuration changed")
    return frozen
