"""Executive summary: publish the complete newly generated source bank without replacing any frozen file."""

import shutil

from independent_finance.protocol import OUT, ROOT, digest, verified_freeze, write

if __name__ == "__main__":
    verified_freeze()
    target = ROOT / "artifacts/independent-financial-source-v1"
    target.mkdir(exist_ok=False)
    names = ("freeze.json", "attempts.jsonl", "analysis.json", "collection_receipt.json")
    for name in names:
        shutil.copyfile(OUT / name, target / name)
    write(target / "manifest.json", {"executive_summary": "Complete new native instances, not historical FinChain corpus.",
          "files": {name: digest(target / name) for name in names},
          "packager_sha256": digest(ROOT / "scripts/package_independent_finance.py"),
          "third_party_code": "../finchain-source-v1/", "historical_corpus_recovered": False})
