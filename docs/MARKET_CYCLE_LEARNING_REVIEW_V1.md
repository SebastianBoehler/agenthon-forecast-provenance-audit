## Executive summary (read this first)

The proposed history-based multilayer perceptron (MLP) is a sound development
pilot for whether training-action coverage changes approximation of an admissible
linear response on closed schedules. It is not a novel simulator or correction.
The noiseless linear reference makes fitted linear and admissible exponential
comparators especially strong. A failed MLP would establish a bounded learner
failure, not a general neural-market defect. This review runs no training/tests.

Review date: 29 September 2026. Reviews the stated design and the subsequently
saved specification, configuration and implementation through read-only inspection.

## 1. Fixed estimator and identifiable comparison

Input: preceding signed quantities, padded to history 16. Output: pre-trade
impact. Proposed network: 16 -> 32 -> 32 -> 1 with tanh hidden activations.
The initial impact is zero. For sequences of at most 16 trades, all causally
relevant prior quantities fit in the observation, so missing ancient history
cannot explain the pilot's errors. Neither the current trade nor a future
balancing trade may enter the pre-trade-impact feature vector.

Use a common correct execution price in every model:
`S_t + predicted_pretrade_impact + gamma*q_t/2 + signed_halfspread`.
Charge identical fees. The changed component is the predicted lagged response;
an omitted-self-impact ledger defect must not masquerade as learning failure.

For deterministic schedules, expected neural cost can be computed directly as
`sum_t q_t*predicted_impact_t + gamma*sum_t q_t²/2 + friction`.
Keep shared martingale price noise separate; Monte Carlo is unnecessary for this
conditional expected-cost calculation. Quantify approximation error relative to
the exact reference and retain a fixed sign convention.

## 2. Equal-budget coverage design

Three training distributions are legitimate distinct interventions:

- One-direction quantities, mirrored at sequence level for balanced global sign.
- Balanced cycles obtained by shuffling eight magnitude-matched positive/negative
  pairs, retaining causally local features only.
- Independently signed random quantities with the same marginal magnitude law.

Match sequence counts, sequence length, training steps, batch sizes, normalization
and architecture. Count the zero-history first step, which has a zero target,
equally across conditions. The final action is not observed by any pre-trade
target in a 16-step sequence; state this indexing convention consistently.

Equal counts alone do not imply equal information. Compare realized absolute
quantity, turnover, impact-target range and history norms by timestep. Shuffled
balanced pairs induce temporal dependence; one-direction histories build larger
accumulated exposure. These differences are part of the coverage intervention,
but prevent attributing every gap specifically to sign composition. Describe a
coverage effect until a separate mechanism ablation disentangles these factors.

Treat signed mirroring explicitly: the paired sequence may be dependent data,
not an additional independent sequence for inference. Reserve independent
sequence draws for train and development; do not split their individual rows
randomly across partitions, which leaks nearly identical histories.

## 3. Baselines and what a positive result would mean

Unconstrained least-squares impulse response can represent the exact target on
the observed finite history. Fit it to the same causal inputs and train labels;
check design rank and residuals. Do not silently regularize a rank-deficient fit
or use privileged true coefficients while describing it as learned.

A fitted admissible exponential response uses the correct model family and fewer
parameters. Fit its parameters using the same observations, restricting gamma
and decay to their valid domains. Keep true-parameter reference as a separately
labeled oracle. Report parameter recovery and any bound/grid resolution effect.

If linear fitting succeeds and the MLP fails, the pilot supports using known
response structure in this setting. It does not establish a new repair method.
If all learners succeed, report a negative pilot honestly. If MLP train error
remains large, diagnose optimization/normalization before claiming extrapolation.

Primary foundation: [Alfonsi, Klock and Schied, section 2](https://arxiv.org/html/1310.4471v3)
already establishes the quadratic-cost response structure. [INTAGS](https://arxiv.org/html/2309.01784v3)
already treats interactive response calibration as a learning/evaluation objective.
Neither generic constrained fitting nor response calibration is novel here.

## 4. Development outcomes and uncertainty

Use in-distribution development prediction error for each condition and a common
cross-condition response/cycle evaluation bank. Reporting each learner only on
its own distribution can falsely suggest equally good fidelity. Separate
prediction RMSE in price units from signed-cycle cost in cash units.

Three initialization seeds measure sensitivity descriptively. Hold training data
fixed across initialization seeds if the stated estimand is initialization;
otherwise label them joint data-and-initialization repeats. Three seeds do not
justify a confident population-level ranking or robust error-bar claim.

Predeclared family schedules of length <=16 can diagnose response composition.
Record total turnover, amplitudes, closure and comparison with training magnitude
support. A distinct exact schedule drawn from the same family is not a held-out
family. If these outcomes inform model/repair selection, they are development
results; future confirmation needs untouched families and seeds.

Avoid hypothesis testing on overlapping schedule rows as independent observations.
The deterministic cost estimator has no exogenous sampling variance. Reference
pilot Gaussian Bonferroni intervals cannot simply be reused for training-seed
variability or an adaptively selected worst cycle.

## 5. Concrete review gates

1. Input excludes present/future actions; history padding, reset and target lag
   conventions agree with the reference equations.
2. Shared correct self-impact/fill ledger remains intact for learned models.
3. Equal budgets and magnitude laws are documented; sequence-level partitions
   and actual normalization are fixed before training.
4. Learned LS/structural baselines are distinguished from privileged reference.
5. Common evaluation error and signed cycle costs are reported for every learner,
   including failures and seeds that do not produce a profitable cycle.
6. No broad learned-generator defect, new correction or acceptance claim is
   inferred from this development pilot alone.

## 6. Read-only review of the actual v1 specification and code

Inspected `MARKET_CYCLE_LEARNING_SPEC_V1.md`, `learning_coverage_v1.json`,
`learning_run.py`, `learning_data.py`, `learner.py`, `learning_audit.py` and the
common reference ledger. No blocking inconsistency was found for the frozen v1
parameters. Lagged feature construction excludes present/future actions; normalized
targets and audit rescaling agree at the configured 20-unit scale. The unused
sixteenth column is explicitly acknowledged and LS rank is saved.

The actual one-direction generator uses independently signed whole sequences,
not literal mirrored duplicate pairs. Train/validation streams use distinct seeds.
Common validation includes all three banks. The specification explicitly limits
claims arising from unmatched marginals and semantic-family overlap.

Structural decay fitting retains the common known gamma, so fitted lagged impact
and instantaneous fill diagonal remain compatible; this is a correctly specified
baseline with acknowledged privileged model-family information. Fixed CPU updates
and saved loss traces permit reporting optimization sensitivity without tuning.

Minor interpretation obligations: action statistics in comparator artifacts are
normalized units, while cycle quantities and cash are physical experimental units.
Report those units explicitly. A biased MLP may predict nonzero impact from the
all-zero initial history; report that prediction as approximation error rather
than silently describing the learned reset response as exactly zero. The audit
remains valid because predicted impacts enter the same execution ledger and
depend only on actions, making zero-shock cash equal expected cash.

This inspection runs neither training nor tests and does not independently
reproduce the resulting numerical outcomes.

## 7. Read-only results interpretation review

Read `MARKET_CYCLE_LEARNING_RESULTS_V1.md` and the saved v1 `results.json`.
The report's table, violation counts and minima agree with that artifact: only
one-direction seeds 102 and 103 violate -0.10, each on both alternating signs.
The other seven neural models and all six classical comparators have no detected
violation in the declared development bank. This is a finite-bank observation.

Response RMSE is correctly labeled currency per asset unit; expected cycle cost
is currency. Conditional action-only model expectations are distinguished from
Monte Carlo market averages. The report appropriately avoids intervals based on
three fixed-data initializations and identifies post-run zero-history diagnostics
as exploratory. Lower own-distribution error cannot be directly compared across
different coverages, and higher common error for balanced models does not certify
greater economic robustness outside these schedules. Those limitations are stated.

**Verdict:** no overclaim or metric-confusion correction is required in this
report. Preserve its qualifications: unequal fitting quality and action marginals
remain null explanations, classical recovery is decisive, and neither a new
mechanism nor a repair or paper-worthy novelty has been established. This verdict
checks saved outputs; it is not an independent numerical reproduction.
