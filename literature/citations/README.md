## Executive summary (read this first)

The current submission draft has 23 cited bibliography keys. Its local CiteProof workspace links cited claims to saved primary-source snapshots and exact excerpt locations. Text identity, bibliographic identity and claim support are separate checks. No automated label certifies the paper. The fuller historical research draft has 34 keys; its preserved runs are described below.

### Current submission source

The current manuscript is `paper/answer_contract_voice_draft.tex`, with its declared
sources in `literature/citations/voice_source_catalog.json`. Source PDFs, downloaded
texts, and generated excerpt workspaces are local and gitignored. Links to `outputs/`
below refer to those local review records, not bundled public files.

After installing the repository's `citations` extra, generate a new review workspace:

```bash
.venv/bin/python scripts/citation_voice.py --fetch
.venv/bin/python scripts/citation_voice.py --check-run outputs/citation-workspace/RUN_DIRECTORY
```

Replace `RUN_DIRECTORY` with the directory reported by the first command. Exact
excerpt checks locate text; the author must assess whether it supports the cited
claim. The historical workspaces below are not certified against this newer draft.

### Current revision and original review workspace

The current immutable run is [run-final-finchain-v1-20260930](../../outputs/citation-workspace/run-final-finchain-v1-20260930/), bound to the revised draft with the local grader comparison and independent FinChain-code bank. It covers **34 keys, 41 citation commands, 37 parsed claims and 175 exact saved-extraction excerpts**, with no uncovered citation command. There are 32 available cited sources; AQER and Knight/Leveson remain unavailable to this source-text integration. All author semantic-review decisions remain pending. Current heuristic flags are 19 unsupported, five contradicted, 12 partially supported and one uncertain; these are retrieval/review cues, not final claim verdicts.

The following details describe the original 29-key historical run; its revision check intentionally fails after the manuscript/catalog changes. The original run is preserved rather than overwritten.

The immutable local run is [run-20260930T135605Z](../../outputs/citation-workspace/run-20260930T135605Z/). Open [citeproof.html](../../outputs/citation-workspace/run-20260930T135605Z/citeproof.html) to inspect the draft and retrieval flags. The machine-readable evidence is:

| File | Purpose |
| --- | --- |
| `claims.json` | 33 parsed claim units, exact draft contexts, character intervals, line locations and fingerprints |
| `citation_occurrences.json` | All 36 citation commands, including cited table cells and appendices; none uncovered |
| `source_manifest.json` | Explicit key-to-source mapping, source version/access scope, retrieval failures and snapshot hashes |
| `excerpt_ledger.jsonl` | 155 contiguous saved-text excerpts with physical PDF page, character interval, source/page/excerpt hashes and duplicate-match count |
| `receipt.json` | Draft, catalog, CiteProof and wrapper code identities, dependency versions and output hashes |
| `summary.json` | Coverage and limits; all author-review decisions remain pending |

27 cited source assets were available. Four additional background candidates are saved but are not inserted into the manuscript merely to increase its reference count. Available assets include dataset cards, code, an abstract-only record and author preprints; this is not 27 publisher-final papers read in full. Raw source and page-extraction snapshots are retained under the run directory. PDFs and generated outputs remain gitignored.

### Run and recheck

Run from the research repository. These commands use the user's existing CiteProof installation; no hosted model, new installation or paid inference is involved.

```bash
/Users/sebastianboehler/Documents/GitHub/citeproof/.venv/bin/python scripts/audit_paper_citations.py --fetch
/Users/sebastianboehler/Documents/GitHub/citeproof/.venv/bin/python scripts/audit_paper_citations.py --check-run outputs/citation-workspace/run-final-finchain-v1-20260930
/Users/sebastianboehler/Documents/GitHub/citeproof/.venv/bin/python -m unittest discover -s tests -p test_citation_workspace.py
```

`--fetch` acquires only explicitly declared missing assets, with no retry or alternative-source fallback. Omitting it uses existing declared local assets/cache. A run creates a new directory and refuses to overwrite an existing run. After draft, catalog or recorded implementation changes, create a new run and use its directory in `--check-run`. Historical runs keep their historical evidence; the current-revision check intentionally rejects them after a draft change.

The original check passes all 155 historical excerpt bindings; the current revision passes 175. Eleven authored adversarial controls pass, including altered numbers, fabricated quotes, joined disjoint passages, shifted offsets, wrong source keys, stale drafts, Unicode/whitespace and blank PDF pages. Matching normalizes whitespace only, then records the exact raw extraction slice. Offsets refer to saved extracted page text, not original PDF byte positions. PDF extraction can lose layout and join words; consult the physical page when meaning or layout matters.

### What CiteProof has and has not checked

This integration uses CiteProof's citation-scoped lexical retrieval and deterministic verifier, not an LLM adjudicator. Its original 29-key flags are 16 unsupported, five contradicted, 11 partially supported and one uncertain. They are review cues. Five apparent contradiction flags were inspected and involve retrieval, badge parsing or reference-list collisions; see [manual triage](../../docs/CITATION_BASE_REVIEW_2026-09-30.md). We preserve the original flags instead of relabeling the report to appear successful.

Exact excerpt matching proves that saved quoted characters occur in the recorded source. It does not prove that the source supports the full claim, that the source itself is correct, or that an author's own result came from that paper. Original experiment claims need the existing experiment ledger and independent numerical replay, while literature claims need a supporting passage from the cited work.

`alignment_only.bib` is a derived key/title/year/URL sidecar for CiteProof syntax and source alignment. The inline manuscript bibliography remains authoritative for drafting. Neither the sidecar nor syntax success validates complete author lists, venue identity or publication status.

The separate [metadata run](../../outputs/citation-workspace/metadata-20260930-v1/) checked 16 declared DOIs using CiteProof's Crossref provider: ten title/year/DOI matches and six HTTP 429 errors. Full author lists were not compared. Rate limiting is an access failure, not evidence of a fabricated reference. Publisher-final text must not be implied when only an author preprint was read.

### Explicit access gaps

- `aqer`: direct publisher retrieval returned HTTP 403. The user's EBSCO library record was found (Business Source Ultimate, accession 194875278; DOI 10.1287/isre.2023.0426), with full HTML availability. Its displayed AI-use restriction means that HTML is not imported into this citation corpus. The automatic source-text check remains incomplete.
- `independence`: the author-hosted PDF timed out. The direct DOI metadata matches, but no new full-text excerpt was acquired in this run.
- `faircheap`: the accessible abstract/public record is saved; the reader-gated manuscript remains unread. Claims about exact experimental overlap must remain unresolved.

### Section-by-section co-drafting

1. Start with the author's spoken notes and the section's intended claim.
2. Identify which statements are literature, our measurements, interpretation, or future work. Split mixed claims when one citation cannot support the whole sentence.
3. Open the saved excerpt and surrounding source page; check wording, context, version and qualifications. For our measurements, use the existing claim/evidence graph and numerical ledgers.
4. Record a human review decision separately from immutable automated output. Retain uncertainty where evidence is incomplete.
5. Edit the current `paper/answer_contract_voice_draft.tex`, rerun citation extraction for its new revision, and check it with the native LaTeX compiler. The fuller research draft retains its own historical review records.

The supporting [contribution review](../../docs/CITATION_CONTRIBUTION_REVIEW_2026-09-30.md) identifies prior art and bounded novelty. The [fresh numerical audit](../../docs/SCIENTIFIC_BASE_AUDIT_2026-09-30.md) records reproduced core counts and experimental-unit limits. Both are review evidence rather than actual professor or organizer feedback.

### Recent discovery leads

Grok/X are used to discover leads; the reports follow them to primary papers. The following records began as leads outside the original 29-key manuscript catalog. Verifier Errors and RecursiveMAS now have bounded citations in the current draft; their source/version limits remain explicit:

- [Three recent financial-evaluation papers](../../docs/RECENT_FINANCIAL_EVALUATION_REVIEW_2026-09-30.md): separate statistical refereeing, paper-based security ratings and reasoning cost from our financial QA findings. Their [v2 local review snapshot](../../outputs/citation-workspace/recent-financial-20260930-v2/) binds all three short quotations to exact PDF slices. The earlier v1 retains a failed line-hyphen match instead of hiding it.
- [Verifier Errors in RLVR](../../docs/RECENT_RLVR_VERIFIER_REVIEW_2026-09-30.md): a close under-review preprint whose main analysis assumes no false negatives; relevant to the distinction between false credits and observed denials of valid answers.
- [Post-Audit Mirage](../../docs/POST_AUDIT_MIRAGE_REVIEW_2026-09-30.md): a public author artifact about missing deployment information, with an author-announced workshop poster. Official acceptance and artifact execution were not verified.
- [RecursiveMAS](../../docs/RECURSIVEMAS_RELEVANCE_REVIEW_2026-09-30.md): official NeurIPS 2026 poster listing confirmed. Eight authored MATH500 controls give a separately replayable current-code scoring diagnostic; four unequal numeric pairs are credited by the extracted native scoring statements. This does not establish historical evaluator equivalence, real benchmark-score effects or financial performance. Replay with `python3 scripts/validate_recursivemas_authored_controls.py`; source fragments and receipts are in `outputs/recursivemas-code-review-v1/`.

The revised current LaTeX source compiled successfully with the native editor on September 30. The preserved historical claim/evidence graph passes 117 evidence-file checks and 58 recorded-value checks; that graph check establishes integrity and recorded-value agreement, not financial truth or coverage of later extensions. Its receipt is [current-artifact-integrity-20260930.json](../../outputs/citation-workspace/current-artifact-integrity-20260930.json). Later scalar and FinChain banks carry separate source/freeze/collection manifests and replay commands.
