## Executive summary (read this first)

We will investigate whether learning market responses from limited action data
introduces profitable closed trading cycles that the generating reference market
does not permit. The proposed contribution is a diagnosed response failure and
a repair that generalizes to unseen trading schedules while retaining useful
market behavior. This is an approved research direction, not an established
result or an acceptance guarantee. The proposal separates experiments with known
counterfactual truth from stress diagnostics on released market generators.

Working title: **Closed-Cycle Consistency in Learned Market Responses**.
Use the stronger “Realistic Prices, Inconsistent Responses” title only if results
establish both properties. Related to Agenthon Track 3 and its simulation,
verification and sequential-decision topics; independent of competition scoring.

## Latest evidence gate

The [matched follow-up and exact training replay](MARKET_CYCLE_MATCHED_RESULTS_V2.md) do not support a new persistent mechanism in the initial linear-surrogate setting. Both original profitable-cycle cases disappear with more optimization; stronger controlled comparisons pass the finite banks. This candidate has not met the paper contribution threshold. Retain the proposal as conditional; next assess [released-generator relevance](MARS_EXTERNAL_READINESS_V2.md) before claiming a mechanism or developing a correction.

## 1. Motivation and research question

Example: buy gradually, pause, sell, and finish with no inventory. A neural
simulator can reproduce ordinary price statistics yet respond incorrectly to the
composition of these actions. A trader optimizing against that simulator could
learn to exploit its response rather than learn a useful execution strategy.
Whether this happens in the selected models is our empirical question.

**Primary question:** When a learned action-response model approximates a known
market with nonnegative expected round-trip costs, what training coverage and
response structure determine whether that property survives on unseen cycles?
Can a targeted repair restore it while preserving held-out execution fidelity?

**External question:** Do released learned order-book generators exhibit analogous
cycle sensitivity, and which controlled interventions explain it? External
profits are diagnostics, not proof of an economically invalid real market.

The geometry intuition is a closed route through inventory and action history.
We compare the cash cost of traversing that route in the reference and learned
systems. Market state need not return to its starting point. Impact has memory;
this is not an assertion that markets are conservative vector fields.

## 2. Literature-derived contribution boundary

| Closest work | What is already established | What our evidence must add |
| --- | --- | --- |
| [Gatheral 2010](https://doi.org/10.1080/14697680903373692) | Restrictions on impact and decay that exclude price manipulation | A specific failure induced by learning a response, not a new no-manipulation principle |
| [MarS](https://arxiv.org/abs/2409.07486) and [TRADES](https://arxiv.org/abs/2502.07071) | Interactive learned markets, realism and impact evaluation | Explain whether fidelity checks miss composition errors; inspect actual implementations |
| [INTAGS](https://arxiv.org/abs/2309.01784) | Agent-guided interactive simulator evaluation and learning | A distinct economic response mechanism and held-out repair result; generic interactive auditing is occupied |
| [RL discovers manipulation](https://arxiv.org/abs/2607.06121) | Optimizers discover manipulation present in a specified impact model | Attribute gains to approximation error relative to the same generating market |
| [Arbitrage-free neural-SDE models](https://arxiv.org/abs/2105.11053) | Financial neural models with no-arbitrage constraints | Action-conditioned impact composition differs from option-price consistency; constrained training alone is not new |
| [Risk-Neutral Market Simulation](https://arxiv.org/abs/2202.13996) | Drift removal with a distributional closeness objective | Repair action-dependent response rather than remove physical-measure expected returns |

These distinctions are research obligations. A conjunction of existing methods
is not automatically a substantial contribution. Full-text comparison with the
newest collisions must precede any priority claim.

### Conditional contributions

1. Identify a reproducible failure mechanism linking action-data coverage or
   response memory to closed-cycle cost errors in learned simulators.
2. Develop and evaluate a mechanism-specific correction with transfer to held-out
   cycle families, against strong structural and penalty baselines.
3. Release an auditable benchmark with known generating responses, interventions,
   ledgers, failure controls, search history and versioned models.

A benchmark is useful only if it provides validated labels, meaningful coverage
and findings beyond a small set of handpicked attacks. No contribution is marked
established until its corresponding experiment is complete.

## 3. Research design versus implementation methods

**Research design:** controlled model-development and falsification study.
First derive the economic assumptions; then implement the audit, establish its
validity on reference controls, diagnose learned errors, evaluate repair on sealed
conditions, and test external relevance. This follows artifact construction and
empirical evaluation, with an explicit decision gate after each stage.

**Methods:** action-conditioned neural response estimation, deterministic fill
accounting, bounded cycle search, response interventions and held-out statistical
comparisons. Reinforcement learning is optional search machinery; it is not the
contribution. Start with finite schedule search to make coverage interpretable.

## 4. Two tiers of evidence

### Tier A: known generating market

Train neural surrogates on trajectories from the same explicitly admissible
reference market used for evaluation. Begin with linear transient impact whose
discretized execution-cost quadratic form is positive semidefinite on zero-sum
schedules, and a martingale unaffected-price process. Positive semidefinite means
that the quadratic form cannot become negative for permitted schedules. Verify
this property for the actual discrete timing and execution-price convention;
a continuous-time citation alone does not validate a discretization.

Vary action coverage: one-direction execution, balanced cycles, and varied
participation schedules under equal data and training budgets. Use an initially
simple neural surrogate before making claims about transformer or diffusion
architectures. Architecture generality requires an actual second architecture.

The reference, surrogate, ledger, initial states, action bounds and external
randomness must agree. Surrogate-generated response is the changed component.
Only here can a reference-versus-surrogate contrast identify an approximation
artifact under the declared assumptions.

### Tier B: released order-book generators

Start with MarS small released weights; investigate TRADES as a second model.
Use supported states and actual exchange fills. Public sample states outside
training support must be labeled accordingly. Do not transfer Tier A economic
assumptions to a pretrained real-data generator.

Reported outcomes: cycle profitability, sensitivity to conditioning/response,
ordinary impact and realism. These can suggest a mechanism; they cannot establish
real-market counterfactual truth. Similarity to Tier A is evidence of plausibility,
not proof of identical causation.

## 5. Accounting and attribution contract

- Signed quantity is positive for purchases. With actual fills, cash changes by
  minus quantity times execution price minus costs. Track inventory separately.
- End with zero inventory through actual liquidation. Include liquidation costs
  and failures; do not discard difficult-to-close episodes or substitute midprice.
- Record spread, fees, partial fills, latency, outstanding orders and borrowing
  assumptions. Initially isolate aggressive orders to avoid liquidity-provision
  profits being mislabeled as response defects.
- A zero-inventory cycle is not risk-free arbitrage. Our Tier A property concerns
  expected manipulation cost under explicit assumptions.
- Use fixed, mirrored, randomized-sign and adaptive schedules, including unequal
  entry/exit rates and timing. Separate positive
  sample profits from positive expected returns after schedule selection.
- Do not erase drift from a physical-measure model and describe that as correcting
  a bug. Legitimate predictability and response inconsistency are different.
- Pair randomness only with stable exogenous draw identities. Same-seed runs
  cannot be assumed paired when actions change event counts or random consumption.
- Failed simulation or closing episodes remain in coverage and failure reporting.

## 6. Hypotheses and distinguishing experiments

**H1:** Models fit on restricted action coverage can have small held-out
observational error yet substantial cycle-cost error on unseen compositions.
Compare equal-budget coverage conditions, not only model architectures.

**H2:** The cost discrepancy follows a measurable response-memory or asymmetry
error. Intervention should remove that error and the cycle effect together.
Compare altered memory/conditioning with a response-frozen diagnostic; disabling
all response is not a successful repair.

**H3:** A mechanism-specific correction generalizes beyond training cycles without
materially worsening ordinary execution fidelity. Predeclare the tolerated
fidelity loss after baseline measurement and before viewing repair results.

Candidate repairs to evaluate after diagnosis:

- A structural admissible impact model fitted to the same data, as a strong baseline.
- A flexible admissible decay-mixture structural comparator.
- An interactive response-calibration comparator motivated by INTAGS.
- A cycle-cost training penalty on newly generated development schedules; the
  sealed confirmatory families never contribute to training or repair selection.
- A response-memory constraint or projection addressing the demonstrated mechanism.

The last method is not selected yet. A generic penalty beating an unconstrained
network alone would be weak evidence of a new method. If a simple classical
structural model solves the problem with equal fidelity, report that comparison.

## 7. Evaluation and protection against selection bias

Split by initial market condition, schedule family and random seed. Search and
choose a repair on development data. Lock the selected model and search procedure
before confirmatory evaluation. Distinguish fresh seeds for the same schedule
from genuinely unseen schedule families.

Primary Tier A outcomes: cost discrepancy, expected net cycle cash gain, and
uncertainty-qualified disagreement with reference admissibility. For each episode,
define cost C as initial cash minus terminal cash after liquidation and costs.
Define discrepancy D = C_reference - C_surrogate in currency units; positive D
means the surrogate makes that cycle cheaper. Normalize separately by executed
notional for cross-size comparisons. A positive D alone does not establish
negative expected surrogate cost. Classify a manipulation finding only when the
held-out upper confidence bound for expected surrogate cost is below a
prespecified negative economic threshold, while the reference satisfies its
analytical admissibility condition. Otherwise report unresolved or no detected
violation at the measured precision. Report effect sizes and
confidence intervals over independent market episodes; repeated overlapping
cycles within an episode are not independent samples. For a prespecified finite
family, correct simultaneous tests; adaptive search uses separate held-out
confirmation. Choose episode count from pilot variance and a stated detectable
effect rather than invent an acceptance-oriented sample size.

Secondary outcomes: held-out response error, impact/decay curves, return/spread/
volume statistics, ordinary execution cost and policy ranking, runtime and
failure rate. Pair episodes only when coupling is valid. Include confidence
intervals and simulator initialization sensitivity.

Controls: validated admissible reference, deliberate inadmissible impact positive
control, replay, uncorrected neural model, structural/decay-mixture baselines, interactive
response calibration, simple penalty,
and the selected repair. An artificial invalid control validates the detector;
it is not evidence that a released learned generator has a defect.

## 8. Academic decision gates

1. **Source gate:** inspect full texts and reference chains for INTAGS, constrained
   neural markets and action-dependent manipulation. Update comparison table.
2. **Validity gate:** discrete reference assumptions and ledger agree; detector
   distinguishes positive controls from admissible references at stated power.
3. **Mechanism gate:** learned error appears beyond accounting bugs and is linked
   to a controlled response intervention.
4. **Contribution gate:** repair transfers to unseen schedules and compares
   favorably with strong baselines without sacrificing required fidelity.
5. **External gate:** released-generator diagnostics use supported artifacts and
   precisely limited interpretation.
6. **Submission gate:** all claims map to evidence, uncertainty and limitations;
   independent review is addressed. No claim of guaranteed acceptance.

If Gate 3 fails, change the question or report a powered negative result; do not
write a failure narrative. If only a known nonlinear-impact effect appears, the
proposed novelty is not supported. External experiments alone cannot substitute
for the causal attribution required by the current headline.

## 9. Paper outline and reproducible research artifact

1. Introduction: execution realism versus composed action response.
2. Foundations and closest work: assumptions and exact contribution boundary.
3. Closed-cycle benchmark and accounting contract.
4. Learned-response mechanism and correction.
5. Controlled results, transfer and external diagnostics.
6. Limitations, reproducibility and conclusion.

Every figure must link to immutable model/data/config versions and the code
revision producing it. Preserve unsuccessful searches and changed hypotheses.
Follow the agent-native artifact principle: each claim links to source evidence
or an executable experiment, with the exploration history retained. Cite the
[ARA paper](https://arxiv.org/abs/2604.24658) after verifying the relevant full text.
Use the existing figures4papers/tueplots conventions for exported figures.

## 10. Next deliverable

Complete the independent novelty review and artifact-readiness ledger, then
prepare the controlled-reference experiment specification. This proposal does
not launch training or claim simulator results. Compute requirements are to be
measured, not inferred from the original papers' full training budgets.

## 11. Independent review response

[Primary-source adversarial review](MARKET_CYCLE_PROPOSAL_REVIEW_2026-09-29.md).

| Review finding | Change and remaining obligation |
| --- | --- |
| Unrelated reference cannot identify pretrained-model defects | Two tiers; only matched known-reference learning supports artifact attribution |
| INTAGS and constrained neural markets overlap | Expanded comparison and actual response-calibration/structural baselines |
| Symmetric cycles can miss existing effects | Unequal entry/exit rates and timing required |
| Optimization schedules cannot also be called unseen | Development penalty schedules separated from sealed confirmatory families |
| Cost sign and noisy mean classification ambiguous | Currency-unit discrepancy defined; uncertainty-based finding rule required |
| Gatheral PDF is slides, not journal full text | Reading status corrected in review; full journal text still required for final derivation |

Design objections above are addressed in the proposal. Mechanism, repair,
generalization and novelty objections require experimental evidence and remain
open. A reviewer agreeing that the design is scoped does not establish results.
