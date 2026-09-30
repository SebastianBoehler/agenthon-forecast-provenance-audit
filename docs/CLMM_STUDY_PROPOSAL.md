## Executive summary (read this first)

**Status: candidate study, not an empirical paper.** The proposed contribution is a reproducible, protocol-grounded evaluation of *action-induced trajectory risk* in concentrated-liquidity (CLMM) agents. A transaction can pass simulation, spend, and slippage checks while a sequence of such actions leaves the portfolio worse off or outside a predeclared mandate. The key comparison holds the market path fixed and asks what the agent's actions add beyond the risk of simply holding the position. This avoids calling a price-driven range exit an agent failure. We should write a results paper for Agenthon only if the preregistered pilot below produces independently checked, nontrivial evidence by the September 30 deadline.

## Research question and contribution

**Question.** Under matched market paths and initial positions, how often do transaction-valid CLMM agent trajectories cause *incremental* mandate violations, and how much useful rebalancing does a trajectory-aware gate preserve relative to transaction-only gating?

The possible contribution has three parts, each conditional on evidence:

1. A public set of replayable, multi-decision CLMM scenarios with a reference state transition, action log, and executable mandate oracle.
2. A paired measurement of action-induced violations: compare each agent path with hold and deterministic-rebalance controls on the same exogenous path and initial state.
3. A measured safety–utility frontier for transaction-only versus stateful trajectory gates, including blocked useful actions, fees, latency, and net terminal value.

This is a **benchmark and empirical evaluation**, not a claim that cumulative budgets or risk constraints are new algorithms. The user's [`orca_clmm_agent`](https://github.com/sebastianboehler/orca_clmm_agent) is a design reference and candidate adapter. Its README already recommends daily spend/loss and position checks; do not misrepresent them as absent. Do not use private wallet logs or live funds for this study.

## Geometry intuition

Each valid trade is a point inside a transaction's allowed region. A portfolio is a *path* through states: inventory, active range, paid costs, and exit capacity evolve after every action and price move. The research question is whether the path crosses a predeclared boundary **because of the agent's choices**, compared with the hold path exposed to the identical market moves. A stateful gate may shorten or redirect the path, but it may also block profitable rebalances; both effects must be measured.

## Closest work and precise boundary

| Work | Already covers | What this study would have to add |
|---|---|---|
| [PACE (2026)](https://arxiv.org/abs/2608.17220) | Typed DeFi intents, signed transaction-level approval, simulation binding; its paper explicitly includes policy-valid harmful legs and leaves multi-step analysis open. | Protocol-grounded *economic trajectories*, matched hold controls, and quantified safety–utility, not another single-transaction guard. |
| [Arcifa et al. (2026)](https://doi.org/10.1109/ACCESS.2026.3690467) | LLM orchestration of CLMM management with deterministic risk gates and replay/live decisions. | A frozen intervention design across the **same** decisions and market paths; independent oracle; specific path failures their evaluation does not measure. Full published text should be checked again before a priority claim. |
| [Chionas et al. (2026)](https://arxiv.org/abs/2608.19389) | Sequential CLMM allocation, risk and transaction costs, RL and sophisticated strategy baselines. | Evaluation of agent action approval and mandate breach, while taking their strategy baselines seriously. Do not claim dynamic CLMM control is new. |
| [NexBench](https://github.com/Nexis-AI/NexBench), [IdempotencyBench](https://github.com/gssanjana4/idempotencybench) | On-chain tasks/poststate verification and duplicate effects after retries. | A different failure mechanism: cumulative portfolio economics after valid actions, with a CLMM state model. |

The existing [adversarial idea review](IDEA_REVIEW_2026-09-27.md) records more source detail. This finite comparison cannot establish a “first” claim. The September 27 source inspection confirms PACE's explicit multi-step limitation and Chionas's sequential risk/cost treatment; Arcifa's publisher PDF is still not locally available, so its exact overlap remains an open review item.

## Research design, methods, and planned paper

The research design is a **controlled, paired benchmark study**. Freeze scenario families, mandates, agent prompts, decision opportunities, and inclusion rules before scoring. Use one CLMM protocol implementation, one pool/fee-tier setting first, and multiple independent market paths. The method is local replay: at each decision point, record state, proposed action, quote, transaction-level decision, execution result, and resulting portfolio state. A protocol reference implementation or independently checked arithmetic must validate position amounts and fees. The user-facing agent must have only information available at that decision time.

The primary unit is an **episode** (initial state plus market path), not each step or random seed. The primary contrast is the paired difference in action-induced mandate violation between the same planner under a transaction-only gate and a trajectory-aware gate. Hold and deterministic rebalance are economic controls. Report raw numerators/denominators and uncertainty clustered by exogenous path; do not turn repeated decisions on one path into independent samples. Secondary measures are net terminal value relative to hold, useful rebalance rate, abstention, transaction costs, model/tool costs, and latency.

The intended paper structure is: (1) exact failure mode and question; (2) prior-work comparison; (3) scenario and protocol mechanics; (4) frozen agent/gate comparisons and outcome definitions; (5) results with per-family failures and safety–utility plots; (6) validity limits; (7) claim-linked artifact and code history. A short paper could be appropriate **only after** a real experiment; the CFP's flexible length does not make an unevaluated proposal a competitive research result.

## Falsification and reviewer objections

- **Tautological safety:** a gate that directly enforces the scored threshold trivially wins. Primary evidence must instead characterize *existing transaction-valid paths* and the cost of avoiding them. Report the gate's false blocks and utility loss. Use some held-out stress families to assess generalization.
- **Existence is already known:** PACE supplies a policy-valid, harmful multi-leg example. One constructed CLMM counterexample would not be a new finding. The paper needs a representative, prespecified set of trajectories and a measured mechanism or trade-off that changes the conclusion from prior work.
- **Market risk mistaken for agent risk:** a hold path can breach inventory or value limits too. Report incremental breach under the identical price path; keep absolute breach as a secondary outcome.
- **Toy simulation:** synthetic shocks are acceptable only as labeled stress tests. Validate CLMM state transitions against protocol code or transaction traces; do not call toy prices real-market evidence.
- **Agentic relevance:** a deterministic pilot validates mechanics but cannot establish how an AI agent behaves. A paper about AI-agent failure needs a frozen, reproducible agent condition plus controls; otherwise frame the outcome as a protocol benchmark proposal, not an evaluated agent study.
- **Unfair agent comparison:** the gate contrast uses the same proposed action stream or common planner/model, decision schedule, information, and seed. If gating changes later proposals, report that mediation and replay the paired agent separately.
- **Cherry-picked cases:** freeze scenario generation and publish all attempts, including no-action and failed runs. Separate development from held-out cases.
- **Confidentiality:** no private Agenthon exam units, wallet secrets, raw live logs, or licensed PDFs in the public artifact.

## Decision milestones

| Date | Reviewable evidence | Stop condition |
|---|---|---|
| Sep 27 | Freeze this question and the [pilot preregistration](CLMM_PILOT_PREREGISTRATION.md); inspect protocol tools and nearest papers. | If Arcifa or another work already performs the same paired path evaluation, revise the claim. |
| Sep 28 | One end-to-end replay episode plus independent state/fee check and both hold and deterministic controls. | If mechanics cannot be checked, no empirical submission. |
| Sep 29 | Locked multi-episode run, raw result ledger, sensitivity checks, and an adversarial coauthor review. | If only hand-authored examples or no baseline survive, no results-paper claim. |
| Sep 30 | Claim-to-run audit, short PDF, source check, disclosure and form check. | Submit only if the result is nontrivial, reproducible, and honestly bounded. |

The [Agenthon CFP](https://www.agenthon.net/#call-for-papers) explicitly welcomes finance agents, sequential decisions, simulation, evaluation and benchmarks. It requests one PDF by September 30, 23:59 AoE; accepted submissions are in-person posters. Acceptance cannot be made confident before results and independent review.
