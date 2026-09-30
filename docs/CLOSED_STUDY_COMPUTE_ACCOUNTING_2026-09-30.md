## Executive summary (read this first)

This reporting-only inventory covers four closed studies: the original 800-answer
panel, the 200-answer Gemma extension, the 256-attempt local JSON pilot, and the
GEPA V1/V2 prompt-adaptation attempts including 432 V2 heldout answers. It uses
saved metadata; no inference or new API request was made. The still-running
quantity-transfer study and its generated outputs were not read.

Recorded API cost is not a complete compute or project-cost measurement. Local
electricity, hardware amortization, cloud accelerator specifications, preparation
time and unrecorded exploratory work remain unavailable. This inventory therefore
does not make a complete project-total claim or resolve checklist item 8 to Yes.

## Measurement definitions and scope

Metadata aggregation completed September 30, 2026, at 10:47:41 UTC. Token totals
sum the saved native token counts or provider-reported usage. Missing counts are
missing, not zero-token attempts. Tokenizers differ, so these totals do not
establish equal compute across models. Counts include attempted failures.

**Summed latency** adds each recorded call/generation's elapsed time. It is not
wall time, accelerator time or training time; concurrent API calls overlap.
**Collection span** is the last recorded completion minus the first recorded
start. It excludes earlier loading, preparation and later analysis. Original
800-panel ledgers do not provide local start/end timestamps, so no collection
wall time is reconstructed for them. GEPA's egress-slot span bounds HTTP work;
it does not measure exact wire times. All reported seconds below are rounded.

The local host is the project-reported 36-GB Mac. Closed freezes establish Apple
MPS/Metal and arm64 macOS, but do not contain a complete chip/core/RAM inventory
or continuous peak-memory measurement. The host description is not a new hardware
attestation. No model weights were trained in these four studies.

## Original 800 saved answers

Each model answers the same 200 questions. The original three-model 600-response
panel and the later 200-response 4B extension retain separate freezes/results.

| Model | Attempts / returned | Input tokens | Output tokens | Summed latency, s | Reported API cost, USD |
|---|---:|---:|---:|---:|---:|
| Qwen3 1.7B | 200 / 200 | 36,876 | 36,371 | 1,685.385 | No provider charge; local cost unmeasured |
| Qwen3 4B | 200 / 200 | 36,876 | 33,601 | 1,889.349 | No provider charge; local cost unmeasured |
| Qwen2.5-Coder 3B | 200 / 200 | 36,076 | 56,315 | 2,397.584 | No provider charge; local cost unmeasured |
| DeepSeek V3.2 | 200 / 200 | 32,600 | 44,761 | 3,676.123 | 0.027243020 |

All 200 rows per model have input/output counts and elapsed times. Two Qwen3 1.7B
returns reach the output cap; the other local rows record EOS. DeepSeek records
200 normal stops and returned provider SiliconFlow. These are returned responses,
not necessarily valid or schema-compliant answers.

Local configuration: FP16 MPS, greedy decoding, Python 3.13.2, PyTorch 2.10.0,
Transformers 4.56.2, maximum 1,024 new tokens. Pinned cached revisions are Qwen3
1.7B `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`, Qwen3 4B
`1cfa9a7208912126459214e8b04321603b3df60c`, and Qwen2.5-Coder 3B
`488639f1ff808d1d3d0ba301aef8c11461451ec5`.

API configuration: DeepSeek V3.2 through OpenRouter's fixed `siliconflow/fp8`
route, fallback disabled, temperature 0, reasoning disabled, maximum 1,024 output
tokens, concurrency four. The price snapshot records USD 0.259/million input and
0.42/million output tokens. All 200 costs are reported in saved usage; remote
hardware, resident memory, actual weights and loading time remain inaccessible.
Evidence: [protocol](MODEL_GRADING_PROTOCOL_V1.md),
[results](MODEL_GRADING_RESULTS_V1.md),
[replay and route limitations](MODEL_GRADING_REPRODUCE.md).

## Gemma 200-answer extension and failed readiness gate

The V2 receipt spans **795.481 s**, 08:06:38.225933–08:19:53.706615 UTC on
September 30. Its 200 attempts all return; summed call latency is 795.460 s.
Native API usage totals **35,976 input / 78,364 output tokens**. Two returns reach
the output cap. There are no selected-question runtime failures or retries.

Configuration: cached `google/gemma-4-e2b` Q4_K_M GGUF, LM Studio 0.4.24+1,
llama.cpp Apple Metal 2.47.0, context 4,096, parallelism one, maximum 1,024 output
tokens, greedy settings, reasoning/tools/speculative decoding disabled. Engine,
template and local weight bytes are hashed; upstream weight commit and actual
offload ratio are unknown. Model metadata reports 4,414,806,160 weight-file bytes;
this is file size, not measured resident or peak memory. Aggregate token counts
are exposed; native token IDs and actual finish reason are not.

The preserved V1 source-free strict gate has **three** returned probes, only one
passing its required format. They use **415 input / 299 output tokens**, summed
latency **2.937 s**. V1 collected no selected questions. V2 reused those probes
after a disclosed availability-gate amendment; do not count them as new V2 calls.
Provider spending is zero for this local extension; local economic cost is not
measured. Evidence: [results and amendment history](MODEL_GRADING_LMSTUDIO_RESULTS_V2.md),
V2 `receipt.json`/`freeze.json`, and V1 `preflight.json`.

## Local JSON interface: 256 attempts, 141 successful generations

Each checkpoint is scheduled on 32 questions crossed with four conditions.
Both use cached pinned checkpoints, FP16 MPS, native chat templates/tokenizers,
greedy decoding, maximum 512 new tokens, and no context truncation or CPU fallback.
The freeze records Python 3.13.2, PyTorch 2.10.0 and Transformers 4.56.2.

| Checkpoint | Attempts | Successful | OOM failures | Observed input / output tokens | Collection span, s | Summed successful latency, s |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3 1.7B | 128 | 128 | 0 | 153,604 / 12,905 | 658.043 | 657.130 |
| SmolLM2 1.7B Instruct | 128 | 13 | 115 | 22,389 / 3,717 | 134.199 | 133.236 |

Qwen's span is 07:03:37.892235–07:14:35.934914 UTC; Smol's is
07:14:58.490668–07:17:12.689961 UTC on September 30. Smol's failed rows have no
invented generation time or token count: its totals cover only 13 successful
generations. All 256 inputs had separate native-token parity/context-budget
audits; that does not make the 115 failed generations token-accounted. Three
Qwen and seven Smol successful generations reach the cap.

Source-free readiness probes additionally record Qwen **253 / 26** and Smol
**262 / 24** input/output tokens, with latencies **1.379 / 1.151 s**. Both generate
but fail their requested output schema. A preceding environment error generated
zero answers; its elapsed resource consumption is not recorded. These are
retained feasibility failures, not exclusions from the financial panel.

Two later source-free long-context diagnostics each complete one of six planned
probes before their declared memory stop. Each uses **2,261 input / 512 output
tokens**, with latencies **37.411 / 36.892 s**. Driver allocation after cleanup
is **42,248,503,296 / 41,225,093,120 bytes** (39.35 / 38.40 GiB). These backend
readings are not a physical-RAM census or a causal explanation of the OOMs.
No selected question is retried. Provider charge is zero; local electricity and
hardware cost remain unmeasured. Evidence: [results](FINANCE_LOCAL_INTERFACE_RESULTS_V1.md),
[independent saved-record checks](FINANCE_LOCAL_INTERFACE_FINAL_VALIDATION_V1.md),
and the two source-free diagnostic JSONs.

## GEPA V1 failure, V2 completion and heldouts

Official GEPA 0.1.1 adapts prompts with two optimizer seeds per objective. Actor
and reflection use the same fixed DeepSeek route: actor temperature 0/512-token
cap; reflection temperature 0.7/1,536-token cap. Each arm has a 256-metric-call
ceiling, 16-reflection ceiling and 40-iteration ceiling. Reflection is additional
compute; metric-call ceilings are not all-API-call ceilings. Peak recorded
global egress overlap is four. Remote hardware and memory remain unknown.

| Attempt/stage | API attempts | Observed input tokens | Observed output tokens | Accounted USD |
|---|---:|---:|---:|---:|
| V1 preflight | 16 | 2,880 | 2,929 | 0.001976100 |
| V1 optimizer actor | 380 | 93,245 | 68,457 | 0.052902395 |
| V1 reflection | 63 | 69,475 | 38,962 | 0.034358065 |
| V2 preflight | 16 | 2,880 | 2,865 | 0.001949220 |
| V2 optimizer actor | 430 | 122,473 | 79,757 | 0.066855796 |
| V2 reflection | 64 | 71,737 | 39,714 | 0.036953833 |
| V2 heldout answers | 432 | 87,528 | 81,868 | 0.057054312 |

V1 retains **459** API records: **165,600 / 110,348** observed input/output tokens,
summed request latency **15,962.293 s**, reported/accounted cost
**USD 0.089236560**. All records report usage and a normal stop. Logging failed
before holdouts; three actor calls lack saved optimizer-evaluation rows but remain
in the API ledger and billing. V1 collection wall time is not established here.

V2 retains **942** API records: **938** reported-usage returns and four transport
errors (three actor, one reflection), with **284,618 / 204,204** observed tokens
and summed request latency **24,932.077 s**. Missing timeout usage is not zero.
Reported cost is **USD 0.159481742**, plus **USD 0.003331419** reserved worst-case
debits for unknown billing, giving accounted cost **USD 0.162813161**. These
reserved debits are budget accounting, not verified invoices.

V2's recorded egress span is **3,997.532 s**: September 29,
21:28:30.911126–22:35:08.442698 UTC. `runtime.json`'s 7,269.932 s measures elapsed
time since the **original V1 freeze**, including the interruption/reexecution
interval; it is not V2 collection wall time. Both attempts together account for
**USD 0.252049721**, against the cumulative USD 0.90 cap. This is a GEPA-only
accounting subtotal, not a project total.

V2's 541 optimizer metric rows include **111 overlong-proposal placeholders**
without API requests. Its 878 actor occurrences comprise 16 preflight, 430
optimizer and 432 holdout calls. All 432 holdout calls return normally: six
strategies over the same 72 questions, not 432 independent questions. Neither
seed passes the declared consequence/repair gates. No weight training or new
inference was performed by the reporting/occurrence validators.
Evidence: [independent result and cost accounting](FINANCE_ADAPTATION_INDEPENDENT_RESULTS.md),
[execution amendment](FINANCE_ADAPTATION_EXECUTION_AMENDMENT.md), and V2
`runtime.json`/`egress_slots.jsonl`. Stage classification is literal: `preflight:`
prefix, `:reflection` suffix, `:evaluation-` infix, otherwise V2 holdout.

## Ledger identities and remaining reporting gaps

SHA-256 binds the exact files aggregated above. Paths below are relative to this
research repository, not to a competition public repository.

| Evidence path | SHA-256 |
|---|---|
| `outputs/model-grading-v1/qwen3-1.7b_responses.jsonl` | `948d2cf051eebcd0efa0a724b3aa89cc0072a4e129b148bc654fc5d96c197fca` |
| `outputs/model-grading-v1/qwen3-4b_responses.jsonl` | `99a3726a81714f49e0466075608e15968445da055584dd894580871185d943db` |
| `outputs/model-grading-v1/qwen2.5-coder-3b_responses.jsonl` | `f97ff5037adfd357c4f15891815d65b134dd1fe829bf488464ff68f3a22cf0fc` |
| `outputs/model-grading-v1/deepseek-v3.2_responses.jsonl` | `5afcd697c9a99869519a95a4ea0d028eec38220cfde4b7540dda2fe18b6ee6e0` |
| `outputs/model-grading-lmstudio-v2/responses.jsonl` | `2363316c9459492ac7018058126ed1bc14ac8c7009f0edb4ee705cf18d51bcc0` |
| `outputs/finance-local-interface-v1/responses_qwen3-1.7b.jsonl` | `0868aea0afc5edce4793dabd9b30623cb926406d1fc4937551b2fb2b65c8746a` |
| `outputs/finance-local-interface-v1/responses_smollm2-1.7b.jsonl` | `11f620e4b002cb6f64fa00784cca069f295752eea7a0f2e924001add403b71dd` |
| `outputs/finance-adaptation-v1/api_calls.jsonl` | `ca6d73475cb12c326090dff5488801651a65b3c9fcc8bbb8e0b55c8b2ffec2e1` |
| `outputs/finance-adaptation-v2/api_calls.jsonl` | `d8eb659fc733384cc581fc223a44afd67d9306a76dd36688ea39bfde15fe554f` |
| `outputs/finance-adaptation-v2/egress_slots.jsonl` | `e9c9354828f1599e0f0fa729b2fbe499c8383d1585d0d5c3334e2437e148ed50` |

This inventory excludes the ongoing 32-question collection, the older remote
96-question study, market-cycle/MarS/looped pilots, literature retrieval, artifact
builds and development outside these ledgers. It does not estimate their cost.
The older runs also lack continuous power/peak-memory accounting and complete
preliminary-run timing. Adding a closed new-study receipt later is a reporting
extension; it must not rewrite these historical rows or imply the excluded work
was free. Formal checklist completion still needs author-reviewed consistency,
honest per-experiment resource gaps and an explicitly scoped total.

At final iteration review, the newer V1 quantity panel has completed and its
separate V2 judge diagnostic has stopped with one unknown charge. Its measured
tokens/timing and known-versus-reserved accounting are in
[FINANCE_QUANTITY_TRANSFER_INDEPENDENT_RESULTS_V1.md](FINANCE_QUANTITY_TRANSFER_INDEPENDENT_RESULTS_V1.md).
This later status note does not change the historical ledger totals above.
