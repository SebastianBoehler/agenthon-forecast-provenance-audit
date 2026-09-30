## Executive summary (read this first)

Derive provisional technical references from the frozen 32 original question/
context packets before source-target unblinding and model inference. Two AI
reviewers work separately; human financial adjudication is still requested.
Numeric/unit agreement does not establish independent semantic truth. No selected
case is replaced when reviews find ambiguity, insufficient evidence or disagreement.

## Record schema and interpretation

Every record contains `case_id`, `status`, `requested_quantity`, `entity`,
`time_scope`, `assumptions`, `operand_bindings`, `unit`, `scale`, `currency`,
`expression`, `value`, `alternatives`, `evidence_paths` and `rationale`.

Status is `determinate`, `conditional`, `ambiguous`, `insufficient_information`
or `non_numeric`. Use determinate only when the visible question/evidence admit
one direct arithmetic reading. Displayed approximate financial inputs can yield
a determinate calculation conditional on those displayed inputs; explicitly record
approximation and do not certify the unseen unrounded economic quantity. Use
conditional for a substantive added interpretation, ambiguous for multiple
defensible meanings, insufficient when literal requested evidence is absent.

`expression` is numeric literals and basic arithmetic only, or null for a
non-numerical/unresolved reference. `value` is the resulting decimal string, never
the native annotation value. Execute only with the existing safe arithmetic
helper. Do not execute corpus programs or infer missing years/denominators.
An alternative reading includes expression/unit/scale and its interpretation.

Unit is exactly one of `currency`, `currency_per_share`, `currency_per_year`,
`percent`, `percentage_points`, `ratio`, `count`, `duration_years`,
`duration_months`, `duration_days`, `boolean` or `unknown`. Scale is `none`,
`thousand`, `million` or `billion`; it is the multiplier of the reported numeric
value for monetary/count quantities. Ratios/rates/durations use scale none.
Percent uses percentage-point numeric representation; percentage_points denotes
an absolute difference between percentage rates. Preserve the semantic type,
including relative rate change versus absolute percentage-point difference.
Currency records the explicitly stated source currency or null; do not invent it.

Bind arithmetic operands to exact table/paragraph locations with their roles.
Support constants such as 100 for percent or an averaging count explicitly.
Source pointers are original_context-relative paths: FinQA `table[row][column]`,
`pre_text[index]`, `post_text[index]`; TAT `table.table[row][column]` and
`paragraphs[index].text`. Finding a numerical literal alone does not establish
its role, entity, year or denominator. The rationale must explain those meanings.

## Validation and lock

Validate exact 32 unique IDs, schema/enums, pointer existence and safe expression/
value consistency. Neither reviewer may read source targets, original QA answer/
program fields, the other review, native source programs or later model outputs.
Reviewer identity, actual timestamps, input/output hashes and AI provenance are
recorded. Prior knowledge/pretraining may correlate failures despite separation.

Lock both complete reviews before comparisons/unblinding. The primary provisional
reference set comprises cases both mark determinate with compatible unit type,
scale-normalized numerical value, requested quantity and time scope. Manual
semantic reconciliation is separately disclosed; it cannot be established by
string matching requested-quantity descriptions. Preserve conditional/ambiguous
cases, alternate signs and percentage conventions outside the primary set.
Numerical allowance is relative 1e-10 with absolute floor 1e-10 for combining
reference arithmetic; it is not the answer-score allowance or economic certainty.

Freeze the combination code before source targets or generated answers are read.
Do not silently upgrade agreement into qualified expertise. A human reviewer can
use the same question-only packet, with a separately recorded review and lock.
Report primary-set coverage alongside all-attempt endpoints and explicit uncertainty.
