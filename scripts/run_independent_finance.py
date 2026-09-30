"""Executive summary: collect all frozen native instances once and seal every attempt plus summary."""

import json

from independent_finance.analysis import collect, summarize
from independent_finance.protocol import OUT, verified_freeze, write, digest

if __name__ == "__main__":
    verified_freeze()
    target = OUT / "attempts.jsonl"
    if target.exists():
        raise FileExistsError("Existing attempts cannot be replaced")
    rows = collect()
    target.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    report = summarize(rows)
    write(OUT / "analysis.json", report)
    write(OUT / "collection_receipt.json", {"attempts_sha256": digest(target),
          "analysis_sha256": digest(OUT / "analysis.json"), "freeze_sha256": digest(OUT / "freeze.json"),
          "attempts": len(rows), "retries": 0, "replacements": 0, "model_calls": 0, "paid_spend": 0})
    print(json.dumps(report, indent=2))
