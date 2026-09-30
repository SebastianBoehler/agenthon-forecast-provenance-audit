## Executive summary (read this first)

Collect a prospective 384-answer document-finance panel: two model configurations,
two label-free instruction conditions, and all 96 previously selected FinQA/TAT-QA
questions. The primary goal is paired financial-validity versus reconstructed/native
grading agreement on unchanged answers. A quantity reminder is a cheap diagnostic
baseline, not a new algorithm or training intervention. This declaration precedes
model collection; the separate blind technical review and native-label audit remain
distinct evidence stages.

## Questions, configurations and intervention

Use the identical original contexts/questions selected in the preparation protocol:
48 FinQA and 48 TAT-QA, with no answer-based selection or exclusions. Remove rubric,
reviewer labels, case identity and every source annotation from the model prompt.
Prompt bytes, their hashes and request configuration are frozen. No independently
reviewed answers, source targets or case-specific corrective hints reach either model.

The two OpenRouter configurations are DeepSeek V3.2 and Qwen3.5 9B, each through
one fixed SiliconFlow FP8 endpoint with provider fallback disabled. Catalogue
metadata and endpoint prices are saved before collection. Temperature is zero,
reasoning is disabled, maximum output is 1,024 tokens, and JSON-object response
format is requested. These are different checkpoints, not a causal size comparison.
Provider tags and reported response identities do not make remote weights immutable.

Baseline requests one JSON answer with status, decimal-string value, unit, monetary
scale, calculation and evidence references. A separately identified yes/no channel
uses `non_numeric_answer`, `yes`/`no`, unit `boolean` and no monetary scale; these
cases remain in the original denominator and are separate from numerical-validity
comparisons. FinQA selection had no numeric-type filter, so the question is not
forced into a numeric answer schema. Percentage values use percentage points;
rate differences are distinguished from relative percent changes. Monetary scale
is explicit. The reminder adds label-free attention to requested quantity, denominator,
signs, time window, units and rounding. It does not expose reviewed operands or labels.
Both conditions use the same output schema; length and realized token use can differ.

The exact strings and parser live in
[`model_protocol.py`](../src/finance_document_review/model_protocol.py).
One attempt per case/configuration/condition is retained; no silent retries, fallback
providers, answer regeneration or parser repair. Transport failures, truncation,
abstentions and parse failures stay in the complete 96-case denominator per arm.
Two authored arithmetic preflight requests may test API shape, one per model,
before scientific collection; they are retained separately and excluded from outcomes.

## Timing, budget and preservation

Freeze this protocol, model constants, runner, parser, original packet and catalogue
hashes before the first preflight/scientific response. Collect after both technical
reviews and the pre-target adjudication record are locked. Native labels may be
inspected only under the technical-review sequence; scientific prompts never change
after that inspection. The freeze is prospective for this panel, not for the earlier
exploratory audit or existing 800-answer study.

The new panel has a $1.50 conservative request-cost bound, including two preflights.
Count visible input UTF-8 bytes plus a message-envelope allowance as an upper input
token bound, and the maximum output budget against the pinned endpoint prices.
Refuse collection if the bound exceeds the cap or current endpoint prices/support
no longer match the freeze. Retain provider-reported usage, cost, failure and latency;
unreported cost is missing, not zero. The cap is not a measured realized cost.

Save raw responses and request/configuration hashes separately from original packet
contents. API credentials remain environment-only. Do not alter old responses,
scorers, freezes or protocol receipts. No local weight training occurs.

## Grading endpoints and controls

First report strict JSON/schema coverage, abstentions and numerical outputs. Financial
validity uses the locked answer-hidden technical reviews and their uncertainty;
independent arithmetic does not turn these into human expert judgments. Show agreed,
conditional, disputed and unresolved cases separately with full source denominators.
Correctness of final values does not certify the calculation trace.

Native FinQA requires executable DSL programs and separately scores program equivalence.
Our JSON calculations do not satisfy that interface. Any scalar comparison is explicitly
an adapted execution-answer comparator reproducing the official five-decimal scalar
rule, not full official FinQA program accuracy. TAT-QA comparison must use inspected,
pinned metric code with its actual answer/scale representation; separately report
answer credit and scale credit rather than assuming a universal numeric tolerance.
Do not convert percentages or monetary scales just to fit a target; record each
declared adapter rule and its information requirements before applying it.

Where native interfaces cannot be reproduced faithfully, report the limitation and
do not label an invented score official. Original-label compatibility, independent
visible-input validity and instruction compliance are separate measurements.

Primary paired counts are valid answers denied credit and invalid answers credited,
within each source/configuration/condition. Include per-case identities, uncertainties
and differences. Reminder effects separately report parsing, requested-quantity,
unit/scale, arithmetic and abstention changes; do not infer a mechanism from a single
pooled accuracy delta. Repeated API calls are not independent research replications.

Test deterministic representation controls independently of model inference:
identity round trips; equivalent fractions/percentages with explicit units;
thousand/million rescaling; wrong sign or denominator; and wrong-quantity values
where the visible task establishes a distinct quantity. These are authored evaluator
diagnostics, not naturally released fault counts. Restrict each control to cases
whose units/semantics are independently established and show exclusions.

If no definite source-label fault transfers to these document tasks, retain that
negative result. If grader differences arise only from output serialization, say so.
If technical review is too uncertain, do not claim an expert-grounded benchmark.
A useful diagnostic panel alone does not establish a novel main-track contribution,
learning harm, representative prevalence or superiority of the reminder method.

## Artifact scope

Report source and case identities, code/configuration hashes, request hashes,
responses and endpoint definitions. Keep corpus contents, original packets and
native target files local under the existing unresolved redistribution boundary.
Use the original pinned preparation to reconstruct inputs. No sealed competition
data, external submission, public release or human contact enters this experiment.
