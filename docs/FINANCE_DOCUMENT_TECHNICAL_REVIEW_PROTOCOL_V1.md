## Executive summary (read this first)

Complete an answer-hidden, AI-assisted technical review of the 96 previously
selected FinQA/TAT-QA questions, then compare the locked reviews with the released
annotations and pinned official evaluator behavior. This extension tests whether
the synthetic-release explanation transfers to independently annotated financial
documents. It is not human expert review, a population prevalence study, or a
new RLVR training-release audit. A passing or inconclusive result is retained.

For example, reviewers independently identify a requested return, its beginning
and ending values, its denominator and units from the original document. They
record the calculation and any defensible alternatives before seeing the native
answer or program. Comparing only their final numbers would miss semantic and
unit ambiguity, so the evidence references and assumptions remain explicit.

## Existing selection and chronology

Use exactly the 96 cases selected under
[the preparation protocol](FINANCE_DOCUMENT_AUDIT_PROTOCOL_V1.md): 48 FinQA
questions from distinct company/year groups and 48 TAT-QA questions from distinct
native contexts. Preserve the original eight frozen inputs, selection metadata,
blank packets and source targets. No resampling, answer-based exclusions or
replacement of difficult questions is allowed. Existing native-type eligibility
and the exact-context annotation join retain their disclosed V1a amendment.

The preparation freeze preceded downloads and selection. This is a later review
stage declaration, not retrospective preregistration of the earlier exploratory
study. Before this stage was declared, the coordinating agent inspected the first
and last blank packet's layout and visible content; it has not read the separate
source targets. That inspection does not change the existing selected identities.

## Independent technical review

Two AI agents review the full question-first packets separately. Each reads only
its assigned blank packet and this protocol; neither sees source targets, native
programs, supporting-fact annotations, model answers, or the other agent's work.
Public benchmark pretraining exposure cannot be ruled out. The agents share an
underlying model family; their agreement is technical corroboration, not independent
human judgments or a quantified independent error probability.

Each reviewer writes one JSON object per original case to a new, local output:
`outputs/finance-document-review-v1/review_a.jsonl` or `review_b.jsonl`.
Required fields:

- `case_id`, `reviewer`, `review_status` (`determinate`, `conditional`,
  `insufficient_information`, or `unresolved`);
- `requested_quantity`, `evidence` with original table row/column or paragraph
  references, `operands` including signs and units;
- `expression` with a reproducible arithmetic expression over cited operands;
  multiple explicitly named expressions if the visible question supports alternatives;
- `answer_values` as decimal strings and `answer_unit`, including scale;
- `requested_precision`, `rounding_policy`, `assumptions`, `alternative_interpretations`,
  `confidence` (`high`, `medium`, `low`) and `notes`.

Use zero-based table row/column indices and distinguish before/after text or native
paragraph order. Use local Decimal or rational arithmetic for nontrivial calculations.
Parentheses indicate negative amounts when the document uses that convention.
Record percent versus percentage-point changes, relative versus absolute changes,
currency scale and time horizon explicitly. Do not silently replace missing facts,
assume every printed input is uncertain, or label a natural rounding discrepancy
as an unconditional arithmetic error. Absent output precision is a recorded absence,
not permission to fit the native target later. Keep unresolved cases in the denominator.

Review outputs contain IDs, independently derived calculations and minimal evidence
references; do not copy entire contexts. Each agent records a completion receipt
with its packet, protocol and output hashes, case count, technical-review role and
disclosure that no native targets or other review were accessed. The coordinator
hash-locks both reviews before reading target annotations. Do not overwrite reviews.

## Adjudication and comparison sequence

1. Validate complete case coverage, identity, required fields and arithmetic
   consistency. Retain exceptions and explicit unresolved decisions.
2. Compare the two locked answer sets and semantic interpretations without targets.
   Record disagreements and any third technical adjudication with its own rationale.
   Lock the resulting pre-target review record; do not call it expert ground truth.
3. Open the native targets only after those locks. Compare source answer, program,
   derivation, scale and rounding conventions. A newly discovered defensible reading
   is recorded as post-unblinding reconciliation, not a preexisting reviewer decision.
4. Inspect the pinned official evaluator and evaluate only where its native schema
   and source conventions are faithfully implemented. Keep arithmetic identity,
   semantic judgment and grader normalization distinct. Never execute arbitrary
   annotation text as Python or import an uninspected upstream application.
5. Freeze any model-answer experiment separately before collecting its outputs.
   Give models only the same original visible contexts and questions. Grading
   disagreements are paired on unchanged answers, with parsing and failure counts.

## Endpoints, controls and falsifiers

Primary descriptive endpoints are complete technical-review coverage, pre-target
agreement by source, and native-answer compatibility on agreed determinate cases.
Report all 48 cases per source and every disagreement/unresolved case separately.
The agreed-case conditional denominator must never replace the full 48/96 count.
No binomial confidence interval over pooled questions or unweighted population
defect prevalence is justified by this mechanism-driven selected set.

Classify post-target comparisons into compatible, definite contradiction under
the locked reading, rounding/representation difference, alternative-reading
compatible, insufficient-information, and unresolved. Distinguish a wrong requested
quantity from a wrong arithmetic operation, wrong unit/scale, evaluator normalization,
and ambiguous wording. A shared conceptual mistake remains possible despite arithmetic
agreement; definite semantic-fault claims require explicit evidence and limitations.

Passing cases are substantive controls. If annotations match the independently
reviewed quantity and only precision/representation accounts for differences, retain
that result and narrow the synthetic-release explanation. If disagreements are
dominated by missing context or technical-review uncertainty, this extension is
inconclusive; do not manufacture a defect census. FinQA/TAT-QA add independently
produced document tasks, not proof of independent realized verifier defects.

Nearest work already studies financial ambiguity, precision and benchmark repair.
An extension supports a stronger contribution only if it yields a transferable
mechanistic explanation or an independently tested distinction beyond merely adding
more datasets. Any new proposed method needs simpler baselines and held-out-source
testing. This review alone establishes neither training harm nor main-track readiness.

## Reproducibility and release boundary

The stage freeze records this protocol, original packet hashes and selected identity
metadata before completed review files exist. Saved reviews, receipts and comparison
code use a separate output directory. The old manuscript and package are preserved
until evidence warrants revision. Source corpora, full packets, native target files
and private teaching material remain local and excluded from public packages.
Licensing notices and unresolved inherited-content permissions retain their prior
status. No sealed competition material, contact, public release or submission occurs.
