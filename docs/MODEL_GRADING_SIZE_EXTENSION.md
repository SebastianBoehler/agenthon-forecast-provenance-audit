## Executive summary (read this first)

Add Qwen3 4B to the same 200-question panel after the user's request for a sound
comparison of model sizes and families. Preserve the originally frozen three-model
study and its separate results. Freeze this extension before any 4B financial answer.
The extended roster has four models and 800 responses.

## Reason and controlled comparison

The original Qwen3 1.7B versus Qwen2.5-Coder 3B comparison mixes size, generation
and code specialization. It cannot identify a size effect. Qwen3 4B uses the same
model family/generation, nonthinking chat mode, FP16 MPS runtime, greedy decoding,
1,024-token limit, system instruction and question panel as Qwen3 1.7B.

This is a within-family comparison of released checkpoints, not a causal
parameter-count intervention: their training can differ. DeepSeek and Qwen give
cross-family robustness evidence, while their runtimes and quantization differ.
Neither those differences nor inference latency identify a family advantage.

The cache revision is `Qwen/Qwen3-4B` at
`1cfa9a7208912126459214e8b04321603b3df60c`. All required weight shards are present.
The wrapper adds only this explicitly documented model specification to the frozen
local engine in memory. Original engine/protocol files and their hashes remain
unchanged. No earlier answer is regenerated.

## Timing, endpoints and outputs

The extension follows the completed DeepSeek run and partial Qwen3 1.7B run;
there are no 4B financial responses before its freeze. It is therefore an
exploratory roster extension, not an originally preregistered four-model study.
Original three-model strict and supplementary results are retained separately.
The extension uses the same strict parser and corrected post hoc numeric extractor.

`extension_manifest.json` records the time, observed original ledger counts,
selection hash, added model and wrapper/scorer/document hashes.
`extension_results.json` and `extension_numeric_sensitivity.json` contain the
additional model's results. `combined_results.json` and
`combined_numeric_sensitivity.json` merge four model records while identifying
and hashing their constituent analyses. All questions retain their denominator.
