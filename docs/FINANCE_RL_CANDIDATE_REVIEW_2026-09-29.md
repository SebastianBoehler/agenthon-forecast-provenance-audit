## Executive summary (read this first)

Generic financial supervised fine-tuning (SFT), Group Relative Policy Optimization
(GRPO), numerical question answering, and deterministic finance benchmarks are
already established. Training another small finance model is not a sufficient
contribution. Two narrower directions remain worth a preflight: an independent
reward-validation audit, and an intervention study of semantic transfer after
post-training. Neither currently passes a novelty or evidence gate. No training,
inference, paid jobs, or experiments were launched for this review.

### Closest primary sources and reading state

| Work | What was actually inspected | What it already establishes / collision |
|---|---|---|
| [Fin-R1 v5](https://arxiv.org/html/2503.16252v5), March 2026 | Full text: data, training §4.2, evaluation; local PDF/text saved | Qwen2.5-7B SFT followed by GRPO on financial reasoning. Although the text describes rule-based rewards, accuracy is judged by Qwen2.5-Max semantic agreement; format is rule-based. Another finance-GRPO recipe is occupied. |
| [Fin-o1 v3](https://arxiv.org/html/2502.08127v3), June 2025 | Full text: rewards §3, tasks §4, experiments and appendix; local PDF/text saved | Finance corpus, SFT, RL-method comparison and FinReason. Accuracy/logic use GPT-4o, with format and context-length rewards. A four-component reward is already explored. |
| [Trade-R1 v2](https://arxiv.org/html/2601.03948v2), January 2026 | Full text: §3–4 and limitations; local PDF/text saved | Evidence/reasoning/decision consistency gates stochastic returns. Qwen3-8B full-parameter GRPO, eight rollouts per query, long contexts and a learned judge. Cross-market generalization already studied. Limited horizon and potential verifier gaming remain limitations, not proof of a new gap. |
| [DianJin-R1](https://arxiv.org/abs/2504.15716), April 2025 | PDF: reward design, experiments §4 and ablations; local PDF/text saved | Finance SFT plus GRPO. Its own 7B ablation reports FinQA dropping from 80.28 to 77.72 after RL, while other datasets improve. Therefore “RL does not always transfer in finance” is already known. |
| [V-FiLLM](https://arxiv.org/html/2608.11047v1), August 2026 | Full text: generation, robustness §5.2, LoRA §5.3; local PDF/text saved | Typed computation graphs, deterministic answers, controllable depth, unit/scale shifts, missing-value and other perturbations, verified-CoT LoRA plus FinQA evaluation. It directly preempts a generic unit-aware synthetic benchmark and low-cost adaptation claim. |
| [FinReasoning official repository](https://github.com/TongjiFinLab/FinReasoning/blob/main/README.md) | README task taxonomy and metrics; paper not close-read | Explicit value/unit/comparison modifications and complex financial calculation tasks. Repository claims are not independently reproduced. |
| [FinMirror](https://github.com/faceWang753/finmirror/blob/main/README.md) | Primary README including scope, assurance, model runs and roadmap | Paired evidence worlds, deterministic finance programs, provenance, abstention and evaluator mutation/equivalence checks. This is a repository artifact, not equivalent to a reviewed paper. It still preempts broad claims to invent these mechanisms. |
| [PIT Finance GRPO + Verifier](https://huggingface.co/NurErtug/pit-finance-grpo-merged) | Model card; weights/code not run | Financial GRPO model with numeric/NLI guards and abstention. Card reports intended architecture, not independently established performance. |
| [GBFR, ACL 2026](https://aclanthology.org/2026.acl-long.1273/) | Authoritative abstract/metadata only | Metric-graph financial calculation, multiple derivation paths, evidence absence versus retrieval failure, safe abstention and counterfactual unanswerability. Full text required before recommending an overlapping method. |

### Direction A: Does financial RL improve the task, or its reward evaluator?

**Research question.** How much of the apparent improvement after financial RL
survives evaluation by an independent, executable semantic checker, and does the
answer depend on which kinds of financial errors the training reward can observe?

**Potential contribution.** A controlled empirical decomposition of measured
post-training gains into genuine task improvement and evaluator-specific gain.
The useful deliverable is a finding about training and evaluation, supported by
an auditable cross-verifier dataset—not a new parser or an accuracy leaderboard.

**Experiment.** Use one fixed small backbone and the same financial questions for
SFT and a limited GRPO comparison. Separate a final-answer reward from a stricter
reward that verifies program execution and typed operands. Evaluate both with a
third independently implemented checker, plus manually reviewed diagnostic cases.
Hold out entire expression families and intervention classes, not merely numbers.
Preserve legitimate alternative formulas rather than checking literal programs.

**Why this might add something.** Fin-R1/Fin-o1 use learned answer judgments;
V-FiLLM verifies generated labels and studies adaptation. The specific remaining
question is whether reward-validator agreement predicts transfer of the policy.
This is an inference from a limited review, not a verified absence claim.
FinMirror already provides evaluator-assurance mechanisms, so using those alone
cannot be presented as the contribution.

**Empirical gate.** Before training, independently label a blinded sample of real
model outputs and financially valid/invalid mutations. Continue only if reward
disagreement is consequential, reproducible, and distinguishable from benign
format/rounding differences. After training, report reward success, semantic
correctness and their gap on the same cases. If the phenomenon is confined to
deliberately bad parsing, this is a software defect study and fails our intended
contribution threshold.

**Feasibility in 1–2 days.** Evaluation-only preflight is plausible with available
models and infrastructure. A reliable matched RL study is uncertain until GPU,
artifact, data, reward and runtime readiness are established. Existing models
alone cannot establish causal effects of training objectives.

### Direction B: Which financial constraints transfer after post-training?

**Research question.** Can small-model post-training learn financial semantic
constraints that transfer to unseen combinations of units, reporting periods,
and formula structures, or does it only learn the transformations it saw?

**Potential contribution.** An intervention matrix that separates transfer across
financial constraints from random-split accuracy, with a controlled explanation
of which training signal preserves transfer. Results must expose an actionable
boundary or establish a robust intervention—not merely show a score increase.

**Experiment.** Train on a disclosed subset of valid finance computation families.
Evaluate clean cases, seen transformations and held-out combinations using
independent inputs: preserve economic meaning under unit conversion; change the
answer under material operand replacement; reject incompatible period/entity
joins. Compare unchanged backbone, equal-data SFT, targeted RL, and an inference
harness with explicit typed checks. These comparisons separate information
provided by the harness from behavior acquired by model weights.

**Collision and remaining distinction.** V-FiLLM already tests unit/scale failures
and LoRA; DianJin already shows a transfer loss after RL. FinMirror already tests
typed evidence relations. Therefore “financial robustness” and “RL generalizes”
are unavailable headline claims. A held-out constraint-composition experiment
could contribute if it reveals a new mechanism or intervention with convincing
cross-family evidence. Merely adding more perturbations is insufficient.

**Empirical gate.** First verify that task generation preserves financial semantics,
that clean baseline performance is measurable, and that unseen compositions
cause a meaningful failure above A/A variation. Train only if a prespecified
intervention can discriminate a real hypothesis. Use separate development and
test groups; do not choose adapters by the eventual test score.

**Feasibility in 1–2 days.** A small diagnostic dataset and baseline evaluation
could be feasible. Matched SFT/RL plus enough independent runs to attribute
effects is high risk on this deadline. Presenting unfinished RL as evidence would
weaken the submission.

### Recommendation and contribution threshold

Direction A is the more direct academic question and easier to falsify before
spending GPU time. Direction B is attractive as a longer project, but has strong
nearest-work collisions and greater implementation scope. Neither justifies
confident acceptance today. Reject generic finance fine-tuning and generic
finance benchmarks as the primary contribution. Advance one candidate only
after a short diagnostic establishes a nontrivial phenomenon and a reviewer can
state exactly what existing work does not establish.

### Reproducibility and access record

New open PDFs and extracted texts are stored in the existing ignored
`literature/pdfs/`: 2503.16252v5, 2502.08127v3, 2601.03948v2,
2608.11047v1 and 2504.15716. These are open primary sources; IU authentication
was not used. Model weights and training datasets were not downloaded. Keep
paper-version IDs, dataset splits, checker revisions, artifact hashes, failures
and rejected experiments in the research artifact; avoid interpreting displayed
reasoning as proof of the model's internal causal reasoning.
