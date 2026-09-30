"""Executive summary: cache pinned converters and record actual released-input inference."""
import hashlib
import importlib.metadata
import json
import pickle
import time
from pathlib import Path
from urllib.request import urlopen
import zstandard
from mars_cycle.runtime import DirectClient

ROOT = Path("data/external-baselines/mars-2m-pinned-v1")
REV = "de761abefc1e3c0a8106a03b4fed6fc73cf702d3"
NAMES = ("price", "price-level", "price-change-ratio", "order-volume", "lob-volume",
         "pred-order-volume", "order-interval", "minute-buy-order-count",
         "minute-trans-vwap-change", "minute-trans-volume", "num-minutes-to-open",
         "minute-cancel-volume", "lob-spread")


def main():
    folder = ROOT / "assets/converters"
    folder.mkdir(exist_ok=True)
    manifest = {}
    for name in NAMES:
        path = folder / (name + ".zstd")
        url = f"https://huggingface.co/datasets/Don-Don/mars-order-assets/resolve/{REV}/converters/{name}.zstd"
        if not path.exists():
            with urlopen(url, timeout=60) as response:
                path.write_bytes(response.read())
        manifest[path.name] = {"url": url, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}
    (ROOT / "converter_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    archive = ROOT / "assets/validation-samples/valid-00-00000000-0-32.zstd"
    start = time.perf_counter()
    # Official pinned artifact format is zstd-compressed pickle, not exchange state.
    samples = pickle.loads(zstandard.ZstdDecompressor().decompress(archive.read_bytes()))
    features, target = samples[0]
    client = DirectClient(ROOT, 7001)
    prediction = client.get_prediction(features)
    result = {"status": "released_validation_input_inference_completed", "sample_count": len(samples),
              "input_shape": list(features.shape), "input_dtype": str(features.dtype),
              "prediction": prediction.tolist(), "inference_seconds": client.seconds,
              "total_seconds": time.perf_counter() - start, "seed": 7001, "temperature": 1.0,
              "device": "cpu", "dtype": "fp32", "ignored_nonconstructor_metadata": client.metadata,
              "versions": {p: importlib.metadata.version(p) for p in ("torch", "transformers", "numpy", "pandas", "scipy")},
              "limitation": "Validation features are not an exchange reset; local CPU transport differs from official CUDA/fp16 service."}
    (ROOT / "runtime_probe.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
