## Executive summary (read this first)

This specification fixes the first controlled-reference experiment. It validates
the cash ledger and cycle detector using an established admissible transient
impact model and an intentionally malformed execution control. It is not a
learned-generator experiment, a novel economic model, or a paper result.
Configuration: `experiments/reference_controls_v1.json`. All parameters are
synthetic experimental definitions, not estimated market measurements.

## 1. Fixed scope and units

One asset, fixed one-second grid, fully filled market orders, no latency, no
partial fills, no passive liquidity provision. Signed quantities q_t are in asset
units; purchases are positive. Prices are currency per unit. Cash is currency.
Inventory starts and ends at zero; initial impact and cash are zero. Borrowing
and short sales are unrestricted within the absolute per-step quantity limit.
No hidden financing cost is assumed. These idealizations are explicit limitations.
Only deterministic, predeclared schedules are considered. Adaptive strategies and
real order books are outside this reference pilot's claim.

## 2. Timing and execution equations

At step t the unaffected price S_t and decayed pre-trade impact h_t are known.
For impact scale gamma, decay rho and grid dt, set a = exp(-rho dt).

1. Fill q_t at average price P_t = S_t + h_t + gamma q_t/2
   + sign(q_t) * half_spread.
2. Update cash by -q_t P_t - abs(q_t) * fee_per_unit; inventory by q_t.
3. Decay post-trade impact: h_(t+1) = a * (h_t + gamma q_t).
4. Sample the next independent zero-mean Gaussian unaffected-price increment,
   with standard deviation sigma sqrt(dt), after the current fill.

For zero orders, the ledger records a zero-quantity row, not an executed trade.
All terminal inventory is closed by the specified final orders; there is no
unreported liquidation or final-price mark-to-market substitution.

Let K_ts = gamma * a^abs(t-s) and k = half_spread + fee_per_unit.
For a deterministic closed schedule sum(q)=0:

E[C(q)] = (1/2) q^T K q + k sum(abs(q_t)),

where C is initial cash minus terminal cash. S_0 cancels and zero-mean shocks
have zero expected contribution. Positive cost means cash was lost.

### Admissibility argument

For 0 <= a < 1, matrix a^abs(t-s) is the covariance of a stationary unit-variance
AR(1) process Z_t = a Z_(t-1) + sqrt(1-a²) epsilon_t. Thus K is positive
semidefinite for gamma >= 0. At a=1 it is a rank-one nonnegative matrix.
Nonnegative spread and fee preserve nonnegative expected cost. Strict positivity
requires additional parameter/schedule conditions; it is not claimed globally.
This is established mathematics, used as reference infrastructure.

Direct foundation: [Alfonsi, Klock and Schied, section 2, Lemma 2.3 and
Proposition 2.6](https://arxiv.org/html/1310.4471v3). The independent
[derivation review](MARKET_CYCLE_REFERENCE_REVIEW_2026-09-29.md) checked the
average execution convention and discrete quadratic cost. Also see
[Gatheral, Schied and Slynko](https://doi.org/10.1111/j.1467-9965.2011.00478.x).

## 3. Intentionally invalid control

Omit gamma q_t/2 from the fill price while retaining the full impact update.
This changes execution economics deliberately; it is not a learned model.
For q=(Q,-Q) separated by one dt:

- valid expected cost = gamma Q²(1-a) + 2k abs(Q);
- invalid expected cost = -gamma a Q² + 2k abs(Q).

Choose gamma a Q² > 2k abs(Q) + delta to make the invalid control detectable.
Pilot delta is 0.10 currency units. Gains from this rule validate the detector;
they do not demonstrate novel manipulation or defects in MarS/TRADES.

## 4. Predeclared reference pilot

Configuration v1: S_0=100, gamma=0.02, rho=0.1 per second, dt=1 second,
half_spread=0.005, fee=0.001 per unit, sigma=0.1 per sqrt(second),
absolute step quantity <=20. Run 512 independent exogenous episodes.
Seed 20260929. Four fixed schedules:

| Name | Signed quantities on the fixed grid |
| --- | --- |
| Two trades | 20, -20 |
| Hold then close | 20, 0, 0, 0, -20 |
| Slow entry, fast exit | 5, 5, 5, 5, -20 |
| Fast entry, slow exit | 20, -5, -5, -5, -5 |

The two controls share identical episode/step shocks. Stable draw IDs here are
(episode, grid step); actions never change the exogenous grid or draw count.
This coupling argument does not automatically extend to event-driven simulators.
Four schedules are detector development data. None is a sealed learned-model
confirmation family. Mirror/randomized signs, sizes, latency and held-out cycle
families are required for the subsequent study, not silently claimed here.

## 5. Statistical interpretation

Let inventory I_t = sum_(s<=t) q_s. Noise cost is
-sum_(t<T-1) I_t * increment_t, with variance
sigma² dt sum_(t<T-1) I_t².
For deterministic schedules with Gaussian shocks, sample-mean variance is
exactly this variance divided by independent episode count.

Use two-sided Gaussian intervals with known variance. Bonferroni adjustment over
four schedules times two controls gives simultaneous coverage at least 95%.
No asymptotic normal approximation or sample-variance substitution is needed.
Shared shocks create dependence, but the Bonferroni union bound remains valid.
Record individual episode ledgers and configuration/source hashes.

Detector development success: valid analytical expected costs are nonnegative;
two-trade invalid control's upper simultaneous cost bound is below -delta;
terminal inventory is zero, and mean costs are reported beside exact expectations.
A realized profitable reference episode is permitted by market noise.
Failure to reject a violation is not proof of model admissibility; the reference
property follows from its algebra, not a collection of nonnegative sample means.

## 6. Implementation and artifact commands

The package `src/market_cycle/` is separate from shared competition scoring.
It has no third-party runtime dependencies and does not reimplement CRPS or
Agenthon gates. All pilot measurements and ledgers remain under ignored outputs.

```sh
PYTHONPATH=src python -m market_cycle \
  --config experiments/reference_controls_v1.json \
  --output outputs/market-cycle/reference-controls-v1.json
```

Outputs are created exclusively; existing research artifacts cannot be silently
overwritten. Preserve explicit failure messages and do not discard episodes.
The current CLI is for this reference pilot only, not a generic market harness.

## 7. Next study gate

After this infrastructure check, freeze a separate known-reference learning
experiment: equal-budget action coverage conditions, model architecture,
training/development split, strong structural and response-calibration comparators,
held-out cycle families, effect threshold and fidelity tolerance. Use pilot
variance to plan confirmation precision. No neural training or paid compute is
launched by this specification. A simple reference passing these checks supplies
no evidence that the proposed paper contribution is novel or established.
