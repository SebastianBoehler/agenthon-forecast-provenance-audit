## Executive summary (read this first)

**PASS for fresh-copy public-data preparation.** The frozen V1a protocol,
configuration and six scripts reproduced all 96 selected identities, native groups
and their order. Selection metadata, both blank reviewer sheets and the separate
unreviewed source-target file match the original recorded bytes and SHA-256 hashes.
All eight freshly fetched public artifacts match their pinned Git blob identities
and the original download hashes. No failed step, fallback or source edit occurred.

This run reused the recorded `.venv/bin/python` runtime, Python 3.13.2. It establishes
preparation reproducibility with a clean file copy. It is neither a new isolated
environment nor expert adjudication. Zero model calls, financial-answer
recomputations, defect labels and human reviews occurred.

## Scope and retained evidence

The clean root is
`outputs/finance-document-reproduction/fresh-v1a/`.
Its initial inventory contained exactly the eight frozen input files and no
finance-document outputs. Before copying, every input hash matched the original
`protocol_freeze_v1a.json`; the original and copied inputs still matched after the run.
No environment or dependency was created or installed.

The five declared commands ran sequentially: `prepare.py freeze`, `fetch`,
`inspect`, `select`, and `check.py`. All exited 0. Each command's arguments, working
directory, start/end times, standard output and standard error are retained in
`outputs/finance-document-reproduction/01-*` through `05-*`.

A separate 239-line metadata checker imported no preparation modules. It rebuilt
the admitted pools and deterministic selection from original input fields and the
declared TAT-QA answer-type metadata. It checked packet input identity and blank
rubrics independently of the copied `check.py`. Its source and machine-readable
result are local:

- [Independent metadata checker](/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/outputs/finance-document-reproduction/independent_metadata_check.py).
- [Comparison summary](/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/outputs/finance-document-reproduction/comparison_summary.json), SHA-256 `b4a99c9e0384ab6f63e1eaade5d015cc71888ea598c6b7981393836977346e83`.
- [Bootstrap inventory and runtime evidence](/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/outputs/finance-document-reproduction/bootstrap_metadata.json).

## Exact deterministic comparisons

Each original artifact first matched its recorded readiness hash. The fresh
artifact then matched both that hash and the original bytes. Source-target
comparison in the independent checker used bytes and hashes only; it did not parse
that file or judge any target. The declared packet checker checks target case and
question identity, with no financial evaluation.

| Artifact | Result | SHA-256 |
|---|---|---|
| `selection_metadata.jsonl` | Exact bytes, IDs, groups and order | `835eda81836f7b9aa67379d6d79d6adf4afcb443a989f48b6948403264f8ce93` |
| `reviewer_a.jsonl` | Exact bytes; 96 blank cases | `7cd3c12033bf97bd6fa4fc59277f06be01b83ee23d155a12b91bb1a7787553b0` |
| `reviewer_b.jsonl` | Exact bytes; 96 blank cases | `df7ae65ed9e2bcd5a7caaeaadd809d4889c13559fe3c5996ce2e6fd46ed427bc` |
| `source_targets.jsonl` | Exact bytes only; remains unreviewed | `6846b11caae406436bbc1e5d9417871710a4fce5140a48a7524a19fc74d77abe` |

The complete admitted-pool metadata also matched original bytes. The independent
reconstruction matched every selected metadata row, including all context,
question-context and order hashes. Reviewer A/B differ only in their reviewer
label. Every rubric has all ten declared fields empty and status
`blank_not_reviewed`. Every packet contains the original question and an exact
allowlisted projection of original context fields. Native annotations, retrieved
FinQA fields and source targets are absent from reviewer packet fields.

## Source identity and sampling checks

Pinned first-party releases were freshly retrieved at
[FinQA revision `0f16e286…`](https://github.com/czyssrs/FinQA/tree/0f16e2867befa6840783e58be38c9efb9229d742)
and [TAT-QA revision `870accc4…`](https://github.com/NExTplusplus/TAT-QA/tree/870accc41953dcde885aabeb963d94aabdc0fbc3).
For all four corpus files and four license/notice files, independently recomputed
Git blob hashes, SHA-256, byte lengths and revision-specific URLs match the frozen
configuration and original ingestion metadata. Full identities are in the
comparison summary; no remote floating branch or alternate source was used.

FinQA public/evaluator files contain the same 1,147 IDs and original questions,
tables and before/after text. All native filename/page identities agree. Their
complete file bytes differ, as previously recorded; answer values were not compared.

TAT-QA reproduces 278 raw contexts/1,669 questions and 277 annotation
contexts/1,663 questions. Context UID overlap and question UID overlap are both
zero. Exact original table, ordered paragraph-text and question identities join
1,626 questions, leaving 43 unmatched raw and 37 unmatched annotation identities.
Those identity differences were not evaluated as defects. Selection uses the
declared unique exact-content join and native annotation type, not numeric targets.

| Source | Eligible questions | Selected | Distinct selected native groups |
|---|---:|---:|---:|
| FinQA | 1,147 | 48 | 48 company/year report groups |
| TAT-QA | 723 | 48 | 48 raw context/table UIDs |

The source order is FinQA then TAT-QA. Independent hash sorting and duplicate
exclusion reproduced the seven FinQA and three TAT-QA group skips before each
48-case stop. TAT-QA selection contains 44 arithmetic and four count questions.
All selected exact contexts and question/context identities are unique. No
postselection balancing or correctness-based selection occurred.

## Prospective chronology

| Fresh event | UTC on 2026-09-29 |
|---|---|
| V1a freeze | 21:42:42.542712 |
| First through last source download | 21:42:50.085186–21:42:59.109649 |
| Schema/identity inspection | 21:43:28.592781 |
| Selection | 21:43:56.764228 |
| Declared preparation checks | 21:43:56.832082 |
| Independent metadata/byte checks | 21:53:34.434716 |

Fresh V1a freeze SHA-256 is
`4d95b8b661e89e5be39b3b571f113a7b87ff43bbb1d2e054d59a29011e71a064`.
It references the same eight input hashes as original V1a. Fresh timestamps and
freeze/manifest bytes naturally differ. This replay starts with the already
amended V1a inputs; it does not reconstruct the original V1-to-V1a schema-discovery
history or change the recorded fact that original V1a followed original inspection.

## Material limits and next gate

Preparation PASS supports conducting the planned blind review. It establishes no
answer correctness, defect frequency, native scoring validity, expert agreement,
training effect or RLVR-release coverage. Two blank sheets are preparation for two
reviews, not evidence that two independent reviews have occurred.

TAT-QA groups are contexts, not identified company/year reports. Cross-source
report disjointness and semantic near-duplicates remain unknown. Exact input
identity and unique selected groups do not establish those broader properties.
The native TAT-QA type filter intentionally uses annotation metadata; “no source
annotations used” would be inaccurate, while “no source numeric target or
correctness used for selection” is supported.

All fresh raw data, full packets and source targets remain under the repository's
ignored `outputs/` path and are local/excluded. Corpus redistribution remains
unresolved under the existing source notice ledger. This run changes no original
freeze, source, protocol, implementation, manuscript, collector or packager. The
next gate remains genuinely independent packet review and explicit adjudication
before comparing conclusions with released annotations and evaluator behavior.
