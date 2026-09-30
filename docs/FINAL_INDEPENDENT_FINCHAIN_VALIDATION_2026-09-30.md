## Executive summary (read this first)

Independent validation passes for all 300 preserved current-code attempts. Six complete upstream files reconstruct to their original hashes; all 300 native question/solution strings regenerate byte-for-byte under Python 3.13.2. Separately written Fraction/Decimal calculations reproduce the final scalars, financial identities, rounding alternatives and every reported family counter.

All 300 answers are compatible with the inspected source's intermediate-rounding convention. Exact-visible-input half-cent compatibility is 82/100 calls, 100/100 WACC and 100/100 compound-interest cases. The 18 call differences are **rounding-dependent discrepancies**, not evidence of debt-for-call computation. One of those 18, seed 40, also breaches the exact-tree lower bound by more than half a cent. All 13 debt/call collisions are exactly zero/zero with both terminal call payoffs zero; those controls are numerically nondiagnostic.

This is an AI technical review of a newly seeded bank from pinned public author code. It is not validation of FinChain's historical corpus, an independent expert reference set, full reasoning-trace correctness, prevalence across financial benchmarks, or an effect on model training. No model calls, new corpus, production implementation edits, or frozen-record changes were made.

### Source and generation reconstruction

Reviewed the [frozen protocol](INDEPENDENT_FINCHAIN_CODE_PROTOCOL_V1.md), `src/independent_finance/`, all source fragments, original freeze, attempt file, collection receipt and analysis. Every checksum in the original freeze and collection receipt matches. The recorded freeze is **2026-09-30 16:13:51.976774 UTC**, Python **3.13.2**, revision **`9bd2942b85d992844b77094a8b822aa16832703c`**. The runner verifies this freeze before generation and preserves all family/seed pairs.

I independently concatenated contiguous source fragments, checked line intervals and fragment hashes, and verified the six reconstructed whole-file hashes: option pricing, WACC, compound interest, entity pools, README and Apache license. Only the three inspected function definitions and literal entity pools were compiled; foreign imports, upstream mains and corpus programs were not executed.

| Selected current-code function | Verified random-call order for each seed | Original strings reproduced |
|---|---|---:|
| [template_op_medium1](https://github.com/mbzuai-nlp/finchain/blob/9bd2942b85d992844b77094a8b822aa16832703c/data/templates/financial_markets/option_pricing.py#L73) | investor choice; asset choice; uniform S0, K, u, d, r | 100/100 |
| [template_easy_wacc](https://github.com/mbzuai-nlp/finchain/blob/9bd2942b85d992844b77094a8b822aa16832703c/data/templates/corporate_finance/wacc.py#L4) | company choice; unit choice; uniform equity, debt, equity cost, debt cost, tax | 100/100 |
| [template_ci_simple_calculation](https://github.com/mbzuai-nlp/finchain/blob/9bd2942b85d992844b77094a8b822aa16832703c/data/templates/investment_analysis/ci.py#L12) | investor choice; project choice; integer principal; uniform rate; integer years | 100/100 |

Each selected function receives a fresh `random.Random(seed)` for every seed 0–99. Original question and solution hashes also match. There are 100 unique question strings per family and no missing, replaced, retried or nondecision attempt. The same seed numbers across templates do not make their random streams statistically independent.

The freeze timestamp and execution structure support the recorded prospective procedure. Replay identifies the preserved records and code; it does not prove the absence of any unlogged earlier exploratory execution. The selected functions were intentionally chosen for correspondence to known task mechanisms, rather than sampled from all FinChain templates.

### Independent arithmetic and extraction

The verifier uses its own regex extraction and Decimal-to-Fraction conversion; it imports no production oracle. It takes only the last nonblank solution line's declared amount/rate. All 300 final lines satisfy that grammar; no intermediate value is substituted for an unsupported final.

- **Call:** with the source's simple-period gross rate `R=1+r/100`, independently compute terminal payoffs, risk-neutral expectation and discounting. Replicating stock/bond holdings reproduce both state payoffs and the call price. Check `max(S0-K/R,0) <= call <= S0` exactly.
- **WACC:** compute tax-adjusted total financing cost divided by capital. Confirm an independently expressed weighted-cost identity. Equity and debt share the generated million/billion scale, which cancels; answers use percentage points.
- **Interest:** accumulate principal once per year, confirm the closed form, then subtract principal. Compound amount is a distinct requested quantity.

Intermediate alternatives use exact nearest-cent state prices, four-decimal WACC weights, or cent-rounded compound amount before subtracting principal. Both nearest alternatives remain allowed at exact ties. Five call instances have a state-price rounding tie; no WACC-weight or compound-amount tie occurs in this bank. Native source execution selects one outcome with Python floating-point rounding; the declared interpretation comparison preserves both legitimate nearest alternatives.

The call source displays risk-neutral probability to three decimals but computes with its unrounded value. The compatibility calculation correctly uses the value derived from the inputs, not that shortened display. This is another reason final-scalar compatibility does not certify the entire printed trace.

| Family | Scheduled / assessed | Unique questions | Within exact ±0.005 | Within source-convention ±0.005 | Authored mutation numerically compatible |
|---|---:|---:|---:|---:|---:|
| Binomial call | 100/100 | 100 | 82 | 100 | 13 |
| WACC | 100/100 | 100 | 100 | 100 | 0 |
| Compound interest | 100/100 | 100 | 100 | 100 | 0 |

The tolerance is half a cent for amounts and half of 0.01 percentage point for WACC. No case lies outside both declared interpretations. These are numerical compatibility counts, not broad grading accuracy estimates.

### Review of all 18 call discrepancies

The signed difference below is native final value minus exact-input call value, in currency units. Every listed native value is within half a cent of at least one source-rounding value. Seed 40 is included in the 18; there are not 19 distinct failures.

| Call seed | Native final | Exact call, approximately | Signed difference, approximately | Exact bound within ±0.005 |
|---:|---:|---:|---:|---|
| 6 | 16.90 | 16.891610122 | +0.008389878 | Yes |
| 10 | 5.84 | 5.845604036 | −0.005604036 | Yes |
| 16 | 15.04 | 15.034925033 | +0.005074967 | Yes |
| 26 | 5.79 | 5.782570305 | +0.007429695 | Yes |
| 27 | 32.35 | 32.344615385 | +0.005384615 | Yes |
| 28 | 4.66 | 4.652960835 | +0.007039165 | Yes |
| 33 | 3.82 | 3.812346014 | +0.007653986 | Yes |
| 38 | 29.48 | 29.472844575 | +0.007155425 | Yes |
| 40 | 39.36 | 39.368301887 | −0.008301887 | **No** |
| 42 | 27.28 | 27.286035210 | −0.006035210 | Yes |
| 46 | 3.18 | 3.174201490 | +0.005798510 | Yes |
| 47 | 11.19 | 11.196092990 | −0.006092990 | Yes |
| 54 | 16.74 | 16.734540143 | +0.005459857 | Yes |
| 55 | 1.32 | 1.313102119 | +0.006897881 | Yes |
| 56 | 9.55 | 9.555331511 | −0.005331511 | Yes |
| 59 | 1.97 | 1.964023068 | +0.005976932 | Yes |
| 77 | 18.93 | 18.924590669 | +0.005409331 | Yes |
| 94 | 11.93 | 11.922993197 | +0.007006803 | Yes |

These differences combine state-price rounding and final cent rounding. The question does not explicitly request intermediate rounding, while the inspected solution/source uses it. Thus an exact-input cent grader and the source convention disagree, but the observed computation has an identifiable approximation policy. Describe this as interpretation-dependent compatibility rather than 18 unconditional wrong labels. The assessment also conditions on the source's simple-compounding convention.

### Bound case and quantitative collision controls

For `binomial_call/40`, exact call price and lower bound are **39.368301886792…**; native final is **39.36**, a shortfall of **0.008301886792…**. Source-rounded terminal prices are 134.95 and 103.54, and its original-factor probability produces **39.364779874214…**, which rounds to 39.36. Both states are in the money.

The source rounds state prices but keeps the probability from original up/down factors. A self-consistent rounded-price tree instead uses `(R*S0-Sd)/(Su-Sd)`; in this case it restores **39.368301886792…**. This diagnoses loss of exact-tree consistency through intermediate rounding. It is a conditional exact-input bound violation and a small approximation artifact, not evidence of computing financing debt or a measured exploitable market opportunity. Source-convention compatibility remains true.

The 13 debt/call collisions occur at seeds **0, 2, 22, 24, 25, 29, 32, 44, 48, 62, 63, 65 and 91**. In every one, both call payoffs are zero, so replicating delta, debt and call value are exactly zero. These are equality collisions, not merely near matches admitted by the tolerance.

The attempted mutation pool therefore has 300 controls, of which 13 are numerically nondiagnostic and 287 change the scalar beyond the declared tolerance: 87 call/debt substitutions, 100 tax-omission WACC computations and 100 amount-for-interest substitutions. Do not describe the 13 as erroneous numerical answers that the checker failed to reject, or their coincidence as evidence that the native solution computes debt. A final-value test cannot identify the reasoning behind a zero payoff.

### Statistical and contribution boundaries

This is a complete fixed-seed bank over three purposively selected current templates. The 300 strings represent three computation mechanisms, not 300 independent conceptual replications or a representative sample of FinChain. Report finite family counts without IID confidence intervals or population prevalence claims.

FinChain supplies a separately authored source comparison, with passing WACC/interest examples and explicit rounding sensitivity. Different authorship does not prove causal independence, distinct mathematical ancestors, or absence of shared conventions. Exact source reconstruction does not bind these new strings to historical published instances or reproduce original benchmark evaluation results.

This result strengthens the audit's specificity: source-faithful rounding can differ from an exact-input reference while genuine quantity substitution remains numerically separable in nondegenerate cases. It also limits overreach: all 300 native values satisfy the declared source convention, and no new FinChain wrong-quantity pattern is established. Preserve that passing comparison alongside the earlier released-supervision defects.

### Evidence bindings

Original freeze SHA256: `3b177b808f63e5a344cb19694847a6b137ca14f39753c1e18a6ea2786333f911`.

Original 300-attempt bank SHA256: `7610545b6fef49861ce3d2c05e1f5513e2ae310cf806f0a4892adf818c1996fb`.

Original analysis SHA256: `542c7ff9d7bcfe8b3fbdc46e945ad23e6ce72bc3eeb67fe97cc5e3d76230cc0e`.

The separately written verifier is retained as [validate_independent_finchain.py](../scripts/validate_independent_finchain.py), **206 lines**, SHA256 `7934260466be2b8dbe91f45d2c116456b87d3b0dc4ee18fcc25bd3a7ba1ffc63`. Run from the repository root with its existing recorded Python 3.13.2 runtime:

```bash
.venv/bin/python scripts/validate_independent_finchain.py
```

This command passed against the retained artifact and source fragments, reproducing all 300 records and counters without importing the production oracle. It checks artifact-manifest bindings and the specific original freeze hash, then prints its own hash and results. The script was authored **after collection**; preserving it does not turn this independent verification into a prospective scientific implementation. The original temporary version remains `/tmp/independent_finchain_validate.py` (114 lines); its successful portable run is recorded locally at `/tmp/independent_finchain_portable_validation.json`.

The separate production replay is [replay_independent_finance.py](../scripts/replay_independent_finance.py). Replaying the same frozen source functions in memory is numerical/source validation, not new model inference or a new generated corpus.
