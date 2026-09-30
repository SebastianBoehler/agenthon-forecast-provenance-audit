## Executive summary (read this first)

Independent primary-source review: advance only as an experimental hypothesis.
The major correction is identifiability: profitable cycles in a pretrained model
do not establish an artificial learned response. An unrelated admissible reference
does not supply counterfactual truth for MarS or TRADES. Use a controlled neural
surrogate experiment for causal attribution, and external pretrained models for
diagnostic stress tests. Novelty remains conditional on a consequential mechanism
and a correction outperforming strong established baselines.

Reviewed 29 September 2026. No code, tests, simulation or training was run.
This review covers the reassessment, source review and subsequently saved
`MARKET_CYCLE_PROPOSAL_2026-09-29.md` draft.

## Recommendation and scientific status

**Proceed to a falsifiable experiment specification, not a novelty certificate.**
Current idea is plausible. Generic interactive simulator validation, arbitrage
correction, and RL discovery of manipulation all have close predecessors.
Combining those terms is not enough to create a substantial contribution.
The target should be a specific failure of learned action-dependent impact
composition that conventional checks miss, followed by an effective correction
and transfer to unseen cycle schedules. The evidence has not been obtained.

## Blocking identification issue

No-manipulation is a property under specified economics and trading rules.
It does not follow from statistical realism, zero terminal inventory, or removal
of a forecasting signal. A real-data generator can retain drift, inventory risk,
legitimate feedback and liquidity provision. An action response may be wrong
without generating profit; a profitable response may be legitimate.

Use two distinct evidence tiers:

1. **Controlled identification.** Learn neural transition/response surrogates
   from a known admissible data-generating process (DGP). Keep the execution
   convention, spread, fees, allowed actions and exogenous shocks identical.
   The reference must be demonstrably admissible under the actual discretized
   execution rules, not only under a continuous-time theorem. Evaluate frozen
   policies in both systems. A learned response deviation with an absent
   reference gain supports a scoped surrogate-artifact claim.
2. **External diagnostic.** Run the same finite schedule family in pretrained
   MarS/TRADES. Report simulator cash gains and response sensitivities. Unless
   a justified matched intervention/reference exists, do not call them false
   real-market counterfactuals or proven learned manipulation artifacts.

Randomized initial buy/sell direction reduces direction selection, but does not
identify genuine market counterfactuals or remove every inventory-response effect.
Freezing the background model is an ablation that changes the environment, not an
oracle. Replay is likewise a diagnostic control, not responsive market truth.

## Closest primary sources and design corrections

| Source and inspected material | Existing contribution | Consequence for us |
| --- | --- | --- |
| [Gatheral 2010](https://doi.org/10.1080/14697680903373692); publisher abstract and [author presentation](https://pdfs.semanticscholar.org/3683/ecb4dae470f4df219d65bb6491d3c7fd4b78.pdf), slides 3–21 | Impact shape and decay must be compatible with nonnegative expected round-trip costs. | Round-trip tests and nonlinear-impact incompatibility are inherited economics. The fetched 47-page PDF is slides, not full journal text; do not record it as the journal paper. |
| [Tsaknaki, Macri and Lillo 2026](https://arxiv.org/html/2607.06121v1), introduction and sections 2–3 | Nonlinear permanent impact plus linear temporary impact admits manipulation; DDPG and SLSQP search compared in finite samples. | RL search is occupied. Diagnose a learning-induced mismatch against the same admissible DGP, rather than rediscover assumed manipulation. |
| [MarS](https://arxiv.org/html/2409.07486v2), sections 4.3–4.4 and Appendix K | Generative order simulation, impact/decay analysis, symbolic-regression mechanisms and RL execution. | Do not claim prior MarS evaluation is only price-path realism. Compare its actual one-direction impact and decay checks with cycle behavior. |
| [TRADES](https://arxiv.org/html/2502.07071v2), section 7.1 | Responsive diffusion simulator tested by a buy-side POV intervention; explicitly limits real-market profitability inference. | An additional profitable trading example is weak novelty. Test composition and reversal, then explain why its intervention diagnostics miss the demonstrated failure. |
| [INTAGS](https://arxiv.org/html/2309.01784v3), introduction, feedback section, Appendix B.1 and D.1 | Interactive simulator calibration by causal response-distribution discrepancy, with confounding correction and ABIDES as experimental reality. | Major omitted predecessor. Generic causal response auditing plus learned simulator correction is occupied. Include a response-calibration comparator inspired by its action-to-next-return/impact objective. |
| [Arbitrage-free neural-SDE market models](https://arxiv.org/html/2105.11053v2), introduction, sections 4.1–4.3 and Appendix A | Neural dynamics with option no-arbitrage constraints; combines statistical reconstruction and dynamic restrictions, validated on known synthetic dynamics. | Learned financial simulation plus arbitrage constraints and fidelity is established. Distinguish action-induced market impact from passive option-surface consistency. |
| [Risk-Neutral Market Simulation](https://arxiv.org/abs/2202.13996), abstract only | Neural spline-flow simulation removes conditional drift while minimizing divergence from historical data subject to risk neutrality. | Drift removal with fidelity preservation is occupied. Read full text before choosing a correction resembling its measure adjustment. |
| [Bridging the Reality Gap](https://arxiv.org/html/2603.24137v1), impact-kernel section and Appendix D | Responsive LOB feedback with power-law-decay target and nonnegative exponential-mixture implementation. | Kernel-based structural response corrections and efficient implementation have strong precedent. A standard admissible kernel alone cannot be the headline method. |

## Do not conflate two different no-arbitrage notions

Classical equivalent-martingale-measure existence is not the assertion that
historical returns have zero conditional expectation under the data measure.
Risk premia and predictable returns need not imply classical arbitrage.
Gatheral-style manipulation concerns expected trading cost caused by the trader's
own impact under explicit dynamics. Option-price martingale constraints target a
different mechanism. Calling both “no arbitrage” without qualification creates a
false novelty comparison and can lead to removing legitimate empirical dynamics.

## Strong comparison set for a proposed correction

- Matched unconstrained learner: same data, architecture, optimization budget.
- Correctly discretized admissible structural impact model: linear response with
  a positive semidefinite quadratic cost on the relevant closed-cycle subspace,
  including the chosen self-impact/execution-price convention.
- Flexible structural response baseline, such as a nonnegative mixture of valid
  decay components; prove or verify the full execution model's condition.
- Interactive response-calibration baseline motivated by INTAGS.
- Simple penalty/clipping and no-response ablations, clearly distinguished from
  useful repairs. Suppressing trading or erasing all response is not success.

Possible learned correction candidates include an audit-generated constraint
penalty with frozen holdout schedules, or projection of a learned finite-grid
linear response onto an admissible cost set. These are candidate baselines until
their difference from established constrained estimation is justified. A PSD
projection is standard linear algebra, not a stand-alone novel contribution.
For nonlinear, state-dependent generators a fitted kernel certificate does not
certify the actual generator; it only characterizes that approximation.

## Experiment requirements before claiming a mechanism

1. Predeclare open-loop cycle families, domain bounds, terminal liquidation and
   economically meaningful gain threshold. Include unequal entry/exit rates;
   symmetric buy-then-sell alone can miss known manipulation mechanisms.
2. Separate action-frequency/latency discretization errors, fill/accounting bugs,
   exogenous drift, and neural history-response mismatch through interventions.
3. Use actual fills and cash ledgers; preserve unfilled orders and forced-close
   costs. Never drop failed closures or favorable/unfavorable simulation failures.
4. Freeze discovered schedules before independent evaluation; report independent
   reset-state blocks, uncertainty, search budget and multiplicity. A single
   shared seed is insufficient when actions alter random draw/event counts.
5. Require repair transfer across held-out schedule shapes, sizes, latency regimes
   and model initializations. Separate extrapolation from interpolation results.
6. Measure the original generator's fidelity and one-way impact/decay metrics,
   held-out execution cost, and runtime alongside cycle results. Predeclare what
   fidelity loss would invalidate the repair.
7. Claim finite-family coverage only. Passing the audit is not universal freedom
   from dynamic manipulation, and negative results require adequate precision.

## Decision gates

### Follow-up review of the concrete draft

The saved draft incorporates the central two-tier correction, discrete-reference
assumptions, actual-fill accounting and selection-bias controls. Three remaining
wording/design corrections should be applied before experiment specification:

- Section 6 says a training penalty includes schedules “unseen during
  optimization.” Every schedule contributing to optimization is training data.
  Say “newly generated development schedules”; reserve a distinct sealed family
  for evaluating generalization, with no penalty, hyperparameter or repair choice
  based on those confirmatory outcomes.
- Add the strong interactive-response calibration comparator motivated by INTAGS
  to the actual methods/control list, not merely the literature table.
- State unequal entry/exit rates and timing as required schedule coverage.
  Symmetric cycles alone can miss established impact incompatibilities.

The wording “reference-minus-surrogate cycle cost” also needs a fixed sign/unit
definition in the experiment specification, and admissibility disagreement needs
an uncertainty-based decision rule rather than classifying noisy means by sign.
These are specification obligations, not reasons to claim the direction failed.

| Gate | Present status |
| --- | --- |
| Controlled DGP and discrete execution assumptions specified | Required |
| Learning-induced cycle defect established | No evidence yet |
| Specific mechanism beats drift/accounting/known-impact explanations | No evidence yet |
| Correction exceeds strong structural and response-calibration baselines | No evidence yet |
| Fidelity and transfer preserved | No evidence yet |
| Exact novelty checked against closest algorithms | Bounded review only |

If the only finding is known impact inconsistency in a toy model, the proposed
paper has not met the user's contribution threshold. If controlled and external
evidence reveal a consequential composition failure with a useful generalizing
correction, that would support a substantially stronger paper. This is a design
judgment, not an acceptance prediction.
