## Executive summary (read this first)

Add one separately frozen Gemma 4 E2B Q4_K_M checkpoint to the original 200-question
synthetic grading panel. This tests robustness of fixed-answer grading disagreement
under another checkpoint/backend configuration. It does not isolate model-family,
size, quantization or backend effects. The original 800-answer panel and failed
local document pilot remain unchanged.

## Model, inputs and inference

Use the already cached `google/gemma-4-e2b` virtual model, its unchanged pinned
`model.yaml` native chat template, concrete GGUF weights and LM Studio 0.4.24+1
llama.cpp Apple Metal backend 2.47.0. Record the concrete model/tokenizer/template
file hashes, live loaded configuration and raw responses. The E2B name describes
effective parameters; LM Studio's nominal parameter metadata must not be treated
as a size-matched comparison to prior models.

All 200 original unique questions remain: 50 each constructed Gordon, binomial
call, ordinary Gordon and WACC. Preserve the original selection ordering,
question hashes, system instruction, 1,024-output-token cap and strict parser.
No examples, new rounding instruction, calculator, grammar-constrained output,
additional source target or corrected answer reaches the model. LM Studio applies
its pinned native chat template to the original system/user strings.

Use a localhost-only server; `/api/v1/chat` explicitly disables reasoning and
integrations, stores no chat history and has no previous-response identifier.
Set temperature zero, top-k one, top-p one, min-p zero and repeat penalty one.
Load context 4,096, parallelism one and no speculative draft; request full Metal
offload with the CLI. The API does not expose the effective GPU-layer ratio.
Record other live load settings rather than claim matched hardware with old runs.
Selected questions are collected sequentially with no retries or resumption.

The native API reports aggregate token counts but not token IDs or a termination
reason. Preserve this limitation. For the unchanged scorer's completion gate,
`stop` denotes a normally returned server reply below the token cap with one
message and no reasoning/tool item; it does not certify a particular EOS token.
At-cap responses receive conservative `length` failure. Missing/invalid stats,
unexpected model identity/items, nonzero reasoning tokens or context-budget
violations receive an explicit runtime error, not an invented answer. Full raw
responses and this normalization rule permit independent replay.

## Readiness and freeze

Before any selected prompt, bind scientific code/input hashes, checkpoint files,
native model configuration and the protocol in a preflight freeze. Run exactly
three authored source-free controls using the unchanged system instruction:
7 plus 14 currency units, half of 9 currency units, and a 50/50 weighted rate of
4 and 8 percent. Their expected finals are 21 currency, 4.5 currency and 6 percent.
Require all three normally completed strict finals to match within 0.0001, with
valid native statistics and no tool/reasoning response. A failed gate stops this
configuration before selected answers; do not tune it on the controls or silently
change model/prompt/mode. Retain all failed diagnostics.

After readiness, create a distinct collection freeze binding the readiness record
and precollection review. No selected answer may precede this collection freeze.
Abort scheduling on five consecutive runtime errors or one hour elapsed, retaining
attempted records and listing unattempted IDs separately. A partial prefix cannot
be reported as a completed 200-answer panel. Do not replace failed cases.
An in-flight request can take up to its 120-second timeout beyond that scheduling
cutoff. A client timeout does not establish when server-side generation ceased.

## Endpoints, interpretation and review

Primary: unchanged strict final-line extraction and displayed-input reference
using the original 1+r binomial convention, with unchanged original-label
comparators. Report all-attempt availability, numeric compatibility, valid answers
denied credit and invalid answers credited, including passing-family controls.

The existing unit-relaxed numeric extraction and union with continuous binomial
compounding are separate, prespecified sensitivities for this new run. Their
historical application to the older panel remains posthoc. Neither certifies full
reasoning traces, and no general model ranking or learning effect is claimed.

Independent saved-response replay must verify freezes, identity/order, raw-response
normalization, score rows and aggregates before adding results to the manuscript.
Existing financial formulas, parsers and scoring implementations are imported,
not rewritten. This is a checkpoint replication, not a new general validator.
Unused report-group validation and expert reference adjudication remain the more
substantive main-track research gaps. Local execution incurs no provider charge;
the user's separate $10 total cloud authorization is a ceiling, not a spend target.
