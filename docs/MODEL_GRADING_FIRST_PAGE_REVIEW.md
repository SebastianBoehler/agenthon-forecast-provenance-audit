## Executive summary (read this first)

The revised binomial-first introduction and source-coupling diagram express the
paper's strongest finding. The model methods clearly retain frozen strict parsing,
unchanged outputs and explicitly post hoc numeric recovery. The current abstract
now also has the binomial-first emphasis and precise training-effect limitation.
The completed DeepSeek slice demonstrates paired grading distortion under the
strict parser as well as supplementary recovery; the full panel is still running.

This review inspected manuscript SHA256
`bc07dcfbdb2db855593b8460f45e4ff146def3499bc740c43f8c331c06afb404`,
the versioned supplementary correction and the 200 saved DeepSeek responses. No
manuscript, protocol, response or implementation was edited. Line references are
to that inspected source. The existing exported PDF lacks the new diagram, so
the new figure's visual placement and fit were unverified at that earlier review.

## Current source assessment after the timing correction

The later source SHA256
`fac88ce3030e148ae3bb601b7bd882e9d0f774c49d8baee42280516cf7a4f895`
resolves the original recommendations on abstract order, training-effect wording,
near-example citations and the figure's metadata label. The new plain-language
NLP explanation is accurate. Methods now distinguish strict final-line compliance
from all system instructions and describe the matched Qwen3 extension without a
causal parameter-count claim. The earlier line-specific recommendations below are
historical observations, not unresolved defects in this later source.

The convention timing is correctly recorded in this source: 19:03 UTC followed
64 Coder answers, including 14 binomial answers, and preceded all 4B responses.
See the [timing correction](MODEL_GRADING_CONVENTION_TIMING_CORRECTION.md).
The earlier 18:29 extraction amendment preceded Coder responses; these are
different amendments. Full 800-output results remain pending. No updated numerical
results or visual rendering were claimed or inspected for this source assessment.

Remaining wording: use “the audited valuation identities/conventions” instead of
“any relevant financial identity” in the conclusion. The convention-results
placeholder should say scoring will follow completion rather than imply all 800
saved responses already exist. “These examples” remains singular after the single
opening example. The model-table renderer creates labelled 50-question family
blocks, so its caption denominator is appropriate; its final grading columns
explicitly retain the simple reference rather than the broadened union reference.

## Highest-value first-page changes

1. At lines 19–24, replace the abstract's “Execution verifies a program against its
   operands” opening with generator/verifier agreement preserving a wrong financial
   quantity. Execution alone does not establish correctness. Present binomial
   wrong-quantity evidence before Gordon rounding. Suggested opening:
   “A generator and its verifier can agree on the wrong financial quantity. In a
   released finance question, the label matches bond financing rather than the
   requested call price. We trace this error in public source and audit 12,655
   selected rows from two synthetic financial-supervision releases.”
2. At lines 32–33, replace “no measured effect on trained models” with “no measured
   effect of these data on model training.” The new experiment measures outputs
   from trained models; it does not establish dataset-induced learning effects.
3. Cite the public generator/verifier and Cox–Ross–Rubinstein identities directly
   in the first example or its caption, rather than waiting for the results
   section. The concrete example currently carries the major factual claim without
   a nearby source citation. The relevant existing keys are `cosimosource` and `crr`.
4. The figure's “Released target / Verified” box should identify a metadata claim,
   for example “Release metadata / verified.” Keep the caption's explicit statement
   that this is source inspection, not an upstream execution trace. The inspected
   code pin is separate from the dataset pin and is not proven to be its generating
   commit. This boundary is already correct in the results; retain it near the
   figure when space permits.
5. “These examples” at line 59 should be singular after the introduction's revision.

The diagram's computational dependencies are scientifically useful. The top row
shows a coupled check; the independent financial identity asks a different
question. It needs no speculative model-result row. A separate paired grading
table can establish the observed consequence once all configurations finish.

## Methods and interpretation

The model methods at lines 136–153 are appropriately bounded: same untouched
questions, heterogeneous models, fixed output budgets, retained failures,
reconstructed policies, and no response regeneration. Add the supplementary
amendment timing or point directly to its artifact: it was introduced after
63 DeepSeek and 60 Qwen3 records existed, before any Coder study response. Later
unseen responses do not make the entire numerical recovery endpoint preregistered.

Specify which displayed score uses all 200 attempts and which uses parsed-completed
answers. Strict format failures are not diagnosed financial errors. Numeric-only
recovery infers absent or placeholder units and does not prove full unit compliance.
The integer-plus-half-unit baseline applies only to constructed Gordon. Its
other-family and mixed-panel aggregates have no intended scientific interpretation.

For binomial models, state the reference convention explicitly: the risk-free rate
is treated as a one-period effective return, giving gross return `1 + r`. The one
DeepSeek mismatch, `cosimo_CFA_Level_I_231729_be0ed4387b76d0b9`, uses `exp(.05)`.
Its final 3.06 differs from the frozen reference `64/21`, but the source question
does not explicitly specify compounding. Keep the prespecified numerical counts
and describe this as convention mismatch, not unequivocal wrong reasoning. The
source label 12.95 is bond financing and remains wrong as a call value under both
interpretations. Two equivalent identities independently implement the financial
calculation but share the assumed compounding convention.

## Independently rescored completed DeepSeek slice

The saved 200-response ledger matches the frozen question panel. Direct rescoring
reproduces these counts; no raw response was regenerated or edited:

| Analysis | Parsed-completed | Reference-convention valid | Source ±0.005 accepted | Reference-valid rejected |
|---|---:|---:|---:|---:|
| Frozen strict parser | 137/200 | 136/200 | 81/200 | 55/136 |
| Exploratory numeric recovery | 200/200 | 199/200 | 102/200 | 97/199 |

The strict source-versus-reference credit difference is 55/200, or 27.5 percentage
points; the exploratory difference is 97/200, or 48.5 points. Thus the phenomenon
does not depend entirely on the post hoc endpoint. The 63 strict failures are
format failures. Report the one convention mismatch beside these reference counts.

Half-unit and 5% source policies each accept 88 strict responses and 150 recovered
responses, rejecting 48 and 49 reference-valid answers respectively. No parsed
numerically reference-invalid answer is accepted by these policies in this slice.
Do not turn the source-authored error-control result into a claim of observed
false acceptance by DeepSeek. Wider policies still lose correct call answers;
they do not create measured false acceptances here.

The supplementary conflicting-unit correction now rejects the reproduced synthetic
edge cases; version-two frozen file hashes verify. The original supplementary
freeze and implementation snapshot remain preserved. The full three-model result,
its family breakdown and any ordering claim must wait for the completed panel.
