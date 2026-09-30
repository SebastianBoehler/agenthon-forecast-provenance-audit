## Executive summary (read this first)

The best *conditional* short-paper route for Agenthon's 30 September 2026 deadline is a systems study of the user's existing Track 3 market simulator: **how much throughput can be gained while preserving event, matching, and output semantics across heterogeneous scenarios?** The implementation and extensive local experiment history already exist. A Development score of 9.126 million events/s across 71 scored units is recorded locally, but it is neither a controlled speedup against ABIDES nor evidence of Final performance. The paper is a go only if public-safe, independent baseline measurements and exact-equivalence checks can be assembled and reviewed before submission. No candidate currently merits a confident acceptance prediction. The `orca_clmm_agent` example is parked, not the chosen direction.

## Venue and scope check

The [official call](https://www.agenthon.net/#call-for-papers) explicitly welcomes market simulation and agent-based models, AI agents for financial software, and evaluation, verification, and benchmarks. It accepts full or short papers as one PDF in any format or length. The call closes 30 September at 23:59 Anywhere on Earth; decisions are promised by 2 October. Accepted papers are posters at the 12 December Atlanta workshop, with at least one author present. The call states no paper acceptance rate or oral-selection process. The competition's T3 task separately asks for an ABIDES-compatible simulator that is faster while preserving matching semantics and stylized facts. Development scores are practice feedback, not controlled Final timing.

## What the wider literature rules out

| Candidate framing | Closest work inspected | What would still have to be new |
|---|---|---|
| “A better finance-agent harness” | [FinanceHarness/FinanceGym](https://arxiv.org/abs/2607.27853) already combines finance workflows with a point-in-time benchmark; [FinHarness](https://arxiv.org/abs/2605.27333) already adds lifecycle monitors and risk routing. | A specific controlled mechanism with hard outcome checks across multiple models and finance tasks. A new wrapper alone is insufficient. |
| “Harness improvements transfer across models” | [Life-Harness](https://arxiv.org/abs/2605.22166) finds substantial transfer in deterministic environments; [HarnessDev](https://arxiv.org/abs/2609.01437) reports limited transfer; [Harness-Bench](https://arxiv.org/abs/2605.27922) maps model–harness interactions. | Explain *when and why* an environment-side intervention transfers in finance, with a factorial comparison. This is a later study, not a three-day claim. |
| “A new financial trading-agent benchmark” | [FORESIGHT-9](https://arxiv.org/abs/2608.29372) already supplies nine counterfactual worldlines, two frameworks, two backbones, and process-state diagnostics. [Finance Agent Benchmark](https://arxiv.org/abs/2508.00828) covers 537 expert tasks. | A distinct oracle or failure mechanism and substantial validated cases. A small synthetic market replay would be a weak addition. |
| “Text helps finance forecasts” | [TimeLitmus](https://arxiv.org/abs/2609.24677) and [Semantics or Structure?](https://arxiv.org/abs/2608.22321) test event-conditioned evidence and text sensitivity; [FinVerse](https://arxiv.org/abs/2608.03259) supplies a large finance-specific forecasting benchmark. | A focused, point-in-time causal intervention tied to probabilistic distribution quality and economic decision value, with a nontrivial result. Current local T2 reports do not establish this. |
| “Fast order-book simulation” | [MAXE](https://arxiv.org/abs/2008.07871) uses a fast C++ core; [JAX-LOB](https://arxiv.org/abs/2308.13289) accelerates many order books on GPUs; [ABIDES Rust](https://github.com/mariotrerotola/abides-rs) offers a Rust implementation; [TRADES](https://journals.sagepub.com/doi/10.3233/FAIA251249) studies generative ABIDES market simulations. | Demonstrate *ABIDES-compatible trace equivalence under diverse agent and latency behavior* together with controlled whole-process throughput and a clear systems analysis. Do not claim first fast, first Rust, or first world model. |
| “Safe CLMM trading harness” | [PACE](https://arxiv.org/abs/2608.17220), [FinHarness](https://arxiv.org/abs/2605.27333), and [Arcifa et al.](https://doi.org/10.1109/ACCESS.2026.3690467) cover action gates, finance safety, and LLM-managed CLMM. | An independently checked, multi-step economic-trajectory result. The current idea has no pilot and is high risk for this deadline. |

These are close-work checks, not a systematic claim that every relevant paper has been found. In particular, exact simulator equivalence and speed must be defined relative to the same scenario, seed, output contract, and machine. Other fast simulators answer related but sometimes different questions; their reported throughput numbers cannot be compared naively.

## Recommended paper question and contribution test

**Working title:** *Fast Without Changing the Market: Trace-Equivalent Acceleration of Agent-Based Market Simulation*.

**Research question:** Across a published range of ABIDES-compatible market scenarios, which implementation changes improve complete-run throughput while keeping the event schedule, exchange behavior, and required output artifacts equivalent to the reference?

The possible paper contribution is a **reproducible equivalence-and-performance evaluation protocol plus a measured systems case study**. Its paper-worthy result would be a quantified frontier: exact semantic checks and stylized-fact diagnostics alongside matched-hardware throughput, broken down by agent mix, queue behavior, latency, and batch size. The code-evolution record, including rejected optimization attempts and frozen promotion gates, should be linked to claims as an artifact. This is analogous to agent-native research artifacts as a reproducibility practice, not a novelty claim.

### Existing evidence and its limit

- A local T3 record reports CodaBench Development submission 943655 at 9,126,164.4816 events/s across all 71 scored units, with zero reported unit failures. The record explicitly says this is Development feedback and that the current run has not been placed on the public leaderboard. Do not cite it as a controlled speedup or Final rank.
- The T3 working directory contains dozens of dated profiling and candidate-rejection reports. That history can support a transparent methods/negative-results section if its provenance and publication rights are checked. It does not replace an independent baseline comparison.
- The newest local full-roster profiling attempt (iteration 78) stopped at preflight: the runtime image's bundled executable was not the retained r4 binary that the benchmark harness mounts. No profile or new speed result was produced. Earlier six-scenario function profiles are leads, not a validated 71-unit bottleneck. Recover and verify the exact retained executable before choosing an optimization target; do not infer one from the failed profile.
- The public T3 repo describes a Python ABIDES adapter, exact semantic checks, stylized-fact gates, and public scenario families. Use only public practice material and release-cleared artifacts. Do not copy sealed scenarios, reference answers, private per-unit outputs, or restricted CodaBench files into this research repo.

### Minimum evidence for a September 30 short paper

1. Freeze the public scenario roster, baseline image, candidate image, hardware, seeds, commands, and timed boundary. Record version hashes and whether output serialization is included.
2. On matched hardware, run baseline and candidate in randomized paired order with enough repeats to show variability. Report complete-process and simulation-only time separately. Do not divide incompatible “events” definitions.
3. For every included scenario, record event count and exact or tolerance-defined equivalence of trace, fills, queue order, ledger, and output schema using the public checker. Report failures and excluded units explicitly.
4. Report effects by scenario family, not only a capped aggregate. Include memory, startup/output costs, batch scaling, and any workload where the native version does worse.
5. Compare with MAXE, JAX-LOB, ABIDES Rust, and the original ABIDES on *contract and workload*, not a false single-number speed race. If feasible, run one external implementation on a genuinely comparable subset; if not, state that limits cross-system claims.
6. Have an independent person or agent review source claims, protocol validity, and every paper figure against machine-readable run IDs. Include public-safe code/trace manifest and a claim-to-evidence table. The final PDF must mark Development-only results as such.

**Go/no-go:** If baseline parity, semantic equivalence, and repeatable paired timing cannot be shown by 29 September, do not submit a performance-results paper. A design-only paper could be submitted under the CFP's flexible length, but acceptance confidence would be low. If the result is a mere language rewrite with no mechanism or explanatory analysis, the novelty claim is too weak. If the comparison and diagnostic pattern are strong, this is the most credible workshop poster candidate among the ideas reviewed, still without a guarantee.

## Ranked options after broad review

| Rank | Direction | Venue fit | Novelty opening | Deadline feasibility | Assessment |
|---:|---|---|---|---|---|
| 1 | Trace-equivalent T3 acceleration and evaluation protocol | Direct T3 and simulation topic | Moderate, conditional on mechanism plus controlled data | Best because substantial code and logs exist | **Lead for evidence audit**, not yet paper-ready |
| 2 | Finance-harness component portability across models and hard-oracle tasks | Agents and benchmarks; likely T1-adjacent | Moderate if interaction mechanism is isolated | Low for 30 Sep: multiple models/tasks and factorial runs needed | Next paper prospect |
| 3 | Multi-step economic safety of CLMM agents | Cross-track finance-agent safety | Possible but crowded | Very low: no validated replay or pilot yet | Parked example |
| 4 | Dated text effects on probabilistic T2 forecasts | Direct T2 | Thin at broad level due recent interventions | Low: no text-using local candidate or independent result | Parked |
| 5 | Forecast-selection or rationale-provenance report audit | Direct T2 | Thin or close to existing work | Low: raw outputs, chronology or blinded ratings missing | Parked |

## Acceptance assessment

The workshop explicitly offers posters and welcomes short papers, which helps a tightly scoped empirical systems paper. Acceptance is **not** predictable from topic fit alone; the call gives no historical rate or formal rubric. The strongest signal for a reviewer would be a distinct question, accurate prior-art boundary, real paired measurements, exact semantics, and a reproducible public-safe artifact. A Development leaderboard score by itself is a competition result, not a sufficient paper contribution. An oral cannot be promised or optimized for from this CFP, which only specifies accepted posters.
