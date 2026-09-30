## Executive summary (read this first)

This is the review index for **When Verified Financial Labels Fail**. The canonical
manuscript is [paper/answer_contract_audit.tex](paper/answer_contract_audit.tex), kept
in the current native LaTeX editor. This [ARA-inspired](https://arxiv.org/abs/2604.24658v3) index connects the study's
claims, methods, results, amendments and retained failures. It uses our own artifact
schema; no formal ARA ontology, Seal certification or novel artifact format is claimed.
Saved-answer measurements can be replayed without model inference or API spending.
The manuscript and artifact are local research drafts; no public release is implied.

## Scientific question and contributions

Can released financial labels reproduce a generator's output while violating the
requested quantity or output instruction? How do reconstructed label comparators
grade the same fixed model answers relative to independently specified numerical
contracts (the formula, input convention, unit and requested rounding)?

The selected-family census covers 12,655 rows from two pinned public synthetic
training releases, representing 10,476 distinct questions within family. Its main
findings are the binomial financing-debt-as-call defect and requested integer-rounding
violations. All 1,000 binomial labels match financing debt and pass the tested call
bounds, while 975 fail independent valuation under both checked conventions.
Separately pinned public generator/verifier code supplies a consistent mechanism;
its revision is not established as the original dataset-generation revision.
Hidden-input precision is an explicitly conditional ambiguity finding. Seven
comparison families pass; repeated templates are not independent failure replications.

The second contribution is paired grading of 800 unchanged answers on 200 distinct
questions, with cheap comparator controls and independently checked calculations.
The strict DeepSeek endpoint denies credit to 55 of 136 valid answers: 48 quantity
and seven rounding cases, with zero from the two passing model-panel families.
Allowing either checked compounding convention yields 56 of 137, in the disclosed
post hoc sensitivity. The study-specific artifact is a reproducibility contribution: it links these findings to
evidence while retaining unsuccessful branches and corrections. No new verification
principle, representative defect prevalence, causal model-size effect, expert human
adjudication, certified reasoning traces or training harm is established.

The later [document extension](docs/FINANCE_DOCUMENT_RESULTS_V1.md) tests scope on
96 original FinQA/TAT-QA questions. Two answer-hidden AI reviews are locked before
native unblinding; 62 numerical/broad-unit readings agree. The 384-attempt panel
retains 383 actual API records, seven returned transport failures and one separate
censored event. DeepSeek unrounded matches change from 25/62 to26/62 with a label-free
reminder; Qwen's strict numeric coverage fails under this wrapper. These are distinct
from financial truth and general ability. Three source quantity errors are corroborated,
two already repaired in FinanceReasoning; native percentage/rounding conventions,
ambiguous signs, prior overlap and our own unit-parser mistakes are reported separately.
The [main-track iteration assessment](docs/MAIN_TRACK_ITERATION_2026-09-30.md) explains
the remaining significance, held-out transfer and expert-reference gates.

## Claim and exploration index

- [Claim/evidence map](experiments/research_claim_evidence_v1.json): bounded assertions,
  limitations and checks against recorded result fields.
- [Exploration graph](experiments/research_exploration_graph_v1.json): retrospective,
  source-supported research branches, decisions, failures and evidence hashes.
- [Artifact validator](scripts/validate_research_artifact.py): local references,
  hashes, graph structure and recorded-value agreement. Passing these checks does
  not establish financial correctness, causal validity or ARA compliance.
- [Validation receipt](outputs/research-artifact-v1/validation.json): 117 linked files,
  nine nodes, four documented edges, 13 bounded claims and 58 recorded-value checks.
- [Measured figure data/metadata](figures/generated/paper-evidence-v1/metadata.json)
  and [generator](figures/paper_evidence.py) bind the strict panel and exploratory
  Gordon comparison to saved results; generated TikZ is embedded in the same manuscript.
- [Artifact design review](docs/RESEARCH_ARTIFACT_DESIGN_2026-09-30.md) and
  [primary-source novelty reassessment](docs/INDEPENDENT_NOVELTY_REASSESSMENT_2026-09-29.md).
- [Poster review and implemented responses](docs/POSTER_ACCEPTANCE_REVIEW_2026-09-30.md):
  organizer-fit, Hennig-informed measurement and Lu-informed contribution checks.
  These are AI-assisted assessments, not faculty feedback or acceptance assurances.
- [Later document-extension manifest](experiments/finance_document_extension_manifest_v1.json)
  preserves the historical graph and links the new protocols, reviews, saved scores,
  source-code controls, derivative overlap and failure-handling amendments.
- [Document native-interface review](docs/FINANCE_DOCUMENT_COMPARISON_INDEPENDENT_REVIEW_V1.md),
  [post-unblinding semantic supplement](docs/FINANCE_DOCUMENT_POST_UNBLINDING_SEMANTIC_AUDIT_B.md)
  and [prior-repair overlap](docs/FINANCE_DOCUMENT_DERIVATIVE_OVERLAP_REVIEW_2026-09-30.md).

## Protocols, endpoints and exact evidence

| Study | Declaration and interpretation | Machine-readable evidence |
|---|---|---|
| Released-label audit | [Protocol](docs/ANSWER_CONTRACT_PROTOCOL_V1.md), [amendments](docs/ANSWER_CONTRACT_PROTOCOL_AMENDMENTS.md); purposively selected families, with earlier discoveries disclosed | [Manifest](outputs/answer-contract-v1/manifest.json), [results](outputs/answer-contract-v1/results.json), [independent summary](outputs/answer-contract-independent/summary.json) |
| Original model panel | [Protocol](docs/MODEL_GRADING_PROTOCOL_V1.md): 600 answers, strict final-line format and declared numerical contract; binomial primary convention is one-period simple compounding `1+r` | [Selection/freeze](outputs/model-grading-v1/selection_manifest.json), [primary results](outputs/model-grading-v1/results.json) |
| Numeric extraction | [Post hoc amendment](docs/MODEL_GRADING_AMENDMENT_NUMERIC.md), [unit correction](docs/MODEL_GRADING_CORRECTION_UNITS.md); recovered final-line number is distinct from strict unit/format compliance | [Corrected V2 freeze](outputs/model-grading-v1/numeric_sensitivity_freeze_v2.json), [original historical freeze](outputs/model-grading-v1/numeric_sensitivity_freeze.json), [combined numeric scores](outputs/model-grading-v1/combined_numeric_sensitivity.json) |
| Matched Qwen3 extension | [Later 4B extension](docs/MODEL_GRADING_SIZE_EXTENSION.md); same 200 questions and settings, separate from original panel | [Extension manifest](outputs/model-grading-v1/extension_manifest.json), [combined 800-answer results](outputs/model-grading-v1/combined_results.json) |
| Compounding sensitivity | [Post hoc analysis](docs/MODEL_GRADING_CONVENTION_SENSITIVITY.md), [timing correction](docs/MODEL_GRADING_CONVENTION_TIMING_CORRECTION.md); binomial validity accepts either simple or continuous convention | [Corrected V2 freeze](outputs/model-grading-v1/convention_sensitivity_freeze_v2.json), [original historical freeze](outputs/model-grading-v1/convention_sensitivity_freeze.json), [scores](outputs/model-grading-v1/convention_sensitivity.json) |
| Adaptation feasibility | [Protocol](docs/FINANCE_ADAPTATION_PROTOCOL_V1.md), [execution amendment](docs/FINANCE_ADAPTATION_EXECUTION_AMENDMENT.md); two objectives/two seeds, seed/manual controls, held-out operands and 24 authored transfer questions | [V1 freeze](outputs/finance-adaptation-v1/freeze.json), [V2 freeze](outputs/finance-adaptation-v2/freeze.json), [V2 results](outputs/finance-adaptation-v2/results.json) |
| Document extension | [Blind-review protocol](docs/FINANCE_DOCUMENT_TECHNICAL_REVIEW_PROTOCOL_V1.md), [prospective model panel](docs/FINANCE_DOCUMENT_MODEL_PROTOCOL_V1.md), [comparison protocol](docs/FINANCE_DOCUMENT_COMPARISON_PROTOCOL_V1.md); 96 fixed cases, original62-case numerical subset, later precision diagnostic separate | [Pre-target lock](outputs/finance-document-review-v1/pre_target_lock.json), [closure receipt](outputs/finance-document-models-v1/interrupted_collection_receipt.json), [compact saved-score replay](outputs/finance-document-replay-v1/manifest.json) |

Read [model results and limits](docs/MODEL_GRADING_RESULTS_V1.md) before comparing
models: strict parsing yields 0, 34, 0 and 137 parsed answers for Qwen3 1.7B, Qwen3
4B, Qwen2.5-Coder 3B and DeepSeek respectively; numeric recovery yields 189, 90,
192 and 200. Every model retains the 200-question denominator. Passing numerical
values do not certify derivations. The family-specific exploratory ranking reversal
is not a general model ranking. Reconstructed policies are not observed upstream
rewards. See [independent model validation](docs/MODEL_GRADING_INDEPENDENT_RESULTS.md).

## Replay from a local artifact copy

The recorded runtime is Python **3.13.2**. Numerical replay dependencies are pinned
in [review_requirements.txt](experiments/review_requirements.txt), which includes
[answer_contract_requirements.txt](experiments/answer_contract_requirements.txt).
Adaptation checks additionally use [GEPA 0.1.1](experiments/finance_adaptation_requirements.txt).
[Model-runtime requirements](experiments/model_grading_requirements.txt) document
optional fresh inference; weights and credentials are unnecessary for saved-answer
replay. Source staging can fetch pinned public bytes and checks their hashes.

Retain an untouched artifact copy for integrity checks; recompute in a separate
working copy containing the saved outputs and recorded runtime. Run the artifact
validator before recomputation: validation receipts acquire new timestamps, and
the audit manifest records the relocated script path and current output inventory.
These commands perform staging, scoring or validation, never model collection:

```bash
.venv/bin/python scripts/validate_research_artifact.py
PYTHONPATH=src .venv/bin/python scripts/stage_answer_contract.py
PYTHONPATH=src .venv/bin/python scripts/run_answer_contract.py
.venv/bin/python scripts/independent_contract_validation.py
PYTHONPATH=src .venv/bin/python scripts/evaluate_model_grading.py
PYTHONPATH=src .venv/bin/python scripts/evaluate_model_grading_sensitivity.py
PYTHONPATH=src .venv/bin/python scripts/evaluate_model_grading_extension.py
PYTHONPATH=src .venv/bin/python scripts/analyze_model_grading_conventions.py
.venv/bin/python scripts/validate_model_grading_outputs.py
.venv/bin/python scripts/validate_model_grading_extension.py
.venv/bin/python scripts/validate_model_grading_conventions.py
.venv/bin/python scripts/census_model_grading_conventions.py
.venv/bin/python scripts/render_answer_contract_tables.py --check
.venv/bin/python scripts/render_answer_contract_figures.py --check
```

For the completed V2 adaptation panel:

```bash
PYTHONPATH=src .venv/bin/python scripts/report_finance_adaptation_v2.py
PYTHONPATH=src .venv/bin/python scripts/validate_finance_adaptation_occurrences.py
```

The second command is the disclosed reporting-only occurrence supplement. The
original frozen validator still fails on nonunique training tags. Its separate
[validation receipt](outputs/finance-adaptation-review/response_validation_occurrences.json)
retains every actual call/duplicate occurrence and uses unchanged numerical rules.
All four optimizer arms selected the seed strategy; both consequence and repair
gates failed. See [independent adaptation review](docs/FINANCE_ADAPTATION_INDEPENDENT_RESULTS.md).

Complete procedures and focused checks are in the [audit](docs/ANSWER_CONTRACT_REPRODUCE.md),
[model grading](docs/MODEL_GRADING_REPRODUCE.md) and [adaptation](docs/FINANCE_ADAPTATION_REPRODUCE.md)
reproduction guides. The [audit clean-replay receipt](outputs/answer-contract-v1/clean-reproduction.json)
covers five byte-identical scientific outputs using fresh downloads and the existing
runtime, not the complete latest artifact or a newly isolated environment.

The later [clean extracted-package replay](docs/FINAL_ARTIFACT_REPLAY_2026-09-30.md)
covers the audit, model analyses, adaptation checks and new grading exports using
the same recorded runtime. Its [machine-readable receipt](outputs/final-artifact-replay-results.json)
records 37 of 44 selected outputs matching exactly, six timestamp-only differences
and one relocated audit-manifest difference. All 15 focused tests pass. The final
poster revision changed the manuscript, reporting renderer and review/index documents;
that historical replay predates this document extension. Its old numerical algorithms,
inputs and saved responses remain unchanged. The later extension has its own replay
and integrity receipts rather than inheriting the earlier full-replay claim.
The [revision check](docs/POSTER_REVISION_CHECK_2026-09-30.md) covers the new reporting
and manuscript consistency. The later archive/inventory check has its own receipt;
the earlier full-replay receipt is retained with its original scope.

Replay the later document scores without API spending:

```bash
PYTHONPATH=src .venv/bin/python scripts/replay_finance_document_artifact.py
.venv/bin/python scripts/render_finance_document_evidence.py --check
PYTHONPATH=src .venv/bin/python scripts/validate_finance_document_extension.py
PYTHONPATH=src:scripts .venv/bin/python scripts/replay_finance_document_diagnostics.py
```

See [document reproduction](docs/FINANCE_DOCUMENT_REPRODUCE_V1.md). Compact unchanged
numeric annotations reproduce all384 paired scores and aggregates. Full original
question/context packets and annotation dictionaries stay outside the review archive;
blind semantic review and fresh collection require their separately documented inputs.
The [collection closure](docs/FINANCE_DOCUMENT_COLLECTION_CLOSURE_V1.md) preserves the
383-record raw ledger and identifies the extra censored event in a derived attempt view.
The [posthoc diagnostic report](outputs/finance-document-diagnostics-v1/REPORT.md)
separates status-only recovery and whole-expression execution. The compact wrapper
checks all diagnostic rows/aggregates; the original frozen full-input script still
requires separately staged original targets. Neither replay certifies trace semantics.

## Retained failures, amendments and unfinished work

| Record | What it limits |
|---|---|
| [Looped forecasting pilot](docs/LOOPED_FORECAST_PILOT_RESULT_V1.md) | No observed gain over its declared controls; not proof recurrence cannot help. |
| [Matched market-cycle follow-up](docs/MARKET_CYCLE_MATCHED_RESULTS_V2.md), [MarS audit](docs/MARS_CYCLE_RESULTS_V3.md) | Proposed positive contribution gates failed; no established arbitrage defect. |
| [Audit evolution](docs/ANSWER_CONTRACT_EVOLUTION.md), [pre-amendment snapshot](outputs/answer-contract-v1/snapshots/before-beta-only-amendment/manifest.json) | Preserve changed interval interpretation and earlier code/results. |
| [Interrupted GEPA V1](outputs/finance-adaptation-v1/execution_failure.json), [execution review](docs/FINANCE_ADAPTATION_EXECUTION_REVIEW.md) | Logging failure before holdouts; incomplete execution is distinct from a measured negative effect. |
| [Historical FinQA/TAT-QA readiness](docs/FINANCE_DOCUMENT_AUDIT_READINESS_V1.md), [fresh-copy preparation](docs/FINANCE_DOCUMENT_AUDIT_REPRODUCTION_REVIEW.md) | Preparation-only receipts remain intact. The later study above adds AI technical review and saved grading; human expert review and prevalence claims remain unsupported. |

This index covers documented research branches rather than a complete commit-level
history. Private course material, credentials, sealed competition answers and full
third-party literature are excluded. Wider scientific claims require the gates in
the [main-track roadmap](docs/MAIN_TRACK_RESEARCH_ROADMAP_2026-09-29.md).
