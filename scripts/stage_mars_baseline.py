"""Executive summary: cache pinned official MarS inputs; do not run model or archive code."""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen


MODEL_REV = "b8f8c818c2a270844961b975f311457628bf2972"
ASSET_REV = "de761abefc1e3c0a8106a03b4fed6fc73cf702d3"
SOURCE_REV = "f04dd87a4d56342a6a2fc271cdb158fbacd83674"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.output_dir
    root.mkdir(parents=True, exist_ok=False)
    files = []
    for filename in ("config.json", "LICENSE", "README.md", "model.safetensors"):
        url = f"https://huggingface.co/Don-Don/mars-order-2m/resolve/{MODEL_REV}/{filename}"
        digest = "4350052857d1d62706521284318cf01a14a0e0874b616f3a2f86bc8fcd1469d6" if filename.endswith("safetensors") else None
        files.append(("model/" + filename, url, digest))
    for filename in ("LICENSE", "README.md", "validation-samples/valid-00-00000000-0-32.zstd"):
        url = f"https://huggingface.co/datasets/Don-Don/mars-order-assets/resolve/{ASSET_REV}/{filename}"
        digest = "f0a9241e708e18520190b58b9396c464802f8e0282d613c82d12de7e72eac24f" if filename.endswith("zstd") else None
        files.append(("assets/" + filename, url, digest))
    files.append(("official-source.zip", f"https://codeload.github.com/microsoft/MarS/zip/{SOURCE_REV}", None))
    manifest = {}
    for relative, url, expected in files:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        hasher = hashlib.sha256()
        with urlopen(url, timeout=90) as response, path.open("xb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
                hasher.update(chunk)
        digest = hasher.hexdigest()
        if expected is not None and digest != expected:
            raise ValueError(f"Publisher checksum mismatch: {relative}")
        manifest[relative] = {"url": url, "sha256": digest, "bytes": path.stat().st_size,
                              "publisher_sha256_verified": expected is not None}
        print("Cached", relative, path.stat().st_size, flush=True)
    (root / "manifest.json").write_text(json.dumps({"status": "staged_only_no_model_execution",
        "model_revision": MODEL_REV, "asset_revision": ASSET_REV, "source_revision": SOURCE_REV,
        "files": manifest}, indent=2) + "\n")


if __name__ == "__main__":
    main()
