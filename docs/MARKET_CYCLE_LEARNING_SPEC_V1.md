## Executive summary (read this first)

This is a frozen CPU development pilot to compare learned pre-trade responses
under three action-data coverage conditions. It uses known synthetic reference
labels, a common correct fill ledger, a fixed architecture/optimization budget,
and strong established comparators. No new correction method is proposed here.
A neural approximation failure alone does not establish a publishable contribution.
Results cannot be treated as sealed paper confirmation or empirical LOB defects.

Configuration: `experiments/learning_coverage_v1.json`. The first run is executed
only after this specification is saved. Any later changes require a new version.

## 1. Question and identifying contrast

Does restricted action coverage leave low validation error on its own distribution
while producing worse response composition and cycle costs on a shared evaluation
set? Compare one-direction, randomly balanced-cycle, and unrestricted signed
training sequences under identical sequence count, number of target rows, model
initializations, architecture, optimizer and full-batch update count.

The reference is the discrete exponential-impact market in
[reference specification](MARKET_CYCLE_EXPERIMENT_SPEC_V1.md). Initial impact is
zero. Keep gamma q_t/2 self-impact, spread, fees, fill rules and unaffected-price
law fixed in every audit. Substitute only pre-trade impact predicted from history.
The deliberately malformed self-impact control is not used as a learned outcome.

## 2. Data-generating process and information contract

Each training sequence has 16 steps and 512 sequences per coverage. At time t,
input x_t is the previous 16 signed quantities, most recent first, normalized by
20 units. Zero-pad before sequence start. Current and future quantities are absent.
The target, normalized by gamma*20, is sum_(lag>=1) a^lag*x_t[lag-1].
Because all evaluated histories begin from zero impact and last <=16 steps, no
response memory is omitted. The sixteenth lag is unused; report active-design
rank rather than assuming 16 independent columns. There is no noise in labels.

- **One direction:** independent integer magnitudes 1..20, one randomly selected
  sign for each entire sequence. Both signs are represented; sequences are not
  literal mirrored duplicate pairs.
- **Balanced cycles:** eight independently sampled magnitudes 1..20; concatenate
  their positive and negative copies and permute all 16 actions independently
  per sequence. The terminal inventory is exactly zero.
- **Unrestricted signed:** independent integer actions -20..20 at each step.

Splits are by whole sequences: train seed 4101, validation seed 4102.
Validation contains 128 fresh sequences of each coverage. These disjoint streams
produce fresh trajectories; equality of individual feature rows across splits
is possible in this finite action domain and is not claimed impossible.

Coverage conditions also change sign transitions, terminal inventory and slightly
change magnitude/zero distributions. Record these differences. The pilot can
identify a coverage-condition contrast, not isolate composition alone from all
marginal differences. A matched-marginal follow-up is required for that stronger
claim. None of these synthetic values is a real-market estimate.

## 3. Learners and comparators

**Neural:** fully connected 16→32→32→1, tanh hidden layers, float64, mean squared
response loss, Adam with learning rate 0.003, 200 full-batch updates, one CPU thread.
Three initialization seeds: 101, 102, 103. Same training data within a coverage
for all seeds. No early stopping, tuning or selection on cycle outcomes.

**Unconstrained linear fit:** least-squares impulse coefficients, no intercept,
using the same features and targets. Save coefficients and design rank.
The reference is linear, so this is an especially strong comparison.

**Admissible exponential fit:** fit decay a in [0.001,1] to the same training
response targets. Impact scale is the common known gamma, also used by the correct
instantaneous self-impact term. Fitting only decay preserves compatibility between
lagged response and fill diagonal. Report fitted decay; do not call it a known-
parameter oracle. An independently fitted scale with unchanged diagonal could
break admissibility, so that is excluded.

**Oracle reference:** exact generating parameters are used only for labels,
reference cost and evaluation differences. Do not count it as a learned baseline.
The structural comparator has the correct parametric family; explicitly acknowledge
this favorable specification rather than claiming a universal model superiority.

## 4. Common evaluation and cycle schedules

Report training response RMSE, fresh same-coverage validation RMSE and one common
validation RMSE over all three coverage banks. Use currency per unit for response
error. Own-distribution error alone cannot support cross-condition comparisons.

Fourteen deterministic cycle schedules are seven families with both buy-first
and sell-first signs: two trades, 14-step pause, slow entry/fast exit, fast entry/
slow exit, eight-step entry and exit blocks, alternating trades, double pulses.
All quantities are within the 20-unit step bound, terminal inventory is zero,
and horizon is <=16. Definitions are saved in the run artifact.

These are predeclared development families; no policy search is performed and
none is a sealed confirmation set. Balanced training permutations can overlap
some cycle patterns. Do not claim a fully disjoint semantic family split.
Distinguish zero exact schedule overlap from meaningful family generalization.

For each schedule, predict pre-trade impact from its past actions and execute
through the unchanged ledger. Compute learned expected cost using zero unaffected
increments. This equals expected cost under the declared zero-mean price law
because response predictions do not depend on price shocks. Save every fill,
reference cost, cost discrepancy and response RMSE.

Report how many cycles have learned expected cost < -0.10 currency units, and
minimum cost. Exact deterministic expectations need no Monte Carlo confidence
interval. Three model seeds describe optimizer sensitivity on fixed data; they
are not independent training datasets or adequate population-level inference.

## 5. Interpretation and falsification

- Low own-coverage error plus cross-coverage cycle failure supports a restricted
  coverage/approximation finding within this stylized setting.
- If least squares recovers the reference and has no failure, report it prominently.
  This may indicate an unnecessarily misspecified neural approximation, not a
  substantive new economic phenomenon.
- If all neural models pass, report no failure in the declared development family.
  Do not tune until a profitable artifact appears and relabel it confirmation.
- A large gap with large common response error does not establish that conventional
  fidelity checks missed the defect. That stronger claim needs a meaningful
  fidelity-matched comparison and mechanism attribution.
- Negative expected cost under this stipulated response does not establish risk-
  free arbitrage, real-market counterfactual truth or an external-generator defect.

## 6. Artifacts and run command

Save training actions/features/targets, comparator coefficients, fitted parameters,
weights for every neural seed, optimization loss trajectories, cycle definitions,
fill ledgers, source/config hashes, runtime versions and elapsed time. Files remain
in ignored outputs; keep failed runs instead of overwriting them.

```sh
PYTHONPATH=src python -m market_cycle.learning_run \
  --config experiments/learning_coverage_v1.json \
  --output-dir outputs/market-cycle/learning-coverage-v1
```

The output directory must not already exist. CPU-only; no remote service, paid
compute, competition data, external checkpoints or publication action is used.
See [independent design review](MARKET_CYCLE_LEARNING_REVIEW_V1.md).

## 7. Following academic decision

Assess whether a fidelity-matched learned composition mechanism remains beyond
ordinary approximation error and known truncation/discretization effects. Only
then select a correction and freeze a new confirmation protocol, with held-out
families, independent training datasets and strong response-calibration baselines.
This pilot does not satisfy those contribution gates merely by completing.
