## Executive summary (read this first)

This review records the September 27 CLMM-specific adversarial pass. The user's `orca_clmm_agent` was offered as an example of a financial harness, not a request to select CLMM as the lead. A [broader cross-topic review](BROAD_TOPIC_REVIEW_2026-09-27.md) supersedes its ranking. The CLMM experiment remains a possible later project with no result. The existing Track 2 report audit is too narrow and incompletely reproducible; generic crypto agents, safe concentrated-liquidity agents, and retry benchmarks have close predecessors.

## Decision frame

Question: What can we contribute that changes what a finance-agent researcher can measure or conclude, beyond a new harness implementation? The desired contribution is a public, reproducible test of **trajectory-level economic safety** for concentrated-liquidity agents: every action may satisfy a transaction-level policy, yet the sequence may exhaust a fee budget, increase inventory concentration, churn ranges, or leave a position exposed after partial rebalancing. The agent's `orca_clmm_agent` supplies engineering context and a decision-loop design; it is not itself a benchmark dataset or evidence of research efficacy. Private runtime logs are excluded unless their release is explicitly cleared.

### Geometry intuition

Imagine every allowed single action as a point inside a safe region. A transaction gate checks each point. The paper question is about the **path** connecting those points. A path can stay inside the per-action region while accumulating cost or exposure that crosses a *trajectory* boundary. In a concentrated-liquidity position, the path includes inventory, range, fee income, gas, and unrealized loss, not only the last transaction's validity. This analogy suggests a measurable failure mode; it does not establish novelty by itself.

## Closest work and collision test

| Primary work | What it already demonstrates | Boundary for our claim |
|---|---|---|
| [PACE (2026)](https://arxiv.org/abs/2608.17220) | Typed DeFi intents, deterministic policy checks, simulation-bound signed approvals, a 40-task/2,800-trial safety evaluation. Its full text explicitly admits policy-valid harmful actions, including a multi-leg drain, and identifies multi-step analysis as future work. | A single-action policy gate or stale-simulation test is not new. Test cumulative *economic* harm with a realistic protocol state machine, not just a new rule list. PACE's main sandbox is in-memory; its paper also has auxiliary live-model/on-chain work. |
| [Arcifa et al., IEEE Access 2026](https://doi.org/10.1109/ACCESS.2026.3690467) | Peer-reviewed LLM orchestrator for concentrated-liquidity management with deterministic gates, 2025 replay, and 351 live decisions from two vaults. | “LLM plus safe CLMM harness” is directly preempted. A paper needs a distinct counterfactual, comparable baselines, and outcome analysis. The IU EBSCO record and author manuscript text were reviewed; the IEEE PDF was not locally cached. |
| [NexBench](https://github.com/Nexis-AI/NexBench) | 214 on-chain tasks, deterministic forked environments, poststate verifiers, DeFi operations, safety and reliability metrics. | “First on-chain agent benchmark” is false. Publicly runnable subset is six tasks; full suite uses a separate reference pack. Compare exact coverage before claiming a new benchmark. |
| [IdempotencyBench (2026)](https://github.com/gssanjana4/idempotencybench) | 320 synthetic tasks with timeout-after-commit, retries, duplicate-effect rate, runtime receipts, and real-model experiments. | Ambiguous confirmation and duplicate retry are already measured. Its own limitations say longer conditional plans and real APIs remain lightly tested. |
| [Agent Crash Test](https://github.com/pavloparaschakis/agent-crash-test) | Local failure injection for stale reads, partial success, duplicate effects, and state contracts. | Generic “verify the effect” tooling is not new. Domain-specific economic trajectory semantics would have to carry the contribution. |
| [INTENT-TX-18K, NDSS LAST-X 2026](https://www.ndss-symposium.org/wp-content/uploads/lastx2026-46.pdf) | 18,000 real-protocol intent/transaction pairs with semantic alignment checking. | Pre-execution intent matching is covered. Our question must concern evolving portfolio state after otherwise aligned actions. |
| [Chionas et al. (2026)](https://arxiv.org/abs/2608.19389) | Interpretable RL for dynamic concentrated liquidity with risk/cost-aware baselines. | “Optimize CLMM ranges with RL” is established. Compare against deterministic and RL controls; do not equate LLM activity with added value. |
| [Chen et al. (2025)](https://arxiv.org/abs/2502.15865), [RISCTrade](https://risctrade.github.io/) | Finance-agent risk at workflow/system level and closed-loop risk-mandate evaluation are already proposed/tested. | “Risk-aware financial-agent benchmark” is too broad. Define the specific unmeasured economic mechanism and exact oracle. |
| [Yao & Zheng (2026)](https://arxiv.org/abs/2606.08285) | Review of execution realism and reproducibility assumptions in LLM trading papers. | Execution timing, costs, and artifact release are methodological requirements, not novelty claims. |

The table is a search result and full-text review of selected close works, not an exhaustive systematic review. Priority cannot be asserted from a finite search.

## Candidate research question and falsifiable hypotheses

**RQ:** In a replayable concentrated-liquidity environment, how often do individually policy-valid actions produce a trajectory that violates a predeclared economic mandate, and can a stateful trajectory gate prevent this without blocking economically useful rebalances?

- H1: A per-transaction gate has nonzero trajectory-level mandate violations under controlled multi-step stress cases.
- H2: A stateful gate using cumulative cost, inventory, and position state reduces violations relative to the same agent and per-transaction gate.
- H3: A simple deterministic policy is a serious competitor to an LLM planner on mandate adherence and net value. A result where the LLM adds no value is scientifically informative and must be reportable.

These are hypotheses, not findings. Avoid claiming a stateful gate is a new algorithm unless its mechanism differs materially from existing budget/portfolio constraints.

## Minimal study design that could justify a short paper

1. **Freeze one protocol and mandate.** Use Orca Whirlpool if its open tooling supports faithful, locally replayable position mechanics; otherwise use an open Uniswap v3 implementation and state the scope. Predeclare starting assets, range, fee tier, gas, maximum total spend, inventory concentration, and action horizon.
2. **Create paired episodes.** For each initial state, run a benign path and a matched path with one controlled perturbation (price jump, range exit, fee/gas spike, interrupted rebalance, or delayed state observation). The oracle checks the final state and full path, not natural-language reasoning. Do not use private competition exam units or pretend synthetic prices are real market evidence.
3. **Cross planner and gate.** Compare a deterministic hold/rebalance policy, a prompt-only agent, an LLM plus per-transaction gate, and the same LLM plus stateful trajectory gate. Hold model, prompts, tools, starting states, time budget, and seeds fixed for gate contrasts. Report all attempted episodes and errors.
4. **Score separately.** Primary: mandate-violation rate per independent episode. Secondary: net-of-cost portfolio value, unnecessary abstentions, missed rebalances, duplicate effects, model/tool cost, and latency. Report a Pareto trade-off rather than hiding safety behind a weighted scalar.
5. **Validate mechanics.** Verify pool arithmetic and fee accounting against the protocol's reference implementation or independently checkable transaction traces. Use held-out episode families; tune on development episodes only. Cluster uncertainty by market path or starting episode, not by dependent decision step.
6. **Artifact.** Release scenario definitions, fixed seeds, version/commit hashes, agent prompts and tool schemas, full allowed traces, oracle code, and a claim-to-run table. Link paper statements to run IDs and preserve the code decision history, following ARA-style reproducibility as a research practice.

### Stop criteria before submission

- No reproducible protocol mechanics or independent oracle by September 29: **do not submit empirical claims**.
- Only synthetic one-step examples or one agent/no baseline: **not sufficient for a research-paper claim**.
- No distinct outcome after comparison with PACE, Arcifa, NexBench, and IdempotencyBench: **do not claim novelty**.
- Private logs, unknown data rights, or competition firewall doubt: **exclude those artifacts**.
- Strong result but inadequate time for independent review: submit only if the paper precisely states exploratory scope; acceptance remains uncertain.

## Historical CLMM-focused ranking, superseded by broader review

1. **Trajectory-level economic safety for CLMM agents:** strongest conceptual opening, with an explicit PACE future-work boundary and relevance to Agenthon's agent verification theme. **Feasibility risk: very high** in three days; current status is a study design, not a submission-ready paper.
2. **Track 2 source-linked forecast-selection case study:** excellent local and track fit, but novelty is thin and raw outputs/chronology remain incomplete. The existing [proposal](PROPOSAL.md) correctly marks it no-go as an empirical results paper until evidence is recovered.
3. **Timestamped text uplift/counterfactual forecast evidence:** direct Track 2 fit, but TimeLitmus and Semantics or Structure? already cover broad interventions. A fresh *causal* information-availability protocol would need substantial data and an experimentally distinct hypothesis.

The Agenthon CFP welcomes agentic finance software, market simulation, RL, and evaluation/benchmarks; this trajectory study is cross-track workshop relevant rather than a submission to a competition track. The CFP specifies accepted **posters**, not an oral route. A rigorous study increases the chance of acceptance but cannot make acceptance “expected and confident” before results and review. It is better to miss this call than submit an under-evidenced near-duplicate.

## Access and verification notes

- Searched the IU EBSCO Discovery Service on September 27 for the exact titles of the 2026 IEEE Access CLMM-agent paper and the Springer *Digital Finance* CLMM-model paper. Both appeared as peer-reviewed journal records; both are open access. The Springer published PDF was downloaded through its publisher link. IU did not provide exclusive gated content for these two sources.
- The IEEE Xplore page for Arcifa et al. is publicly marked open access and exposes the article text. Direct terminal PDF retrieval returned HTTP 418; no local PDF is claimed. The author manuscript text on ResearchGate was used only to inspect sections beyond the publisher abstract. EBSCO's ACM RecSys counterfactual-audit record still led to an ACM page requiring sign-in; only its abstract is verified.
- Public PDFs of PACE, the NDSS LAST-X paper, Chionas et al., the Springer paper, IdempotencyBench, Chen et al., and Yao & Zheng were downloaded to ignored `literature/pdfs/` and confirmed as PDF files. Local copies are for research; do not publish licensed PDFs in the GitHub repository.
- The search reviewed close papers across publisher pages, a peer-reviewed proceedings PDF, arXiv full texts, public benchmark repositories, and IU catalogue records. A full systematic review and protocol-implementation audit remain outstanding.
