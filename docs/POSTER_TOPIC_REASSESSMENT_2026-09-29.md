## Executive summary (read this first)

Novelty takes priority over deadline convenience. The previous constraint-training
proposal has substantial overlap and is not selected. A stronger provisional
candidate audits and repairs action-induced inconsistencies in learned financial
market simulators using closed trading cycles. The proposed contribution is an
economically grounded validation and correction method with controlled evidence.
No simulator defect, correction benefit, or publication novelty is established.
Workshop precedents clarify possible contribution types; they cannot guarantee
Agenthon acceptance or supply an acceptance probability.

See the [accepted-paper evidence review](WORKSHOP_ACCEPTED_PAPER_COMPARISON_2026-09-29.md)
and the [new-gap source review](NEW_FINANCE_GAPS_REVIEW_2026-09-29.md) for reading
status, cached sources and further rejected candidates.

## Accepted-paper comparison

Agenthon describes 2026 as its first NeurIPS edition. Its 2025 predecessor is not
a historical sample of the same paper workshop. Use the officially listed
NeurIPS 2025 Generative AI in Finance papers as a comparable, distinct venue:
[accepted roster](https://sites.google.com/view/neurips-25-gen-ai-in-finance/accepted-papers).

- **The Losing Winner**: a focused empirical negative finding about market
  prediction versus economic returns; [paper](https://openreview.net/pdf?id=FzahgVWy59).
- **FinAgentBench**: a dataset and evaluation contribution separating document
  selection from passage selection, including fine-tuning;
  [paper](https://arxiv.org/abs/2508.14052).
- **Robust Decisions via Generative Wasserstein Distributionally Robust
  Optimization**: a method combining conditional generation, robustness and
  end-to-end learning, with theory and battery-storage experiments;
  [accepted paper](https://openreview.net/pdf/16d415900385039eac1074b828bd3428af0b899f.pdf).

Inference: a bounded negative result, a validated benchmark, and a focused method
can all be legitimate workshop contributions. Their acceptance does not reveal
the rejection pool, acceptance rate, or the organizers' causal selection rule.
Do not confuse workshop inclusion with main-conference acceptance.

## Preferred candidate: closed-cycle consistency in market world models

**Question:** Do learned market simulators admit action-induced profitable closed
trading cycles in settings where a validated reference model rules them out, and
can we correct the inconsistency without sacrificing useful market fidelity?

Working title: **Realistic Prices, Inconsistent Responses: Closed-Cycle Audits
for Financial World Models.** This title must change if the hypothesized failure
does not occur. A world model here means an action-conditioned learned simulator,
not an ordinary price forecaster.

### Concrete experiment

An agent buys, waits, sells and ends with zero inventory. Repeat and reverse
controlled schedules; account for actual execution prices, spreads, fees, partial
fills, latency and inventory constraints. Pair exogenous randomness across the
learned and reference environments where coupling is legitimate. Hold out entire
schedule families, market conditions and random seeds from adaptive search.

Start with a specified no-signal, martingale reference regime whose impact model
satisfies the appropriate no-manipulation conditions. Profits from predictive
information, legitimate liquidity provision, or genuine reference-market
manipulation are not evidence of a learned-model defect. Positive sample PnL alone
is insufficient. Net-zero inventory does not imply zero risk or no information.

### Proposed contribution package

1. A precisely scoped closed-cycle audit with a known-valid reference and known
   invalid positive controls, capable of separating accounting bugs, stochastic
   profit and model-induced response errors.
2. Empirical evidence that selected conventional fidelity measures can miss a
   consequential closed-loop inconsistency. This finding requires actual models;
   it cannot be assumed from general world-model arguments.
3. An explicit response correction or training constraint, compared with matched
   unconstrained training and simple clipping/penalty baselines. Measure both
   economic consistency and held-out predictive/market fidelity.
4. A reusable, source-versioned benchmark artifact and complete failed searches,
   accounting traces, model revisions and code evolution.

A benchmark plus a demonstrated failure mechanism and effective correction is
more substantial than adding one metric. If existing work already establishes
this package, the candidate fails the novelty gate. If all tested models pass,
report that honestly; a dataset of unsuccessful attacks alone may not satisfy
the intended contribution threshold.

### Geometry intuition

Observational fidelity checks how plausible a route through market states looks.
The proposed audit asks how the learned system responds when our actions trace a
closed loop. A response inconsistency can create an artificial cash gain while
inventory returns to its start. The analogy is circulation around a loop, but
dynamic market impact, noise and trading costs must be modeled explicitly; this
is not a claim that market dynamics form a conservative vector field.

## Closest work: what we cannot claim

| Primary source | Existing contribution | Required distinction |
|---|---|---|
| [Gatheral 2010](https://doi.org/10.1080/14697680903373692) | No-dynamic-arbitrage restrictions on market impact and decay | We do not invent no-manipulation or round-trip tests |
| [MarS](https://arxiv.org/abs/2409.07486) | Generative financial market simulator, market-impact and RL experiments | Test and repair a specific action-response failure, not introduce another simulator |
| [TRADES](https://doi.org/10.3233/FAIA251249) | Learned responsive order-flow simulation and realism evaluation | Compare the proposed cycle audit against its actual response/fidelity evaluation |
| [RL discovers price manipulation](https://arxiv.org/abs/2607.06121) | RL discovers manipulation already present in a specified nonlinear impact model | Distinguish model-induced artifacts from economically permitted manipulation; RL search alone is occupied |
| [Decision-centric world-model evaluation](https://arxiv.org/abs/2606.15032) | Calls for interventions, ranking, optimization and exploitability tests | Generic exploitability or policy-ranking metrics are insufficient novelty |
| [DSGE-Gym](https://arxiv.org/abs/2607.03144) | Economic world models and off-policy counterfactual evaluation | A general economic world-model benchmark is already occupied |

The remaining gap is an inference from inspected sources, not proof that no
matching paper exists. Trace these works' references and inspect their actual
code/evaluation before claiming firstness.

## Alternative candidate: evidence sufficient for a financial decision

Ask whether an agent learns when uncertain inputs already settle a decision,
versus when it must obtain a particular missing fact. Example: approve a project
only if net present value is positive for every value permitted by explicitly
rounded inputs; request a targeted refinement when the feasible set straddles the
decision boundary. Exact-answer abstention and decision sufficiency differ.

Potential package: independently checked decision labels, adaptive evidence
acquisition, and a training reward based on justified decisions and acquisition
costs. Classical robust optimization, interval arithmetic and value of
information are prior foundations, not our inventions. Close collisions include
[FinVerBench](https://arxiv.org/abs/2605.29586),
[CAM-DF](https://arxiv.org/abs/2607.27083), and financial evidence/abstention
benchmarks. Further source review is required; empty keyword searches are not a
novelty certificate. This alternative has not passed a stronger novelty gate than
the market-cycle candidate.

## Decision and next academic step

Advance the market-cycle candidate to a one-page contribution specification:
explicit economic assumptions, closest-work comparison, actual available learned
simulator artifacts, proposed correction and experiments that could falsify it.
Choose the implementation scope after judging scientific value. Do not begin
paid training before compute readiness and budget are established.

Agenthon fit is market simulation, RL, evaluation and verification. It is related
to Track 3, but is independent of our paused simulator-speed paper and does not
use private competition answers. The live call specifies posters; no oral route
or acceptance certainty follows from these comparisons.
