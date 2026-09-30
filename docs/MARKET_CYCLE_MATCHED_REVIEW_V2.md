## Executive summary (read this first)

The proposed v2 pilot removes several v1 confounds by pairing signed quantity
multisets and comparing validation-error-matched models before seeing new cycle
outcomes. This supports a conditional coverage-ordering comparison, not universal
economic robustness or causal attribution to one specific mechanism. Two exact
identities sharpen the diagnostic design: reset centering cannot alter closed
cycle costs; oddization equals averaging raw costs across mirrored schedules.
This review performs no training or tests.

Review date: 29 September 2026. Reviews the stated design and subsequent saved
specification/code. Proposed 18 MLPs, three datasets, three initializations,
two paired coverage conditions, fixed checkpoints.

## 1. Matched action multisets: what is actually controlled

For each dataset seed and sequence, sample eight magnitudes. The blocked and
shuffled conditions must contain the exact same sixteen signed actions: one
positive and one negative instance of every sampled magnitude. Save paired arrays
and record the multiset equality. Randomize blocked orientation independently.
Shuffling changes temporal composition while preserving quantity support,
sequence turnover and terminal inventory.

It does not preserve per-timestep magnitude laws, previous-history distribution,
target variance, inventory exposure or history norms. Those differences are
consequences of ordering. Report their diagnostics before claiming a particular
response-memory cause. Shared multisets strengthen an ordering intervention but
do not make blocked and shuffled learning equally informative.

Use causal histories only; the balancing quantities of a blocked sequence must
never become future features. Keep zero initial impact and horizon/history16.
Retain sequence-level partitions. Histories for the final action should use only
its fifteen predecessors, with the structurally unused sixteenth lag explicit.

## 2. RMSE matching rule

Use one independently generated common validation bank for both coverage models.
Match corresponding data-seed/initialization pairs using only this bank's response
RMSE. Predeclare the exact tolerance formula, not just “10% and 0.005”: additive
absolute/relative tolerance, conjunctive gates and disjunctive gates differ.
Specify reference denominator and tie-breaking order.

Select among the fixed 200/600/1200 checkpoints without looking at cycle values.
If no feasible match exists, report unmatched; do not expand budgets/tolerances
after observing failures. Save every candidate error, chosen checkpoint pair and
unmatched pair. Show raw all-checkpoint development outcomes separately, clearly
distinguished from the frozen matched comparison.

Choosing different update counts makes this a conditional fidelity comparison,
not an equal-optimization-budget causal coverage experiment. Report update counts
and the unmatched equal-checkpoint comparisons. A feasible matched subset may
select unusual seeds; state how many of nine pairs are retained.

Matching average response RMSE cannot equate maximum error, conditional error,
error direction or cost-relevant alignment. For a given cycle,
`C_learned(q)-C_reference(q)=sum_t q_t*e_t(q)`.
Equal error norms can have different dot products with q. Hence a cost discrepancy
at matched RMSE is a meaningful bounded observation, not proof that training
coverage alone is the identified underlying mechanism.

## 3. Exact diagnostic invariances

Let raw response f(x_t) enter the fixed correct execution ledger, and let
`C(q)=sum_t q_t*f(x_t) + common_selfimpact_and_friction` for a closed cycle.

### Reset centering

For `f_center(x)=f(x)-f(0)`,
`C_center(q)-C_raw(q)=-f(0)*sum_t q_t=0`.

Thus initial-response centering changes response RMSE but cannot change closed
cycle cost here. Any meaningful observed cost change indicates a ledger,
transformation or closure inconsistency. This invariance relies on applying the
same constant to every fill; centering only the initial fill is a different
intervention. Do not attribute violations to a constant reset bias.

### Oddization

For `f_odd(x)=(f(x)-f(-x))/2`, paired histories obey x_t(-q)=-x_t(q).
With sign-symmetric common self-impact/friction,
`C_odd(q)=[C_raw(q)+C_raw(-q)]/2=C_odd(-q)`.

Oddization removes sign asymmetry, but leaves the mirrored mean unchanged.
It cannot repair a negative mirror-average. Individual threshold labels can
change around the mean; report pair-average cost and asymmetry explicitly.
The v1 alternating schedules were negative under both signs for the failing
models, so oddization cannot eliminate those particular expected-cost failures.

These algebraic identities are diagnostics for this action-only ledger, not
new mathematical contributions or general fixes for interactive LOB generators.

## 4. Cold bank and interpretation

Generate new quantities/timings from a fixed saved recipe and retain both signs.
Freeze selection before inspecting the new cost bank. Label it finite-bank
confirmation of a stated conditional comparison, not unseen semantic families
unless family definitions truly exclude the training construction.

The v1 schedules remain development diagnostics. Training data seeds, initializer
seeds and fixed bank schedules provide different sources of variation; eighteen
models are not eighteen independent data realizations. Do not use all schedule
rows as independent observations or extrapolate an acceptance probability.

Evaluate raw/centered/oddized response RMSE as well as cash costs. Matching raw
models does not also match transformed-model fidelity. Established structural
and LS fits remain decisive comparators in this noiseless linear DGP.

## 5. Source-derived scientific limits

[Alfonsi, Klock and Schied, section 2](https://arxiv.org/html/1310.4471v3)
already establishes the average-fill quadratic cost and positive-definite impact
foundation. [INTAGS](https://arxiv.org/html/2309.01784v3) already uses interactive
response calibration for simulator validation and learning. This experiment
must therefore add a consequential identified composition mechanism, beyond
matched-error model comparisons or symmetry projection, to justify a new method.

Proceed as a predeclared mechanism-development step. Positive findings require
further distinct-model/external relevance and correction evidence; negative or
unmatched results are valid scientific outcomes and should remain visible.

## 6. Read-only specification and source inspection

Inspected `MARKET_CYCLE_MATCHED_SPEC_V2.md`, `matched_{data,train,audit,run}.py`
and shared learner/audit functions. No concrete source error was found in the
requested checks. All four base schedules close exactly with integer quantities,
and reversal/mirroring preserves closure; lengths are <=16 and magnitudes <=20.
Histories, weights and model tensors remain float64, with the same gamma and
instantaneous half-self-impact in learned and structural audits.

Signed multisets are checked by row-wise sorting. Checkpoint selection follows
the exact conjunctive tolerance and lexicographic rule. It is saved before audit
evaluation. Equal-budget1200 and conditional-error comparisons are separate.
Raw/centered/odd transformations retain common fill rules and record the relevant
algebraic residuals. Saved source definitions fix the new bank before outcomes.
This is static inspection, not a test or independent run.

## 7. Could this alone justify the intended paper?

Not at the contribution threshold currently requested. A matched-error failure
in a small MLP approximating a noiseless known linear response would strengthen
the empirical premise but still have an elementary explanation: equal average
error need not equalize its cost-weighted direction. Symmetry diagnostics and
classical exact-fit superiority add scientific honesty, not a new algorithm.

For the current empirical simulator paper, substantial response-calibration
comparisons and relevance to a genuinely learned market generator remain material
requirements. An alternative could be a nontrivial general method/theoretical
result plus broad validation. External data is not universally necessary for
every publishable theory paper; this particular pilot does not supply such theory.
Evaluate results before selecting the next route, keeping negative evidence and
the simple structural solution visible.

## 8. Independent read-only outcome review

Read `MARKET_CYCLE_MATCHED_RESULTS_V2.md`, saved v2 results and the separate
original-data duration-diagnostic results. Reported minima, retained match counts
and threshold conclusions agree with the artifacts. The three matched pairs are
all initialization203, each selecting1200/1200. All eighteen equal-budget models
have no raw or oddized threshold violations in either finite bank.

The duration artifact records exact200-update tensor replay for all three original
initializations, and original negative minima disappear at600 and1200 updates.
This supports sensitivity to optimization duration on those same cases. The
report correctly marks the diagnostic exploratory and distinguishes it from the
v2 distribution change; it does not claim universal stability or prove the absence
of failures in other policies. No metrics, signs or bank roles are conflated.

**Verdict:** no overclaim correction is required. The decision that this toy
finding fails the requested contribution gate is consistent with the evidence.
External MarS artifact availability is readiness only; no external forward pass,
cash outcome, calibration result or manipulation diagnosis follows from caching
weights. This review reads saved outcomes and does not independently rerun
training, compare checkpoint tensors or execute tests.
