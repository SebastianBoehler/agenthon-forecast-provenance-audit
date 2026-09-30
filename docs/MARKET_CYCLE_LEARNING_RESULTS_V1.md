## Executive summary (read this first)

The frozen development pilot trained nine small neural response models and
six fitted classical comparators. Two of three one-direction-trained neural
models produced negative expected costs on the declared alternating schedules.
The balanced-cycle and unrestricted-sign neural models had no detected violation
among the fourteen schedules at the -0.10 currency threshold. Both classical
fits recovered the linear reference almost exactly and had no violation.

This supports a limited action-coverage/approximation finding. It does not yet
establish a new mechanism, a fidelity-preserving correction, real-generator
defects or paper-level novelty. Different fitting quality and changed action
marginals remain alternative explanations.

## Frozen run and artifacts

- Configuration SHA-256: `7df7af29723599c6c463f7d2fcd597edf03ebe1aa8d6c0470631efcbc2f3b832`.
- Training/analysis elapsed: 8.00 seconds on CPU.
- Runtime: Python 3.13.2, PyTorch 2.10.0, NumPy 2.4.3, SciPy 1.16.2.
- Training: 512 × 16-step sequences per coverage, fixed data seed, three neural
  initialization seeds, 200 equal full-batch optimization updates per model.
- Each model uses the same correct half-self-impact, spread and fee ledger.
- Training arrays, all nine checkpoints/loss histories, fitted coefficients,
  cycle fills, runtime/config/source hashes and artifact hashes are retained in
  ignored `outputs/market-cycle/learning-coverage-v1/`.
- Results have status `development_pilot_not_confirmatory`.

## Results

| Coverage / model | Own validation RMSE | Common validation RMSE | Minimum expected cost | Cycles below -0.10 |
| --- | ---: | ---: | ---: | ---: |
| one_direction/linear_ls | 5.39132e-16 | 6.50878e-16 | 1.001301 | 0 |
| one_direction/admissible_exponential | 1.57787e-08 | 1.0003e-08 | 1.001301 | 0 |
| one_direction/mlp_seed_101 | 0.0891715 | 0.0944475 | 0.209947 | 0 |
| one_direction/mlp_seed_102 | 0.0917294 | 0.103507 | -5.316997 | 2 |
| one_direction/mlp_seed_103 | 0.0894562 | 0.096308 | -4.859397 | 2 |
| balanced_cycles/linear_ls | 4.5531e-16 | 4.0571e-16 | 1.001301 | 0 |
| balanced_cycles/admissible_exponential | 2.43203e-09 | 7.3084e-09 | 1.001301 | 0 |
| balanced_cycles/mlp_seed_101 | 0.0136061 | 0.138287 | 0.624835 | 0 |
| balanced_cycles/mlp_seed_102 | 0.0138012 | 0.133975 | 0.603708 | 0 |
| balanced_cycles/mlp_seed_103 | 0.0137782 | 0.136083 | 0.572478 | 0 |
| unrestricted_signed/linear_ls | 1.02688e-15 | 9.54923e-16 | 1.001301 | 0 |
| unrestricted_signed/admissible_exponential | 5.99364e-09 | 9.46379e-09 | 1.001301 | 0 |
| unrestricted_signed/mlp_seed_101 | 0.0314617 | 0.106463 | 0.414015 | 0 |
| unrestricted_signed/mlp_seed_102 | 0.0313467 | 0.106408 | 0.431240 | 0 |
| unrestricted_signed/mlp_seed_103 | 0.0308234 | 0.107311 | 0.445473 | 0 |

RMSE is response error in currency per asset unit. Cost is currency, including
spread and fees. Negative expected cost is positive expected terminal cycle cash.
Expected costs are exact for each frozen action-only predictor under the specified
zero-mean unaffected-price law; they are not means over real market episodes.
No confidence intervals are assigned to three fixed-data initialization seeds.

## What happened and what remains unproved

- One-direction seeds 102 and 103 each violated the cost threshold for the two
  mirrored alternating schedules. Minimum costs were -5.316997 and -4.859397.
- Seed 101 in the same coverage did not violate it; initialization matters here.
- Least-squares design rank was 15 of 16 in all three datasets. The last lag is
  structurally unobserved; all fifteen relevant lag coefficients were recovered.
- Fitted exponential decay agreed closely with the reference. Its gamma was
  fixed to the common self-impact scale, as declared in the protocol.
- Balanced-cycle training had lower own-distribution response error but higher
  common-bank error than one-direction training. Despite this, its tested cycle
  costs stayed positive. These results show that the chosen scalar error metric
  does not order this particular finite-family cost statistic; they do not prove
  broadly realistic simulators can hide economic defects.
- One-direction neural fitting error is materially larger than the near-exact
  classical fit. Ordinary model misspecification/underfitting is a strong null
  explanation. No claimed correction is justified by this run.

## Independent review and exploratory diagnostic

The [design/code review](MARKET_CYCLE_LEARNING_REVIEW_V1.md) found no blocking
inconsistency in the frozen setup. It identified initial-state prediction error
as a reporting issue. Post-run, we inspected all-zero-history neural predictions:
- one_direction/mlp_seed_101: -0.00061825 currency per unit; minimum-cost schedule `alternating_buy`.
- one_direction/mlp_seed_102: -0.00005521 currency per unit; minimum-cost schedule `alternating_buy`.
- one_direction/mlp_seed_103: -0.00297641 currency per unit; minimum-cost schedule `alternating_sell`.
- balanced_cycles/mlp_seed_101: -0.00065421 currency per unit; minimum-cost schedule `two_trade_buy`.
- balanced_cycles/mlp_seed_102: -0.00004795 currency per unit; minimum-cost schedule `two_trade_sell`.
- balanced_cycles/mlp_seed_103: 0.00107168 currency per unit; minimum-cost schedule `two_trade_sell`.
- unrestricted_signed/mlp_seed_101: -0.00000567 currency per unit; minimum-cost schedule `two_trade_buy`.
- unrestricted_signed/mlp_seed_102: 0.00066735 currency per unit; minimum-cost schedule `two_trade_sell`.
- unrestricted_signed/mlp_seed_103: 0.00145353 currency per unit; minimum-cost schedule `two_trade_sell`.

This diagnostic was added after viewing results and is explicitly exploratory.
Do not claim every neural model respects the zero-impact reset exactly. No
centering correction was applied, no model retrained and no seed dropped.

## Coverage and inference limits

The coverages differ in sign transitions, terminal inventory and magnitude/zero
marginals; this is not a composition-only intervention. Recorded mean normalized
absolute actions were approximately 0.526, 0.522 and 0.515. Multiply by 20 for
physical units. Fixed-data initialization repeats do not establish a distribution
over training datasets. The development schedule bank is finite and can overlap
balanced training pattern families. No sealed confirmation family was used.

## Figure and reproducibility

[Development figure](../figures/generated/learning-coverage-v1/coverage_pilot.pdf).
PNG preview and plot metadata are alongside the PDF. Shared tueplots style and
figures4papers-inspired clarity/vector-export conventions were used. Points are
individual models; classical fits overlap. Analysis canvas is provisional and
does not establish a final paper template. The figure was visually inspected.

## Runtime failures and recovery

Two launches failed during SciPy import before data generation: the installed
1.15.3 and a freshly installed same-version wheel had a malformed PROPACK binary
on this Mac. A local ignored `.venv` with system-site-packages and a SciPy 1.16.2
wheel resolved the import. The global environment was unchanged. This changed
the dependency runtime, not data/architecture/optimization configuration.
A failure record remains under ignored outputs. The successful command was:

```sh
PYTHONPATH=src .venv/bin/python -m market_cycle.learning_run \
  --config experiments/learning_coverage_v1.json \
  --output-dir outputs/market-cycle/learning-coverage-v1
```

## Next academic decision

Proceed to a matched-marginal, fidelity-controlled learning specification with
independent training datasets and mechanism interventions. Inspect whether the
failure persists after comparable fitting quality and initial-state handling;
include classical comparators throughout. Do not turn this toy result into the
paper headline without that evidence and external relevance. The larger novelty
and useful-repair gates remain open.
