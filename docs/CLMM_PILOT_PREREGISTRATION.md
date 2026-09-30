## Executive summary (read this first)

This freezes the **first pilot's question, comparisons, outputs, and failure criteria before pilot results are inspected**. It is a study protocol, not a claim that scenarios, agents, or outcomes already exist. The decisive feasibility question is whether a multi-step CLMM replay can produce protocol-checked portfolio states and a paired hold control in time for an honest Agenthon paper.

## Scope and admissibility

- One documented concentrated-liquidity protocol and pool configuration; record exact SDK/program versions and fee tier. Prefer Orca Whirlpools only if position accounting can be independently checked locally. A change of protocol after looking at results starts a new, labeled exploratory study.
- No live transactions, real wallet keys, or private competition materials. Public historical price paths may be used only with documented provenance and timestamp availability. Generated paths must be labeled synthetic stress tests and cannot support real-market frequency claims.
- Decision opportunities, maximum horizon, initial state, all fee/slippage assumptions, and mandate thresholds are fixed in a machine-readable manifest before evaluation. No unseen future prices in agent observations.
- A pilot episode includes at least two decisions and a final state. A single trade cannot test the central path claim.

## Scenarios and controls

Use at least four distinct mechanism families in the development pilot: (1) alternating range exits/reentries that may cause churn, (2) directional movement and inventory concentration, (3) fee or execution-cost shock, (4) interrupted close/reopen or stale post-action state. Each family contains a benign paired path and a perturbed path sharing the same starting position. No outcome label is assigned solely from the perturbation name.

At every decision point compare: **hold**; a fixed, simple rebalance policy; a planner with transaction-only approval; and the *same planner* with transaction plus trajectory approval. Fix allowed actions and information. The planner may be deterministic for the first mechanics pilot; an LLM comparison is a later study stage, not something to claim from a deterministic pilot. A stateful gate's thresholds must be set on development paths, with an untouched path family or later time block reserved for evaluation.

## Mandate and outcome definitions

The mandate is fixed *before* observing path results. At minimum it specifies: cumulative external spend limit, maximum allocation to one token at decision checkpoints, minimum exit-fee reserve, and a maximum allowed cost of needless rebalances. Specify units and valuation currency. For each rule, define whether the baseline hold path can violate it through market movement alone. Do not equate terminal loss with a policy violation.

**Primary descriptive result:** among episodes where every submitted action passed the transaction gate, count the episodes whose agent trajectory breaches a mandate that the matched hold trajectory does not breach at the same checkpoint. Show each family and the full denominator; also report absolute breaches, including those shared with hold.

**Primary gate contrast:** paired difference in episode-level action-induced breach between transaction-only and trajectory-aware approval for the same planner and paths. Report uncertainty using the exogenous path as the cluster and explicitly label a small pilot descriptive. Do not report a general population rate from crafted stress cases.

**Utility:** mark each prevented breach alongside lost net value versus the transaction-only branch, feasible rebalances blocked, total fees, and decision latency. A gate that blocks everything fails the usefulness criterion even if its breach rate is zero. Report hold and deterministic-rebalance net value as context.

## Oracle and data integrity

1. Reconstruct token inventory, liquidity, fees, execution costs, and current range after each action and price move. Reconcile independently against the protocol reference arithmetic or a publicly inspectable transaction trace. If no such check is available, label the model unvalidated and stop paper-level result claims.
2. Keep an append-only, per-episode event log: input state hash, observation cutoff, proposed action, transaction gate verdict, trajectory gate verdict, accepted execution, resulting state hash, and oracle values. Failed and abstained actions remain in the denominator.
3. Hold exogenous path and initial state fixed across policies. Use common random numbers where sampling cannot be removed. Any downstream change in planner proposals after a blocked action is part of the treatment and must be recorded.
4. Maintain development/held-out manifests and a dated claim-to-run table. Pin dependencies, prompts, seeds, and code revisions. Preserve rejected ideas and failed runs as part of the research artifact, following [Agent-Native Research Artifacts](https://arxiv.org/abs/2604.24658) as reproducibility practice.

## Pilot pass/fail review

**Pass to expanded experiment** only if: the state/fee oracle is independently checked; one complete multi-decision episode is replayable from a clean checkout; hold and deterministic controls run on the same path; the transaction-only branch has a nontrivial, explainable result; and the claim survives comparison with [PACE](https://arxiv.org/abs/2608.17220), [Arcifa et al.](https://doi.org/10.1109/ACCESS.2026.3690467), and [Chionas et al.](https://arxiv.org/abs/2608.19389). This is a mechanics gate, **not** a paper-acceptance gate. Before an AI-agent results paper, run a frozen agent condition on a prespecified set of independent episodes and have an external reader audit at least the oracle and claim-to-run table.

**Stop or reframe** if only a threshold-enforcement demonstration is available, the result needs private wallet data, mechanics are unvalidated, the "agent failure" also occurs under hold, or there is no acceptable safety–utility tradeoff. A null result is reportable when the experiment is sound; it is not a reason to alter the mandate after seeing outcomes.
