"""Executive summary: retain one fixed-provider attempt per frozen document question and condition."""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request

from .model_protocol import MODELS, request_body


def answer(model_key: str, condition: str, row: dict) -> dict:
    body = request_body(model_key, condition, row["prompt"])
    encoded = json.dumps(body, ensure_ascii=False, sort_keys=True).encode()
    record = {"model_key": model_key, "condition": condition, "case_id": row["case_id"],
              "prompt_sha256": hashlib.sha256(row["prompt"].encode()).hexdigest(),
              "request_sha256": hashlib.sha256(encoded).hexdigest(), "text": "",
              "finish_reason": "transport_error"}
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions", data=encoded,
        headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"],
                 "Content-Type": "application/json"},
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            raw = json.load(response)
        record["raw_response"] = raw
        choice = raw["choices"][0]
        record.update({"text": choice["message"].get("content") or "",
                       "finish_reason": choice["finish_reason"], "usage": raw.get("usage", {}),
                       "provider": raw.get("provider"), "returned_model": raw.get("model")})
        if record["provider"] != MODELS[model_key]["provider_name"]:
            record["finish_reason"] = "provider_mismatch"
            record["error"] = {"type": "ProviderMismatch"}
    except urllib.error.HTTPError as error:
        record["error"] = {"type": "HTTPError", "status": error.code}
    except Exception as error:
        record["error"] = {"type": type(error).__name__}
    record["elapsed_s"] = time.perf_counter() - started
    return record
