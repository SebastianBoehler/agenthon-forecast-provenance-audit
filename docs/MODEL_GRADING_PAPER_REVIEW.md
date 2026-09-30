## Executive summary (read this first)

The approved model-grading extension can materially strengthen this paper. Its
new claim should be **observed evaluation distortion on fixed model outputs**,
alongside the existing released-supervision audit. It does not establish causal
training harm or a new general verification method. The strongest opening is the
binomial generator's wrong financial quantity and its common computational error
with the published verification harness. Rounding and hidden precision are
supporting findings with direct prior art.

The frozen 200 distinct questions, four families and three identified model
configurations are adequate for a bounded workshop extension. Sampling, generation,
parsing and comparator policies were fixed before study responses. Score each
unchanged output against both source labels and independent visible-question
formulas. Report passing-family controls, failed attempts and paired grading
changes. Treat any model-ordering change as a result on this specific panel.

Updated after inspecting the frozen protocol and selection manifest: inference is
underway and no completed model-grading result file was present. This review assesses
the paper and actual design; it does not announce model results. No partial live
responses were inspected. No manuscript or implementation was edited.

## Frozen three-model design

The roster was fixed before study outputs: `Qwen/Qwen3-1.7B` at revision
`70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`,
`Qwen/Qwen2.5-Coder-3B-Instruct` at revision
`488639f1ff808d1d3d0ba301aef8c11461451ec5`, and OpenRouter's
`deepseek/deepseek-v3.2`, catalogue slug
`deepseek/deepseek-v3.2-20251201`, routed only to `siliconflow/fp8`.
Both local configurations use float16 MPS inference and greedy decoding; Qwen3 and
DeepSeek use nonthinking mode. All have the same question, output instructions and
1,024-token budget. The selection SHA256 is
`75c5b694db2d9a174e089c594e3f756867e0f840f12ac4634e5dc20173acf0cc`.
The [protocol](MODEL_GRADING_PROTOCOL_V1.md) and
[manifest](../outputs/model-grading-v1/selection_manifest.json) preserve the full settings.

This is a heterogeneous set of answer-producing configurations, not a controlled
model-size experiment. The [Qwen3 card](https://huggingface.co/Qwen/Qwen3-1.7B)
supports switching off thinking; the
[Qwen2.5-Coder card](https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct)
explicitly describes code specialization. Generation, model family, specialization,
precision and access path differ. The
[serving catalogue](https://openrouter.ai/deepseek/deepseek-v3.2) identifies available
providers, but a dated API identifier does not independently certify immutable
served weights. Preserve returned provider/model metadata. Three models improve
the number of observed configurations, not the scope of population claims.

## Material measurement limitation: strict and post hoc extraction

The [numeric amendment](MODEL_GRADING_AMENDMENT_NUMERIC.md) follows observed
unit-format failures. Its supplementary freeze is 2026-09-29 18:29:11 UTC, with
63 DeepSeek and 60 Qwen3 ledger records and no Coder study output; the
[freeze record](../outputs/model-grading-v1/numeric_sensitivity_freeze.json) retains
those snapshot hashes. These are disclosure counts, not completed-study results.
The original primary analysis and every response remain unchanged.

The strict parser measures an introduced formatting requirement as well as
numerical correctness. Rejecting `FINAL: 16` or `Final: 16 <unit>` does not establish
a financial calculation error. Parse failures receive no credit under either
grader, so they can mask a numerical grading disagreement. Report both all-attempt
scores and paired decisions among parsed-completed answers, with their distinct
denominators. Do not use the latter as an unqualified full-panel success rate.

The numeric sensitivity recovers only a last-line scalar with one final marker.
It is exploratory and post hoc, including for later families and Coder: observing
only part of the panel does not make the complete endpoint preregistered. Preserve
its absent/placeholder/explicit-unit categories and never convert a fraction into
percentage points. This endpoint does not establish full response compliance or
general numerical accuracy of unparseable responses. Both parsers still require
a final marker and completed generation. Any headline based on recovered answers
must name the exploratory sensitivity and retain the strict result nearby.

The initial supplementary parser accepted contradictory dollar/percent signals.
The [versioned correction](MODEL_GRADING_CORRECTION_UNITS.md) now rejects them;
synthetic checks reproduced the fix and all version-two freeze hashes agree. The
initial freeze and implementation snapshot are preserved, and primary code is
unchanged. Independent re-extraction should check that strictly accepted values
remain identical in the sensitivity and every policy grades the same scalar.

The completed DeepSeek slice has one convention mismatch: the model interprets
the binomial risk-free rate continuously, while the predeclared reference uses
one-period gross return `1 + r`. The question does not explicitly specify
compounding. Preserve frozen counts but describe reference-convention agreement,
not an unequivocal reasoning error. The source bond-as-call diagnosis remains
robust in this example under either convention. See the
[current first-page review](MODEL_GRADING_FIRST_PAGE_REVIEW.md) for slice counts.
The convention freeze followed 14 Coder binomial answers; see the separate
[timing correction](MODEL_GRADING_CONVENTION_TIMING_CORRECTION.md).

## Current evidence and what the extension adds

The executed audit already supports the following finite, family-specific claims:

- In 1,000 binomial-call rows, 975 source labels disagree with two equivalent
  financial valuation identities. All 1,000 match the positive bond-debt quantity
  calculated by the inspected public generator. The published verifier regenerates
  that same template, so a common computational mistake can be reproducible.
- In 1,000 constructed-response Gordon rows, 946 cent-level targets violate the
  requested whole-unit answer. A simple integer-plus-half-unit baseline solves the
  tested numerical conflict. No complex new repair is necessary for this family.
- The highlighted 627 preference pairs have an invalid chosen answer and an
  invalid rejected answer. They need a valid chosen replacement, not a reversal.
- Hidden-precision findings are conditional on interpreting displayed values as
  rounded. The corresponding numerical patch declares exact operands and therefore
  changes the task specification.

These conclusions agree with the strongest argument in the
[course-informed review](../outputs/course-review/DATA_LITERACY_AND_LU_REVIEW_2026-09-29.md):
reproducibility and measurement validity are different questions. That report's
anticipated feedback from Prof. Lu is an inference, not his endorsement or actual
review. It also correctly identifies actual model-output consequences as the
highest-value remaining empirical gap.

The extension adds a genuinely different measurement if ordinary models generate
answers first and those fixed answers receive different grades afterward. The
model's success under an independently justified financial specification is not
constructed by the correction algorithm. This avoids the particular tautology of
scoring a corrected target with the same rule that generated it. The reference
formula checker still defines numerical correctness; it is an oracle, not another
competing general validator.

## Contribution positioning against primary prior work

[FinanceReasoning](https://aclanthology.org/2025.acl-long.766.pdf), Section 2.1,
already repairs ambiguous questions, wrong labels and output units/precision.
[FinChain](https://aclanthology.org/2026.acl-long.662.pdf), Section 3.2 and
Appendix A.3, explicitly checks completeness, precision and displayed-versus-hidden
operand mismatches. [FinVerBench](https://arxiv.org/html/2605.29586v1), Sections
3.5 and 6.5, already studies observability and model-performance consequences of
financial rendering. Therefore neither label repair, answer contracts nor the
general claim that rendering changes measured performance is new.

The contribution is the new external evidence for these released training and
preference sources: a wrong financial quantity that survives generator-coupled
verification, independent attribution, and grading consequences on observed model
outputs. A model experiment strengthens relevance; it does not transform the
concept into a first-of-its-kind verification principle.

The binomial diagnosis is justified by Cox, Ross and Rubinstein's original
replication and risk-neutral valuation identities, rather than by model consensus.
[Original author paper, Section 3](https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/7/36891/files/2017/07/CRR79-1yy8av8.pdf).
The source-level mechanism is independently inspectable in the
[generator](https://github.com/btech-software/cosimo/blob/20668622104bf8237837efd67debd1419f7bbe33/dataset/pipelines/templates/cfa_l1.py#L441)
and [verification harness](https://github.com/btech-software/cosimo/blob/20668622104bf8237837efd67debd1419f7bbe33/dataset/verification/run_verify.py#L47).
The inspected Git revision remains separate from the pinned dataset revision;
do not assert that it is the exact generation commit.

## Necessary comparisons and controls

| Condition | What it establishes |
|---|---|
| Source numeric label, ±0.005 | A clearly reconstructed serialization-level grading baseline. It is not asserted to be the source's deployed model scorer. |
| Source numeric label, ±0.5 and 5% relative tolerance | Whether simpler tolerance widening fixes false rejection and what incorrect observed outputs it accepts. Retain both successes and failures. |
| Independent visible-input formula plus requested projection | Family-specific reference correctness, with two binomial valuation identities and exact integer instruction handling. |
| Gordon integer constraint plus source-label ±0.5 | The obvious successful cheap baseline; show it beside the complete numeric contract. |
| Ordinary Gordon and WACC, 50 questions each | Passing-label controls on the same generation/parsing/scoring pipeline. They help distinguish source-label effects from a generally broken evaluation path. |
| Simple call-price bounds | Existing structural diagnostic: source labels already pass these bounds. If applied to model outputs, it remains a coarse check rather than an independent valuation. |

The integer-plus-half-unit policy applies only to constructed Gordon. The current
scoring implementation emits it for all families; mark the other-family cells not
applicable and do not interpret its mixed-family aggregate as a competing grader.

The three models are answer-producing comparison systems. They need not be portrayed
as representative of all models or selected as a leaderboard. No new tool-use,
fine-tuning or expensive baseline campaign is necessary for the present question.

Use the same unit convention and numerical allowances when comparing grades.
Currency decoration and numerically equivalent strings are harmless. A percentage
versus fraction, sign error, omitted rounding instruction, or wrong financial
quantity is not harmless normalization. The source's cent serialization does not
prove that an unqualified question requests exactly two decimal places.

## Protocol obligations and execution checks

1. Choose 50 unique visible questions uniformly within each of `cr_eq_gordon`,
   `deriv_binomial_call`, `eq_gordon` and `corp_wacc` using a recorded selection rule.
   Preserve question IDs, source rows, question hashes and input revisions. If
   multiple source rows share one question, declare the representative-label rule.
   The four-family panel is purposive; sampling within it does not make the source
   selection representative of financial AI.
2. Record exact model identifiers, provider/access path, generation settings,
   prompt text and any response-format instruction. Each model sees only the
   visible question and common answer instructions, never gold labels, metadata,
   generator code, the manuscript or this review. Record tool access. A model
   evaluated inside a research agent's full conversation would be contaminated by
   the audit findings and cannot support ordinary answer-generation claims.
3. Save every attempt and immutable raw output. Obtain one completed answer per
   selected question/model under the fixed generation policy. Distinguish transient
   provider retry attempts from completed responses; do not regenerate inconvenient
   answers, choose the best response, or silently exclude failures.
4. Fix answer extraction before scoring. Prefer an explicit final-answer field
   rather than guessing which of several numbers is final. Preserve parse failures
   and raw text, report them per model/family, and count them in the full panel's
   denominator. A common-format request is an evaluation intervention and should
   be disclosed. Parse failure is distinct from a numerically wrong answer.
5. Grade each identical parsed answer under every prespecified comparator and the
   independent numerical reference. Preserve a row table with model, question,
   extracted value/unit, source grade, reference grade and reason for disagreement.
   Do not prompt models again for each grading condition.

The ordinary and constructed Gordon groups can be comparison families without
being a matched causal intervention. Unless their operands and questions are
paired except for the added rounding instruction, do not claim the model behavior
difference isolates that instruction. The paper can still measure each group's
grader disagreement without that stronger design.

## Reporting that makes the claim assessable

For each model, family and policy, report the fixed denominator, parse failures,
reference-correct answers, source-accepted answers, and this paired table:

| | Reference correct | Reference incorrect |
|---|---:|---:|
| Source accepts | Correctly credited | Source false acceptance |
| Source rejects | Source false rejection | Correctly rejected |

Call these decisions by their reference-relative meaning, rather than interpreting
any source/reference disagreement as model reasoning failure. Wrong derivations
with a correct final value remain numerically correct unless an independent trace
criterion is evaluated; the existing 34 projected-source collisions demonstrate
why a final-value checker cannot certify reasoning.

Report the source-versus-reference score difference and question IDs for key
disagreements. Make family results primary. A balanced-panel macro average weights
the four families equally and is not the score on the full dataset. If relative
model ordering changes, print both score pairs and describe the change on this
200-question panel. Do not infer a stable general ranking from three models and a
small purposely selected family set. Exact paired counts and effect sizes are
more useful here than field-wide confidence claims.

This panel excludes the hidden-input families, which helps keep its financial
reference explicit. DCF/CAPM ambiguity remains a supporting analysis. Mixing their
rounded and exact conventions into one headline correctness rate would weaken
interpretation. Results may be null: if the models produce no relevant valid
answers or policies agree, report that honestly and retain the independent source
audit as the paper's contribution.

## Suggested opening and abstract structure

Lead with this concrete example:

> A released finance question asks for a one-period call price. Its verified label
> is 45.28, while replication and risk-neutral valuation both give 12.72. The
> generator has computed bond financing rather than the call value. Its published
> verifier regenerates the same template, so the same computation mistake survives
> verification. The issue is which financial quantity is verified, not whether the
> program reproduces its own result.

Then explain why this matters for supervision and measured model scores. Introduce
the Gordon instruction conflict and conditional hidden precision only after the
principal mechanism is clear. The current manuscript instead opens with rounding
and DCF; shifting this order would strengthen significance without changing claims.

Use an abstract with four moves, filling model-result numbers only after execution:

1. **Problem:** generator agreement can verify the wrong requested financial
   quantity; concrete binomial case.
2. **Audit:** 12,655 selected public supervision rows; 975/1,000 binomial and
   946/1,000 whole-unit Gordon conflicts, plus passing comparison families and
   distinct conditional hidden-precision findings.
3. **Observed consequence:** three identified model configurations answer 200 distinct
   questions; unchanged responses receive the measured source/reference grading
   differences under declared reconstructed policies. Include the strongest actual
   effect size, not a placeholder assertion of ranking reversal.
4. **Scope:** source-level diagnosis, pinned artifacts and numerical patches;
   empirical grading consequences, no causal training claim or new general method.

## Likely reviewer objections and defensible answers

- **“This is only a bug report.”** The answer is systematic released-supervision
  evidence, two independent valuation identities, published common computational
  failure, passing-family controls and observed model-output grading consequences.
  Dataset popularity and deployment impact remain unestablished; do not invent them.
- **“The new verifier is an oracle.”** Correct. Its purpose is reference numerical
  adjudication for declared families. The new empirical measurement is grading
  unchanged model outputs; repair consistency is not learned-validator accuracy.
- **“These are invented scorers.”** The policies are reconstructed and explicitly
  labeled. The experiment demonstrates consequences under those policies, not a
  measured error rate of an unreproduced upstream training system.
- **“Rounding explains the whole result.”** It does not explain the debt-as-call
  error. The independent price identities and source attribution distinguish that
  mechanism. For Gordon, the cheap baseline is sufficient and should be retained.
- **“Three models and 200 questions are too small.”** They support a finite paired
  measurement on audited families. They do not support field prevalence, causal
  learning harm or universal rankings. The full corpus audit supplies complementary
  deterministic coverage; larger generated counts alone would not close those gaps.
- **“Who validated the assumptions?”** Separate rational arithmetic and source
  inspection validate technical calculations. They are not blinded human expert
  adjudication. Keep the model and human-author assistance disclosures accurate.

The extension is worth executing now for the stated workshop objective. Its best
scientific framing is a precise failure of generator-coupled verification with
observed evaluation consequences. No acceptance probability or professor approval
follows from this review. A results/manuscript rereview should check the immutable
response ledger, exact sample/model identifiers, paired counts, failure accounting
and whether the abstract's strongest claim matches what actually happened.
