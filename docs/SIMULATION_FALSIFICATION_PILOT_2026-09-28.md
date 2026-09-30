## Executive summary (read this first)

This is a proposed pilot, not a frozen executable campaign or completed experiment. Its purpose is to determine whether the candidate in [the novelty page](NOVELTY_JUSTIFICATION_2026-09-28.md) deserves a full study. No expensive run, new optimizer, competition upload, or publication follows merely from this document. Freeze exact artifacts, commands, observations, repetition counts, and a bounded resource budget before execution.

## Research design versus implementation methods

**Research design:** controlled paired implementation comparison, followed by a mechanism ablation. Exploratory pilot cases diagnose feasibility and noise; later confirmation uses previously unmeasured seeds/configurations. Historical optimization selections are discovery data and cannot be independent confirmation.

**Implementation methods:** run the same public scenario through the pinned Python ABIDES adapter and retained native executable. Capture market events and message observations. Run both under matched CPU/memory/network limits. Compare structured outputs; time the process externally. Reuse the shared qfbench toolkit for competition gate diagnostics without copying its scoring mathematics.

## The three contrasts

1. **A/A control:** identical executable, inputs, and output obligations in two randomly assigned positions. Detect order effects and normal host variability.
2. **Python/native comparison:** fixed Python engine, adapter, patch, dependencies and container versus native executable; same scenario and seeds. This estimates the effect of the complete implementation package, not the causal effect of Rust as a language.
3. **Native mechanism ablation:** build native control and candidate with identical compiler, flags, dependencies and profiling policy; change one named mechanism. Existing reports suggest columnar ledger capture as a candidate, but its contract and matched build must be checked before selection. Do not compare a profile-guided candidate against a differently built control and call the effect source-only.

## Public workload selection

Start with three existing public workload structures: cancellation/partial-fill races, a deep order book, and heterogeneous agent activity. Confirm their inputs and baseline support before fixing exact IDs. Examples available in the public repository include `s012_partial_fill_cancel_race.json`, `mr_deep_book_state_size.json`, and `ra05_shock_momentum_heavy.json`. These are examples for selection, not an approved sample.

Use two supported scales and several new declared seeds per structure, plus one deterministic edge case where applicable. This is a coverage target, not a power calculation. Match supported schema and resource limits. Do not alter the financial model to accommodate an implementation. Select a later set of public parameter variations before viewing confirmatory measurements. New seeds test generalization within these scenarios; they do not establish generalization to arbitrary strategies or exchange rules.

## Observation contract

Before running, enumerate every compared schema, type, ordered field, and tolerance. Compare event order, timestamps, prices, quantities, identifiers and required message-ledger fields where exposed. Check random-generator algorithms, draw order and per-agent streams: identical integer seeds across languages do not establish identical draws. Handle equal-time ordering according to the actual pinned implementation rather than an invented universal ABIDES rule. Record first disagreement and its input/revision.

Require exact decoded equality on declared discrete fields. Any floating-point tolerance must be justified before results are seen. Equivalent decoded values need not have identical Parquet bytes. Check agent-visible information and final state where instrumentable; if unavailable, document that blind spot. Even identical output files do not prove identical hidden state or universal program equivalence. If full kernel messages are unavailable, state the restricted observable contract and narrow the conclusion.

Generate fresh baseline observations locally from public inputs. Keep these generated comparison artifacts in ignored research paths; do not place answer/expected/reference directories in a public competition repository. Never use sealed units or outcomes. Keep library PDFs ignored and do not redistribute gated PDFs.

## Timing and uncertainty

- **Primary:** complete process elapsed time from launch to successful exit after required outputs are finalized; include parsing, simulation and output encoding. Define whether process creation is included in the launcher.
- **Secondary:** simulation-loop time, peak memory, event counts, output size, and container lifecycle time separately. Verify timer boundaries in source. Image build and pull costs are reported separately if relevant.
- Pair arms in randomized balanced order on one otherwise-idle host; record host, frequency policy, limits, contention and artifact hashes. Do not compare local absolute rates with official scores.
- Use the noise pilot to allocate repetitions across launches and independent scheduling blocks, following Kalibera and Jones. Freeze the confirmatory budget and uncertainty calculation before viewing its treatment results. Repeated launches are not new scientific workloads.
- Report complete-run speed ratios with uncertainty and per-workload results. Define the aggregate explicitly. Preserve nulls, crashes and mismatches; give their denominators. No optional extension until significance appears.

## Falsification and decision rules

| Question | Evidence that blocks the proposed claim |
|---|---|
| Same declared experiment? | Any unallowed observable mismatch, unsupported baseline input, or changed output obligation. |
| Measurement reliable? | A/A variability/order effects prevent resolving the proposed effect within the fixed resource budget. |
| Native acceleration useful? | Complete execution shows no repeatable useful gain on the tested workload set, despite inner-loop gains. |
| Mechanism explanatory? | Matched ablation cannot separate the mechanism from compiler/profile/output changes. |
| Contribution substantial? | Results only restate an expected language-port benefit or existing T3 checks without useful new explanation/coverage. |

If timing-dependent ranking reversals become the paper's main finding, require repeated public examples across independently selected workloads/variants and explain the cause. One instance of moving work outside a timer does not establish a new evaluation contribution.

No universal percentage threshold is invented here. Before confirmation, specify the smallest useful reduction for the intended experiment budget and whether pilot noise can resolve it. A negative result may be useful, but is not automatically a publishable contribution.

## Reproducibility and outline

Preserve scenario/seed manifest → source revision → build receipt → randomized schedule → structured observations → analysis → claim. Preserve failed designs and code evolution in an ARA-inspired history. ARA is an artifact practice, not the simulator's scientific novelty.

Proposed paper outline: problem and closest work; observable contract; native architecture and one mechanism; paired study and results; failure/clock-boundary analysis; limitations and reproduction instructions. Generate only evidence-backed figures using the repository's figures4papers/tueplots conventions.

## Current readiness

The public baseline pin is `f9cbe51342b7dedd9587e4e069040d68a5c6477f`, but its adapter and pomegranate-removal patch are also necessary. Their exact hashes and a successful fresh baseline launch remain to be recorded. Existing baseline README performance values have unrecorded/different hardware and cannot establish our speedup.

The private native workspace now contains later reports through iteration143, superseding the earlier iteration78 profiling-status snapshot. Iteration143 records identical A/B output files and a positive six-batch reported-rate contrast, while complete process timing regresses and the full reported-rate contrast is inconclusive. This compares native artifacts, not Python against native. We inspected its report, not independently re-executed its analysis. Restricted report details are not copied into this proposed public study.

Next deliverable: artifact-and-input manifest plus a bounded executable pilot plan. A full study and final paper claims depend on that pilot.

## Independent review response

The [independent review](NOVELTY_REVIEW_2026-09-28.md) found substantial prior art, including JaxMARL-HFT's matched CPU counterpart and complete training timing. We removed any broad claim that prior work lacks equivalent baselines or complete timing. We added explicit random-stream, equal-time ordering, agent-state and cross-workload checks. The substantial-contribution gate remains open: neither the review nor this revision establishes novelty or acceptance readiness.
