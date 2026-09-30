"""Executive summary: record direct DOI metadata checks separately from claim support."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path

from citation_assets import digest, write_json

ROOT = Path(__file__).resolve().parents[1]


def main():
    from citeproof.bibliography import BibEntry
    from citeproof.metadata import verify_entry_metadata
    from citeproof.metadata_providers import CrossrefProvider

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    catalog_path = ROOT / "literature/citations/source_catalog.json"
    catalog = json.loads(catalog_path.read_text())

    def check(source):
        entry = BibEntry(source["key"], "misc", {
            "title": source["title"], "year": str(source["year"]), "doi": source["doi"]})
        class RecordingCrossref(CrossrefProvider):
            def search(self, entry):
                records = super().search(entry)
                write_json(output / f"{entry.key}-provider.json", {
                    "provider": self.name, "requested_doi": entry.fields["doi"],
                    "captured_utc": datetime.now(timezone.utc).isoformat(),
                    "request_url": "https://api.crossref.org/works/" + entry.fields["doi"],
                    "records": [asdict(record) for record in records],
                    "scope": "CiteProof parsed publisher-deposited metadata; not source-text entailment",
                })
                return records
        result = verify_entry_metadata(entry, [RecordingCrossref(timeout=15)]).to_dict()
        result["full_author_list_compared"] = False
        return result

    eligible = [entry for entry in catalog["sources"] if entry.get("doi")]
    with ThreadPoolExecutor(max_workers=4) as pool:
        checks = list(pool.map(check, eligible))
    write_json(output / "checks.json", checks)
    write_json(output / "receipt.json", {
        "executive_summary": "Direct DOI identity diagnostics only. Missing/unmatched records do not alone prove fabricated references.",
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "catalog_sha256": digest(catalog_path.read_bytes()),
        "script_sha256": digest(Path(__file__).read_bytes()),
        "checked_doi_entries": len(checks), "source_text_support_certified": False,
        "output_sha256": {p.name: digest(p.read_bytes()) for p in sorted(output.glob("*.json"))},
    })
    print(json.dumps({"output": str(output), "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
