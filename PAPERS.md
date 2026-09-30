## Executive summary (read this first)

This file records paper candidates and their novelty boundaries. The [broader topic review](docs/BROAD_TOPIC_REVIEW_2026-09-27.md) makes Track 3 exact-semantics simulation the best conditional short-paper route for the September 30 call. The CLMM trajectory-risk idea was a brainstorming example and is parked, with no result. The forecast-selection case study below remains high risk because its evidence and novelty gates have not cleared.

## Paper 1 — earlier forecast-selection candidate (high-risk / no-go unless gates pass)

### Working title

**Do Calibration-Selected Forecast Changes Transfer? A Report-Level Audit of Probabilistic Finance Forecast Selection**

### Candidate contribution

An exploratory, report-level T2 case study of what happened to selected forecast changes on later validation, with available domain and score-component diagnostics. The 15 located reports are not proven to be every experiment attempted. Batch 10 is the clearest reported later-validation failure; Batch 11 is a positive report-level case, but its period was reused in Batch 12 design. Batch 14 shows cross-period FX disagreement, but it was rejected by the older calibration/tail gate and is not evidence that a recent-selected model failed an older holdout. Current evidence does not support candidate-rank transfer or pooled frequency estimates.

### Novelty boundary and feasibility

Temporal holdout design, selection bias, regime robustness, multivariate probabilistic-score reliability, and multi-objective forecast selection are established. Do not claim the aggregate-versus-components framing, a general selection rule, or a regime-aware benchmark as novel. A transparent Agenthon T2 case history may be useful documentation, but its scientific novelty is not demonstrated. See the adversarial review and no-go milestones in [the proposal](docs/PROPOSAL.md).

The current evidence supports only an exploratory proposal. Related work now also makes the broad aggregate-versus-components framing insufficiently novel. Unless raw data and chronology can be verified and a non-obvious finding emerges before the CFP deadline, do not submit this as a completed empirical paper. The CFP's “any format and length” statement does not itself establish that proposal-only submissions are accepted.

## Paper 2 — parked

### Previous working title

**Can You Tell How the Forecast Was Made? A Blinded Provenance Audit for Probabilistic Finance Forecasts**

### Candidate contribution

Run a matched, blinded study in which the visible task context and probabilistic forecast are held fixed while the rationale provenance differs: derived before forecast commitment versus written after the forecast is fixed. Compare human and model reviewers with simple baselines such as arithmetic replay and evidence checks. Report discrimination, honest-case false alarms, reviewer agreement, and uncertainty.

### Novelty boundary

Generic instance-level detection of unfaithful chain-of-thought is already studied by [FaithCoT-Bench / FINE-CoT](https://arxiv.org/abs/2510.04040). Answer-conditioned post-hoc rationale generation is studied in [Measuring and Mitigating Post-hoc Rationalization in Reverse Chain-of-Thought Generation](https://arxiv.org/abs/2602.14469). Forecast-explainer faithfulness metrics are also studied in [Validating Explainer Methods: A Functionally Grounded Approach for Numerical Forecasting](https://doi.org/10.1002/for.70060). The provisional gap is the controlled, probabilistic-finance setting and the question of whether audit-visible traces reveal answer-first construction when forecast and visible evidence are matched. This is a provisional gap, not a completed literature-wide novelty claim.

The study measures detectable cues of construction order. It does not prove that a rationale is a causal record of the model's hidden computation.

## Paper 3 — parked

**When Does Dated Text Change a Probabilistic Finance Forecast?** Use matched corpus interventions to measure whether removing or changing a timestamped document changes forecast distributions and proper scores. Broad context ablations already exist in multimodal time-series work; a future version needs a more specific causal identification contribution. The current Track 2 candidate does not consume text, so it cannot support a text-uplift claim.

## Paper 4 — parked

**Do Behavioral Forks Improve Causal-Localization Efficiency?** Test whether externally measured divergence points in candidate continuations improve causal localization per intervention cost over position-, surprisal-, and entropy-matched controls. This comes from the user's separate mechanistic-interpretability research direction and is less directly tied to Agenthon forecasting.

## Reproducibility practice

Use [Agent-Native Research Artifacts](https://arxiv.org/abs/2604.24658) as an artifact-design reference: keep claims linked to code, experiment history, and evidence. This is research practice, not the novelty claim of Paper 1.
