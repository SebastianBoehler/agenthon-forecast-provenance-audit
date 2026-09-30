"""Executive summary: record native-template local attempts, model bytes and runtime nondecisions."""

import json
import platform
import time
from urllib.request import Request, urlopen

from .protocol import ROOT, OUT, CONFIG, MODELS, REPEATS, frozen, write, digest, now
from .scalars import final_scalar, scalar


def api(route, body=None):
    request = Request("http://127.0.0.1:1234" + route,
                      data=None if body is None else json.dumps(body).encode(),
                      headers={"Content-Type": "application/json"})
    with urlopen(request, timeout=120) as response:
        return json.load(response)


def metadata(model):
    rows = [m for m in api("/api/v1/models")["models"] if m["key"] == model["key"]]
    if len(rows) != 1:
        raise ValueError("Required model metadata missing")
    instances = [i for i in rows[0]["loaded_instances"] if i["id"] == model["instance"]]
    if len(instances) != 1 or instances[0]["config"]["context_length"] != 4096:
        raise ValueError("Required 4096-token native model instance missing")
    return rows[0], instances[0]["config"]


def attempt(model, prompt, loaded_config):
    body = dict(CONFIG, model=model["instance"], input=prompt)
    record = {"started_utc": now(), "request": body, "status": "runtime_nondecision"}
    started = time.perf_counter()
    try:
        _, live = metadata(model)
        if live != loaded_config:
            raise ValueError("Native load settings changed")
        raw = api("/api/v1/chat", body)
        record["raw_response"] = raw
        if raw.get("model_instance_id") != model["instance"]:
            raise ValueError("Unexpected returned model instance")
        stats = raw["stats"]
        if any(type(stats.get(k)) is not int or stats[k] < 0
               for k in ("input_tokens", "total_output_tokens", "reasoning_output_tokens")):
            raise ValueError("Invalid native token accounting")
        if stats["input_tokens"] == 0 or stats["input_tokens"] + 1024 > 4096:
            raise ValueError("Invalid native context headroom")
        if stats["reasoning_output_tokens"] or stats["total_output_tokens"] > 1024:
            raise ValueError("Native reasoning or output budget violated")
        if len(raw["output"]) != 1 or raw["output"][0].get("type") != "message":
            raise ValueError("Unexpected native output blocks")
        text = raw["output"][0]["content"]
        if not isinstance(text, str) or (text and not stats["total_output_tokens"]):
            raise ValueError("Invalid native message")
        record.update(text=text, stats=stats, status="returned",
                      at_output_cap=stats["total_output_tokens"] == 1024,
                      cap_origin="native token count; no native finish reason assumed")
    except Exception as exc:
        record["error"] = type(exc).__name__ + ": " + str(exc)
    record.update(completed_utc=now(), elapsed_s=time.perf_counter() - started)
    return record


def collect(name):
    cohort = frozen()
    model = MODELS[name]
    root = OUT / name
    root.mkdir(exist_ok=False)
    info, config = metadata(model)
    freeze = {"frozen_utc": now(), "model": info, "loaded_config": config,
              "checkpoint_path": model["checkpoint"], "checkpoint_sha256": digest(model["checkpoint"]),
              "checkpoint_bytes": __import__("pathlib").Path(model["checkpoint"]).stat().st_size,
              "request_config": CONFIG, "scientific_freeze_sha256": digest(OUT / "freeze.json"),
              "platform": platform.platform(), "native_tokenizer_and_template": True,
              "seed": None, "seed_note": "unseeded stochastic repetitions; replay saved answers exactly"}
    write(root / "model_freeze.json", freeze)
    probes = []
    for prompt, expected in (("What is 7 + 14?", "21"), ("What is half of 9?", "4.5"),
                             ("What is -3 + 1?", "-2")):
        record = attempt(model, prompt, config)
        answer = final_scalar(record.get("text", ""))
        record["probe_pass"] = (record["status"] == "returned" and not record["at_output_cap"]
                                and answer is not None and scalar(answer) == scalar(expected))
        probes.append(record)
    write(root / "probes.json", probes)
    if not all(r["probe_pass"] for r in probes):
        raise ValueError("Source-free readiness probes failed; no cohort calls")
    completed = 0
    import hashlib
    for repetition in range(REPEATS):
        ordered = sorted(cohort, key=lambda c: hashlib.sha256(f"{repetition}|{c['id']}".encode()).hexdigest())
        for case in ordered:
            record = attempt(model, case["prompt"], config)
            record.update(case_id=case["id"], model=name, repetition=repetition)
            write(root / f"attempt-{repetition}-{completed:03d}.json", record)
            completed += 1
            print(json.dumps({"model": name, "completed": completed, "scheduled": 48,
                              "status": record["status"]}), flush=True)
    write(root / "collection_receipt.json", {"completed_utc": now(), "scheduled": 48,
          "recorded": completed, "files": {p.name: digest(p) for p in root.glob("*.json")}})
