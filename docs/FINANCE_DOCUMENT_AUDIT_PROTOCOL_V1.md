## Executive summary (read this first)

Prepare two independent document-finance audit candidates: 48 FinQA public-test
questions and 48 TAT-QA public-test arithmetic/count questions. Freeze eligibility,
sampling, code and the blank review rubric **before downloading or opening corpus
contents**. This is blind packet preparation, not an audit result, human review,
financial answer calculation or verified-RLVR experiment. FinChain is excluded.

Example: a selected report-table question appears with its original question,
table and surrounding text. Each reviewer receives empty fields for requested
quantity, evidence, units, precision and their independent answer/reasoning.
The source answer and derivation are stored in a separate local target file.

## Scope and pinned provenance

Use only the pinned first-party repositories and Git blob identities in
[source configuration](../experiments/finance_document_audit_sources_v1.json).
The [source ledger](MAIN_TRACK_SOURCE_LEDGER_2026-09-29.md) records official papers,
revisions, split/evaluator conventions and notices. FinQA and TAT-QA are distinct
human-annotation pipelines, not demonstrated released RLVR reward implementations.
Two admitted packet sources do not establish independent verifier defects.

FinQA canonical selection input is `dataset/test.json`; its official evaluator's
`code/evaluate/test.json` is downloaded solely to reconcile identities. Compare ID
sets, question/table/text and schema; never choose records by original target values
or require a target discrepancy to admit a case. Private challenge data is excluded.

TAT-QA input is raw public test plus its separately released public test annotations.
V1a joins unique exact original question-plus-context hashes, preserving both native
identities; it never fuzzy-matches or rewrites text. The only
annotation field available to the eligibility function is native `answer_type`.
Retain strict raw/gold context comparison and report UID joins in the manifest.

The initial schema assumption is FinQA list records with native report/page/example
ID, `qa.question`, `table`, `pre_text`, `post_text`; TAT-QA list contexts with
`table.uid`, `table.table`, ordered `paragraphs[].text` and `questions[].uid/question`.
Unrecognized schema fails visibly. A necessary material change must preserve its
freeze and receive a new prospective amendment/hash before any case selection.

### Prospective amendment V1a: changed TAT-QA identities

Initial V1 froze at 2026-09-29T21:18:10.198552 UTC before every download. Schema-only
inspection found raw 278 contexts/1,669 questions versus gold 277/1,663, with zero
native context/question UID overlap. Exact original table/ordered-text hashes match
272 contexts, and exact question/context hashes match 1,626 unique pairs. No answers
were computed, inspected for correctness or used for this identity comparison.

Preserve the initial freeze and all seven exact code/config/protocol files under
`outputs/finance-document-audit-v1/protocol-history/v1/`. Before selection, freeze
V1a code/config/protocol. Raw native UIDs remain the grouping and packet identities;
joined gold UIDs remain separately in the local annotations. Exclude unmatched
raw identities (43) because no exact annotation counterpart exists; record unmatched
gold identities (37). Do not infer defective labels from these version differences.
Native `answer_type` is read only for matched records. Eligibility/ranking/rubric,
source order and the 48-per-source target remain as prospectively declared.

## Frozen eligibility and selection

Eligibility uses only native identity, question, context and native TAT-QA type.
Require nonempty original questions and nonempty string-cell tables. Preserve
original strings and ordering without numerical rewriting. FinQA accepts all
public-test question types; there is no gold-program-based numeric filter.
TAT-QA accepts exactly native types `arithmetic` and `count`; report other counts.
No answer correctness, defect status, model answer or original gold value may enter
the selection function, ranking, replacement rule or exclusion decision.

FinQA native IDs must match company/year/page-PDF/example; group by company/year
report identity, at most one question per report. TAT-QA groups by native table/context
UID, at most one per context. Its report identity is initially unknown and must be
reported as unknown; context uniqueness is not a report-disjoint claim.

Compute SHA-256 of canonical UTF-8 JSON for table/ordered paragraph context, then
question-plus-context identity. Order candidates by SHA-256 of
`[salt, source, native_id, question_context_hash]`, with native ID as tie breaker.
Salt is fixed in configuration. Process FinQA then TAT-QA. Skip already selected
native groups and exact context/question-context duplicates across both sources.
Stop at 48 per source, or exhaust the eligible pool and report the actual shortfall.
Never resample for attractive defects, actor failures or difficult questions.

Record eligible counts, type exclusions, native grouping counts, exact duplicate
contexts and known report identities within/cross source. Do not infer report
disjointness from an absence of exact text matches. No semantic near-duplicate,
PDF retrieval or report/company matching occurs in this stage. No comparison to
old synthetic financial operand tuples establishes document-task independence.

## Blank independent review packets

Produce identical question sets for reviewers A and B in separate JSONL sheets.
Each contains original question/table/text and the configured blank rubric:
requested quantity; supporting evidence locations; visible inputs/units;
information sufficiency; ambiguity/assumptions; requested precision; acceptable
answer set/units; independent reasoning trace; confidence; notes.

Keep FinQA text before/after the table distinct. Keep native TAT-QA paragraph UIDs
and order with their original text. Context hashes use table plus ordered text in
a shared representation; reviewer presentation preserves the native layout.
Do not include source answers, derivations, programs, supporting-fact annotations,
answer type/scale metadata, calculated results, proposed defects or score hints.
Native IDs identify cases but no answer annotation is forwarded. Blank sheets are
not evidence of review. Future reviewers work independently before seeing source
targets or each other's sheets. Qualified human financial review remains required
before claiming expert adjudication; no reviewer is contacted in this stage.

Keep complete selected source annotations separately in local `source_targets.jsonl`.
They are unreviewed annotations. No execution, equation evaluation, labeling,
adjudication, inference or training occurs now.

## Files, timing and admission gates

`outputs/` is already Git-ignored. Full corpus files and notices live only under
`outputs/finance-document-audit-v1/raw/`; raw corpora, targets and review sheets
remain excluded from publication bundles. This task does not edit any packager.
Source targets are public benchmark annotations, not private scoring outcomes.

First syntax-check only the new scripts. `prepare.py freeze` records UTC time and
SHA-256 of this protocol, configuration and every script, before any raw directory
exists. For the current run initial V1 remains immutable; `amend` freezes V1a before
selection after preserving exact initial bytes. A fresh reproduction can freeze
the already declared V1a protocol before its own downloads. `fetch` verifies the active freeze, downloads only the pinned listed files,
verifies Git blob SHA-1 and saves SHA-256/bytes/UTC timestamps. `inspect` records
identity/schema checks without selecting. V1a writes a separate schema/identity
report, preserving V1 inspection. Inspect that report before `select`.
Every step refuses overwrite or silently changed protocol/code.

FinQA repository MIT does not resolve all inherited FinTabNet/report-content
notices. TAT-QA code MIT and current dataset CC BY 4.0 remain distinct; preserve its
older noncommercial wording discrepancy. Archive exact notices locally and expose
these unresolved redistribution fields in the manifest. Download/preparation does
not declare permission to redistribute any corpus or derivative packet.

Success check: prospective freeze predates every source download; exact pinned
source hashes and UID/context identities are recorded; deterministic selection
obeys native grouping and avoids selected exact context duplicates; two blank
gold-free sheets and a separate unreviewed source-target file exist; actual counts
and unknown report identities are explicit. No models, defects or human reviews
are represented as completed. This prepares the roadmap's later independent audit
and held-out task stages without claiming their breadth/novelty gates have passed.
