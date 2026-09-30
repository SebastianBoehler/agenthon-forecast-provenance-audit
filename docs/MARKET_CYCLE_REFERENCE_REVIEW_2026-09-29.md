## Executive summary (read this first)

The proposed discrete exponential-impact reference is mathematically sound under
the stated average-fill convention, fixed grid, zero initial impact and an
unaffected martingale price. Its half-self-impact term is essential. Removing
that term provides a valid detector control, but represents a stipulated
execution-model defect, not evidence of a neural-model failure or novel result.
No implementation, simulation or tests were run during this review.

Review date: 29 September 2026. This checks the supplied derivation and the
subsequently saved experiment specification, implementation and pilot report.

## 1. Exact contract and independent algebra

Let trades occur at times t=0,...,N-1 on a grid of spacing delta>0. Let q_t be
signed shares, positive for buying, and require sum(q_t)=0. Set gamma>0,
rho>0, a=exp(-rho*delta), and friction k>=0 in cash per share.

Before the current trade, impact is

`h_t^- = gamma * sum_{s<t} a^(t-s) q_s`.

The actual average execution price is stipulated as

`p_t = S_t + h_t^- + gamma*q_t/2`.

The last term follows from integrating a linear price change through the current
block order. Cash decreases by `q_t*p_t + k*abs(q_t)`. Inventories increase by
q_t, with every stipulated quantity filled. There is no hidden mark-to-market
liquidation, partial fill, limit-order rebate or external initial impact.

Define purchase cost `C = sum_t q_t*p_t + k*sum_t abs(q_t)`; terminal cycle cash
gain is `-C`. Therefore

`C = sum_t q_t*S_t + (gamma/2)*sum_t q_t²`
`    + gamma*sum_{s<t} a^(t-s)*q_s*q_t + k*sum_t abs(q_t)`.

For a deterministic schedule and an integrable martingale S_t,
`E[sum_t q_t*S_t] = E[S_0]*sum_t q_t = 0`.
Consequently, with `K_st = gamma*a^abs(t-s)`,

`E[C] = (1/2)*q^T*K*q + k*sum_t abs(q_t)`.

This derivation is algebra for the proposed specification. It does not establish
that an empirical LOB follows this contract.

## 2. Positive definiteness and parameter edges

For 0<a<1, take a stationary unit-variance AR(1) process Z_t with innovation
variance 1-a². Its covariance is `Cov(Z_s,Z_t)=a^abs(t-s)`, hence
`q^T*K*q = gamma*Var(sum_t q_t*Z_t)>=0`. Independent nondegenerate innovations
also imply strict positivity for any nonzero finite q. Thus nontrivial closed
cycles have positive expected impact cost, before adding nonnegative friction.

If rho=0, K is rank one and its cost vanishes on closed cycles; it remains
nonnegative, but strict positivity is lost. gamma=0 likewise removes impact.
Negative gamma, rho or friction are outside this reference contract. Numerical
eigenvalue tolerance is an implementation check, not the theoretical proof.

## 3. Positive detector control

Omit the current-trade half-self-impact term while retaining lagged response.
For the two-trade schedule `(Q,-Q)` spaced by delta,

- Valid expected cost: `gamma*Q²*(1-a) + 2*k*abs(Q)`.
- Malformed expected cost: `-gamma*a*Q² + 2*k*abs(Q)`.

The malformed control is detectably profitable only when
`gamma*a*Q² > 2*k*abs(Q)`, and its gain should exceed the predeclared minimum
detectable effect within permitted quantity bounds. With insufficient quantity,
friction can mask the defect; the detector should not manufacture a positive
label. This control isolates an execution convention, not neural learning.

## 4. Timing, adaptation and noise

State explicitly that S_t is observed before q_t and the next martingale shock
arrives after that trade. Fixed exogenous shock identities support valid pairing.
For identical deterministic q, the reference-minus-surrogate impact contrast can
cancel the shared unaffected-price term; genuine cycle PnL still has price noise.

Bounded adaptive schedules can also be covered under appropriate filtration and
integrability assumptions: writing post-trade inventory as X_t,
`sum_t q_t*S_t = -sum_{t=0}^{N-2} X_t*(S_{t+1}-S_t)` for a closed cycle.
Its expectation is zero when X_t is measurable before that increment and the
increment has zero conditional mean. Keep the initial scientific claim confined
to deterministic schedules unless adaptive admissibility is explicitly specified.
Adaptive actions cannot see future noise or a privileged simulator seed.

The martingale is an explicit synthetic-world assumption under the simulation
measure. It is not an inference that historical returns lack drift, nor a
risk-neutral measure transformation of an empirical generator.

## 5. Direct primary-source grounding

[Alfonsi, Klock and Schied, Multivariate transient price impact and matrix-valued
positive definite functions](https://arxiv.org/html/1310.4471v3), section 2,
Lemma 2.3, Proposition 2.6 and its proof, directly specifies discrete block trades,
average pre/post execution prices, a martingale unaffected price and quadratic
expected cost. Its general positive-definite-kernel condition covers the scalar
specialization here. This is a more direct discretization reference than citing
Gatheral's continuous-time analysis alone. The model and proof are established
foundations, not our contribution.

[Gatheral, Schied and Slynko 2012](https://doi.org/10.1111/j.1467-9965.2011.00478.x)
provides the related continuous-time linear transient-impact foundation; its
publisher abstract was inspected, not its complete journal text in this review.

## 6. Implications for the experiment

- Keep the neural response experiment's ledger correct; do not make self-impact
  omission its purported learned failure. Train and evaluate the same fill rule.
- Label this controlled reference separately from external pretrained LOB models.
- Validate the gain threshold against friction before choosing positive controls.
- Report absolute cash units and normalized cost with an explicit denominator.
- Preserve neural initialization, coverage and schedule-family splits; a PSD
  response baseline may outperform unconstrained learning and must be compared.
- The audit is finite-family coverage. This reference's analytic guarantee does
  not confer a guarantee on an unconstrained neural generator.

An additional author-hosted primary document,
[Passivity-Preserving Model Reduction for Transient Cross-Impact](https://aalampour.com/papers/Passivity-Preserving%20Model%20Reduction%20for%20Transient%20Cross-Impact.pdf),
was found. Its bibliographic status needs verification before a formal reference;
it is relevant prior art for structure-preserving response reduction and should
be read before claiming an efficient admissible-kernel correction is novel.

## 7. Read-only inspection of the implemented pilot

Inspected `MARKET_CYCLE_EXPERIMENT_SPEC_V1.md`, the pilot report and
`src/market_cycle/{reference,pilot,__main__}.py`. No concrete inconsistency was
found within the fixed pilot scope. Execution adds half-self-impact and signed
spread, charges absolute-quantity fees, decays the post-trade response, and then
advances the unaffected price. Analytical cost and inventory-exposure variance
match these rules. Controls share stable grid/episode shocks.

For m schedules and two controls, the code uses the Gaussian quantile
`Phi^-1(1-alpha/(4*m))`: eight two-sided intervals at m=4, so the Bonferroni
coverage claim is correct despite their shared-noise dependence. Known Gaussian
variance justifies this calculation for deterministic schedules. Reported mean
differences equal the omitted half-self-impact cost; quoted intervals and claims
are consistent with the displayed expectations. The report properly confines
these measurements to reference infrastructure and claims no learned-model result.
This is static inspection, not an independently rerun experiment or test.
