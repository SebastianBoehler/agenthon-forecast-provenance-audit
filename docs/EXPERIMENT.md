## Executive summary (read this first)

The experiment asks whether a reviewer can infer rationale construction order from the visible artifact alone. Matched pairs share exactly the same context and forecast; only the rationale and its known provenance differ. Reviewers never see both members of a pair.

## Hypothesis and estimand

The primary estimand is reviewer discrimination between `derived` and `answer_first` rationales under blinded, matched presentation. Report balanced accuracy and AUROC where the rating format permits, alongside the false-positive rate on `derived` cases. Include uncertainty intervals and per-reviewer results rather than a single pooled headline.

The principal null is chance discrimination after controlling the visible context and forecast. Secondary comparisons can include human versus model reviewers and simple replay/evidence baselines, provided each baseline is defined before scoring.

## Pair construction

For each case, freeze the forecasting task, timestamped evidence, target distribution, and forecast output. Create two independently authored traces under documented procedures. Preserve the exact prompt, model/version or author, decoding settings, run identifier, and artifact hashes in a restricted generation record:

1. `derived`: the author/model receives the task and evidence, forms the forecast, then records the rationale.
2. `answer_first`: the author/model receives the same task and evidence after the forecast has been fixed, then writes a rationale supporting that fixed forecast.

Keep model version, decoding settings, prompt budget, evidence access, and allowed tools matched. The order-of-generation instruction is the intended manipulation. Record deviations. Do not claim that this distinguishes internal causal faithfulness; it tests whether observers can detect construction-order cues in the visible artifact.

## Blinding and assignment

The packet builder validates that each pair contains exactly one case per condition and identical context and forecast objects. It assigns one member per pair to a selected subset of reviewers, balances reviewer workload and conditions, hides source IDs, pair IDs, and labels, then randomizes case order. The separate key stores the mapping and random seed. A reviewer never sees both members of a pair.

Reviewers should be independent and blinded to the condition prevalence and case pairing. Lock predictions and confidence before unblinding. Record reviewer instructions, model/prompt versions, exclusions, and missing judgments.

## Outcomes and controls

- Primary: discrimination of provenance, with uncertainty intervals.
- Safety/validity: false-positive rate on derived rationales.
- Reliability: inter-reviewer agreement and calibration if confidence is elicited.
- Baselines: arithmetic replay, evidence verification, and any pre-registered text-only classifier.
- Ablations: remove one audit signal at a time only if the sample supports interpretable estimates.

Do not use the pilot's 4/4 catches as a detector-performance estimate. Do not use arithmetic reproducibility or verbal admissions as ground truth; the pilot indicates both can mislead.

## Limits and decision gate

The existing pilot has eight traces, one reviewer per trace, one model family, and simulated answer-first construction. Its 0/4 false-positive observation is too imprecise for a deployable gate. Before making a detector claim, predefine a sample size based on the desired false-positive bound and recruit multiple independent reviewers. If that is infeasible, frame the paper as a preliminary case study and report the limits prominently.

## Expanded validation target

The provisional target is **60 unique matched pairs**: 15 per T2 family (F1–F4), with the pair count—not the number of reviewer ratings—as the unit for generalization. Spread pairs across at least two forecast/rationale generator families where available, block generation family within each T2 family, and keep model identity hidden from reviewers. Sample distinct historical episodes; do not inflate the count with repeated prompts or paraphrases of the same episode.

Use 12 human reviewers as the primary evaluation, with six reviewers assigned to each pair (three per provenance condition). Each reviewer sees 30 cases total. This produces 360 ratings, but only 60 distinct matched pairs and 120 distinct rationale texts. Treat repeated ratings as clustered observations, not as 360 independent examples. If resources allow, add two or more LLM reviewer families as a separate secondary analysis; do not pool them with human judgments.

At the trace level, predefine a reviewer aggregation rule before unblinding. Report sensitivity and false-positive rate on the 60 unique traces in each condition, plus confidence intervals. With zero false positives among 60 independent `derived` traces, the one-sided 95% exact binomial upper bound is about 4.9%; fewer than 30 such traces cannot establish even a 10% upper bound under this zero-error scenario. Also report per-reviewer results, confidence calibration, inter-reviewer agreement, and a pair/reviewer-clustered interval for discrimination metrics. State the assumptions behind every interval.

Balance or measure rationale length, formatting, forecast complexity, card family, and generation model. Hold the exact forecast and evidence packet fixed within each pair. Use a pre-registered label question and confidence scale. Lock judgments before revealing pair IDs or provenance. Keep realized outcomes out of prompts and reviewer packets. Do not train a classifier on the same traces used for the reported test result; if automated detection is explored, use a separate development set and a held-out generator family.

The existing packet CLI accepts `--reviewers-per-pair` for this incomplete-block assignment. A 60-pair/12-reviewer/6-reviewers-per-pair run yields the allocation above. The target is a design proposal, not a claim that these cases or reviewers are already available.

## ARA-style research artifact

For each paper claim, preserve the source data reference, code revision, prompt/configuration, run command, raw permitted evidence, and analysis output. Preserve rejected experiments and decisions as provenance, with dates and authorship. Keep sealed outcomes and any restricted review key outside public release unless the data owner authorizes release.
