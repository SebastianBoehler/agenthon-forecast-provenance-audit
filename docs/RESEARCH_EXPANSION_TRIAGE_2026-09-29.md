## Executive summary (read this first)

Keep the released-supervision audit as the paper's core. One bounded extension is
worth considering: optimize the same answering prompt against released financial
targets and against independently repaired targets, then measure financial
correctness on unseen operands and unseen wording. GEPA is the best fit for that
experiment because it changes prompts without updating model weights. This would
strengthen an empirical consequence claim if it passes the gates below. It would
not establish a new optimization method or a general financial benchmark.

Combining GEPA, world models, looped transformers and tiny reinforcement learning
(RL) would currently add several unrelated hypotheses. The missing contribution
is a consequential measurement with independent ground truth, not an architecture.
This is a research recommendation only; no new inference or training was run.

## What the current evidence supports

The [saved model study](MODEL_GRADING_RESULTS_V1.md) contains 800 responses from
four models on the same 200 questions. Changing the reconstructed grader reverses
two models' ordering on the constructed-Gordon family under post hoc numeric
recovery. It does not measure adaptation, training degradation or monetary harm.
Several local models also have severe final-answer formatting failures. Those
cannot be silently converted into evidence about financial reasoning.

The released binomial-call targets often represent financing debt instead of the
call price. Whole-unit Gordon targets conflict with the requested rounding.
These are observed release defects. DCF hidden precision is conditional on the
interpretation of printed inputs; avoid treating every printed number as uncertain.
The independent [novelty reassessment](INDEPENDENT_NOVELTY_REASSESSMENT_2026-09-29.md)
already establishes that precision, observability and label correction are prior art.

The [looped forecasting pilot](LOOPED_FORECAST_PILOT_RESULT_V1.md) failed its
text-benefit gate. The [MarS pilot](MARS_CYCLE_RESULTS_V3.md) found no demonstrated
action-response defect. Their infrastructure remains useful; their positive
hypotheses have not become results.

## Closest collisions, checked against primary sources

| Primary source | What it already establishes | Remaining distinction here |
|---|---|---|
| [Gao et al., reward overoptimization](https://arxiv.org/abs/2210.10760), 2022 | Optimizing an imperfect proxy can increase measured reward while degrading a separate gold reward, under RL and best-of-n selection. | Naturally occurring, traced defects in released financial supervision; the general dissociation is established. |
| [Egashira et al., *Delay, Plateau, or Collapse*](https://arxiv.org/html/2605.02909v2), COLM 2026, revised August 17 | Controlled arithmetic RLVR distinguishes systematic false negatives, false positives, plateaus and collapse. Error pattern matters beyond initial error rate. Section 4.6 already tests intermittent oracle correction. | Actual financial target corruption, its semantics, and repair under independent transfer tests. A synthetic wrong-reward RL demo would closely overlap. |
| [Shao et al., *Spurious Rewards*](https://arxiv.org/html/2506.10947v1), 2025 | Incorrect or random rewards can improve certain Qwen models; other model families behave differently. | Bad labels alone do not imply learning harm. Measure it and restrict claims to the tested actor and optimizer. |
| [Gallego, EPO-Safe](https://arxiv.org/html/2604.23210v1), ALA 2026 | Reflective prompt adaptation with reward alone can worsen hidden safety performance; a separate danger oracle supplies corrective information. | Financial correctness under real released labels. A second oracle channel plus reflection is already an existing pattern. |
| [FinVerBench](https://arxiv.org/html/2605.29586v1), 2026 | Observability exclusions and rounded/unrounded financial rendering change verification results. | The unit here is released training/preference supervision and its adaptation consequences, rather than injected statement errors. |
| [FinChain](https://aclanthology.org/2026.acl-long.662/), 2026; [FinanceReasoning](https://aclanthology.org/2025.acl-long.766/), 2025 | Existing financial datasets discuss hidden precision, representation checks, question repair and numerical grading. Their detailed overlap is recorded in the independent reassessment. | A reproducible external audit and consequential correction experiment; no first precision-contract claim. |

The newest direct collision is the August 2026 revision of *Delay, Plateau, or
Collapse*. Its experiments use Qwen3-1.7B-Base and OLMo3-7B, with additional
instruction-model and algorithm controls. Using a small Qwen model would not
distinguish our work by itself. Its discussion explicitly identifies experiments
on practical, interacting verifier failures as future work. Finance provides a
possible application of that gap, not proof of a novel general mechanism.

GEPA itself is established: the [paper](https://arxiv.org/abs/2507.19457), revised
February 14, 2026, and [official implementation](https://github.com/gepa-ai/gepa)
describe reflective prompt evolution with Pareto selection. The implementation
accepts an evaluation metric and exposes `max_metric_calls`. A call cap does not
bound tokens, money or elapsed time; those need separate accounting.

## Fit of the four proposed directions

| Direction | Scientific fit | Decision |
|---|---|---|
| GEPA prompt optimization | Directly tests whether an optimizer learns financial behavior that the released labels reward. The unchanged model allows a cheap, paired objective intervention. | Best bounded extension. Call it prompt adaptation, not RL training or a new GEPA method. |
| Tiny neural policy with PufferLib | [PufferLib](https://github.com/PufferAI/PufferLib) supplies efficient RL machinery. Choosing among a few precomputed financial formulas would be a contextual bandit; exhaustive action evaluation or supervised classification is a necessary simple baseline. | Reject formula-selection toy as the paper's new contribution. Useful only for a genuinely sequential problem with grounded observations and action costs. Local runtime compatibility is unverified. |
| Looped transformer | [LoopFormer](https://loopformer.github.io/) already studies budget-conditioned recurrent depth with compute-matched comparisons. Recurrence cannot supply information absent from a question. | No current mechanism connecting recurrence to these released-label defects. Would require clean/corrupt objectives, tied/untied equal-compute controls and transfer; current forecasting pilot failed. |
| Learned world model | [DreamerV3](https://www.nature.com/articles/s41586-025-08744-2) learns environment transitions and improves a policy through imagined trajectories. [MarS](https://github.com/microsoft/MarS) already applies generative models to market simulation. | The audit supplies no transitions or counterfactual action-response oracle. A simulator learned from these answers would manufacture a separate problem; existing MarS evidence does not justify it. |

A meaningful longer-term sequential extension could study when to acquire a
missing financial input before making a decision. It needs decision loss,
acquisition cost, independent financial scenarios and value-of-information
baselines. The existing reassessment notes the collision with
[Graph-Bounded Financial Reasoning](https://aclanthology.org/2026.acl-long.1273/).
That would be a separate research program, not a deadline repair.

## One bounded experiment with the highest immediate value

**Question:** Does prompt adaptation to the audited released targets change
financial correctness on unseen questions, and does repairing the objective
prevent that change? Use the four existing families: whole-unit Gordon, binomial
call, ordinary Gordon and WACC. The latter two are passing controls.

This is a proposed new freeze. The previous 200 questions have already been
examined and must not be called a fresh held-out set. Exclude those IDs and exact
operand tuples before deterministic selection. Keep the original study unchanged.

1. Freeze eight source questions per family for optimization and eight per family
   for development selection. Use a documented hash order, without conditioning
   selection on discrepancy size or actor success. Exact questions and operand
   tuples cannot cross partitions.
2. Freeze twelve further source questions per family as a 48-question numerical
   holdout. Their wording is inherited from the source, so this tests new operands,
   not unseen templates.
3. Separately freeze 24 transfer questions: three independently authored wording
   templates per family, with two new operand tuples each. No transfer wording or
   operand tuple may enter optimization or development. Retain the source financial
   meaning and explicit requested units/rounding. Specify the effective one-period
   rate for binomial questions to remove compounding ambiguity. Record researcher
   authorship and independent program review; do not claim expert annotation.
4. Use one fixed actor, preferably the existing DeepSeek route because it already
   computes almost all recovered answers correctly. Pin the provider as before and
   record returned identities. A dated API identifier is not immutable weights.
   Cached Qwen3-4B is an optional subsequent replication, not required for this pilot.
5. Compare the unchanged seed prompt and a frozen manual finance instruction with
   GEPA selected against released targets and GEPA selected against repaired targets.
   Run both objectives with two optimizer seeds and identical 256-metric-call caps.
   Keep the answer-format wrapper fixed. Never optimize parser code or the oracle.
6. Use the same strict extraction for both rewards. Released-target reward is a
   declared, reconstructed cent comparator; no executable upstream reward has been
   recovered. Repaired reward uses independently reviewed financial mathematics
   and the requested output projection. Forward only the assigned objective's
   feedback to the optimizer. The evaluation oracle remains separate.
7. Score every saved output against both targets. Report all-attempt parsing,
   financial validity, incorrect quantities accepted, requested-rounding violations,
   and the released-reward versus financial-validity trajectory. Report numerical
   holdout and wording transfer separately. Do not use raw per-row confidence
   intervals that pretend a handful of shared templates are independent.

The manual baseline is necessary: a simple correct formula and rounding instruction
may solve the problem. If it matches GEPA, the finding concerns the objective and
released targets; it is not evidence of an optimizer-specific advance.

The plan uses about 1,472 actor responses: 1,024 optimization evaluations, 432
holdout evaluations for six final prompts, and 16 format checks outside the splits.
At the study's logged prices, 1,200 input tokens and 256 output tokens per actor
call imply about $0.617. At most 32 reflection calls capped at 8,192 input and 1,024
output tokens add about $0.082 at those same prices. These are conditional bounds,
not a freshly quoted price or proof that each GEPA run needs only 32 reflections.
Enforce both token bounds and stop accounting before the remaining $1 budget is
exhausted; prohibit silent provider substitution. Recheck current prices before
execution. Existing raw ledgers show about 31.5 minutes for 200 Qwen3-4B responses
and 61.3 minutes for 200 serial DeepSeek responses. Allow a measured three-hour
pilot cap with bounded concurrency; cancel the optional extension if that cap fails.

## Success, kill gates and claim boundaries

- Before optimization, require at least 15 of 16 off-split format checks to parse
  under the fixed wrapper. If it fails, stop; do not tune extraction on the test.
- Before inference, verify binomial prices by replication and discounted expected
  payoff; verify rounding ties and WACC units independently. If independent
  derivations disagree, the oracle is not ready and the experiment stops.
- Evidence for an adaptation consequence requires increasing released-target reward
  alongside worsening financial validity on both numerical holdout and wording
  transfer, in both source-objective optimizer seeds. A finite pilot gate is a
  decision rule, not statistical evidence of population generality.
- Evidence for repair requires better transfer validity than source-objective
  optimization, with no deterioration on either passing family. Report every
  failure and seed, including a null effect or improvement under corrupted reward.
- If only formatting changes, only the old grader ordering reappears, transfer fails,
  or effects depend on selecting a favorable seed, keep the audit alone. A known
  wrong-label toy does not earn a method claim. If the optimizer never improves its
  assigned objective, the adaptation test is inconclusive rather than a negative
  result about label consequences.
- A benchmark claim needs more independent source releases, held-out financial
  mechanisms, documented labeling/adjudication, leakage checks and durable splits.
  Three authored wordings per family establish limited transfer within these
  calculations; they do not establish professional finance coverage.
- No result here measures weight-training harm, investor loss, market forecasting,
  simulator fidelity or general verifier accuracy. API and template dependence limit
  external validity. Keep the stronger audit paper ready for the existing deadline;
  include this extension only if its full independent checks finish in time.

## Access record

Primary pages were checked on September 29, 2026. New overlap checks used arXiv
abstracts and HTML, official GEPA/PufferLib/MarS repositories, the LoopFormer author
page and the published DreamerV3 article. The detailed existing finance-paper review
was reused where explicitly linked. This was targeted triage, not an exhaustive
proof of novelty. No new model calls, weight updates, manuscript edits, source-data
changes, public posting or contact with authors occurred.
