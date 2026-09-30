## Executive summary (read this first)

The first evidence-integrity pass found 15 public T2 experiment reports and preregistrations for Batches 2–15. Batch 1 has a report and README, but no separate preregistration file. The raw experiment CSV/JSON outputs currently visible under `experiments/` and `out/` are from the two Batch 11 reruns; the other reported aggregates have not yet been independently recomputed from local raw outputs. Git-level timestamps could not be inspected in this environment because the installed Git command exits until the Xcode/Command Line Tools license is accepted. Treat the current numbers as report-sourced, not independently verified paper results.

## Inventory and current evidence status

| Batch | Pre-registration file | Reported result in one line | Local raw experiment outputs found in `out/` |
|---|---|---|---|
| 1 | No; README + report | Student-t5 and corrected factor semantics helped; macro horizon correction narrowed tails too much. | No |
| 2 | Yes | Nested factor semantics and macro width selection improved over the Gaussian reference. | No |
| 3 | Yes | Adaptive covariance selection did not transfer; fixed small gains were under threshold. | No |
| 4 | Yes | Coherent Student-t5 horizon paths improved the joint score. | No |
| 5 | Yes | Stationary bootstrap promoted; IID replay breached the factor guardrail. | No |
| 6 | Yes | Volatility-filtered candidates had large regressions. | No |
| 7 | Yes | Reverse-time replay was effectively tied; signed replay was worse. | No |
| 8 | Yes | Balanced deterministic path candidates were rejected. | No |
| 9 | Yes | Monthly innovation width 3 was promoted after nested selection. | No |
| 10 | Yes | Early calibration selected historical episode replay; later validation worsened the composed aggregate. | No |
| 11 | Yes | F4 width 1.5 passed the reported calibration-to-validation gate. Two isolated output directories are present. | Yes, two reruns |
| 12 | Yes | F4 directional centre shifts failed a rates/FX guardrail despite an improved aggregate. | No |
| 13 | Yes | Adaptive block-duration composition did not pass its validation gate. | No |
| 14 | Yes | FX log-return replay improved its recent slice but worsened older calibration and tail diagnostics; it was rejected. | No |
| 15 | Yes | A follow-up mixture selected zero log-path share on older calibration; it is dependent on Batch 14. | No |

This table transcribes report summaries. It does not validate them or make the batches commensurate. They differ in scope, candidate sets, periods, origins, normalization, and selection protocols. Do not add their headline scores, count them as 15 independent replications, or treat random seeds as new finance episodes.

## Chronology and leakage observations

- Batch 10 says it selected each domain's method using the first 24 origins and froze the composition before measuring the last 24. That is the clearest report-level calibration-to-later-validation test. The broader project may subsequently have inspected those same periods; project-wide blindness remains to be audited.
- Batch 11 says it selects on cards through 2021 and validates on cards from 2022 onward. Batch 12's preregistration states that the recent holdout had already selected the width in Batch 11. Therefore the Batch 11 period was reused in later design work and is not a project-wide untouched confirmation set for the whole sequence.
- Batch 14 describes 2022–2024 as its validation slice but separately says older calibration direction must agree. Its recent win/older loss is a disagreement across periods that leads to rejection; it is not an example of a recent-selected candidate failing an older holdout.
- Batch 15 is explicitly a follow-up mixture test after the Batch 14 tail result; do not count it as independent confirmation.

## Artifact audit still required

1. Extract and hash every experiment configuration, raw score table, report, scorer/toolkit version, and result file.
2. Recover commit/run timestamps and prove when each candidate family, split, threshold, and analysis choice was frozen.
3. Search beyond the current `out/` directories for permitted run outputs; distinguish reruns from new candidates and exact duplicates.
4. Map shared cards, target dates, rolling origins, episodes, and seeds across all batches. The same underlying shock can recur across multiple rows or reports.
5. Recompute the report metrics from per-card/per-origin records and the official shared scorer. Check lower-is-better signs, normalization, and the definition of every component, especially the tail diagnostic.
6. Confirm which outcomes were viewed before later candidate design. A per-batch “untouched” label is not the same as project-wide independence.
7. Verify release permission and the public/private firewall before extracting any card-level records or rationales into the paper artifact.

## Review decision

The proposal can advance as an **exploratory retrospective case-study design**, but the current local evidence does not yet support an independently recomputed full-history result. Do not write a results section from these report summaries alone. The next gate is to recover raw outputs and chronology. If these cannot be recovered before the CFP deadline, present the work only as an explicitly exploratory methods/experience note, or do not submit it as a completed empirical paper.
