"""Executive summary: retain exact single-provider attempts and observed billing without retries."""

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

from .protocol import body


def now():
    return datetime.now(timezone.utc).isoformat()


def answer(identity, system, user):
    request_body = body(system, user)
    encoded = json.dumps(request_body, ensure_ascii=False, sort_keys=True).encode()
    record = {
        **identity, "started_utc": now(), "request_body": request_body,
        "request_sha256": hashlib.sha256(encoded).hexdigest(),
        "text": "", "finish_reason": "transport_error",
    }
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions", data=encoded,
        headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"],
                 "Content-Type": "application/json"},
    )
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            raw = json.load(response)
        record["raw_response"] = raw
        choice = raw["choices"][0]
        record.update({"text": choice["message"].get("content") or "",
                       "finish_reason": choice["finish_reason"],
                       "usage": raw.get("usage", {}), "provider": raw.get("provider"),
                       "returned_model": raw.get("model")})
        if record["provider"] != "SiliconFlow":
            record.update(finish_reason="provider_mismatch", error={"type": "ProviderMismatch"})
    except urllib.error.HTTPError as error:
        record["error"] = {"type": "HTTPError", "status": error.code}
    except Exception as error:
        record["error"] = {"type": type(error).__name__}
    record.update(completed_utc=now(), elapsed_s=time.perf_counter() - start)
    return record
