## Executive summary (read this first)

We should stop promoting new paper topics until one passes a literature-to-question review. Based on the supervisor's emails supplied by the user (29 September and 4 October 2025; 15 April 2026), the next deliverable should be a roughly one-page novelty justification with a specific research question, a cited gap-comparison table, and a feasible evaluation design. This is our interpretation of those actual emails, not a fresh recommendation or approval from Prof. Lu. A standard process improves scientific quality; it cannot ensure acceptance.

## What went wrong in this thread

1. **We switched topics before completing their comparisons.** Rationale provenance, forecast-selection history, CLMM trajectory risk, and simulation acceleration each acquired proposal documents before their closest-work review and empirical prerequisites were settled.
2. **We conflated submission feasibility with scientific promise.** Existing T3 code makes that direction more feasible for this deadline. It does not prove that it is the most original idea, nor establish a controlled speedup.
3. **We treated broad overlap as too decisive.** A prior finance harness or fast simulator defeats a broad first-of-its-kind claim. It does not rule out a different mechanism, validated benchmark, or informative finding in the same area. Finite searching cannot prove that nobody has studied an idea.
4. **We counted papers instead of accounting for evidence.** Cached PDF, reviewed abstract, close-read methods, and a verified source comparison are different states. We need to record them separately.
5. **Our research questions drifted with available artifacts.** A project report is not a random sample, a Development score is not a baseline speedup, and a drafted protocol is not a result. We must select a question for its significance and answerability, then check whether our artifacts can answer it.

## What the supervisor actually requested

| Supplied feedback | What it requires here |
|---|---|
| 29 Sep: identify limitations of current methods; cite recent work and at least one seminal source | Read beyond close empirical competitors: foundations, reviews, current methods, and evaluation literature. |
| 29 Sep follow-up: roughly one page of motivation, research question, and gap table; no separate literature-review chapter in the exposé | Integrate literature where it justifies the question and choices. A separate internal evidence map is useful; an exposé need not be a long survey. |
| 29 Sep: distinguish methodology from solution methods | State the research design and its steps, then the concrete implementation, inputs, outputs, and measurements. Use one suitable organising framework if helpful; do not stack unrelated frameworks. |
| 29 Sep: justify evaluation against accepted alternatives | Define baselines, metrics, experimental units, uncertainty, and failure handling with sources. An LLM judge cannot be its own sole validation. |
| 4 Oct: comparison table missing; literature needs foundations/reviews; ablations and runtime unspecified; contents missing | Supply a closest-work table, ablation design, runtime/cost measurements where relevant, and a paper outline before calling the proposal complete. |
| 15 Apr: limitations cannot simply be discussed away | Narrow claims or add evidence. Persuasive writing does not repair missing controls or an unsupported estimand. |

These instructions came from the earlier thesis/paper, so applying them here is a methodological inference. They are not Agenthon requirements.

## The next research cycle

### Gate 1 — bounded literature map

Choose at most two serious directions to inspect deeply. Treat T3 simulation as a candidate with existing engineering evidence, not an automatically adopted topic. For each direction:

- Identify the core problem and who benefits from solving it.
- Read the two or three closest papers in full; inspect methods, results, limitations, and artifacts.
- Add a foundational source, a relevant review, and accepted evaluation-method references. These are coverage categories, not a magic paper-count requirement.
- Follow relevant references backward and inspect recent citing work forward. Record which seed paper led to which source and why it was included or excluded.
- Verify title, authors, year, venue/version, and source URL. Prefer the published version when accessible; record any preprint/version distinction.
- Mark access and reading states: abstract only; full text retrieved; methods reviewed; artifact checked. Do not call the whole field reviewed because a PDF directory is large.

**Pass condition:** the map explains the closest approaches and their actual limits, with no central novelty comparison supported only by an abstract. No exhaustive priority claim is warranted.

### Gate 2 — one-page novelty justification

Write: problem → observed limitation in existing work → precise research question → proposed contribution → evidence needed.

The comparison table should use meaningful columns: problem, assumptions, intervention, data/workloads, evaluation, demonstrated result, and remaining limitation. A checkmark column saying that our combination is unique is not enough.

Finish with a bounded statement: “A and B address X under assumptions Y. We will test Z under conditions W.” Explain why the difference changes what can be measured, explained, or done. Do not merely say “nobody has combined these technologies.”

**Pass condition:** we can state the distinction plainly, identify its nearest competitor, and specify an experiment that could refute our premise.

### Gate 3 — feasibility and research design

Declare the unit of analysis, independent inputs, baseline, intervention, confounders, metrics, ablations, error denominator, and uncertainty method. Audit public/private boundaries and data rights. Estimate run costs and remaining time from actual artifacts.

For a simulator: same workload and semantics, matched hardware, complete-run timing, exact/tolerance-defined output agreement, and workload-specific regressions. For a forecasting audit: genuine chronological separation, common candidate forecasts, proper score definitions, and dependence across overlapping windows. For a harness study: multiple models/tasks and controlled component contrasts, not only complete-system comparisons.

**Pass condition:** every proposed primary claim has a concrete output and a credible baseline. If one cannot be obtained, narrow the question before implementation.

### Gate 4 — small falsification pilot

Freeze a limited pilot, its controls, and stop criteria before seeing its outcome. First check that the measurement distinguishes an intervention from an unchanged control. Then test the hypothesized mechanism. Preserve failures and null results. A pilot result is exploratory and is not independent confirmation.

**Pass condition:** either the mechanism is credible enough to justify a larger study, or the recorded result supports a principled stop/reframe. Do not change the question repeatedly to rescue a positive result.

### Gate 5 — proposal review and study freeze

Produce the full exposé: one-page rationale, cited comparison table, research design versus methods, metrics/baselines, ablations, threats to validity, reproducibility plan, outline, and realistic milestones. Have a separate reviewer try to invalidate its central novelty and evaluation claims. Record objection → evidence or change → remaining limit.

Only then freeze the confirmatory design and start the full study. A substantial new benchmark may qualify if its tasks, oracles, coverage, validation, and demonstrated findings are useful. A systems contribution may qualify if the mechanism and controlled performance are useful. Neither requires inventing an entirely new field.

### Gate 6 — draft and submission review

Write claims from verified results. Link each table/figure to inputs, code revision, configuration, command, outputs, and analysis. Preserve code evolution and rejected designs using the project's ARA-inspired artifact practice. Apply figures4papers/tueplots when actual figures are ready.

Review source accuracy, novelty, methodological soundness, claim strength, reproduction, limitations, and venue requirements separately. Make a submission decision from that evidence; do not manufacture confidence from the deadline or the existence of a polished PDF.

## Immediate deliverable

Use the [literature audit](LITERATURE_AUDIT_2026-09-28.md) to fill the missing reading, then produce one comparison-backed novelty page. Do not start another simulator rewrite merely because low-level speed sounds promising. The [September 27 topic ranking](BROAD_TOPIC_REVIEW_2026-09-27.md) is a feasibility hypothesis to review, not a scientific decision already made.
