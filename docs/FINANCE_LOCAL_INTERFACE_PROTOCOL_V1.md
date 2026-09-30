## Executive summary (read this first)

This is a new prospective local discovery-cohort pilot, after the earlier document
panel was observed. It does not overwrite prior prompts, outputs or freezes, and
does not become a held-out semantic benchmark. Its NLP question is whether a
quantity-checking instruction changes numerical answers, and whether asking for
a calculation/evidence record changes usable output. Native tokenization is an
implementation validity check, not method novelty or a claimed NLP encoding result.

## Fixed design

- Two pinned released checkpoints: Qwen3-1.7B with thinking disabled and
  SmolLM2-1.7B-Instruct. Same FP16 Apple MPS backend, greedy decoding, no sampling,
  512 maximum new tokens. These are checkpoint comparisons, not causal size or
  family effects. Do not substitute another model after inspecting its results.
- Select 16 FinQA and 16 TAT-QA cases from the existing 96-case cohort by salted
  case-ID hash, without filtering by previous answer, native label, reviewer
  agreement, uncertainty, error status or model success. Preserve all 32 cases.
- Four conditions cross a baseline/quantity reminder with a compact four-field
  versus full six-field JSON request. The numerical instructions and the four
  shared fields remain identical. The full calculation field permits only an
  arithmetic expression; neither reminder requests prose there. Evidence is
  requested only in the full condition. This factor changes requested response
  content/burden, not merely serializer mechanics.
- Two models × four conditions × 32 cases = 256 planned one-shot attempts.
  Rotate condition order deterministically by case index; keep model runs
  sequential on the same device. No selected-case retries, prompt edits, repairs,
  constrained decoding or successful-case substitution.

## Before selected financial inference

Verify both complete pinned checkpoints and native tokenizer files. Hash selected
inputs, source packets, reference/compact annotation inputs, code, protocol,
native adapter and model files. Keep source targets out of model messages.

For every selected prompt/condition/checkpoint, require token-ID equality between
native chat-template tokenization and rendering followed by tokenization with
additional special tokens disabled. Separately record whether the old default
retokenization path differs; do not infer an old tokenizer defect without actual
ID differences. Preserve prompt token counts/IDs hashes and rendered-text hashes.
Verify full input plus 512 output tokens fits the actual model context window.
Do not truncate, summarize context, or equalize different tokenizers' token IDs.

Source-free arithmetic probes check that each model loads and generates on MPS.
Wrong toy answers or schema violations are recorded diagnostics, not a reason to
exclude a frozen checkpoint or secretly adjust prompts. Launch gates are runtime
availability, token identity/budgets and parser controls. Freeze before any
selected financial answer, even if toy formatting fails. Preserve all probe output.

## Endpoints and failure accounting

Primary endpoints are strict requested-schema numerical availability out of all
32 attempts per condition and unchanged locked value/broad-unit agreement on the
fixed eligible intersection of this cohort with the original 62-case reference.
That intersection is 24 questions: 11 FinQA and 13 TAT-QA. Every condition also
reports eight outside-reference questions without silently dropping their attempts.
Booleans, abstentions, malformed responses, runtime failures and exhausted token
budgets remain explicit. Eligibility is not re-estimated from model answers.

Compact answers are scored through an explicit adapter adding empty calculation
and evidence fields for the existing scorer only. Those fields are neither
observed nor certified traces. Full answers use the unchanged six-field parser.
Secondary status-only normalization requires all originally requested fields;
it changes only an originally string-typed diagnostic status tag, never a value, unit, scale or missing
field. Keep it separate from strict compliance. Native/adapted scores and the
previously specified reference-projection sensitivity remain separate channels.
Reject duplicate fields and nonstandard JSON constants (`NaN`, `Infinity`,
`-Infinity`) before the unchanged shared parser. Runtime/token-validation failures
receive no strict or recovered credit even if a failed record retains valid text.
Typed-schema availability does not certify evidence locations, executable arithmetic,
eight-significant-digit compliance, or semantic correctness.

Report paired reminder transitions within each schema and paired schema
transitions within each reminder setting. Classify discordances as availability,
changed numeric value, changed unit/scale, or mixed differences; do not call a
unit/parser change improved arithmetic. Report full-condition executable coverage
separately; it has no compact-condition counterpart. No population confidence
intervals, causal family superiority or semantic truth from broad-unit matching.

Any interrupted run reports completed versus scheduled attempts and retains its
ledger; do not invent API/model responses or restart difficult questions. A full
panel result requires 256 unique model/condition/case records. No inference
spending or public release is involved. Model checkpoints are public downloads.

## Interpretation and paper decision

Quantity reminder effects concern this selected discovery cohort and local output
wrapper. A compact-output gain is output-interface sensitivity, potentially also
changed reasoning behavior; it is not a general financial-reasoning improvement.
The study tests a known measurement concern rather than proving a new verifier.
Only completed, independently checked results may enter the manuscript. Null
results are retained. Source quantity errors, known prior repairs and ambiguous
readings remain separate from all comparator disagreements.
