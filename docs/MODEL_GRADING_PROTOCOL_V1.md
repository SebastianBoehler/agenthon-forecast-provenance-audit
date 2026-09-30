## Executive summary (read this first)

Freeze 200 distinct public financial questions before model inference. Collect one
answer per question from two small local Qwen models and one cheap DeepSeek API
model. Grade the same stored answers using explicit original-label comparator
policies and independently calculated visible-question answers. This measures
grading consequences on observed outputs; it does not measure training harm.

## Question selection and research status

Use the already pinned Cosimo CFA Level I release, revision
`42244d29c6b9912683213a08d1a9c5b0373b381b`, verified by its recorded SHA256.
Choose 50 distinct prompts from each of `cr_eq_gordon`, `deriv_binomial_call`,
`eq_gordon`, and `corp_wacc`. The first two families contain established defects;
the latter two are passing comparisons. These families are purposively selected.
This extension follows the original exploratory audit; it is not preregistration
of the earlier discoveries or a representative financial benchmark.

Within each family, deduplicate exact visible questions, keep the smallest source
case ID, rank by SHA256 of `model-grading-v1-20260929` concatenated with the exact
question, and take the first 50. Do not choose cases by gold discrepancy, model
success, or model agreement. Record every selected ID and the full selection hash.
The same 200 questions are shown to every model. No source label, verification
metadata, derived target, audit finding, or source generator is provided to models.

## Models and resources

- Local `Qwen/Qwen3-1.7B`, revision
  `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`; nonthinking mode.
- Local `Qwen/Qwen2.5-Coder-3B-Instruct`, revision
  `488639f1ff808d1d3d0ba301aef8c11461451ec5`. This is a code-oriented instruction
  model, not a size-matched general-purpose control.
- OpenRouter `deepseek/deepseek-v3.2`, catalogue canonical slug
  `deepseek/deepseek-v3.2-20251201`, nonthinking mode, pinned to
  `siliconflow/fp8`, with provider switching disabled. Save catalogue/endpoint
  metadata and every response's returned model/provider. The API's dated
  catalogue identifier is not proof that immutable weights were served.

Local models use cached, hash-recorded full-precision files, float16 PyTorch MPS
inference on this MacBook, greedy decoding, and at most 1,024 new tokens.
The API uses temperature 0 and at most 1,024 output tokens. No tools, browsing,
calculator, few-shot examples, fine-tuning, or retries of model answers.
These settings do not establish bitwise cross-machine inference determinism.

The API price observed before freezing is $0.259/million input tokens and
$0.42/million output tokens. The 200-answer API run is bounded by $1; local runs
have no API charge. Infrastructure failures are preserved, not replaced by another
provider. A predeclared infrastructure retry may only follow an explicit protocol
amendment; successful, malformed, or truncated model answers are never regenerated.

## Prompt and extraction

All models receive the same system prompt followed by the untouched question:

> Solve the financial question using the information shown. Briefly show the calculation in at most five sentences. Respect any rounding instruction in the question. If no rounding instruction is given, give at least four decimal places. End with exactly one final line in this format: FINAL: <number> <unit>. Use currency as the unit for monetary values. Use percent for a rate, expressed in percentage points (for example, 7.25 percent rather than 0.0725). Do not put Markdown formatting on the final line.

Extract exactly one `FINAL:` marker on the last nonempty line. Accept signed
decimal/scientific notation and valid thousands separators. Its unit must be
`currency` for the three valuation families or `percent` for WACC. No silent
conversion of unitless fractions, no searching for a convenient earlier number,
and no manual replacement of malformed final lines. `31`, `31.0`, and `31.00`
are numerically equivalent. Decimal values and all raw text are retained.

Empty responses, nonfinal/multiple markers, malformed numbers, wrong units,
truncation before a final answer, transport errors, and refusals remain in the
200-question denominator. Report their reason separately. The primary endpoint
uses successfully parsed final answers; unfinished generations cannot be silently
treated as complete responses.

## Scoring and endpoints

Independently derive formulas at 50-digit Decimal precision from visible operands,
using the existing audit and independent rational validation. Monetary valuations
and WACC percentage points have absolute serialization tolerance 0.005. Gordon
constructed responses must be an integer equal to the nearest whole value; both
adjacent integers are accepted at exact half ties because the question has no
tie-breaking rule. Binomial call values must agree with replication and discounted
risk-neutral expected payoff.

For each identical model output, compare visible-question validity with these
explicit original-label sensitivity policies: absolute 0.005, absolute 0.5, and
relative 5%. Add the integer-plus-original-half-unit baseline for constructed
Gordon. These are reconstructed comparators, not executions of an upstream reward
implementation. Relative tolerance is 5% of the absolute source gold.

Report per model and per family: all attempts, parsed/completed answers, visible
validity, original-label acceptance, valid answers rejected by each source policy,
invalid numerical answers accepted by each source policy, and paired grading
changes. Parsing failures count as unsuccessful under every policy and are reported
separately from numerical errors. Record equal-weight aggregate counts for the
four selected families. Show ordering if it changes, but do not infer a reliable
population ranking from two hundred dependent template questions.

No significance test or independent-row confidence interval is a primary endpoint.
The evidence concerns the frozen finite set and model configurations. A repaired
answer is not shown to models. Correctness of model outputs can therefore fail,
unlike acceptance of formula-generated correction targets by their own oracle.

## Validation and release

Freeze selection, prompt, extractor, numerical rules, model roster, and code hashes
before the first study output. A simple arithmetic health check outside the selected
financial questions may verify model-loading feasibility before the freeze.
After execution, independently validate the selected formulas and rescore the
saved outputs, inspect cases of grading change, and verify all denominators.
Generate manuscript numbers and figures from stored results.

Prepare a blinded human-review packet with a separate key. No person is contacted
by this protocol and no human annotation is claimed without completed review.
Human adjudication and transfer to an unseen dataset remain explicit limitations.
Only public source questions, model outputs, aggregate results, and reproducibility
metadata enter the paper artifact. API credentials and private teaching materials
are excluded. Submission and public release remain separate actions.
