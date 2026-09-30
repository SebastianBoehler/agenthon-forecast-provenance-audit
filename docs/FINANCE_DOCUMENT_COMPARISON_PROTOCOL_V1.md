## Executive summary (read this first)

Separate source-annotation validity, independent visible-answer validity, model
instruction compliance and native/adapted scoring. Compare unchanged answers and
retain uncertainty. This later analysis declaration precedes native-target unblinding
and model collection. It tests an explanation; it does not assert that an intended
native convention is a bug or that technical reviewers supply expert ground truth.

## Locked review and independent units

Use every original selected case, 48 per source. Check the two independently
completed technical reviews against the frozen packets and their declared arithmetic.
Record original review hashes before comparing them. Before native targets are
opened, create a separate combined record with each review's requested quantity,
answer values, units, scale, assumptions and ambiguity. Retain both original records.

Map units to explicit canonical types: percent, percentage points, ratio, currency,
count, duration or nonnumeric. Keep monetary scale explicit. Equivalent dollar,
thousand-dollar or million-dollar representations share economic value; percent and
ratio conversion requires the same requested quantity, not only numerical proximity.
An unknown currency is not silently identified as USD, and a rate difference is
not silently made a relative change. Each unit mapping cites its original review
field; no native target is used to infer the mapping or a multiplication factor.

For agreed determinate cases, both reviewers must support the same quantity/unit
and independently calculated value. Calculation agreement uses a relative numerical
guard of 1e-10 with a 1e-12 absolute floor in the recorded answer unit. Conditional,
disputed, insufficient-information, unresolved and nonnumeric cases remain separate.
Do not collapse disconnected interpretations into a min/max interval. A root-agent
technical adjudication, if needed, is separately labeled, justified from visible
context and hash-locked before targets; it is not independent human adjudication.

## Financial and source compatibility

Financial validity compares a candidate's declared quantity-compatible unit and
scaled value with the locked reading. For unrounded model output, use relative
numerical allowance 1e-7 with an absolute floor 1e-8 in the recorded reference unit,
consistent with the requested eight significant digits and decimal arithmetic.
An explicit precision instruction overrides this allowance with its declared output
projection. Report the allowance; it is a study comparator, not an upstream rule.
Keep wrong-unit/scale, numeric disagreement, abstention and parse failure distinct.
Final-value validity does not certify an evidence citation or calculation trace.

Source annotation compatibility is evaluated separately. TAT-QA supplies native
answer/scale; interpret that pair under its declared metric semantics. FinQA's
native execution scalar lacks units: retain the literal scalar and any explicit
textual answer units separately. A reviewer-derived unit cannot silently retrofit
the annotation. Missing source-unit interpretation is unresolved unless the native
task/program convention establishes it. Record post-unblinding reconciliations.

Classify native comparisons as compatible, definite contradiction under locked
reading, rounding/representation difference, defensible alternative, insufficient
information or unresolved. Keep all source counts and conditional denominators.
A discrepancy in a disputed reading is not a definite label error. Do not count
previously corrected derivative cases as first discoveries without a provenance check.

## Native and adapted interfaces

Call the inspected pinned TAT-QA metric with the candidate answer/scale pair.
Map model percent or percentage-point units to native `percent` scale; retain the
semantic distinction in the independent endpoint. Monetary scales map verbatim,
and `none` maps to the native empty scale. This is an explicit interface adapter.
Report answer EM/F1 and scale accuracy separately. Unsupported units/interfaces
receive an explicit adapter-ineligible classification, not invented native credit.

FinQA JSON answers are not FinQA DSL programs. The primary adapted scalar condition
compares the literal candidate value after the official five-decimal result rounding
with `exe_ans`; report that its scalar channel ignores units and scale. It is not
official full-program accuracy. A separately labeled percentage-as-fraction
sensitivity may divide a candidate percent/percentage-point value by 100 using only
its declared unit. This is a target-independent representation intervention, not
a conversion selected to maximize gold agreement. Other conversions require an
explicit native convention and remain separate from the primary scalar condition.

Never call serialization differences under this adapted model interface an official
FinQA evaluator implementation defect. Preserve the native task's global program
conventions and output requirements in the interpretation. Do not replace native
scoring with a generic tolerance while calling it official.

## Controls, paired outcomes and uncertainty

For each source/configuration/condition, partition the full 96/48 denominator into
parse failure, nonnumeric answer, abstention and numeric response. Within the locked
agreed determinate numerical cases, report independent-valid/native-credited,
independent-valid/native-denied, independent-invalid/native-credited and
independent-invalid/native-denied. Show uncertain/ineligible cases outside this
matrix; conditional matrix totals must never appear as all-case accuracy.

Use source-correct cases as controls for grader disagreements. Separate wrong-source
labels from correct-source-label/serialization or normalization effects. The reminder
contrast is paired by question and model, with raw change counts and source strata.
Parsing or scale gains are not automatically quantity-grounding gains. Do not label
every numeric mismatch an arithmetic error; inspect calculation/evidence only in a
separately disclosed attribution step.

Authored boundary controls include equivalent percent/fraction representations,
monetary rescaling, sign flips, factor-100/1,000 errors and explicit rounding
boundaries. Restrict inherited-case controls to independently supported semantics;
do not count them as natural annotation defects or independent cases. Report both
error directions and successful cheap alternatives. Native-class identity round
trips and scale channels establish adapter consistency, not financial correctness.

Source-correct/native-credit disagreement after faithful adaptation is a candidate
mechanism, not automatic novelty. If remaining differences are familiar precision
choices, missing task instructions, known annotation repairs or adapter mistakes,
retain the result and narrow the claim. More cases or reminder gains alone do not
earn a general benchmark/method or main-track claim. Report per-source observations
without pooled-row prevalence intervals, and state the unmeasured human expertise,
report dependence, model contamination and lack of learning consequences.

## Evidence retention

Preserve raw reviews and the pre-target lock, original annotations locally, pinned
evaluator bytes and controls, frozen model requests, raw responses and per-case
paired outcomes. Freeze this protocol and the completed pre-target record before
unblinding. New source-specific adapters are hashed before their first selected-case
use. Do not mutate the older paper's scientific ledgers, graph or freeze manifests.
