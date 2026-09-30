## Executive summary (read this first)

The frozen Qwen3-4B extension adds a useful within-generation comparison with
Qwen3-1.7B. It holds the question panel, prompt, inference precision, runtime,
decoding, thinking setting and output budget constant. It does not isolate a
causal effect of parameter count because the released checkpoints can differ
in training. Keep the original 600-attempt panel, added 200-attempt extension and
combined 800-attempt presentation identifiable.

The strongest scientific ablations change the grader while holding every model
output fixed. Model-size and cross-family results are checkpoint comparisons.
The paper is an NLP-for-finance data and evaluation audit: language models read
financial questions and write answers; the study examines whether released labels
and explicit scoring rules credit those unchanged answers correctly.

## Frozen extension assessment

The [extension protocol](MODEL_GRADING_SIZE_EXTENSION.md) and
[manifest](../outputs/model-grading-v1/extension_manifest.json) identify
`Qwen/Qwen3-4B` revision `1cfa9a7208912126459214e8b04321603b3df60c`.
The extension was frozen at 2026-09-29 18:50:42 UTC after 188 Qwen3-1.7B and
200 DeepSeek responses existed, before any 4B financial response. The same selection
hash is retained. Review verified extension-document, wrapper, scorer and selection
hashes. No inference or manuscript edit was performed by this reviewer.

The wrapper adds the model to the original local engine in memory. It does not
replace earlier model specifications or change original frozen protocol/engine
files. The extension scorer checks full model/question coverage and supplementary
version-two hashes; combined outputs retain constituent-analysis hashes and reject
overlapping model keys. These are appropriate provenance controls.

Until execution completes, call 800 the planned combined number of attempts, not
800 observed successful responses. Treat the 4B run as an exploratory roster
extension motivated after earlier responses were available. Freezing before its
first answer preserves the added run's configuration; it does not retroactively
make the original experiment an initially preregistered four-model design.

## Comparison and causal boundaries

| Comparison | Held constant | Defensible interpretation |
|---|---|---|
| Qwen3-1.7B versus Qwen3-4B | Model generation, panel, prompt, FP16 MPS, greedy decoding, nonthinking mode, token cap | Paired comparison of released Qwen3 checkpoints of different sizes. |
| Qwen3 versus Qwen2.5-Coder-3B | Panel, prompt and local inference procedure | Robustness across released configurations; generation, specialization and size remain mixed. |
| Qwen versus DeepSeek endpoint | Panel, answer instructions, nominal token cap and scoring | Robustness across answer-producing configurations; family, capacity, training, runtime and precision differ. |
| Source comparator versus financial reference | Exact saved model answer and extraction | Exact grading intervention on this finite set under declared reference assumptions. |
| Strict versus numeric recovery | Exact saved response and financial comparator | Exploratory sensitivity to the extraction rule introduced by the experiment. |

Use “within-family checkpoint comparison” in the manuscript. Avoid “effect of
model size,” “code specialization improves financial reasoning,” “Chinese models
are better,” or an inference-latency comparison as evidence of a family advantage.
The comparison does not match training data, training compute or post-training.
The endpoint is agreement with declared numerical references, including the
binomial `1 + r` convention, rather than a certified assessment of every derivation.

Question pairing allows reporting exactly which outcomes differ between models.
It does not make the template questions independent population draws. Keep family
results primary and show strict completion/format counts beside numerical recovery.
A four-family equal-weight score remains specific to this purposively chosen panel.
Any ranking statement must specify the panel, extraction and comparator.

## Scientific ablations with existing evidence

Do not call model roster rows causal ablations. Use the existing audit component
comparisons and frozen model-output policies to isolate measurement choices:

| Component comparison | Scientific question | Interpretation limit |
|---|---|---|
| Source ±0.005, source ±0.5 and source 5% | Does tolerance widening rescue reference-valid answers, and which observed invalid answers does it credit? | Report false rejection and false acceptance separately; effects vary by family and candidate pool. |
| Formula-only versus formula plus requested projection | Does correctly computing the quantity suffice when the question requests an integer? | Existing Gordon controls identify the missing projection; the reference defines numerical validity. |
| Integer constraint plus source ±0.5 versus full reference | Does a simple baseline suffice for Gordon without recomputing its formula? | Its scientific application is Gordon only; success is bounded to the inspected inputs and tested answers. |
| Basic call-price bounds versus two valuation identities | Can a coarse structural check detect the source's wrong financial quantity? | All inspected source call labels pass the tested bounds; exact valuation exposes the wrong quantity. |
| Strict extraction versus post hoc numeric extraction | How much do format requirements hide otherwise measurable grading disagreement? | Recovery is exploratory and does not establish explicit-unit or complete response compliance. |

Keep source-authored rejected answers, rounded source-error controls and observed
model answers in separate rows or panels. They are different candidate pools.
Reference-generated targets accepted by their own checker remain consistency
checks. Actual model outputs supply empirical grading consequences. Zero reference
false acceptance is not general-validator accuracy when that reference defines
which candidates are invalid.

The simplest Gordon baseline should remain visible. An additional reviewer check
of adjacent integers in all 1,000 constructed-Gordon cases found no integer accepted
by source ±0.5 but rejected by the financial reference. This agrees with its success
on the existing tested controls. It does not make tolerance widening a general
solution to the separate binomial wrong-quantity error.

If an extra model-output component condition is desired, derive it from the saved
outputs, label it post hoc and retain the frozen primary policies. Do not alter
generation or rerun difficult responses to obtain cleaner ablations. The existing
component evidence is already enough to explain why Gordon and binomial need
different interventions.

## Plain-language NLP paragraph for the introduction

Suggested prose:

> This is an evaluation problem for language models. Each model reads a financial
> question and writes a calculation and a final answer. We keep that answer fixed
> and ask how different scoring rules grade it. If the released label names the
> wrong financial quantity, the grade can change even though the model's response
> has not changed. The study therefore evaluates the reliability of financial
> supervision and numerical scoring, rather than whether these data caused a model
> to learn an error.

If defining NLP explicitly is useful outside the specialist audience:

> Natural language processing studies how computers work with written or spoken
> language. Here, the language task is answering written financial questions with
> stated numerical inputs and rounding instructions.

No new architecture, fine-tuning method, retrieval system or learned correctness
judge is introduced. The numerical checks are independently specified financial
formulas. The study does not isolate language comprehension from arithmetic; no
text-only intervention is performed. Its NLP contribution is evidence about
financial question-answer supervision and measurement on actual model outputs.

## Title and manuscript integration

“When Verified Financial Labels Fail” is five words. It is concise and accurately
expresses the observed failure without claiming a new method or population rate.
Short-title citation studies cannot establish a causal acceptance benefit; the
title should be justified by accuracy and readability. No new title experiment or
additional literature search is needed to select this wording.

The currently inspected manuscript still describes the original three-model panel
in its abstract placeholder and model-method paragraph. Once complete results are
available, add one concise sentence identifying the separate 4B extension and its
timing, then report the original and added analyses transparently. Do not replace
the original roster's freeze history with a four-model history.

Use the existing source-coupling figure; no additional diagram is needed for this
extension. Keep manuscript work in the current native LaTeX editor and follow the
user's instruction against producing a separate compiled PDF. This review makes
no compilation or publication claim.
