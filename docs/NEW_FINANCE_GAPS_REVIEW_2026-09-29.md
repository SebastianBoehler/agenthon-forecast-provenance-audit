## Executive summary (read this first)

This review prioritizes scientific contribution over implementation time. The strongest new lead is a mechanistic audit and repair of action-cycle inconsistencies in learned financial market simulators. A second lead studies which market decisions can actually be certified under response ambiguity. Neither has established novelty or results. Acceptance cannot be promised from a topic or historical workshop examples.

Research date: 29 September 2026. No training or simulator experiments were performed. Primary full-text sections were inspected through arXiv HTML; published journal and conference sources were included where accessible. This is a bounded candidate review, not an exhaustive systematic literature review.

## 1. Candidate: closed trading cycles expose incorrect learned response

### Research question

Can a learned market simulator reproduce ordinary market statistics and one-way market impact while rewarding closed action cycles because its learned response is economically inconsistent? Can a targeted correction eliminate that failure without destroying observed-data fidelity?

### Concrete intuition

An agent buys and then sells the same quantity, ending with zero inventory. We ask whether its profit arises from legitimate predictive information or market mechanisms, or from the simulator's learned reaction to its own orders. A realistic-looking price path is insufficient to distinguish these explanations.

### Proposed substantive contribution

- Define a finite, explicit family of closed action cycles and a reference regime with no predictive signal, known cash accounting, and declared no-manipulation assumptions.
- Separate conditional forecasting alpha, favorable random noise, actual price-manipulation incentives, accounting defects, and artificial response created by a learned generator.
- Attribute the failure to a specific response mechanism, such as impact persistence or asymmetric history conditioning, through controlled intervention and ablation.
- Develop a correction to that mechanism, then test whether it preserves distributional fidelity, ordinary impact behavior, and held-out execution-policy performance.
- Release reset states, actions, fills, cash ledgers, seeds, and diagnosis traces as reproducible artifacts.

The paper contribution would be an established failure mechanism plus an effective intervention across learned generators. A new metric, a profitable toy policy, or an RL agent finding manipulation alone is insufficient.

### Closest predecessors and limits on novelty

| Primary source | What it already establishes | Possible distinction requiring proof |
| --- | --- | --- |
| [Gatheral, No-dynamic-arbitrage and market impact, Quantitative Finance 2010](https://doi.org/10.1080/14697680903373692) | Connects nonnegative expected round-trip cost to compatible impact shape and decay. | We would diagnose learned conditional order generators; the economic principle is inherited, not new. Publisher abstract/notes inspected, full text not accessed. |
| [MarS, arXiv 2409.07486v2](https://arxiv.org/html/2409.07486v2) | Order-level generative simulation; TWAP injection, square-root impact checks, and RL execution demonstrations. Sections 3.2, 4.3, 4.4, Appendix K inspected. | Identify and repair closed-cycle response defects not established by its reported one-way impact checks. Do not assert MarS has such a defect before measurement. |
| [TRADES, arXiv 2502.07071v2](https://arxiv.org/html/2502.07071v2), [published proceedings version](https://doi.org/10.3233/FAIA251249) | Conditional diffusion order generator; prediction usefulness, stylized facts, and a one-direction POV intervention. Sections 5, 7.1, Appendix F inspected. | Controlled round-trip response auditing with mechanism attribution rather than checking that the market reacts. Check published version for changes. |
| [Tsaknaki, Macri, Lillo, Can Reinforcement Learning Efficiently Discover Price Manipulation?, 2607.06121](https://arxiv.org/html/2607.06121v1) | DDPG discovers manipulation in an explicit nonlinear Almgren–Chriss impact model and compares with model-based optimization. Full-text introduction, setup, experiment and conclusion inspected. | Auditing learned neural simulators and repairing their learned response is different from discovering incentives intentionally present in a specified impact model. This is a major collision: generic RL round-trip discovery is occupied. |
| [How Should World Models Be Evaluated?, 2606.15032](https://arxiv.org/html/2606.15032v1) | Decision-centered metrics include ranking, optimization and exploitability. | Finance-specific response mechanism and intervention, rather than transplanting its generic evaluation metrics. |

### Critical methodological safeguards

- A profitable round trip is not by itself proof of a simulator defect: real market mechanisms may permit manipulation, and public information can predict returns.
- Declare economic assumptions before calling any result a no-arbitrage violation. No-dynamic-arbitrage under an impact model differs from universal no-arbitrage in a real LOB.
- Require actual fills, fees, spreads, terminal liquidation, and strict cash/inventory conservation. Mark-to-market gains cannot substitute for realized cash on a closed cycle.
- Use mirrored buy/sell schedules, nonadaptive schedules, randomized signs, and independent evaluation seeds; account for policy selection when estimating uncertainty.
- Shared randomness requires stable event/random-draw identities. Reusing one seed is not automatically a valid paired counterfactual when interventions change event counts.
- Compare a known admissible reference, a deliberately incompatible impact reference, replay, and available learned generators. None is a universal oracle for real market counterfactuals.
- Repair evaluation must include held-out cycles and ordinary trading policies; preventing trading or erasing impact is not a successful correction.

### Kill criteria

Reject this as the headline if no reproducible learned-response defect appears, if only cash-accounting bugs remain, if the result is fully explained by known nonlinear impact manipulation, or if correction merely suppresses legitimate market dynamics. A demonstrated negative result could still be useful but must have power and meaningful coverage.

### Novelty assessment

Promising but conditional. The exact conjunction of learned-generator diagnosis, cycle-consistency mechanism, and fidelity-preserving repair was not found in this bounded search. That does not establish absence. Required follow-up: newest neural LOB papers, simulator issue trackers, transient-impact arbitrage studies, and adversarial market-model validation.

## 2. Candidate: certify decisions across observationally compatible markets

### Research question

Given several market-response models that fit the same observed evidence, which execution-policy comparisons are determined, and what additional intervention resolves the others?

### Proposed contribution

Build a market-specific ambiguity set under explicit calibration constraints. Instead of reporting one best policy, compute the minimum policy-value difference across compatible models. A positive bound certifies that comparison only within the declared set. Otherwise report unresolved ranking and select a finite intervention that maximally reduces decision ambiguity. Evaluate interventions on a known synthetic reference and keep observed-market identification claims separate.

The substantial contribution would require a useful market-specific construction or efficient certification/experimental-design method, not merely observing that simulation rankings disagree.

### Closest sources

- [JMLR, Hauser and Buhlmann 2012](https://jmlr.org/papers/v13/hauser12a.html): interventional equivalence and causal identification are established foundations. Primary journal page inspected; full PDF should be read before using its algorithms.
- [ICML, Yang, Katcoff and Uhler 2018](https://proceedings.mlr.press/v80/yang18a.html): general-intervention causal equivalence is already formalized; primary proceedings abstract inspected.
- [DSGE-Gym, 2607.03144](https://arxiv.org/html/2607.03144v1): economic counterfactual distribution shifts, structured-model coverage and off-path evaluation already studied. Sections 3–6 inspected. It measures transition prediction, whereas this candidate concerns identified policy comparisons across compatible response models.
- [DoTime, 2607.27263](https://arxiv.org/html/2607.27263v1): synthetic intervention/time-series benchmark explicitly includes nonidentifiability and known causal ground truth. Sections 5–8 and exploratory identifiability discussion inspected. Generic causal time-series benchmark is occupied.
- [Decision-centric world-model position, 2606.15032](https://arxiv.org/html/2606.15032v1): policy ranking and exploitability already proposed. Do not claim these metrics as new.

### Assessment

More ambitious and theoretically sharper than generic policy ranking, but novelty uncertainty remains high because robust optimization, partial identification, and active causal design have mature literatures. Requires further targeted review before recommendation. A finite-family minimum bound is elementary; meaningful contribution needs a nontrivial set construction, tractable method, or consequential empirical result.

## 3. Rejected generic route: stale evidence and financial restatements

A finance-agent revision benchmark is not a safe fresh choice. [Point-in-Time SEC Financial Data, SSRN 7415198](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7415198), September 2026, explicitly describes acceptance timestamps, controlling accessions, non-reliance intervals and evidence-state changes. Search-index abstract inspected; publisher page failed to open. [Fin-RATE v4](https://arxiv.org/html/2602.07294v4) already targets SEC analytics and tracking. The parent research also found FinFIRST 2609.25192 covering point-in-time provenance. A specific new revision mechanism might remain, but broad temporal financial evidence evaluation is occupied.

## Recommended academic next step

Prioritize a contribution specification for Candidate 1, followed by independent adversarial review against Tsaknaki et al., MarS, TRADES, and Gatheral. Define the null explanations and the distinguishing evidence before experimentation. Do not select the topic because it sounds fashionable or infer acceptance probability from related accepted papers.
