"""Executive summary: bind Gemma weights, native configuration and unchanged grading inputs."""

import json
import plistlib
from pathlib import Path

from model_grading.protocol import frozen_selection
from model_grading_lmstudio import OUT, ROOT, CONFIG, INSTANCE, api, digest, now, write


def main():
    OUT.mkdir(exist_ok=False)
    selection = frozen_selection()
    models = api("/api/v1/models")["models"]
    model = next(m for m in models if m["key"] == "google/gemma-4-e2b")
    instance = next(i for i in model["loaded_instances"] if i["id"] == INSTANCE)
    required = {
        "context_length": 4096,
        "parallel": 1,
        "speculative_draft_mtp": False,
        "speculative_draft_simple": False,
    }
    if any(instance["config"].get(k) != v for k, v in required.items()):
        raise ValueError(
            "Loaded context/parallel/speculation settings violate protocol"
        )
    index = json.loads(
        (Path.home() / ".lmstudio/.internal/model-index-cache.json").read_text()
    )
    entries = [
        r
        for r in index["models"]
        if r.get("containingDirSubpath") == "google/gemma-4-e2b"
        and not r.get("virtual", {}).get("isAlt")
    ]
    if len(entries) != 1:
        raise ValueError("Concrete model index is ambiguous")
    entry = entries[0]
    checkpoints = (
        [entry["entryPoint"]["absPath"], entry["visionAdapter"]["absPath"]]
        if entry.get("visionAdapter")
        else [entry["entryPoint"]["absPath"]]
    )
    checkpoints += [
        r["absPath"] for r in entry["selfFiles"] if r["ext"] in ("json", "yaml", "md")
    ]
    engine = (
        Path.home()
        / ".lmstudio/extensions/backends/llama.cpp-mac-arm64-apple-metal-advsimd-2.47.0"
    )
    checkpoints += [str(p) for p in sorted(engine.iterdir()) if p.is_file()]
    checkpoints.append(
        str(Path.home() / ".lmstudio/.internal/backend-preferences-v1.json")
    )
    files = [
        "docs/MODEL_GRADING_LMSTUDIO_PROTOCOL_V1.md",
        "scripts/prepare_model_grading_lmstudio.py",
        "scripts/run_model_grading_lmstudio.py",
        "scripts/analyze_model_grading_lmstudio.py",
        "src/model_grading_lmstudio.py",
        "scripts/analyze_model_grading_conventions.py",
        "tests/test_model_grading_lmstudio.py",
        "docs/MODEL_GRADING_GEMMA_PRECOLLECTION_REVIEW_V1.md",
    ]
    files += [
        str(p.relative_to(ROOT))
        for folder in ("src/answer_contract", "src/model_grading")
        for p in sorted((ROOT / folder).glob("*.py"))
    ]
    original = json.loads(
        (ROOT / "outputs/model-grading-v1/selection_manifest.json").read_text()
    )
    files += list(original["frozen_sha256"])
    files += [
        "outputs/model-grading-v1/selection_manifest.json",
        "outputs/model-grading-v1/selection.jsonl",
    ]
    app = plistlib.loads(
        Path("/Applications/LM Studio.app/Contents/Info.plist").read_bytes()
    )
    freeze = {
        "executive_summary": "Preflight identity freeze; no selected Gemma answer collected.",
        "created_utc": now(),
        "scheduled": len(selection),
        "request_config": CONFIG,
        "files": {p: digest(ROOT / p) for p in sorted(set(files))},
        "checkpoint_files": {p: digest(p) for p in checkpoints},
        "model_metadata": model,
        "loaded_config": instance["config"],
        "app_version": app["CFBundleShortVersionString"],
        "engine": "llama.cpp-mac-arm64-apple-metal-advsimd@2.47.0",
        "native_token_ids_available": False,
        "native_finish_reason_available": False,
        "full_metal_offload_requested": True,
        "effective_gpu_layer_ratio_exposed": False,
    }
    write("preflight_freeze.json", freeze)
    print(
        json.dumps(
            {
                "scheduled": len(selection),
                "checkpoint_files": len(checkpoints),
                "preflight_freeze_sha256": digest(OUT / "preflight_freeze.json"),
            }
        )
    )


if __name__ == "__main__":
    main()
