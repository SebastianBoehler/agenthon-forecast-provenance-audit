## Executive summary (read this first)

**Independent review: conditional proceed to a public pilot; novelty and submission readiness have not passed.** A native CPU port of ABIDES, deterministic scheduling, differential checks, or a broader timing boundary cannot alone support a substantial novelty claim. The defensible target is a systems case study: a concrete optimization mechanism, its measured benefit on unchanged public market experiments, and an explanation of where that benefit disappears or changes sign. A reusable workload suite and verification contract support that contribution. They do not create it automatically.

This review reads primary full texts and first-party repository documentation. It does not execute or verify other implementations. Repository claims below remain author claims. No sealed competition traces or results were copied into this note.

### 1. Closest collisions that the proposal must acknowledge

| Source and evidence read | Already established | Consequence for our claim |
| --- | --- | --- |
| [ABIDES](https://arxiv.org/abs/1904.12066), kernel and agent API sections; cached full text | Asynchronous message scheduling, computation/network delays, market protocols, and event logging. | Event order and information availability belong to the simulation model. Matching-engine agreement alone does not establish experiment equivalence. |
| [MAXE](https://arxiv.org/abs/2008.07871), §6; cached full text | Native financial multi-agent simulation and an ABIDES runtime comparison over increasing populations, with memory behavior discussed. | “Faster low-level simulator than ABIDES” is an established direction. Their protocols and agent implementations differ; our study must specify whether it preserves the source experiment. |
| [JAX-LOB](https://arxiv.org/abs/2308.13289), abstract and performance sections; cached full text | Accelerated matching and end-to-end RL use. | Matching throughput and application timing are both prior evaluation targets. |
| [JaxMARL-HFT](https://arxiv.org/html/2511.02136v1), §4 and §5.1; full HTML | Both environment and training measurements, an explicitly comparable CPU-MARL implementation, and acknowledged imperfect ABIDES/PyMarketSim comparability. | Do not claim existing work generally ignores end-to-end performance or exact counterpart baselines. Its step-based replay/agent setting differs from preserving a fixed asynchronous ABIDES experiment. |
| [abides-rs](https://github.com/mariotrerotola/abides-rs), current README | Rust native kernel, deterministic scheduler, seed control, multiple RMSC scenarios; compatibility limitations acknowledged. | Rust, deterministic operation, and ABIDES-like scenarios are not unique. README inspection cannot establish or refute exact ABIDES agreement. |
| [Quant Systems Lab](https://github.com/div0rce/quant-systems-lab), current README | C++ matching, independent OCaml differential replay, minimized disagreements, profiling and explicit microbenchmark limits. | Differential testing and honest timing scopes are existing engineering practice. This is an exchange command engine, rather than the entire asynchronous agent population. |
| [T2J-Bench](https://arxiv.org/abs/2605.29054), §3; cached full text | Fixed external observational equivalence contracts for whole-codebase conversion. | A semantic contract plus cross-implementation comparison is already a general research method. We need a domain-specific finding or useful mechanism beyond adopting it. |

### 2. Proposed claim, narrowed to something falsifiable

**Question:** Which native implementation changes accelerate a fixed public ABIDES market experiment when agent behavior and observable event trajectories are preserved, and under which workload and timing boundaries does the acceleration persist?

The contribution can become substantive through either of two empirical outcomes:

1. **Systems result:** identify a concrete mechanism, isolate it with an ablation, demonstrate useful complete-run gains across materially different workloads, and explain a scaling boundary. An unnamed combination of compiler options and many tuning attempts is weak evidence for a general lesson.
2. **Evaluation result:** demonstrate repeated, practically meaningful ranking reversals between an inner throughput metric and time to obtain the required outputs, identify the cause, and show why a stated evaluation boundary prevents an incorrect optimization decision. A single reversal caused by moving work outside the timer is an illustration of known measurement bias, not sufficient novelty.

The benchmark contribution is stronger if it exposes scientifically relevant incompatibilities or optimization decisions that ordinary matching checks miss. More scenarios alone is insufficient. Exact observable agreement also cannot certify market realism: it shows preservation of the reference model, including its limitations.

### 3. Smallest credible empirical gate

This is an exploratory gate, not a power calculation or an acceptance prediction.

- Freeze source commit **and** adapter/patch hashes, candidate binary, compiler flags, output schema, random streams, and event tie-breaking. Identical seed integers do not imply identical draws across languages.
- Use at least three public workload families that stress distinct behavior, with two scales and several unseen seeds per family. Include collisions in event time, cancellation/partial-fill behavior, and feedback from trades to agents.
- Compare externally observable event fields and final agent state under a declared contract. Establish that the observer sees what agents can react to. Require zero disagreements for a claim of exact agreement; any tolerated numeric differences need justification and a narrower claim.
- Measure complete native execution and time to required outputs, alongside the inner kernel metric. Report setup, input loading, serialization, synchronization and output work separately. Do not confuse simulator-process timing with clean-container startup timing.
- Randomize paired run order, include unchanged-binary A/A repeats, and select repeat counts after measuring variability. Preserve per-case results and uncertainty; an aggregate win must not conceal systematic regressions.
- Isolate one optimization with an on/off ablation. Accept a systems claim only when complete-run improvement exceeds the assay noise and extends beyond its tuning workloads. If ranking reversal is the claim, reproduce it across independent workloads/variants and explain the excluded work.

### 4. Findings that refute this direction

Stop or reframe if equivalent public workloads cannot be constructed, if observer agreement misses agent-visible state changes, if gains disappear under complete execution, if only tuning cases improve, or if the isolated mechanism is ordinary port overhead without an informative scaling result. A close implementation already providing the same preservation contract, workloads, mechanism and findings would remove the proposed distinction.

The private iteration143 observation supplied for this review is a reason to investigate timing, not a paper result: higher reported EPS with slower complete native execution cannot justify a baseline speedup claim. It needs an independently reproducible public experiment.

### 5. Review decision

**The direction is plausible for a focused workshop systems paper, but the current novelty claim is still a hypothesis.** Public empirical evidence must establish the contribution before the abstract promises acceleration or a new evaluation finding. Reproducible code history and an ARA-style claim-to-evidence package improve auditability; they should support the science rather than substitute for it. No standard review process guarantees acceptance.
