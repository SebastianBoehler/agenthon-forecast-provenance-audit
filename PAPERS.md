## Executive summary (read this first)

This file records the current paper idea and two follow-on candidates. The first paper tests a bounded, finance-specific audit question; the other ideas remain parked until they pass their own novelty and feasibility review.

## Paper 1 — current

### Working title

**Can You Tell How the Forecast Was Made? A Blinded Provenance Audit for Probabilistic Finance Forecasts**

### Candidate contribution

Run a matched, blinded study in which the visible task context and probabilistic forecast are held fixed while the rationale provenance differs: derived before forecast commitment versus written after the forecast is fixed. Compare human and model reviewers with simple baselines such as arithmetic replay and evidence checks. Report discrimination, honest-case false alarms, reviewer agreement, and uncertainty.

### Novelty boundary

Generic instance-level detection of unfaithful chain-of-thought is already studied by [FaithCoT-Bench / FINE-CoT](https://arxiv.org/abs/2510.04040). Answer-conditioned post-hoc rationale generation is studied in [Measuring and Mitigating Post-hoc Rationalization in Reverse Chain-of-Thought Generation](https://arxiv.org/abs/2602.14469). Forecast-explainer faithfulness metrics are also studied in [Validating Explainer Methods: A Functionally Grounded Approach for Numerical Forecasting](https://doi.org/10.1002/for.70060). The provisional gap is the controlled, probabilistic-finance setting and the question of whether audit-visible traces reveal answer-first construction when forecast and visible evidence are matched. This is a provisional gap, not a completed literature-wide novelty claim.

The study measures detectable cues of construction order. It does not prove that a rationale is a causal record of the model's hidden computation.

## Paper 2 — parked

**When Does Dated Text Change a Probabilistic Finance Forecast?** Use matched corpus interventions to measure whether removing or changing a timestamped document changes forecast distributions and proper scores. Broad context ablations already exist in multimodal time-series work; a future version needs a more specific causal identification contribution. The current Track 2 candidate does not consume text, so it cannot support a text-uplift claim.

## Paper 3 — parked

**Do Behavioral Forks Improve Causal-Localization Efficiency?** Test whether externally measured divergence points in candidate continuations improve causal localization per intervention cost over position-, surprisal-, and entropy-matched controls. This comes from the user's separate mechanistic-interpretability research direction and is less directly tied to Agenthon forecasting.

## Reproducibility practice

Use [Agent-Native Research Artifacts](https://arxiv.org/abs/2604.24658) as an artifact-design reference: keep claims linked to code, experiment history, and evidence. This is research practice, not the novelty claim of Paper 1.
