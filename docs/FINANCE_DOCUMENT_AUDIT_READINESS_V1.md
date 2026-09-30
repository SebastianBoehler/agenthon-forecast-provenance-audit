## Executive summary (read this first)

Blind preparation selected **96 unreviewed questions**: 48 FinQA questions from
48 native company/year report groups, and 48 TAT-QA questions from 48 native raw
context UIDs. Both targets were met. Two separate reviewer sheets contain original
questions/contexts and blank rubrics; source annotations remain in a separate local
file. No financial answer was recomputed, no defect labeled, no human review
completed and no model called.

This is admission for local review preparation, not permission to redistribute
corpora or packets and not completion of the main-track independent-audit gate.
FinQA/TAT-QA are independently described human annotation pipelines, not demonstrated
released RLVR reward implementations. FinChain was not instantiated.

This readiness report is unfrozen and its packaging/status wording was revised
after preparation. The historical readiness manifest retains its earlier report
hash. `reporting_checksums_v2.json` records the current report hash and checks the
unchanged eight V1a frozen inputs; no historical manifest or freeze is replaced.

## Prospective sequence and source identities

| Event | UTC timestamp | Evidence |
|---|---|---|
| Initial code/config/protocol freeze V1 | 2026-09-29 21:18:10.198552 | `protocol_freeze_v1.json` |
| First through last listed source download | 21:18:33.162962–21:18:41.294897 | `ingestion_manifest.json` |
| First source schema/identity inspection | 21:18:56.693147 | `schema_inventory.json` |
| Prospective identity amendment V1a | 21:24:55.004155 | `protocol_freeze_v1a.json` |
| Blind selection complete | 21:25:08.467149 | `selection_manifest.json` |
| Packet isolation/grouping checks | 21:25:26.000145 | `preparation_checks.json`, PASS |

The first freeze predates every corpus download. Its seven exact source files are
preserved under `protocol-history/v1/`. The amendment followed schema inspection
and preceded any selection. The amended protocol, configuration and six scripts
are frozen. Both freeze hashes and the download freeze reference remain recorded.

FinQA `dataset/test.json` and `code/evaluate/test.json` have different file bytes
but exactly the same 1,147 IDs, questions, tables and before/after text. The dataset
copy additionally contains retrieved table/text fields; those never enter packets
or selection. All 1,147 `filename` values equal the page part of the native ID.
Canonical input remains `dataset/test.json`. Original answer values were not compared.

TAT-QA raw test contains 278 contexts/1,669 questions; its public annotation file
contains 277/1,663. Native question and context UID overlap is zero. Therefore
the originally assumed native UID join could not work. V1a admits only unique
**exact original question plus table/ordered paragraph-text hashes**. It matches
272 contexts and 1,626 questions, excludes 43 raw identities without a counterpart,
and records 37 unmatched annotation identities. These are source-version identity
differences, not defect labels. Raw native UIDs identify packets/groups; annotation
UIDs remain in the separate targets. No fuzzy match or semantic rewrite occurred.

## Admitted pools and selection

| Source | Eligible questions | Eligible native groups | Selected | Selected grouping |
|---|---:|---:|---:|---|
| FinQA | 1,147 | 278 reports | 48 | One per company/year report group |
| TAT-QA | 723 | 271 contexts | 48 | One per raw table/context UID |

For TAT-QA, matched native types are 683 arithmetic, 40 count, 693 span and
210 multi-span. The 903 nonnumeric types were excluded under the frozen type rule;
43 unmatched raw identities were separately excluded. Selected types are
44 arithmetic and four count, with no postselection balancing. FinQA has no native
type filter; no gold program was used to classify its questions.

The frozen salt is `finance-document-audit-v1-2026-09-29-prospective`. Candidate order
uses SHA-256 of canonical JSON `[salt, source, native_id, question_context_hash]`,
then native ID. FinQA precedes TAT-QA. Seven FinQA and three TAT-QA candidates were
skipped for already selected native groups before their 48-case stop. No selection
decision uses source numeric targets, correctness, defect flags or actor outputs.

Question-first ordering with a one-per-group limit is not uniform sampling over
reports: larger eligible groups have more chances to appear early. Any eventual
unweighted defect fraction describes this selected set, not population prevalence.

Eligible FinQA has 380 exact contexts, 351 repeated-context groups and nine repeated
question/context groups. Eligible TAT-QA has 271 exact contexts and 268 repeated
context groups, with zero repeated question/context groups. No exact context or
question/context group crosses sources. All selected contexts/question-contexts
are unique, and selected native groups are unique within source.

TAT-QA has no report/company/year metadata in these raw contexts. Its 48 contexts
cannot be described as 48 reports, nor as report-disjoint from FinQA. Exact-string
comparison does not detect semantic near-duplicates, rewritten tables or shared
underlying reports. Public historical benchmarks may have been seen during model
pretraining; any future “unseen” claim must specify unseen by our adaptation process.

## Local artifacts and exact hashes

All data artifacts live under `outputs/finance-document-audit-v1/`, already ignored
by the repository. Full corpus downloads remain in `raw/` and are excluded from
release bundles. Scripts and provenance metadata can accompany the research artifact;
review packets and targets remain local. Source-specific MIT/CC BY notices
and unresolved inherited-data/older-noncommercial wording are recorded in the
configuration, ingestion manifest and source ledger. Redistribution remains unresolved.

| Artifact | SHA-256 |
|---|---|
| `protocol_freeze_v1.json` | `f87912dd9dfd333cd5a81a29e287eb098247f8eb2b914b774877af303c2781c1` |
| `protocol_freeze_v1a.json` | `68a0fd22de16c5c2aaae584f46176629bbea49327045097c358265f97abca378` |
| `ingestion_manifest.json` | `8c3c39b95bb6cf17c485775a4c8c061cb20abdbc62a5d605334951b2dc7aa778` |
| `schema_inventory_v1a.json` | `f8d93788a87058fbc1e10e1c3e59133d7b4d2ea63dc62cfb0303f5da47798890` |
| `selection_manifest.json` | `7d56d93f5087792f1e9488a6aba64fc4671c0929fb76a7326f3e59c72ef9e735` |
| `selection_metadata.jsonl` | `835eda81836f7b9aa67379d6d79d6adf4afcb443a989f48b6948403264f8ce93` |
| `reviewer_a.jsonl` | `7cd3c12033bf97bd6fa4fc59277f06be01b83ee23d155a12b91bb1a7787553b0` |
| `reviewer_b.jsonl` | `df7ae65ed9e2bcd5a7caaeaadd809d4889c13559fe3c5996ce2e6fd46ed427bc` |
| `source_targets.jsonl` | `6846b11caae406436bbc1e5d9417871710a4fce5140a48a7524a19fc74d77abe` |
| `preparation_checks.json` | `c2f30344c457d14eab9255db4e4e0198e6e2a4e044728ca715a310d2504a5284` |
| `metadata_identity_checks.json` | `6f0547cf4e9f738cb2214165d878a3e059b85d870befddd5f531f71fcf7d2459` |

Pinned corpus byte identities, independently checked against expected Git blobs:

| Corpus artifact | SHA-256 |
|---|---|
| FinQA canonical public test | `831dbfb2e785dbc227f895ce3f24046433467aec67b09db2bd6ac7692a8a30dc` |
| FinQA official evaluator test | `1a509efc61d87796728decfc405f053055214946f294de04578c237237155bad` |
| TAT-QA raw public test | `6efcf044cedeba3661eb70b1b93595673fd3f3dfcc1f78288ec5115682e7a96c` |
| TAT-QA public test annotations | `c4d08418359c1d76468dec420ee748a37f48c06b63cb8ec2766f19d5d314b597` |

`admitted_pool_metadata.jsonl` identifies all eligible cases and contexts without
question text or targets. `selection_metadata.jsonl` identifies the selected cases,
groups, input hashes and hash order. The two reviewer sheets have identical original
input content and empty rubric fields, with distinct reviewer labels. Original source
annotations are stored only in the separate targets file. PASS checks cover actual
source hashes, freeze/download chronology, unique selected groups/contexts, blank
rubrics, forbidden target-field isolation and question identity.

## Reproduce the declared V1a preparation

Use a clean local copy containing the protocol, configuration and six scripts,
with no existing `outputs/finance-document-audit-v1/`. Reuse the existing Python
runtime; no dependencies are installed. Run from that copy's root:

```bash
/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/.venv/bin/python scripts/finance_document_audit/prepare.py freeze
/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/.venv/bin/python scripts/finance_document_audit/prepare.py fetch
/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/.venv/bin/python scripts/finance_document_audit/prepare.py inspect
```

Review the resulting schema/identity report without inspecting answers for faults,
then run:

```bash
/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/.venv/bin/python scripts/finance_document_audit/prepare.py select
/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/.venv/bin/python scripts/finance_document_audit/check.py
```

Fresh timestamps/freezes/manifests differ by run; deterministic selected IDs,
`selection_metadata.jsonl`, packets and source-target bytes must match the hashes
above for these exact sources/code. The original current-run V1-to-V1a amendment
history is preserved rather than retroactively described as a pre-download V1a
freeze. Commands refuse existing outputs or altered frozen files.

## Remaining gate

The next work is genuinely independent review of these blank packets, followed
by explicit adjudication and only then comparison with released annotations and
native evaluator behavior. Current preparation supplies two candidate producers
and document tasks. It establishes no defect frequency, financial ground truth,
training consequence, RLVR-release breadth, novelty or expert agreement.
