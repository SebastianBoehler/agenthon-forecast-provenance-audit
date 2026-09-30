## Executive summary (read this first)

**Provisional candidate:** *Same Market, Faster Execution: A Controlled Study of Native ABIDES Simulation*. The contribution would be a measured systems result about accelerating fixed market experiments, supported by a reusable public evaluation artifact. It is not yet a demonstrated contribution. A Rust port, correctness checks, or a leaderboard score alone would not justify our novelty claim. We should advance to a small falsification pilot, not declare the paper submission-ready.

## Motivation and research question

Consider a market-maker order racing with a cancellation. Changing which message arrives first can change fills and subsequent agents' decisions. A faster simulator is useful for repeated strategy experiments only if the relevant experiment remains comparable. ABIDES models agent computation delay, network latency, and per-agent random streams; its kernel discussion explains why these affect experimental interpretation [1, §3.1].

**Research question:** On a declared subset of public ABIDES market experiments, which native implementation changes reduce complete execution time while preserving ordered market events and required message-ledger observations, and where do gains measured inside the simulation fail to carry through to the complete run?

This question concerns implementation fidelity to a specified model. Agreement with ABIDES does not establish realism relative to actual markets. Realism requires separate empirical validation; *Get Real* provides that distinction and relevant measures [5].

## Closest-work comparison

| Work | What it establishes | Boundary of our proposed study |
|---|---|---|
| ABIDES [1] | Deterministic asynchronous market simulation with latency and individual agent random streams. | Preserve declared observations of its pinned implementation; determinism is inherited, not invented. |
| MAXE [2, §6] | A compiled C++ multi-agent framework, with ABIDES runtime comparisons as population grows. | Its compared agents/protocols differ. Our target is measured acceleration of matched public experiments, not a claim that compiled simulation is new. |
| JAX-LOB [3, §§4–7] and JaxMARL-HFT [4, §5.1] | GPU acceleration; the latter also includes a matched CPU counterpart and complete training measurements. | Our target is asynchronous ABIDES execution with recorded observable agreement, not a new GPU or end-to-end benchmarking principle. |
| abides-rs [6] and Quant Systems Lab [7] | A deterministic Rust market simulator; an exchange engine with independent differential checks. | Neither Rust nor differential testing is our contribution. A meaningful measured mechanism or reusable findings must distinguish our artifact. |
| T2J-Bench [8, §3] | Codebase conversion evaluated under fixed observable equivalence contracts. | Applying an equivalence contract to simulation is insufficient novelty by itself. We must show useful domain-specific results. |

## Proposed contribution and its novelty boundary

We would contribute **one controlled empirical systems study**, with three linked outputs: (1) a reproducible public workload/observation contract; (2) a native implementation with a named optimization and matched ablation; (3) measurements explaining when that optimization improves complete execution and when output production, build choices, or workload structure erase the benefit. The artifact should let another researcher rerun the same comparison and inspect disagreements.

The candidate distinction is the experimentally supported relationship between **asynchronous market behavior, implementation mechanism, and complete execution cost**. This is a bounded research hypothesis, not a verified priority claim. Republishing Agenthon's existing gates and scenarios would add little; reused material must be credited, and our added measurements, coverage, and findings must be explicit.

## Evidence required before writing a results paper

Use the pinned Python engine **and its adapter/patch** as a fresh same-host baseline. Freeze observable fields, timing boundaries, public workloads, new seeds, and one mechanism before the pilot. Keep unchanged-binary A/A timing controls. Report failures and per-workload regressions, not only aggregate throughput. Follow systems benchmarking guidance on variation and effect-size uncertainty [9].

Existing native optimization reports make execution feasible but do not establish a controlled Python-to-native speedup. Recent reports also show conflicting gains across timing boundaries. Those are discovery clues; they need public-safe, independently scheduled measurements. If the chosen mechanism has no repeatable complete-run benefit and the study supplies no substantial explanatory finding, stop this framing. **Acceptance remains uncertain until the empirical and novelty gates pass.**

## References

1. Byrd et al., *ABIDES*. [Full text](https://arxiv.org/abs/1904.12066). Cached PDF; kernel and experiment passages reviewed.
2. Belcak et al., *Fast Agent-Based Simulation Framework…* (MAXE). [Full text](https://arxiv.org/abs/2008.07871). Cached v3; architecture and §6 reviewed.
3. Frey et al., *JAX-LOB*. [Full text](https://arxiv.org/abs/2308.13289). Cached; implementation and timing comparisons reviewed.
4. Mohl et al., *JaxMARL-HFT*. [Full text](https://arxiv.org/html/2511.02136v1). Cached; §5.1 reviewed.
5. Vyetrenko et al., *Get Real*. [Full text](https://arxiv.org/abs/1912.04941). Cached; realism measures and conclusion reviewed.
6. [abides-rs](https://github.com/mariotrerotola/abides-rs). README inspected; independent execution not performed.
7. [Quant Systems Lab](https://github.com/div0rce/quant-systems-lab). README inspected; independent execution not performed.
8. Song et al., *Converted, Not Equivalent*. [Full text](https://arxiv.org/abs/2605.29054). Cached v2; introduction and contract formulation inspected.
9. Kalibera and Jones, *Rigorous Benchmarking in Reasonable Time*. [Author manuscript](https://kar.kent.ac.uk/33611/45/p63-kaliber.pdf). Cached; variation/repetition guidance inspected.
