"""Executive summary: build a revision-bound CiteProof review workspace with exact excerpt checks."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import importlib.metadata
import inspect
import json
from pathlib import Path

from citation_assets import digest, snapshot, write_json
from citation_draft import audit_bib, inventory
from citation_evidence import bind_evidence, check_run, loaded_sources

ROOT = Path(__file__).resolve().parents[1]
DRAFT = "paper/answer_contract_audit.tex"
CATALOG = "literature/citations/source_catalog.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="Acquire only explicitly declared missing primary sources")
    parser.add_argument("--output", type=Path, help="New local run directory; existing runs are never replaced")
    parser.add_argument("--check-run", type=Path, help="Check saved draft/source/code/excerpt identities; no retrieval")
    args = parser.parse_args()
    if args.check_run:
        print(json.dumps(check_run(ROOT, args.check_run.resolve()), indent=2))
        return
    from citeproof.bibliography import verify_bibliography
    from citeproof.dashboard import paper_report_to_html
    from citeproof.models import Claim
    from citeproof.paper import PaperVerificationReport, render_paper_report
    from citeproof.sources import build_chunks
    from citeproof.verifier import verify_claim
    import citeproof

    started = datetime.now(timezone.utc)
    output = (args.output or ROOT / "outputs/citation-workspace" / started.strftime("run-%Y%m%dT%H%M%SZ")).resolve()
    output.mkdir(parents=True, exist_ok=False)
    catalog = json.loads((ROOT / CATALOG).read_text())
    claims, occurrences = inventory(ROOT / DRAFT)
    cited = {key for occurrence in occurrences for key in occurrence["citation_keys"]}
    entries = catalog["sources"]
    declared = {entry["key"] for entry in entries if not entry.get("candidate")}
    if cited != declared:
        raise ValueError(f"Update catalog to match cited keys: {cited ^ declared}")
    (output / "alignment_only.bib").write_text(audit_bib(entries, cited))
    write_json(output / "claims.json", claims)
    write_json(output / "citation_occurrences.json", occurrences)
    # Every worker has a separate source key/cache/output path; no request retries.
    with ThreadPoolExecutor(max_workers=4) as pool:
        manifest = list(pool.map(lambda entry: snapshot(ROOT, entry, output, args.fetch), entries))
    write_json(output / "source_manifest.json", manifest)
    sources, lookup = loaded_sources(manifest, output)
    chunks = build_chunks(sources)
    results, excerpt_records = [], []
    for claim in claims:
        verified = verify_claim(Claim(claim["claim"], tuple(claim["citation_keys"])), chunks).to_dict()
        verified["claim_id"] = claim["claim_id"]
        verified["author_review_status"] = "pending"
        results.append(verified)
        for index, evidence in enumerate(verified["evidence"]):
            excerpt_records.append(dict(claim_id=claim["claim_id"], evidence_index=index,
                                        automated_label=verified["label"], **bind_evidence(evidence, lookup)))
    with (output / "excerpt_ledger.jsonl").open("x") as stream:
        for record in excerpt_records:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
    bibliography = verify_bibliography(ROOT / DRAFT, output / "alignment_only.bib").to_dict()
    report = PaperVerificationReport(bibliography, results, len({s.citation_key for s in sources}), len(sources))
    (output / "citeproof.json").write_text(report.to_json() + "\n")
    (output / "citeproof.md").write_text(render_paper_report(report))
    html = paper_report_to_html(report, source_text=(ROOT / DRAFT).read_text())
    notice = ('<aside style="padding:1em;background:#fff0c2">Draft review only. '
              'Automated labels are not certification. Exact excerpt locations are saved in excerpt_ledger.jsonl. '
              'Sources have differing access/version scopes. All claims await author review.</aside>')
    (output / "citeproof.html").write_text(html.replace("<body>", "<body>" + notice, 1))
    summary = {
        "executive_summary": "Citation-scoped retrieval and exact saved-text locations for co-drafting; no whole-paper truth claim.",
        "citation_keys": len(cited), "citation_occurrences": len(occurrences), "parsed_claims": len(claims),
        "uncovered_citation_occurrences": sum(not x["parser_covers_keys"] for x in occurrences),
        "available_cited_sources": sum(x["status"] == "available" and x["key"] in cited for x in manifest),
        "unavailable_sources": [{"key": x["key"], "error": x.get("error")} for x in manifest if x["status"] != "available"],
        "optional_candidate_sources": [x["key"] for x in manifest if x.get("candidate")],
        "automated_labels": dict(Counter(x["label"] for x in results)),
        "excerpt_integrity": dict(Counter(x["integrity"] for x in excerpt_records)),
        "bibliography_syntax_errors": bibliography["error_count"],
        "bibliography_note": "Alignment-only sidecar; full author/venue/year/DOI identity needs primary metadata review.",
        "all_claims_require_author_review": True, "expert_adjudication": False,
        "hosted_model_calls": 0, "paid_inference_usd": 0,
    }
    write_json(output / "summary.json", summary)
    own_code = [Path(__file__).resolve(), *sorted(Path(__file__).parent.glob("citation_*.py"))]
    citeproof_root = Path(inspect.getfile(citeproof)).parent
    code = own_code + sorted(citeproof_root.rglob("*.py"))
    receipt = {
        "executive_summary": "Frozen local citation run: hashes establish identity and excerpt integrity, not semantic truth.",
        "started_utc": started.isoformat(), "completed_utc": datetime.now(timezone.utc).isoformat(),
        "draft": DRAFT, "draft_sha256": digest((ROOT / DRAFT).read_bytes()),
        "catalog": CATALOG, "catalog_sha256": digest((ROOT / CATALOG).read_bytes()),
        "citeproof_version": importlib.metadata.version("citeproof"),
        "pypdf_version": importlib.metadata.version("pypdf"),
        "retrieval": "CiteProof lexical citation-scoped retrieval", "verifier": "CiteProof deterministic heuristic",
        "physical_pdf_blank_pages_preserved": True,
        "code_sha256": {str(p): digest(p.read_bytes()) for p in code},
        "output_sha256": {str(p.relative_to(output)): digest(p.read_bytes()) for p in sorted(output.rglob("*")) if p.is_file()},
        "public_release": False, "manuscript_edited": False,
    }
    write_json(output / "receipt.json", receipt)
    print(json.dumps({"output": str(output), **summary, "integrity_check": check_run(ROOT, output)}, indent=2))


if __name__ == "__main__":
    main()
