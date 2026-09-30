## Executive summary (read this first)

Public inputs, source-file identities, native artifact identity and a balanced exploratory schedule are prepared. **The experiment is not runtime-ready:** no verified Python ABIDES baseline image was found in the bench image inventory. No simulation or timing run was launched. The private native workspace's standing AGENTS.md prohibits dependency downloads and requires exclusive use of the existing bench. A baseline build involving downloads needs an explicit exception to that rule.

## Frozen inputs and provenance

Active campaign: `data/simulation-pilot-20260928-public-v2/` in this private research repository. Inputs contain public parameters only. Generated outputs will stay ignored. The tracked [preparation script](../scripts/prepare_simulation_pilot.py) recreates the manifest and schedules from the named source files and checks the retained native identity. It refuses to overwrite an existing campaign.

- Manifest SHA-256: `36a85161c3da28cfc3c6b0616d964d866e5e8822ab95ede4e9209f3c2c3f754a`.
- Python upstream: `f9cbe51342b7dedd9587e4e069040d68a5c6477f`.
- Baseline source freeze includes the current Dockerfile, both CLI shims, every adapter Python file and **all four patches**: pomegranate-free sampling, message ledger, exchange STP, and scheduled oracle jump. This corrects the earlier one-patch description. Individual digests are in the manifest; upstream commit alone is insufficient.
- Native executable SHA-256: `f1f0ff871568407e1d8bfe9b68fa39a35e2b505362d8e0da5583c145cc79f577`. Independently computed from the retained local file and existing bench artifact; they agree.
- Existing native runtime image: `sha256:9b960d3275acd32ca23198a7a2feaff753be3b5168038ad0829f1c3b484bf77d`, inspected as linux/amd64. The executable is mounted separately; the image's bundled executable is not assumed to be r4.

The current baseline Dockerfile pins package versions but uses a mutable Python base tag and unpinned apt repositories. A built image's content identity is essential; archival reproduction additionally needs base digest, package/build receipts, and retained image layers. Baseline patches include behavioral extensions, so describe the comparison as the **Track 3 ABIDES adapter**, not unmodified upstream ABIDES.

## Workloads and scales

| Public source | Intended stress | Two scales |
|---|---|---|
| `s012_partial_fill_cancel_race.json` | Cancellation and partial-fill activity | Original horizon; twice the horizon |
| `mr_deep_book_state_size.json` | Market-maker depth with heterogeneous activity | Original horizon; twice the horizon |
| `ra05_shock_momentum_heavy.json` | Reactive agents responding to a scheduled shock | Original horizon; twice the horizon |

Two fresh seeds, `2026092801` and `2026092802`, give **12 cases**. All other model parameters remain as supplied. Scheduled jump timing stays unchanged. Horizon extension is a duration scale, not a population/depth scaling experiment. Names and descriptions do not prove that a desired race or deep-book event occurs: inspect observed event coverage during preflight before claiming coverage. No manual event sequence or unexposed final agent state has been validated.

## Bounded stages

1. **Runtime preparation:** verify baseline image contents against the frozen source set, record immutable image ID/base/dependencies and benchmark launcher hashes. Resolve bench ownership before creating any container. No automatic pull or source substitution.
2. **Semantic preflight:** one Python and one native launch for each of 12 cases: **24 launches**. Compare every ordered decoded field/type/null in both trace tables and validate sidecar counts/digests. Any mismatch stops the timing stage. This does not invoke a sealed oracle or assert universal program equivalence.
3. **Noise control:** identical r4 artifact under two aliases on one case per workload, four alternating pairs: **24 launches**. Assess timing variability and launch-order effects descriptively; this small pilot cannot certify an effect-size threshold or statistical power.
4. **Implementation comparison:** four complete blocks, randomized case order, exactly two Python-first and two native-first pairs for each case: **96 launches**. All arms perform identical required output obligations.

Maximum **144 launches**, 120 seconds per launch, and **30 minutes total execution budget** after runtime preparation. The total cap is a stop condition, not a completion estimate. If it expires, retain partial evidence and report incomplete; do not silently continue or select favorable completed cases. Builds/image preparation are excluded from this measurement budget and separately recorded. No mechanism ablation runs are included: matched mechanism artifacts remain a subsequent gate.

## Timing and observation rules

External complete-process elapsed time is primary: begin immediately before creating the child process and end after successful child exit with required output files closed. Retain Docker lifecycle elapsed separately, excluding SSH transport. Baseline's internal `wall_clock_sec` only surrounds `abides.run`; it excludes config construction, trace extraction and serialization. Never compare that clock directly with complete-process time.

Record every raw paired time, launch order, case/seed, resource limit, image/artifact identity, return code, timeout, output count and validation result. Use 4 CPUs, 16 GiB, no swap, no network and no GPU use for both arms. Preserve complete outputs at least once per arm/case and re-decode any changed repeat. Different Parquet encoding is permitted; each file's own digest must validate.

Use the exact trace/message field lists in the manifest. Do not reorder rows to rescue an ordering mismatch. Agent-visible state and random-stream preservation need additional instrumentation evidence; the output-only pilot conclusion is limited to its observable contract.

Report per-case median paired complete-time ratios and ranges, plus each block's aggregate log-ratio across all 12 cases. Four blocks provide descriptive exploratory evidence; do not manufacture a precise population confidence interval from them. A/A uncertainty or workload regressions can require a later powered design. No clipping at the competition's 10M cap and no extrapolation to Final or official hardware.

## Readiness observations and review correction

Read-only SSH checks confirmed the retained artifact digest and native image identity. No active container was listed at that instant; this is not a reservation. The inventory listed native/T2/Rust/Python3.13 images but no tagged Python3.11 ABIDES baseline. A bounded directory check found no shallow cached `abides_core` source tree. This does not prove an unpublished baseline cannot exist elsewhere; it establishes that we have not identified one usable for this experiment.

The existing private harness accepts native executables in one native image, uses an existing competition roster, and validates against cached observations. Its `--baseline` argument does **not** support selecting an arbitrary Python baseline image. Do not run it as though it implements this fresh-input cross-implementation study. A focused launcher adapter with external child timing and a separate fresh-output comparator is still required once the baseline is available.

The initial generated v1 schedule randomized first-arm positions without guaranteeing balance for each case. It was caught before any execution. v2 fixes each case to two launches in each first-arm position and includes the A/A schedule. Preserve v1 as superseded preparation history; no experimental result used it.

## Decision

The input/schedule preparation step is complete. Runtime freeze and the pilot are pending the verified baseline and launcher. No new speedup, exact agreement, mechanism benefit, or submission readiness is established. The next action is obtaining or building the pinned baseline, then preparing the launcher and executing the bounded semantic/noise pilot under exclusive bench ownership.
