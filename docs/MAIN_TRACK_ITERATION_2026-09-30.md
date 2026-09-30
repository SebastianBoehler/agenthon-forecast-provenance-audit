## Executive summary (read this first)

This iteration replaces an unexecuted document-extension proposal with a bounded,
prospective study on 48 FinQA and 48 TAT-QA questions. It strengthens external
evidence and the distinction between source defects and grading conventions.
It does not certify a main-track contribution or promise workshop/poster acceptance.
The canonical paper remains `paper/answer_contract_audit.tex`; existing scientific
records and the historical exploration graph remain unchanged.

## What a strong paper needs

The [NeurIPS 2026 reviewing guidelines](https://neurips.cc/Conferences/2026/ReviewerGuidelines)
assess technical support, clarity, significance and originality. A new model is
not mandatory: an empirical insight can qualify. A negative result still needs
explanatory depth and community relevance. Consequently, larger response counts,
cleaner figures or an unsuccessful training run do not by themselves raise this
paper to that standard.

The central question is whether released targets evaluate the financial quantity
specified by model-visible information. The synthetic study has a specific mechanism:
generator/verifier reuse can reproduce financing debt when the question requests
a call price, even while passing the tested price bounds. The document study asks
whether related problems persist outside manually generated formula templates.

## Research done in this iteration

1. Preserve the earlier draft/archive and freeze two answer-hidden technical reviews.
   Review every preselected question; retain ambiguous, missing-information,
   nonnumeric and disputed cases. These are AI technical reviews, not expert labels.
2. Lock both completed reviews and their numerical/broad-unit agreement before
   native answers are opened. Keep all original judgments and disclose later
   reconciliation, software mistakes and semantic disagreements separately.
3. Reproduce pinned TAT-QA answer/scale metrics and the explicitly adapted FinQA
   scalar endpoint. Validate them with authored representation and integrity controls.
4. Freeze a two-model, two-condition panel: DeepSeek V3.2/Qwen3.5-9B, original
   context only, baseline/label-free quantity reminder, one attempt per case.
   Keep provider failures, malformed JSON and abstentions in the 96-case arm denominator.
5. Separate source annotation errors, native representation choices and the
   unrounded-value instruction. Report native answer and scale channels individually;
   retain the later precision diagnostic as exploratory.
6. Check overlap against BizBench/FinanceReasoning. Prior repairs are corroboration,
   not new discoveries; absence of a matching released derivative is not proof of priority.
7. Keep raw local evidence and provide compact saved-score replay without paid
   inference. Full report contexts and original annotation dictionaries stay excluded.

The collection's toy-format preflight exposed a Qwen status error; shell sequencing
allowed the frozen run to continue. The deviation is recorded, and no prompt,
parser or response was repaired. A unit-parser substring mistake also created two
false disputes outside the original 62-case numerical subset. This error is retained
and separately corrected; it does not justify silently expanding the primary subset.

## Hennig-informed and Lu-informed assessment

These are hypothetical research lenses, not feedback from either professor.

The measurement lens asks what each reported number means. The 96-case cohort was
selected by question-first salted ordering and grouping, not a representative report
sample. TAT-QA report dependence is unknown. Two AI reviewers can agree on a value
and still miss semantic ambiguity. A strict unrounded answer may disagree with an
appropriate rounded target. These distinctions belong next to results, not only
in an appendix, and they preclude pooled independent-row prevalence intervals.

The contribution lens asks what a reader learns beyond existing label correction.
FinanceReasoning already corrects two concrete wrong-year cases rediscovered here.
The novel claim remains the source-traced synthetic mechanism and its bounded
grading consequences, with a document extension that tests its scope. The reminder
is a cheap diagnostic baseline, not a new optimizer. We must explain which
disagreements remain after faithful representation handling, and where the broad
failure hypothesis weakens. More datasets alone are not the contribution.

The posthoc calculation diagnostic exposes a concrete design issue: the reminder
permits assumption prose in a field the common instruction describes as a numeric
expression. Its lower executable coverage cannot establish worse arithmetic.
Status-only recovery separates Qwen format failure from numerical availability.
Executing saved expressions has direct Program-of-Thoughts precedent and remains
a selected-subset diagnostic, not method novelty or a demonstrated prompt benefit.

## Next gates toward a main-track submission

| Gate | Concrete success check | Why it matters |
|---|---|---|
| Expert semantic adjudication | A domain reviewer checks disputed signs, time periods, denominators and answer units without fitting the released label. Preserve disagreements. | Establishes which interpretations are defensible beyond correlated AI review. |
| Frozen procedure on held-out tasks | Develop rules on this discovery cohort, then evaluate unchanged rules on additional report/context groups or an independent task source. Include simple execution, normalization and tolerance baselines. | Tests transfer of an audit procedure rather than hand-corrected oracle consistency. |
| Consequential result | Demonstrate a practically important evaluation decision that survives source-correct controls, native conventions, rounding and uncertainty. Measure both error directions. | Establishes significance beyond another list of benchmark faults. |
| Learning claim, if pursued | Use coherent traces and matched initialization/data/compute in source-versus-repaired training; freeze held-out quantity tests and retain seeds/failures. | Required for causal training-harm or training-benefit claims. Not required for an empirical audit claim. |
| Reusable evidence resource | Release permission/notices resolved; compact artifacts, source acquisition, saved-score replay and per-case limitations independently checked. | Makes the contribution usable and auditable. |

The earlier GEPA pilot retained every seed prompt and failed its contribution gates.
Do not relabel it a positive adaptation result. Looped transformers, world models
and PufferLib RL need their own causal research question and controls; attaching
them to this audit would increase scope before resolving the present evidence gaps.
The next efficient experiment is the held-out procedure test, after semantic
reference quality and unit typing are fixed prospectively.

For that test, freeze an identical output contract across conditions with separate
assumption and executable-expression fields. Compare final-number output, execution,
representation normalization and the quantity check on the same complete attempt
roster. Keep uncertainty, schema failures and unsupported expressions explicit.
Use report/context groups excluded from this discovery analysis and derivative
provenance checks; known source repairs cannot count as novel held-out discoveries.

## Decision

Improve and retain the current submission as a bounded empirical paper. Use the
new completed study and negative controls to make the contribution harder to
misinterpret. Main-track readiness remains conditional on the significance,
transfer and reference-quality gates above. No external submission, professor
contact, public dataset release or acceptance assurance is implied.
