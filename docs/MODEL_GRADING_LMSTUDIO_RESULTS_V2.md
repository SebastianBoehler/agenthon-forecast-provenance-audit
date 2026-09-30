## Executive summary (read this first)

The new local Gemma checkpoint completes the original 200-question synthetic
panel. Independent replay agrees with all four 200-row scoring streams. A
prespecified unit-relaxed extraction shows 22 correct whole-unit answers denied
by the cent comparator. Strict extraction admits none of that family's answers.
Keep this bounded rounding result separate from the stronger original call/debt
evidence, and distinguish two WACC window disagreements from label faults.

## Configuration and complete accounting

Model: `google/gemma-4-e2b`, cached Q4_K_M GGUF, LM Studio 0.4.24+1,
llama.cpp Apple Metal 2.47.0. The publisher's effective-parameter definition and
local nominal metadata differ; this is not a size-matched family comparison.
Native template, weights, engine files and loaded configuration are hash-bound.
Upstream weight commit is unknown. Original prompts/order, 1,024-token cap and
scorers remain unchanged; no calculator, grammar or answer key reaches the model.

Collection: September 30, 08:06:38–08:19:53 UTC. All 200 attempts return, with
zero runtime errors and two conservative output-cap cases. Reported totals are
35,976 input and 78,364 output tokens. The native API exposes no token IDs or
actual finish reason, so the adapter's below-cap `stop` is not certified EOS.
No inference is retried. Our model is unloaded and the previously stopped local
server is stopped again after collection; no other loaded model was present.
Cloud spending on these follow-ups is **$0 of the authorized $10 total cap**.

## Results and scientific interpretation

Each family has 50 attempted questions. Numeric columns use the prespecified
unit-relaxed extraction; compatibility initially uses the original 1+r convention.

| Family | Strict parsed | Numeric parsed | Numeric compatible | Compatible denied by cent comparator |
|---|---:|---:|---:|---:|
| Explicit whole-unit Gordon | 0 | 25 | 24 | 22 |
| Binomial call | 0 | 36 | 0 | 0 |
| Ordinary Gordon | 0 | 34 | 30 | 0 |
| WACC | 43 | 50 | 22 | 2 |

Strict totals are 43 parsed and 18 compatible, all WACC. Its one compatible
denial and one incompatible credit arise from opposing rounded-label/formula
tolerance windows. These are not documented WACC label defects.

Numeric totals are 145 parsed and 76 compatible. Its 24 compatible denials
comprise 22 whole-unit instruction/rounding consequences and two WACC windows.
Absolute 0.5 accepts all compatible answers but credits 32 incompatible answers;
relative 5% credits 33. Apply integer projection only to the explicitly whole-unit
family; the aggregate all-family integer-policy count has no financial meaning.

The two-compounding-convention sensitivity adds one continuous-compatible call,
producing 77 numeric compatible answers and 25 cent denials. Its value 2.050511
lies within 0.005 of independently computed continuous price
2.0471735733791988704..., while the source gold is 9.13. Its trace contains an
incorrect intermediate product. This is final-value compatibility, not certified
reasoning or a primary/strict binomial replication. It does not establish
family-independent financial reasoning or broad automatic audit accuracy.

## Amendments, reporting mistake and validation

The original source-free strict launch gate fails 1/3; V1 has no selected-question
collection. The [explicit V2 amendment](MODEL_GRADING_LMSTUDIO_AMENDMENT_V2.md)
changes launch readiness to runtime availability before the selected questions,
without changing prompts, inference or scorers. The failed gate stays preserved.

The frozen analyzer's imported writer saves the V2 summary in the V1 directory.
The [reporting correction](MODEL_GRADING_LMSTUDIO_REPORTING_CORRECTION_V2.md)
preserves it and copies identical bytes to V2, with a separate correction receipt.
Independent Fraction/formula and 100-digit compounding replay checks all 800
score records, aggregate/family counts, freezes, raw requests and native accounting.
It verifies concrete external hashes; this is saved-record correctness, not
semantic certification or a controlled backend/family effect.

Independent receipt: `outputs/model-grading-lmstudio-v2/independent_validation.json`,
SHA256 `d1f8e7d8659df8882dd92fba12ac5f69cfa0152b01b2ab568d08035a8c57682a`.
Summary SHA256 (both retained locations):
`ec1ab58b11a39a1aac7cd9b1e73eb08ceaf75e82b5fef00272b21bfcf4795015`.
The original 800-answer panel and historical archive are unchanged.
Unused-group transfer and qualified semantic adjudication remain unmeasured.
