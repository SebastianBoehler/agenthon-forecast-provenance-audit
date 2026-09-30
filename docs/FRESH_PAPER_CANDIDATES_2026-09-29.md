## Executive summary (read this first)

The accepted user-turn paper is excluded from this decision. The earlier Track 3
proposal remains paused. Generic financial fine-tuning, reinforcement learning,
synthetic numerical benchmarks, and unit-aware counterfactual audits have close
precedents. The best current lead is a study of whether financial training rewards
measure correctness from the information actually shown to a model. This is a
conditional research recommendation, not a passed novelty gate or an acceptance
prediction. A fresh model-training project is less predictable within two days.

## Four concrete approaches

| Approach and question | Potential paper contribution | Closest collision | Deadline assessment |
|---|---|---|---|
| Reward-data validity: can a correct financial answer receive the wrong reward because rendered inputs differ from the answer generator's inputs? | Reproducible audit, explicit observability contract, measured false reward decisions and a validated repair | FinVerBench already studies rendering and observability; V-FiLLM already generates verified finance problems | Best preflight lead; one small dataset defect is insufficient |
| Controlled financial RL: do gains under the training reward survive an independent financial validator? | Matched SFT/RL experiment decomposing genuine improvement and evaluator-specific gain | Fin-R1, Fin-o1, DianJin, Trade-R1; generic finance RL and transfer loss already known | Stronger training extension, uncertain in two days without a ready GPU/pipeline |
| Constraint-composition transfer: do learned units, periods and entity constraints survive unseen combinations? | A held-out composition study identifying what training transfers and what requires explicit checks | V-FiLLM robustness/LoRA, FinReasoning modifications, FinMirror paired evidence worlds | Interesting longer project; high setup burden and substantial novelty collision |
| Learning versus harness: where do weight updates and executable checks complement each other? | Controlled interaction across base/tuned models and tool/no-tool conditions with equal information and budgets | Existing financial program/tool methods and modular-verification studies | Evaluation with compatible existing checkpoints may be feasible; causal training claims need matched checkpoints |

The ranking reflects evidence and delivery risk, not estimated acceptance rates.
Hugging Face provides implementation tooling; using a trainer is not itself a
scientific contribution. FinQA/OpenEnv explicitly designates its evaluation
dataset as evaluation-only, so it must not become our training split.

## Recommended short-paper question

**When execution-verified financial examples are converted into model-visible
questions, do the resulting rewards remain correct, and how can we repair and
independently validate that boundary?**

Working title: **Execution Is Not Enough: Auditing the Validity of Financial
Training Rewards.** This is a hypothesis-led title, not an established conclusion
about all datasets.

Concrete example from the initial dataset inspection: a question exposes cash
flow 740, discount rate 10.0%, and growth rate 3.5%. The corresponding solution
uses 9.95% and 3.46%. Computing from the displayed question gives approximately
11,384.62; computing from the hidden values gives approximately 11,402.16.
Execution can confirm the latter code calculation while failing to establish
that it answers the former question. Whether this causes a wrong reward decision
depends on the actual reward's tolerance and rounding policy. A discrepancy
alone does not prove a training failure or reward rejection.

For geometric intuition, the generator works at a precise point and the rendered
question places the model at a nearby point. The evaluator may still grade it
against the original point. Near a financial formula's steep regions, a small
input displacement can create a large output displacement. We would measure the
gap between the information surface and the reward surface, then align them.

## What would make this a substantial contribution?

1. Establish a failure class across independently sourced examples or generators,
   rather than inspecting only a tiny three-formula dataset.
2. Separate numerical disagreement, ambiguity and actual false acceptance or
   rejection under documented reward tolerances.
3. Measure consequences for model evaluation or training signals on genuine
   outputs; use no fabricated model performance or hypothetical rank reversals.
4. Repair the rendering/reward contract and independently check the repair,
   preserving valid alternative answers and explicit rounding conventions.
5. Release a legally distributable audit tool and diagnostic cases, with pinned
   source revisions, case lineage, rejected hypotheses and reproducible results.

The novelty would be the demonstrated reward-validity phenomenon, its measured
consequence and validated intervention. Unit checks, symbolic generation,
reproducibility manifests and a new name are insufficient alone. FinVerBench is
a particularly close comparison and must be read fully before an absence claim.

## Academic decision gate before writing results

### Stage 1: evidence and nearest-work challenge

Read the closest full texts and artifacts. Write a comparison based on their
actual methods, not missing words in abstracts. Check references and version
history. Treat repositories/model cards as prior public artifacts without
equating them to peer-reviewed empirical evidence.

### Stage 2: prespecified diagnostic

Freeze public source revisions and inclusion rules. Reconstruct calculations
from visible inputs without executing untrusted upstream code. Record meaningful
error thresholds and actual reward policies. Review ambiguous cases separately.
Find a second independent source before generalizing beyond a single artifact.

### Stage 3: contribution decision

Proceed with a short paper only if the effect matters to a stated use case and
survives the closest-work comparison. Narrow a single-source result honestly;
do not claim financial RL generally fails. Stop or change the question if the
effect disappears under legitimate tolerances or is already fully established.

### Stage 4: optional controlled training

Only after the preflight and compute readiness: use the same backbone, training
questions, development budget and held-out evaluation for an original-reward
versus repaired-reward comparison. Keep an unchanged model and SFT baseline.
Report compute, seeds and failures. Existing unrelated checkpoints cannot isolate
the causal effect of our reward change. A completed evaluation paper can stand
without RL; unfinished training must not be presented as evidence.

## Venue relationship

This addresses the Agenthon call's evaluation, verification and benchmarks for AI
in finance topic. It is adjacent to Track 1 financial calculation/code checking
and Track 4 evidence grounding. It is not a Track 2 forecasting submission or a
Track 3 simulator contribution. The paper call does not require competition
participation. The live call says accepted papers are posters; it gives no
published acceptance probability or oral-selection procedure.

## Sources and reading record

- [Financial RL review](FINANCE_RL_CANDIDATE_REVIEW_2026-09-29.md): reading status,
  exact versions, training designs and detailed collisions.
- [Benchmark review](FINANCE_BENCHMARK_CANDIDATE_REVIEW_2026-09-29.md): benchmark
  collisions and preliminary dataset audit, including source hashes and limits.
- [V-FiLLM](https://arxiv.org/abs/2608.11047): verified generation, perturbations
  and LoRA already exist. Full text read and PDF cached.
- [FinVerBench](https://arxiv.org/abs/2605.29586): observability and rounding change
  financial verification evaluation. Full HTML inspected in the benchmark review;
  its prior findings substantially constrain our novelty claim.
- [FinMirror](https://github.com/faceWang753/finmirror): paired finance evidence,
  provenance, abstention and evaluator assurance already public.
- [FinQA OpenEnv](https://huggingface.co/docs/openenv/environments/finqa): reward
  specification and evaluation-only data boundary.
- [Agenthon call](https://www.agenthon.net/#call-for-papers): scope and venue rules
  checked September 29, 2026.

Both reviews cached open PDFs and extracted texts in the existing ignored
literature folder, with some overlapping sources. IU authentication was not used
in this pass. No training or paid compute was launched. Initial dataset screening
is diagnostic evidence; it is not a completed model or training experiment.
