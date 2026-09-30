## Executive summary (read this first)

This private research repo develops the Agenthon workshop paper and a future main-track research project. [When Verified Financial Labels Fail](paper/answer_contract_audit.tex) audits 12,655 selected public supervision rows and grades 800 saved answers from four models on 200 questions. See the [audit reproduction guide](docs/ANSWER_CONTRACT_REPRODUCE.md), [model results](docs/MODEL_GRADING_RESULTS_V1.md), and [independent validation](docs/MODEL_GRADING_INDEPENDENT_RESULTS.md).

The separate GEPA feasibility pilot completed 432 held-out responses after a disclosed logging repair. All four arms retained the seed prompt; neither consequence nor repair gate passed. Its [independent results](docs/FINANCE_ADAPTATION_INDEPENDENT_RESULTS.md) disclose the failed V1 attempt, unchanged scientific rules, repeated-minibatch bookkeeping supplement and approximately $0.25 cumulative accounted inference cost. It is inconclusive about adaptation effects.

The [IU EBSCO search](docs/EBSCO_SEARCH_LEDGER_2026-09-30.md) and [extended literature review](docs/EXTENDED_LITERATURE_REVIEW_2026-09-30.md) strengthen the 22-reference manuscript and narrow novelty. The [artifact design](docs/RESEARCH_ARTIFACT_DESIGN_2026-09-30.md) follows Agent-Native Research Artifacts as a precedent, preserving unsuccessful branches and amendments. It does not claim a new artifact protocol or formal ARA compliance.

A [96-question document review set](docs/FINANCE_DOCUMENT_AUDIT_READINESS_V1.md) is prepared from FinQA and TAT-QA with blank, gold-free sheets; answer correctness and human review remain unexamined. The [main-track roadmap](docs/MAIN_TRACK_RESEARCH_ROADMAP_2026-09-29.md) sets novelty, independent-source, transfer and training gates. No weight-training effect, completed human review, external submission or public release is claimed. Earlier market-cycle, simulator-speed, concentrated-liquidity and forecasting proposals remain historical or parked.

## Earlier market-cycle contribution gate

**The original toy failure has not passed the paper contribution gate.** The [controlled follow-up](docs/MARKET_CYCLE_MATCHED_RESULTS_V2.md) found no violations in the new finite bank; exact replay showed the original V1 violations disappear with more optimization. Do not present those early failures as an established new mechanism or a novel repair.

The [approved research proposal](docs/MARKET_CYCLE_PROPOSAL_2026-09-29.md) remains a conditional direction. The [pinned MarS external audit](docs/MARS_CYCLE_RESULTS_V3.md) now has actual model inference and 60 attempted exchange cycles. It found only one negative-cost completed cycle and eight noise-initialization failures. This does not pass the contribution gate. The new [looped-finance triage](docs/LOOPED_FINANCE_IDEA_TRIAGE_2026-09-29.md) records the user’s next candidate and the direct prior-art collision to resolve.

Completed evidence:

- [Reference specification and proof](docs/MARKET_CYCLE_EXPERIMENT_SPEC_V1.md), [review](docs/MARKET_CYCLE_REFERENCE_REVIEW_2026-09-29.md), [pilot](docs/MARKET_CYCLE_REFERENCE_PILOT_2026-09-29.md).
- [Initial learning pilot](docs/MARKET_CYCLE_LEARNING_RESULTS_V1.md), [frozen V1 specification](docs/MARKET_CYCLE_LEARNING_SPEC_V1.md), [review](docs/MARKET_CYCLE_LEARNING_REVIEW_V1.md).
- [Matched V2 specification](docs/MARKET_CYCLE_MATCHED_SPEC_V2.md), [review](docs/MARKET_CYCLE_MATCHED_REVIEW_V2.md), [results and isolated duration diagnostic](docs/MARKET_CYCLE_MATCHED_RESULTS_V2.md).
- [Topic reassessment](docs/POSTER_TOPIC_REASSESSMENT_2026-09-29.md), [accepted-paper comparison](docs/WORKSHOP_ACCEPTED_PAPER_COMPARISON_2026-09-29.md).

## Paused Track 3 research question

The process reset now has a [comparison-backed novelty page](docs/NOVELTY_JUSTIFICATION_2026-09-28.md), a [falsification pilot design](docs/SIMULATION_FALSIFICATION_PILOT_2026-09-28.md), and an [independent review](docs/NOVELTY_REVIEW_2026-09-28.md). The decision is conditional proceed to a public pilot; novelty and submission readiness have not passed. See also the [full-text and reference audit](docs/LITERATURE_AUDIT_2026-09-28.md).

The [concrete run plan](docs/SIMULATION_RUN_PLAN_2026-09-28.md) now fixes 12 public cases and balanced schedules. Inputs and artifact hashes are prepared; execution still requires a verified Python baseline runtime and launcher.

**Across public ABIDES-compatible market scenarios, which implementation changes improve complete-run throughput while preserving event, matching, and output semantics?** See the [broader review](docs/BROAD_TOPIC_REVIEW_2026-09-27.md). This is a candidate question, not a completed paper.

## Earlier Track 2 research question

**For Track 2 candidate changes with a documented calibration/validation split, what happened to the candidate selected on calibration when it was evaluated on later validation, and which domain or score-component diagnostics explain the reported outcome?**

The earlier Track 2 work is a proposal and source audit, not a completed study. Fifteen reports were located, but this is not evidence that every attempt is represented. Raw outputs and commit-level chronology are missing or unverified. Do not infer candidate rankings, pooled frequencies, or confirmatory status from report summaries. See [the proposal](docs/PROPOSAL.md), [the evidence ledger](docs/EXPERIMENT-LEDGER.md), and [the literature ledger](literature/README.md).

## Paper queue

1. **Current direction:** Released financial supervision and numerical-grading audit; see the [manuscript](paper/answer_contract_audit.tex). Closed-cycle consistency remains an earlier rejected branch; its [proposal](docs/MARKET_CYCLE_PROPOSAL_2026-09-29.md) and failed pilots remain available.
2. **Research direction for later:** A controlled finance-harness portability study across models, tasks, and environment contracts. Existing harness work makes a generic transfer claim insufficient.
3. **Parked:** Concentrated-liquidity trajectory risk; [proposal](docs/CLMM_STUDY_PROPOSAL.md) and [pilot protocol](docs/CLMM_PILOT_PREREGISTRATION.md). No pilot result exists.
4. **Parked:** Calibration-to-validation transfer audit and blinded rationale-provenance audit.
5. **Possible separate papers:** Causal dated-text interventions in forecasting and behavioral forks for causal localization, each requiring a sharper novelty boundary.

The parked follow-on ideas are candidates, not active studies. The CFP welcomes open submissions beyond competing teams, but any question about submitting multiple papers must be checked against the organizer's current instructions.

## Repository layout

- `docs/PROPOSAL.md` — research question, novelty boundary, comparison table, methodology, paper outline, and review gates.
- `literature/README.md` — source/access ledger; full open PDFs are cached in the ignored `literature/pdfs/` folder.
- `docs/EXPERIMENT.md` — parked rationale-provenance study design, outcomes, and limits.
- `docs/PLOTTING.md` — paper-figure conventions using figures4papers and tueplots.
- `figures/style.py` — shared Matplotlib paper-style context for generated figures.
- `PAPERS.md` — prior-art boundary and the parked follow-on ideas.
- `src/provenance_audit/` — standard-library-only packet randomizer.
- `data/`, `packets/`, `restricted/` — ignored paths for local inputs and outputs.

Do not place sealed Agenthon answers, private competition data, or identifiable participant material here without authorization. This GitHub repository is private. Case data and unblinding keys are ignored by Git.

## Parked rationale-provenance tool

The following case format and commands describe the parked blinded study, not Paper 1. Keep these instructions with the code so the earlier work remains reproducible.

### Case input

Provide one JSON object per line with exactly these fields:

```json
{"case_id":"case-001-forward","pair_id":"case-001","provenance":"derived","context":{"task":"...","evidence":[...]},"forecast":{"summary":"..."},"rationale":"...","generation_record":{"protocol":"v1","model_revision":"...","prompt_hash":"..."}}
```

Each `pair_id` must have exactly two cases: one `derived` and one `answer_first`. Their `context` and `forecast` objects must be exactly equal. The rationale text must differ. `generation_record` is retained in the restricted key for provenance and replication; it is never sent to reviewers. Do not use this abbreviated example as experiment data.

### Build blinded reviewer packets

After installing the package with `python -m pip install -e .`, run:

```bash
provenance-audit blind \
  --input data/cases.jsonl \
  --packet-dir packets/run-001 \
  --key-out restricted/run-001-key.json \
  --reviewers 12 \
  --reviewers-per-pair 6 \
  --seed 20260926
```

Each reviewer receives at most one randomly assigned rationale per pair, in a randomized order. With 60 pairs, 12 reviewers, and 6 reviewers per pair, each reviewer sees 30 cases and each pair receives three ratings per condition. Packet records omit source IDs, pair IDs, and provenance labels. The key contains those fields and the seed; it is written outside the packet directory with owner-only permissions. Keep the key restricted to the study operator until reviews are locked. See [the expanded validation target](docs/EXPERIMENT.md#expanded-validation-target); it is a design target, not completed data collection.

### Validate the packet workflow

The repository uses Python's standard-library test runner, so no runtime or test dependency installation is needed:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

GitHub Actions runs this suite on Python 3.11, 3.12, and 3.13 for pushes and pull requests.

## Current status

The manuscript is a compiled local draft with independently checked numerical evidence, a completed 800-answer model panel and an inconclusive completed GEPA pilot. Formatting limits model-size comparisons. The 96-case document set has completed source/packet preparation, with no financial answer audit or expert adjudication. Coauthors/affiliation, human review and external submission remain outstanding. The CLMM study has a proposal and pilot protocol but no experiment. The old packet code supports the parked rationale study.
