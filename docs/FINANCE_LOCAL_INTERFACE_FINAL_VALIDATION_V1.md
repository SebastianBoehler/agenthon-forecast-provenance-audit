## Executive summary (read this first)

**PASS for saved-artifact consistency, with failed comparative feasibility.**
All 256 scheduled attempts are present once. Only 141 returned successful
generations: 128 Qwen and 13 Smol; 115 Smol attempts failed with MPS out-of-memory
errors. Strict numerical availability and locked matches are zero in every arm.
Qwen's six status-only numerical recoveries also yield zero locked matches.
These results support a runtime-feasibility failure and an interface-availability
floor under this collector. They do not support a two-family financial comparison,
latent-capacity conclusions, or a causal reminder/schema effect on financial quality.
This is AI-assisted technical validation, not human expert adjudication.

## Scope and independently reproduced accounting

Read the unchanged local protocol, runtime, scoring, collector, analyzer and freeze;
checked every saved response and score, both completion receipts, all 41 bound
inputs and all 19 bound checkpoint files, including multi-gigabyte weights.
The prospective freeze was `2026-09-30T07:02:33.110703+00:00`, before the first
selected answer. Model revisions, MPS/FP16 flags and disabled CPU fallback match
the frozen settings. Token identity/context checks were successful for every
returned generation. No model was loaded or generated during validation.

| Saved accounting | Qwen3-1.7B | SmolLM2-1.7B-Instruct |
|---|---:|---:|
| Attempted records | 128 | 128 |
| Successful generations | 128 | 13 |
| Retained runtime failures | 0 | 115 |
| EOS / length / error finishes | 125 / 3 / 0 | 6 / 7 / 115 |
| Observed returned completion tokens | 12,905 | 3,717 |
| Summed successful generation seconds | 657.130 | 133.236 |

All expected model/condition/case identities and cyclic condition orders match.
Each model attempted all four conditions on the same 32 selected questions,
16 FinQA and 16 TAT-QA, with no replacement or retry. Reference eligibility is
fixed at 24 questions per arm: 11 FinQA and 13 TAT-QA; eight are outside that
reference. Failure records remain in all-attempt and fixed-reference denominators.

Qwen collection ran from `2026-09-30T07:03:37.892235+00:00` to
`2026-09-30T07:14:35.934914+00:00`; Smol followed from
`2026-09-30T07:14:58.490668+00:00` to `2026-09-30T07:17:12.689961+00:00`.
There was no model-run overlap. Smol's first failure is collection index 14,
`compact_baseline`, case `finqa:GS/2014/page_165.pdf-2`. Every subsequent attempt
also retains an out-of-memory error. All 13 Smol successes are FinQA: three complete
question blocks and one condition of the fourth. All 64 TAT-QA attempts failed.
Successful counts by compact baseline/reminder and full baseline/reminder are
3/3/3/4. This partial prefix cannot support the planned factorial comparison.
The ledger establishes the error sequence, not its causal resource mechanism.
Failed attempts have no returned token IDs or completion counts; actual partial
work inside them is unknown and is not assigned zero computation.

## Parsing and numerical endpoints

Own standard-JSON validation rejects duplicate fields/nonstandard constants and
checks the requested compact/full fields; compact trace fields are unobserved.
Own status-only normalization changes only a string status, preserving the other
fields and every failure gate. Fraction arithmetic independently checks locked
value/broad-unit matching and the separate reference-projection channel. The
native adapter is shared and hash-verified; its replay is implementation agreement,
not an independent semantic oracle. Every candidate, parse reason, match, native
score and aggregate equals the saved artifacts. Offline native-tokenizer decoding
independently reproduces all 141 returned texts from their saved continuation IDs.

| Qwen endpoint, out of 32 attempts | Compact baseline | Compact reminder | Full baseline | Full reminder |
|---|---:|---:|---:|---:|
| Strict numerical availability | 0 | 0 | 0 | 0 |
| Status-only numerical availability | 3 | 2 | 0 | 1 |
| Strict locked matches, out of 24 | 0 | 0 | 0 | 0 |
| Status-only locked matches, out of 24 | 0 | 0 | 0 | 0 |

Smol strict/status numerical availability and matches are zero in all four arms;
its 13 returned texts fail JSON or requested-field checks. All native, projected
reference and percent-fraction credits are zero. Full-expression support is zero
because no full response contains a strict numerical answer; it does not measure
arithmetic correctness. All paired locked transitions are 24 `False->False`
with zero discordances. This is a measurement floor that includes failures,
not evidence of equal capabilities or absence of a prompt effect.

The original selection is a discovery-cohort sample, not an unseen semantic test.
Broad-unit matching remains weaker than dimensional or financial truth. The
prospective gates established probe availability, token identity and parser
controls; they did not establish sustained financial-run resource feasibility.
Later source-free resource diagnostics are separate from this V1 validation.

## Reproduction and exact identities

Run from the repository using its recorded existing runtime; this does not load
weights or call a model. Use a **new** output path because the checker refuses to
overwrite a receipt:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python scripts/validate_finance_local_interface.py --output outputs/finance-local-interface-v1/independent_postflight_validation-replay.json
```

Original validation completed `2026-09-30T07:26:45.350398+00:00`. Only the new
checker, independent receipt and this report were written. Original scientific
code, inputs, freeze, responses, scores, results and earlier reviews are unchanged.
The original receipt records full hash verification and accounting; subsequent
offline decoding described above is an additional read-only check.

| File | SHA256 |
|---|---|
| `scripts/validate_finance_local_interface.py` | `94ff322225a1d8ae958ebdf2289de48dc146f524b8b5247b99bf75b0e71737c5` |
| `outputs/finance-local-interface-v1/independent_postflight_validation.json` | `00e1f7add17976df1529faa4a1c7f40580743be166163506ad70258a14a18942` |
| `outputs/finance-local-interface-v1/freeze.json` | `357b05c9f525773d19b6dff2cd64dc34d5e7d43c64a2b821f2df2f3ec7981a22` |
| `outputs/finance-local-interface-v1/responses_qwen3-1.7b.jsonl` | `0868aea0afc5edce4793dabd9b30623cb926406d1fc4937551b2fb2b65c8746a` |
| `outputs/finance-local-interface-v1/responses_smollm2-1.7b.jsonl` | `11f620e4b002cb6f64fa00784cca069f295752eea7a0f2e924001add403b71dd` |
| `outputs/finance-local-interface-v1/scores.jsonl` | `2f803fc2cc50b19a7967c8d38f5be78191482467759ebeb7ce845efd457e0d36` |
| `outputs/finance-local-interface-v1/results.json` | `3abb551f3f867dde4a9af3fa16180f3ec9a04889a73f9a5642b17a8475c73b0d` |
