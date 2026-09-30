## Executive summary (read this first)

This proposal asks what happened when selected Track 2 forecast changes moved from calibration data to later validation. The available evidence supports a report-level audit of selected candidates versus controls, not a candidate-ranking study or a claim that the report inventory is the complete experiment history. This is a proposal, not a completed study. Empirical and novelty claims remain conditional on recovering raw outputs, chronology, and data-reuse history.

## 1. Working title

**Do Calibration-Selected Forecast Changes Transfer? A Report-Level Audit of Probabilistic Finance Forecast Selection**

## 2. Research question

### Primary question

For Track 2 candidate changes with a documented calibration/validation split, what happened to the candidate selected on calibration when it was evaluated on later validation, and which domain or score-component diagnostics explain the reported outcome?

### Secondary questions

1. Which axis accounts for each reported disagreement: time period, finance domain, or score component (marginal, joint, or tail)?
2. What do the located positive, negative, and rejected decision reports reveal that a final-model-only summary would hide?

The current files document 15 reports found, not necessarily every experiment attempted. Historical decision timestamps, full candidate configurations, and most raw score outputs are not verified. This draft therefore makes no candidate-ranking, experiment-frequency, causal gate-effectiveness, or complete-history claim. Reopen those analyses only if the missing evidence is recovered.

## 3. Why this is interesting

A forecaster does not have one performance number in practice. It has a vector of scores across time periods, rates/FX/macro/factors, and marginal/joint/tail criteria. The public leaderboard or a paper abstract compresses that vector to one visible number. A recent aggregate win can therefore hide a failure in a different regime or in tail calibration.

The analogy that generated this question comes from reliability engineering. A machine can pass its average-throughput target while one critical subsystem fails under stress. In the forecasting setting, regimes, domains, and score components play the role of distinct operating conditions and subsystems. The structural relation is: **an aggregate can improve while a consequential component regresses**. This is an idea-generation scaffold inspired by analogical reasoning; it is not a claim that this analogy or a new general selection method is itself novel. The proposed report-level study can describe whether such disagreements appear in the located cases; it cannot establish their general frequency or test a new gate.

## 4. Why it matters to Agenthon

Track 2 asks systems to produce future panels from time series and timestamped text, and scores probabilistic distributions with a composite that includes marginal, joint, and tail behavior. A candidate that wins aggregate calibration but loses on later validation or tail support may be poorly matched to a finance evaluation, even if its single displayed aggregate looks better. The [Agenthon call](https://www.agenthon.net/#call-for-papers) explicitly includes probabilistic and text-informed forecasting and evaluation/verification. This proposal is relevant to T2's validation problem; its current evidence comes from text-blind public-panel experiments and cannot support a claim about text uplift.

The study would use only public practice data and aggregate outputs. It would not inspect or reproduce sealed exam answers, private scoring materials, canaries, or participant submissions. All applicable repository rules and data permissions must be verified before release.

## 5. Prior work and the novelty boundary

Temporal validation, rolling origins, multiple test periods, financial backtest overfitting, proper scoring, and live temporal-generalization benchmarks are established. We do **not** claim novelty for regime-aware validation, a new backtest method, a new probabilistic score, or the observation that aggregate metrics can conceal subgroup performance.

The only defensible provisional distinction is a source-linked account of specific candidate decisions reported in Agenthon T2's public practice materials. That is a context-specific artifact and possible case study, not yet a demonstrated scientific gap. Prior work already covers adaptive selection bias, temporal validation, regime-dependent performance, multivariate probabilistic-score reliability, and multi-objective forecasting. Unless raw outputs reveal a specific, non-obvious result that changes how practitioners evaluate or promote forecasts, the current idea is likely too incremental for a strong research paper.

| Work | Question and evidence | Relation to this proposal | Remaining distinction to verify |
|---|---|---|---|
| Tashman (2000), [Out-of-sample tests of forecasting accuracy](https://doi.org/10.1016/S0169-2070(00)00065-0) | Publisher abstract describes fixed/rolling origins, multiple test periods, recalibration, and competition design. | Establishes that evaluation-window design is longstanding; rules out claiming chronological validation itself as new. | Publisher abstract and IU/EBSCO record checked; full text not cached in this pass. It predates this project's setting, but any more specific contrast needs full-text review. |
| Cawley & Talbot (2010), [On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation](https://jmlr.csail.mit.edu/papers/v11/cawley10a.html) | Shows model selection can overfit finite-sample validation criteria and bias the resulting performance estimate. | The general mechanism of adaptive selection and optimistic evaluation is established. | This project-specific descriptive record is not a new account of selection bias; it would need a precise additional empirical finding to justify a paper. |
| Arian et al. (2024), [Backtest overfitting in the machine learning era](https://doi.org/10.1016/j.knosys.2024.112477) | IU/EBSCO and publisher metadata/abstract reviewed; concerns financial backtest validation under non-stationarity and regime shifts. | Shows financial model-selection validation is established and active. | Full text not cached or verified in this pass. Do not make a detailed methods contrast until full-text access is obtained. |
| Garza et al. (2026), [Impermanent](https://arxiv.org/abs/2603.08707) | Open paper page reviewed; proposes a live benchmark that scores sequentially under temporal change. | Makes a broad temporal-generalization benchmark claim inappropriate. | PDF not cached in this pass; the proposed distinction from finance forecast decisions is provisional. |
| Akinci & Martinez-Morales (2026 preprint), [Why Model Selection Fails in Time Series Forecasting](https://arxiv.org/abs/2605.01608) | Tests descriptor-based model selection across four datasets and forecasting horizons; reports ranking instability and poor selector accuracy. | Directly overlaps broad claims that data regimes make model rankings unstable. | It tests rule-based model identification with point-error metrics; our narrow difference is a longitudinal audit of real candidate-promotion decisions for probabilistic finance forecasts, if the evidence supports it. |
| [Multi-Objective Model Selection for Time Series Forecasting](https://arxiv.org/abs/2202.08485) (2022) | Benchmarks 13 methods on 44 datasets using probabilistic nCRPS and considers accuracy/latency trade-offs and multi-objective defaults. | Score trade-offs and multi-objective selection are established; the “vector versus scalar” analogy is not itself novel. | It does not appear to audit Agenthon's reported promotion decisions, but a local case study alone may be too narrow to count as a scientific contribution. |
| [Regions of Reliability in the Evaluation of Multivariate Probabilistic Forecasts](https://arxiv.org/abs/2304.09836) (2023) | Studies finite-sample ability of proper scores to discriminate distributional errors using synthetic and real time-series data. | Directly studies when multivariate probabilistic scores can identify forecast errors. | Any new score-diagnostic claim must distinguish itself from this analysis; our candidate currently does not. |

Two nearby Agenthon-specific literatures also bound the claims. [TFRBench](https://arxiv.org/abs/2604.05364) evaluates forecasting reasoning across five domains, including finance. [TimeLitmus](https://arxiv.org/abs/2609.24677) tests event-conditioned finance/traffic prediction and evidence-faithfulness with counterfactual and contrastive interventions. These make general claims about reasoning-aware forecasting or explanation audits untenable. [Semantics or Structure?](https://arxiv.org/abs/2608.22321) directly intervenes on multimodal time-series text, so generic “does text matter?” ablations are not a fresh angle either.

## 6. Preliminary evidence (not study results)

The reports establish that the candidate question is grounded in actual development decisions, but they tell different stories and use different scopes. For example:

- The historical-episode candidate was selected on early calibration origins, then worsened on later validation by 0.097863, with macro contributing most of the loss. This is the clearest reported calibration-to-later-validation failure. [Batch 10 report](</Users/sebastianboehler/Documents/GitHub/agenthon-2026-t2-forecasting/experiments/tenth_batch/REPORT.md>).
- A separate F4 width change passed its preregistered validation gates: all-card aggregate improved by 0.023448 and its F4 slice by 0.089884. It is a positive transfer case and must be included. [Batch 11 report](</Users/sebastianboehler/Documents/GitHub/agenthon-2026-t2-forecasting/experiments/eleventh_batch/REPORT.md>).
- FX log-return replay improved a reported recent nine-card slice by 0.096995 but worsened the 25-card older calibration set by 0.057916, including a tail-component regression. This shows cross-period disagreement, but the older calibration result rejected it; it does **not** show a recent-selected winner failing an older holdout. [Batch 14 report](</Users/sebastianboehler/Documents/GitHub/agenthon-2026-t2-forecasting/experiments/fourteenth_batch/REPORT.md>).
- Batch 15 tested mixtures after Batch 14 and selected 0% log-path share on older calibration cards, so it is a dependent follow-up rather than an independent replication. [Batch 15 report](</Users/sebastianboehler/Documents/GitHub/agenthon-2026-t2-forecasting/experiments/fifteenth_batch/REPORT.md>).

These examples motivate the question; they are not an unbiased sample. The reports' use of words such as “untouched” does not prove independence from the broader sequential research process. The descriptive inventory should include every located report, including null and rejected outcomes, and distinguish report-stated holdouts from periods known to have been revisited later. It must not be described as an exhaustive candidate or attempt inventory.

## 7. Proposed research design and methods

### 7.1 Research design (methodology)

This is a retrospective, single-project observational case study. The study unit is a **reported candidate decision** in the public T2 development record. No treatment is assigned, and the paper will make no causal claim that a gate prevented failure or that a score component caused an outcome. The case corpus is the 15 reports located so far, explicitly treated as a non-exhaustive corpus. This design can describe the cases; it cannot estimate population rates or support statistical generalization.

### 7.2 Evidence-collection and analysis methods

Use document and artifact analysis to transcribe each located report's candidate/control comparison, stated selection basis, evaluation period, domain/component diagnostics, and missing evidence. The primary metric is the report's official Track 2 composite probabilistic score on its later evaluation slice; existing marginal, joint, and tail components are secondary diagnostics. Reuse the shared scorer definitions and report direction/units exactly; do not implement scoring math here. Independently recompute a reported delta only where permitted raw inputs, outputs, scorer version, and commands are available. Do not impute missing candidate scores. Prediction latency is outside this study's question and is not consistently available in these reports, so it will not be added as an outcome. Do not invent a new composite, optimize thresholds, or run inferential tests on this incomplete corpus.

### 7.3 Forensic report reconstruction

Build a manifest for every located report and any directly recoverable candidate output. Record the source of each field: candidate configuration; selection metric; calibration and validation periods; domains/components; seeds; number of origins/cards; output hashes; any stated threshold or gate; reported decision; raw-output availability; and chronology/data-reuse confidence. Join reports to code and outputs when possible. Preserve failures and reruns. The current host's Git command is blocked by an Xcode license gate, so commit-level chronology is not verified. Reports and preregistration files establish a report-level sequence only; they do not prove when results were viewed, that every attempt is represented, or that a stated holdout remained unseen project-wide. See [the evidence ledger](EXPERIMENT-LEDGER.md).

**Gate 0:** the current artifacts do not establish chronology, complete candidate sets, or project-wide data exposure. Unless those gaps are resolved, stop confirmatory analysis and describe only the located reports as exploratory evidence.

### 7.4 Units and estimands

The unit for description is a **reported candidate decision**, not an individual score row, seed, or overlapping forecast origin. Repeated seeds and origins are nested measurements and must not be counted as independent decisions.

Primary descriptive summaries, if reconstructable:

- **Selected-candidate transfer:** for each report that provides the relevant comparison, transcribe the selected candidate-versus-control outcome on later validation, with the reported calibration rationale and diagnostics.
- **Component/domain discordance:** show domain and marginal/joint/tail diagnostics alongside aggregate change where available.
- Do not report rank agreement, promotion-rule effectiveness, or cross-report frequencies unless complete candidate-by-split data, decision chronology, and a consistent eligibility rule are independently recovered.

Do not pool headline scores across batches whose panels, origins, normalizations, scopes, or scorers differ. Give per-experiment results first. Provide a summary count across batches only if the forensic audit establishes a consistent eligibility rule and decision definition; otherwise leave the cases side by side.

If later evidence supports a common set of cases, report numerator and denominator, uncertainty intervals with assumptions, and the full candidate-level table. Under the current evidence, do not calculate pooled counts or intervals. If gates were not fixed before outcomes were inspected, report decisions as descriptive historical behavior, not as causal gate effectiveness.

### 7.5 Comparisons

Compare selected candidates and controls only within reports where their inputs and splits are documented:

1. **Reported calibration choice:** identify the selected candidate and stated calibration rationale; do not infer the full candidate set from a winner/control comparison.
2. **Later validation outcome:** transcribe the reported comparison, while separately recording whether the wider project may already have inspected that slice.
3. **Component diagnostics:** show domain and marginal/joint/tail changes beside the aggregate. This is descriptive, not an optimized replacement gate.

Do not tune thresholds on these results. If a new policy is proposed after inspecting the located reports, mark it exploratory and reserve new data or a later independent run for evaluation.

### 7.6 Statistical handling

The current evidence inventory does not support a common inferential sample or pooled uncertainty estimate. Report each case with its source, scope, and missingness. If raw outputs are recovered later, preserve candidate → origin/card → seed nesting and do not bootstrap score rows as independent. Avoid significance language unless an independently defensible sample and uncertainty model become available.

### 7.7 Reproducibility and evidence

For every paper claim, link source report, code revision, configuration, permitted input manifest, command, output hash, and analysis. Maintain a dated decision log that includes rejected and superseded experiments and distinguishes human-authored decisions from agent-generated suggestions. This follows [Agent-Native Research Artifacts](https://arxiv.org/abs/2604.24658) and [Reproducibility in the Age of Agentic AI](https://arxiv.org/abs/2609.11728) as artifact practice; those ideas are not the paper's scientific novelty.

## 8. Expected contributions (conditional)

If Gate 0 passes and the full analysis supports them, the paper could contribute:

1. A public-safe, reproducible report-level case study of selected probabilistic-finance forecast changes.
2. A transparent account of the domain and score-component diagnostics available for those reported decisions.
3. A claim-linked evidence artifact that preserves located positive, negative, and rejected reports without implying exhaustive coverage.

These are intended contributions, not findings. There is no guaranteed positive result: stable rankings or no added value from component checks would be a valid result and must be reported.

## 9. Adversarial review and submission decision

| Criterion | Reviewer assessment | Status |
|---|---|---|
| Significance | Validation reuse and aggregate-score trade-offs matter, but their general importance is established. The application could be useful to T2 practitioners. | Moderate, context-specific |
| Novelty | No distinct scientific gap is demonstrated yet. The narrow case-history angle may be viewed as an engineering report or anecdote. | **Major concern** |
| Soundness | Claims are now report-level, but most results cannot be independently recomputed and chronology is unavailable. | **Major concern** |
| Reproducibility | Source-linked reports exist; raw candidate outputs and commit chronology are incomplete. | Incomplete |
| Feasibility by CFP | A verified, independently reviewed empirical paper is unlikely to be completed responsibly by 30 September from the current evidence state. | **High risk** |
| Agenthon fit | Forecast evaluation and verification are explicitly in scope; direct T2 relevance is clear. | Good |

**Current recommendation: do not submit this as a completed empirical paper unless the evidence gate is cleared and a genuinely non-obvious finding emerges.** The call's “any format and length” language does not establish that a research proposal without results is an acceptable submission type. If organizers confirm proposals or work-in-progress papers are welcome, consider a proposal separately; otherwise prioritize a sound full study for a later venue. Acceptance cannot be guaranteed by process compliance.

### Possible stronger study (redesign, not current evidence)

If we continue this direction beyond the current call, a more testable question is: **Does adding predeclared domain/component guardrails to composite-score selection reduce out-of-time selection regret for probabilistic finance forecasts?** Recompute a matched set of candidate forecasts on the same public T2 panels; select candidates using either the composite alone or the existing, frozen track gate; evaluate both choices on chronologically later blocks never used for policy design. Report out-of-time composite regret, worst-domain regret, and rejection/promotion decisions, with repeated market episodes treated as dependent. Use only official scorer outputs; introduce no new score formula. This would replace the anecdotal report inventory with a controlled policy comparison, but it still needs a fresh literature audit, complete candidate forecasts, clean temporal blocks, and substantial analysis. Existing multi-objective and score-reliability work means its novelty is not established, and it is not feasible to complete rigorously before the 30 September deadline from the current artifacts.

## 10. Threats to validity and stop conditions

- **Adaptive reuse of data:** repeated development can consume a nominal holdout. Reconstruct all information flow; do not label a repeatedly viewed slice untouched.
- **Selection and dependence:** candidate variants, overlapping origins, shared shocks, and seeds are dependent. Keep each reported decision as a descriptive case and display its reported scope; do not treat cases as independent replications.
- **Small, project-specific sample:** a single system's experiment history cannot estimate a universal failure rate. Frame the work as a case study, not a benchmark law.
- **Researcher degrees of freedom:** do not cherry-pick the reversal examples or invent a gate after seeing outcomes.
- **Data and role boundary:** use public practice artifacts only; check competition policy, contributor permissions, attribution, and the public/private firewall before release.
- **Venue fit:** Agenthon welcomes evaluation and verification work, but a paper about one participant's internal development process may need stronger general lessons or a broader comparison to be compelling.

**Stop or reframe** if aggregates cannot be released lawfully, if report-level comparisons cannot be independently checked, or if the result reduces to selected anecdotes without a coherent bounded question. A short exploratory paper is appropriate only if the call permits it and reviewers can distinguish report-derived observations from verified results; otherwise do not submit this idea as a completed empirical study.

## 11. SMART milestones and go/no-go

The CFP deadline is 30 September 2026, 23:59 AoE. This is a short feasibility schedule, not a promise that a full empirical study can be completed in time.

| Date | Specific deliverable | Measurable completion condition | Decision |
|---|---|---|---|
| 27 Sep | Freeze the located-report inventory and check permission/public-safety boundaries. | Every located report has a source path, summary, and raw-output/chronology status in the evidence ledger. | If any source is restricted or unsafe, exclude it. |
| 28 Sep | Attempt independent recomputation only for cases with recoverable raw inputs and scorer versions. | At least one claimed result exactly reproduces from recorded commands and permitted artifacts; otherwise mark all results as report-sourced. | If no key finding is independently verifiable, no empirical-results submission. |
| 29 Sep | Run an adversarial novelty and claim audit against the comparison table; request a human coauthor/advisor read if available. | Every contribution claim maps to distinct prior work and a verified result; reviewer objections are logged and answered. | If the distinction remains only project-specific documentation, do not represent it as novel research. |
| 30 Sep | Make final submit/no-submit decision and, only if all gates pass, prepare and upload one PDF. | PDF opens, all claims resolve to sources or outputs, limitations and any applicable disclosures are present, and form requirements are checked. | Submit only as a complete, honest paper type permitted by organizers; do not relabel a proposal as a results paper. |

## 12. Planned paper structure

1. **Introduction:** the projected-away score dimensions; the practical selection question; scope and contributions.
2. **Related work:** out-of-sample forecasting, financial backtest overfitting, temporal benchmarks, proper scoring; explicit novelty boundary.
3. **T2 setting and report corpus:** forecast outputs, domains/components, reported candidate decisions, and public-data boundary.
4. **Study design:** chronology audit, unit of analysis, comparison policies, estimands, inference.
5. **Results:** report inventory, selected-candidate outcomes, available component/domain diagnostics, and explicit evidence gaps.
6. **Discussion:** what a forecast developer can learn; what does not generalize; relation to Agenthon evaluation.
7. **Limitations and responsible release:** one-system case study, adaptive data reuse, dependence, disclosure limits.
8. **Reproducibility artifact:** claim-to-evidence map, commands, versions, hashes, and report-level decision history.

### Planned figures and tables

- **Figure 1 — score-space intuition:** a candidate's vector across periods, domains, and score components, followed by its one-number aggregate projection. It is explanatory, not data.
- **Figure 2 — report-history map:** reported candidate families, chronological splits, and documented later-reuse links. Mark unknown chronology explicitly.
- **Figure 3 — selected candidate vs control:** per-report outcomes and available domain/component diagnostics. Use small multiples; show no pooled estimate or candidate ranking.
- **Table 1 — prior-work boundary:** the comparison table above.
- **Table 2 — located-report ledger:** all 15 located reports, including positive, negative, and ambiguous reported outcomes, with chronology confidence and raw-output availability. Label this as a report inventory, not an exhaustive experiment ledger.

Final figure sizing and typography will follow the project notes for [figures4papers and tueplots](PLOTTING.md). No inferential interval will be drawn unless the evidence supports a defensible independent unit and uncertainty method.

## 13. Draft abstract (proposal stage)

Probabilistic forecast development often selects candidate distributions using calibration data and evaluates changes on later observations. We propose a report-level audit of selected forecast changes in the Agenthon Track 2 public development materials. For reports that document the comparison, we will describe selected-candidate outcomes on later validation alongside available domain and marginal, joint, and tail diagnostics. The located reports include both a negative later-validation outcome and a positive one, plus a separate cross-period disagreement. The current artifacts do not support complete candidate rankings, exhaustive experiment coverage, or verified project-wide data chronology. We will state the source and scope of each observation and document known and unknown data reuse. The intended contribution is an exploratory, claim-linked case study of forecast-selection decisions in a multi-domain probabilistic-finance setting, conditional on independent checks of the underlying reports and permission to release the evidence.

## 14. Review-cycle checklist

### Review log

- **Novelty review:** broad regime-dependent ranking instability is already studied, including Akinci and Martinez-Morales (2026). Removed the claim that this is a new general selection problem; the proposed difference is only a report-level Agenthon T2 case study.
- **Novelty review, second pass:** added work on selection bias, multivariate score reliability, and multi-objective forecasting. These further weaken the score-vector framing as a novel contribution. No novelty claim is accepted until a specific result is distinguished from these papers.
- **Evidence review:** the original ranking-transfer estimand was unsupported because most batches lack raw candidate-by-split outputs. Narrowed the question to reported selected-candidate-versus-control decisions. The 15 reports found are not asserted to be the complete history, and Git commit chronology remains unverified due to the host Xcode license gate.
- **Design review:** separated the retrospective case-study design from document/artifact collection and descriptive analysis methods. Removed causal and population-level interpretations.
- **Open review gate:** determine whether lawful raw data and provenance can be recovered and whether they produce a non-obvious result. If not, stop this paper direction for this call.

### Review 1 — novelty and source accuracy

- Verify every related-work claim against full text, not abstract alone.
- Compare directly against at least two current temporal-validation/backtest papers and the closest Agenthon-relevant forecasting benchmarks.
- Replace “novel” with a bounded comparison statement unless the exact distinction is supported.

### Review 2 — methods and evidence integrity

- Reconstruct the located reports and mark what is and is not knowable about decision chronology.
- Verify no outcome used for confirmation informed a later candidate or threshold.
- Recompute key deltas from source outputs; audit score sign conventions and proper-score normalization.
- Confirm that no report-level cases are treated as independent replications; quantify nothing unless the source corpus and unit justify it.

### Review 3 — adversarial review

- Ask whether this is only a collection of project anecdotes, and whether the data can support the proposed estimands.
- Ask whether Tashman/Arian/Impermanent or financial forecasting papers already do the same empirical comparison.
- Ask whether a null/stable-selection result would still be useful and how the paper would report it.
- Remove any claim that is not tied to a source artifact, analysis output, or cited primary paper.

### Review 4 — submission readiness

The [official call for papers](https://www.agenthon.net/#call-for-papers) was checked on 2026-09-27. It states:

| Item | Verified requirement | Proposal consequence |
|---|---|---|
| Format and length | Full papers or short papers, in any format and length; upload one PDF. No template or page/word limit is stated. | We can choose a concise short-paper format; no CFP-mandated template was found. |
| Author eligibility | Submissions are open to everyone, whether or not they compete in Agenthon. | Competition participation is not required. |
| Prior publication | The workshop is non-archival; work under review or published elsewhere is welcome. | Prior publication or concurrent review is allowed by the call. |
| Presentation | Accepted papers are posters. At least one author must present in person in Atlanta on 12 December 2026. | An author must be able and willing to attend in person. The call does not describe an oral-presentation track. |
| Submission form | One PDF upload; Google account sign-in; asks for the presenting author's NeurIPS account email. | The submission account and presenter details must be ready. |
| Deadline and decision | Deadline: 30 September 2026, 23:59 AoE. Decisions: 2 October 2026, 23:59 AoE. | Submit before the displayed AoE deadline; leave time for form completion. |
| Disclosure rules | The public call does not specify AI-use disclosure, anonymization, conflict-of-interest statements, or a separate ethics form. | Do not infer that these are waived. Recheck the form and any linked author instructions before submission. The form itself could not be read through the available fetch path in this audit. |

Before submission, compile the final LaTeX and rerun every claimed analysis from a clean environment. Release only public-safe artifacts and state the evidence limitations plainly. The call permits any length; that does not reduce the need for a sufficiently supported empirical contribution.

The next work session should start with Review 2's chronology and artifact audit, not prose polishing. A polished narrative cannot repair a contaminated comparison.

## References

- Ahamed et al. (2026). [TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems](https://arxiv.org/abs/2604.05364).
- Akinci and Martinez-Morales (2026 preprint). [Why Model Selection Fails in Time Series Forecasting: An Empirical Study of Instability Across Data Regimes](https://arxiv.org/abs/2605.01608).
- Cawley and Talbot (2010). [On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation](https://jmlr.csail.mit.edu/papers/v11/cawley10a.html).
- Arian, Norouzi Mobarakeh, and Seco (2024). [Backtest overfitting in the machine learning era](https://doi.org/10.1016/j.knosys.2024.112477).
- Barba (2026). [Reproducibility in the Age of Agentic AI](https://arxiv.org/abs/2609.11728).
- Garza et al. (2026). [Impermanent: A Live Benchmark for Temporal Generalization in Time Series Forecasting](https://arxiv.org/abs/2603.08707).
- Gong et al. (2026). [TimeLitmus: A Diagnostic Benchmark for Cross-Modal Understanding and Explanation Faithfulness in Event-Conditioned Time-Series Prediction](https://arxiv.org/abs/2609.24677).
- Liu et al. (2026). [The Last Human-Written Paper: Agent-Native Research Artifacts](https://arxiv.org/abs/2604.24658).
- Liu et al. (2026). [Unlocking LLM Creativity in Science through Analogical Reasoning](https://arxiv.org/abs/2605.11258).
- Tashman (2000). [Out-of-sample tests of forecasting accuracy: An analysis and review](https://doi.org/10.1016/S0169-2070(00)00065-0).
- [Semantics or Structure? Auditing Text Sensitivity in Multimodal Time-Series Forecasting](https://arxiv.org/abs/2608.22321) (2026).
- [Multi-Objective Model Selection for Time Series Forecasting](https://arxiv.org/abs/2202.08485) (2022).
- [Regions of Reliability in the Evaluation of Multivariate Probabilistic Forecasts](https://arxiv.org/abs/2304.09836) (2023).
- Sarfati et al. (2026). [What LLM Forecasters Know but Don't Say](https://arxiv.org/abs/2607.08046).
