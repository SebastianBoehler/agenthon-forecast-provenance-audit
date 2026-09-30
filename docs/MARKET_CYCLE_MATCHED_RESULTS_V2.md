## Executive summary (read this first)

The stronger matched-data follow-up found no negative-cost cycles in either
coverage condition, across eighteen final neural fits. Only three of nine paired
fits met the frozen fidelity-matching tolerance; those also showed no violation.
An isolated replay then showed that the original V1 failures disappeared with
more optimization on the exact same training data and initializations.

Decision: the current toy failure does not meet the requested paper contribution
threshold. Do not claim a novel response-composition defect or successful novel
repair from these experiments. Continue only toward genuine learned-generator
evidence or a separately justified substantive method, retaining these negative
controls and strong classical comparators.

## 1. What was fixed before execution

[V2 specification](MARKET_CYCLE_MATCHED_SPEC_V2.md), config
`experiments/matched_coverage_v2.json`, three dataset seeds × three model
initializations × two orderings. Each paired sequence contains exactly the same
signed action multiset. All models train for 1,200 updates and save checkpoints
at 200, 600, 1,200. Matching uses common validation response RMSE only.

Selection file was saved before cycle audits. New audit bank: sixteen fixed
schedules held out of training and selection, not semantic-family certification.
The fourteen V1 schedules were separately reused as development diagnostics.

## 2. Finite-bank results

| Comparison | Coverage | Models | Models with cost below -0.10 | Minimum raw expected cost |
| --- | --- | ---: | ---: | ---: |
| new_bank/fixed_budget | blocked | 9 | 0 | 1.424725 |
| new_bank/fixed_budget | shuffled | 9 | 0 | 1.084055 |
| new_bank/fidelity_matched | blocked | 3 | 0 | 1.501493 |
| new_bank/fidelity_matched | shuffled | 3 | 0 | 1.084055 |
| v1_development/fixed_budget | blocked | 9 | 0 | 0.890771 |
| v1_development/fixed_budget | shuffled | 9 | 0 | 0.876955 |
| v1_development/fidelity_matched | blocked | 3 | 0 | 0.914759 |
| v1_development/fidelity_matched | shuffled | 3 | 0 | 0.898534 |

Oddized predictors also had zero threshold violations in both banks. All
classical least-squares and admissible exponential fits passed these banks.
Costs are deterministic expectations for frozen action-only predictors under
the stipulated martingale reference, in currency including spread and fees.
No universal absence of manipulation follows from a finite passing bank.

## 3. Matching coverage and exact identities

Three of nine pairs matched; all were initialization 203, across the three
independent training datasets. All selected checkpoints were at 1,200 updates.
The other six pairs are reported unmatched; tolerance was not relaxed.
Do not describe this as nine successful fidelity-matched comparisons.

| Dataset | Blocked common RMSE | Shuffled common RMSE | Updates each |
| --- | ---: | ---: | ---: |
| data_5101_init_203 | 0.020867 | 0.021869 | 1200 |
| data_5102_init_203 | 0.020891 | 0.022025 | 1200 |
| data_5103_init_203 | 0.020753 | 0.019852 | 1200 |

Maximum centering cost-identity residual: 5.46e-12 currency.
Maximum oddization/mirror-average identity residual: 3.52e-12 currency.
The identities agree to floating-point precision. Centering cannot fix these
closed-cycle profits; oddization cannot fix a negative raw mirror average.

## 4. Isolated training-duration diagnostic

V2 alone changes the original training distribution, so it cannot prove that
extra training caused the V1 failures to disappear. A separate post-V2 diagnostic
was frozen before its run and uses original saved one-direction data, original
initialization seeds and the original fourteen development cycles. It is clearly
exploratory and is not a new confirmation bank.

Every 200-step checkpoint reproduced the original V1 saved state tensors exactly.
Then continue the same fixed optimization recipe to 600 and 1,200 updates.

| Initialization | 200-step minimum cost | 600-step minimum cost | 1,200-step minimum cost |
| --- | ---: | ---: | ---: |
| 101 | 0.209947 | 1.207576 | 1.078388 |
| 102 | -5.316997 | 0.902459 | 1.133039 |
| 103 | -4.859397 | 0.782706 | 1.034730 |

Both initial negative-cost cases disappeared by 600 updates and remained absent
at 1,200 among the declared cycles. This supports an optimization-quality
explanation for the observed V1 failures. It does not prove all schedules pass
or that every learned market generator behaves this way. No constraints or
claimed novel repair were required for this disappearance.

## 5. What this establishes and what it does not

- The original neural result is reproducible, and susceptible to training duration.
- Matched signed action multisets remove the original turnover/terminal-inventory
  confound in V2, but do not match temporal state occupancy or target distributions.
- This finite controlled follow-up does not establish a persistent composition defect.
- Different scalar response errors do not by themselves provide a new method or
  certify economic consistency. Our structural baselines remain decisive.
- Three dataset seeds and only three matching pairs limit inferential scope.
- This is a failed contribution gate, not a failed implementation or erased run.

## 6. Artifacts and review

V2 config SHA-256: `910cb51f0307c1750cbb5808fa4622a77a43c1094e3dfa830d57beb39d82b684`.
V2 training/audit time: 99.38 seconds, CPU.
Runtime: `{'python': '3.13.2', 'torch': '2.10.0', 'numpy': '2.4.3', 'scipy': '1.16.2', 'device': 'cpu'}`.
Exact source snapshots, all checkpoints/data, selection and validation files,
fill ledgers and hash manifests remain in ignored output directories:

- `outputs/market-cycle/matched-coverage-v2/`
- `outputs/market-cycle/v1-duration-diagnostic/`

[Independent specification/code review](MARKET_CYCLE_MATCHED_REVIEW_V2.md).
No classical comparator, failed match, initialization or negative result was
removed. No training outcome or simulator profit was advertised as established
publication novelty.

## 7. Next contribution gate

[Pinned MarS artifact readiness](MARS_EXTERNAL_READINESS_V2.md) is now concrete.
Before a new paper claim, implement real fill accounting and response interventions
in the released generator, compare original realism/impact checks with cycle
diagnostics, and establish the interpretation limits. Profitable external cycles
alone still cannot prove a false real-market counterfactual. If that route supplies
no consequential gap either, change the research question rather than tune this
linear toy until a favorable result returns.

## Figure

[Controlled follow-up figure](../figures/generated/matched-coverage-v2/followup.pdf) shows the exact-data training-duration diagnostic beside the matched-multiset final models. Left-bank and right-bank minima are from different schedule sets and must not be compared as if they shared the same audit bank. Each point represents a fitted model; no confidence interval over three initializations is claimed. Plot metadata records the pinned tueplots 0.2.4 release, style/source hashes, fonts and result-file hashes.
