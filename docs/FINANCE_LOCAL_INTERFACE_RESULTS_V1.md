## Executive summary (read this first)

The frozen local pilot failed comparative feasibility. All 256 scheduled attempts
are recorded, but only 141 generations succeeded. Qwen completed 128; SmolLM2
completed 13 FinQA generations before 115 retained MPS out-of-memory failures.
Neither model produced a strict numerical answer under the frozen interface.
This is a runtime/interface floor, not evidence of equal financial capability,
absence of reminder effects, or a usable two-family benchmark result.

The [independent postflight check](FINANCE_LOCAL_INTERFACE_FINAL_VALIDATION_V1.md)
passes saved-artifact consistency. It verifies every attempted identity, failure
gate, score and aggregate, 41 frozen inputs and 19 checkpoint files. Independently
decoded native continuation IDs reproduce all 141 returned texts. Original
protocols, inputs, responses, scores and freezes remain unchanged.

## Frozen comparison and accounting

The [protocol](FINANCE_LOCAL_INTERFACE_PROTOCOL_V1.md) crosses compact/full JSON
with baseline/quantity-reminder instructions on 32 metadata-selected questions:
16 FinQA and 16 TAT-QA. Both models use their native tokenizer/chat template,
greedy FP16 MPS inference, 512 new tokens, no context truncation and no CPU fallback.
Full-output arms have the same pure-expression calculation grammar. Selection and
the 24-reference intersection (11 FinQA, 13 TAT-QA) precede model answers.

| Accounting | Qwen3-1.7B | SmolLM2-1.7B-Instruct |
|---|---:|---:|
| Attempted records | 128 | 128 |
| Successful generations | 128 | 13 |
| Runtime failures | 0 | 115 |
| Strict numerical answers | 0 | 0 |
| Status-only numerical recoveries | 6 | 0 |
| Locked matches after status-only recovery | 0 | 0 |
| Length-capped successful generations | 3 | 7 |

Qwen's six status-only recoveries are 3/2/0/1 in compact baseline/reminder and
full baseline/reminder order; values, units and scales are untouched. None matches
the fixed reference endpoint. This recovery does not replace the strict result.
Smol's 13 successes comprise three complete FinQA case blocks and one condition
of the fourth, with 3/3/3/4 successes per condition. All 64 Smol TAT-QA attempts
fail. Its first OOM is attempt 14; every subsequent attempt retains its error.
Failed generations have no invented answer or completion-token count.

All 256 precollection native-token audits pass. Explicit chat-template tokenization
matches rendered-template tokenization without added special tokens; the older
default tokenization path also matches for these inputs. Maximum input lengths
are 2,237 Qwen and 2,283 Smol tokens, within their recorded context limits.
This provides no evidence of an encoding defect and is not a research finding.

## Separate source-free runtime diagnosis

After collection, `scripts/diagnose_finance_local_mps.py` uses authored inventory
contexts, not selected financial questions. Both runs retain their actual texts,
continuation IDs and memory readings. Neither retries or repairs V1 answers.

| Diagnostic | Planned probes | Completed before resource stop | Driver allocation after cleanup |
|---|---:|---:|---:|
| Unchanged runtime | 6 | 1 | 42,248,503,296 bytes (39.35 GiB) |
| Explicit garbage collection and MPS empty-cache | 6 | 1 | 41,225,093,120 bytes (38.40 GiB) |

Each stops at the declared 10 GiB driver-allocation threshold after one successful
generation. Explicit cache cleanup does not establish a sustained-runtime fix.
These readings locate a resource problem under this collector/backend; they do
not isolate its causal mechanism, validate financial quality or diagnose every
MPS workload. No memory-watermark relaxation or CPU fallback was used.

## Consequence for the paper and follow-up

Keep the failed pilot in an appendix and the reproducibility record. Its results
must not be presented as 256 completed answers, a successful family replication,
or an effective NLP repair. The earlier four-model synthetic panel and separate
96-question remote document panel retain their own endpoints and limitations.

A further local collector study needs a new protocol, sustained long-context
source-free readiness tests and a functioning output interface before financial
collection. Do not tune on successful V1 cases or silently rerun its failed cases.
This would establish feasibility; substantive novelty still requires semantic
quantity checks and useful performance on unused report/context groups.

Saved evidence lives under `outputs/finance-local-interface-v1/`: `freeze.json`,
both response ledgers/completion receipts, `scores.jsonl`, `results.json`,
`independent_postflight_validation.json` and the two source-free diagnostics.
The completed V1 integrity check is separate from later runtime diagnosis and
from expert semantic adjudication, which has not been performed.
