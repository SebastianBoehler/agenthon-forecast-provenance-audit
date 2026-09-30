## Executive summary (read this first)

This prespecified follow-up compares temporal ordering with identical per-sequence
signed action multisets, three independent training datasets, three initialization
seeds and common-response fidelity matching. It diagnoses whether closed-cycle
failures survive beyond marginal-action changes, reset bias and sign asymmetry.
These are known diagnostic tools, not a claimed novel repair. If ordinary
approximation explains the result, the paper contribution remains unsupported.
The specification and config are saved before the run.

## 1. Shared economics and data intervention

Retain the v1 reference, units, correct self-impact, spread/fees and action-only
response. All sequences begin from zero true impact and have <=16 steps. Features
contain past quantities only; the exact reference response has no omitted memory.

For each dataset seed generate 512 independent magnitude vectors of length eight,
with integer quantities 1..20. Form eight purchases followed by their negative
copies, with one random overall orientation per sequence. **Blocked** keeps this
order. **Shuffled** permutes each identical 16-action signed multiset.

For each paired sequence, total turnover, marginal signed quantities, net terminal
inventory and sequence length agree exactly. Their time-position distributions,
history occupancy, target ranges and sign transitions can differ: those temporal
changes are the intervention, not confounders silently eliminated by matching.
No claim that every time-position marginal is matched is made.

Dataset seeds 5101, 5102, 5103; initialization seeds 201, 202, 203: 18 neural fits.
Same initialization is reused across paired coverages for a given dataset seed.
An independent validation seed 6101 produces 128 sequences per matched coverage
plus 128 unrestricted signed sequences, combined into one shared validation bank.
Splits are by full sequences. Individual feature repetition in the finite domain
is possible. Save actions, features, targets and metadata.

## 2. Fixed training and comparisons

Same v1 architecture: 16→32→32→1 tanh MLP, float64, Adam lr=0.003,
one CPU thread, full-batch MSE, checkpoints after 200/600/1200 updates.
Every model receives the entire 1200-update budget regardless of intermediate
metrics. Save every checkpoint and loss history; no cycle-based early stopping.
Fit least-squares response and an admissible exponential-decay comparator on each
same dataset. Its impact scale remains the common known self-impact scale.

**Equal-budget comparison:** final 1200-update checkpoints in both coverages.

**Conditional fidelity comparison:** for each same-dataset/same-initialization
pair, enumerate its 3×3 checkpoints. Let H=max(RMSE_b,RMSE_s),
D=abs(RMSE_b-RMSE_s), with RMSE in currency per asset unit on the common bank.
A pair is feasible if D<=0.005 and D/H<=0.10 (zero/zero ratio defined as zero).
Choose the feasible pair minimizing (H,D,blocked_epoch,shuffled_epoch)
lexicographically. If none exists, report unmatched; do not relax thresholds.
Selections are saved before any cycle evaluation. Report selected epochs and
matched subset size; it is not a pure equal-optimization-budget causal contrast.
Matched scalar RMSE does not match pointwise errors or their alignment with trades.

## 3. Fixed audit banks

**New bank:** four declared templates, each time-reversed and mirrored in sign,
for 16 schedules. Templates are stored in `matched_data.heldout_schedules`:

- increasing entry magnitudes followed by eight equal exits;
- unequal-size fragmented entry/exit pulses with idle steps;
- nested entry and unequal exits;
- delayed alternating trades of different sizes.

All are fixed before model training, close inventory exactly and satisfy the
20-unit step bound. The entire bank is held out of model loss and checkpoint
selection. It is not necessarily a disjoint semantic family from random training
permutations, so passing it is finite-bank evidence, not family-wide certification.

**Development diagnostic bank:** the fourteen v1 schedules, explicitly reused and
reported separately. Do not relabel those old schedules as new confirmation.

For each selected and equal-budget model, evaluate the raw response and these
prespecified diagnostic interventions:

1. **Reset-centered:** f_c(x)=f(x)-f(0).
2. **Odd:** f_o(x)=(f(x)-f(-x))/2.

Keep the common correct ledger unchanged. Closed-cycle cost expectations use zero
unaffected shocks because f depends only on fixed past actions; no Monte Carlo
uncertainty is required for these frozen-model expectations. Across datasets and
initializations report individual results, not inflated independent cycle counts.
The -0.10 currency threshold is unchanged from v1.

## 4. Exact diagnostic identities

Centering subtracts the same price offset from every fill, so its cycle-cost
change is -f(0)*sum(q)=0. It cannot repair any closed-cycle violation here.
Record maximum numerical residual as an accounting/implementation consistency
check. Correcting initial-history predictions should not be called a profit repair.

With symmetric common self-impact and friction:

C_odd(q) = [C_raw(q)+C_raw(-q)]/2 = C_odd(-q).

Thus oddization removes mirror asymmetry but cannot eliminate a negative mirror
average. Report these identity residuals. Symmetry alone is not a no-manipulation
guarantee. Both identities are direct algebra under our contract, not inventions.
See the [independent review](MARKET_CYCLE_MATCHED_REVIEW_V2.md).

## 5. Interpretation and paper gate

- Persistence across independent datasets and matched errors would strengthen a
  scoped temporal-coverage/response-error finding, not prove a novel mechanism.
- Disappearance under longer training supports the underfitting explanation.
- Disappearance only under oddization suggests asymmetric response error; it
  does not establish a new correction method.
- A failure persisting after oddization is compatible with symmetric impact
  misspecification. It requires further mechanism attribution and comparison
  against the fitted structural methods, not a stronger name for the same error.
- If few checkpoint pairs match, report that matching comparison as incomplete.
- Classical fits are expected to recover this linear reference; do not suppress
  them to present the neural approximation as a necessary solution.

No response-calibration comparator or second architecture is run in v2.
External MarS/TRADES relevance, fidelity-preserving repair novelty and a larger
benchmark contribution remain open. Decide next experiments from these gates;
do not force a favorable narrative from profitable toy cycles.

## 6. Reproducibility and run

Config: `experiments/matched_coverage_v2.json`. Output directory must be new.
Save exact source snapshot before execution, all training inputs/checkpoints,
validation bank, validation-only selections, audit ledgers, config/runtime
metadata and SHA-256 artifact manifest. Keep prior v1 source snapshot intact.

```sh
PYTHONPATH=src .venv/bin/python -m market_cycle.matched_run \
  --config experiments/matched_coverage_v2.json \
  --output-dir outputs/market-cycle/matched-coverage-v2
```

CPU only, no paid training, private competition data or publishing.

## Post-run diagnostic addendum

V2 produced no finite-bank violations. Its data differ from the original V1
one-direction condition, so it cannot attribute disappearance to training duration.
Before executing a separate diagnostic, freeze `experiments/v1_training_duration_diagnostic.json`: replay the original one-direction data and all three original initialization seeds at 200/600/1200 steps; require exact tensor equality with the saved original 200-step checkpoints. Audit the same V1 development bank, raw/centered/odd. This isolates optimization duration, but is explicitly a post-V2 exploratory diagnostic, not confirmation or a new checkpoint-selection rule.
