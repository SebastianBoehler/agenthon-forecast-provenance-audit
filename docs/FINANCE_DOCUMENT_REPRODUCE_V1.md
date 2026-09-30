## Executive summary (read this first)

Replay the completed document extension's saved scores without model access or
API spending. All 384 attempts are retained:383 actual API records and1 clearly
identified censored collector event. Compact unchanged numerical annotations
reproduce the actual scoring inputs without full report contexts/programs.
Original source review and fresh inference are distinct procedures.

## Saved-score replay

From an untouched extracted review archive using the recorded Python runtime and
dependencies in `experiments/finance_document_review_requirements.txt` (which includes
the earlier replay dependencies and adds SciPy, SymPy and tqdm for native code):
set `AUDIT_PYTHON` to that environment's executable. The example below uses the
existing environment outside the extracted directory; the archive contains no venv.

```bash
AUDIT_PYTHON=/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/.venv/bin/python
PYTHONPATH=src:scripts "$AUDIT_PYTHON" scripts/validate_finance_document_extension.py
PYTHONPATH=src:scripts "$AUDIT_PYTHON" scripts/replay_finance_document_artifact.py
PYTHONPATH=src:scripts "$AUDIT_PYTHON" scripts/replay_finance_document_diagnostics.py
PYTHONPATH=src:scripts "$AUDIT_PYTHON" scripts/finance_document_review_independent_controls.py --output independent-controls-replay.json
"$AUDIT_PYTHON" scripts/render_finance_document_evidence.py --check
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=src:scripts "$AUDIT_PYTHON" -m pytest -q tests/test_document_review_arithmetic.py tests/test_document_model_parser.py tests/test_document_comparison.py
```

The validators verify the inventories and exact score/aggregate equality;
the controls command exercises independent authored unit/precision checks and
requires a fresh output filename, refusing to overwrite an existing receipt. Native source
code/notices are pinned/hash checked, and the native adapter can separately replay
33 authored controls with16 actual FinQA execution checks and15 schema rejections.
Do not mistake authored fixtures for additional natural source defects.

The existing local `.venv` uses the recorded Python 3.13.2 environment; it is not
a newly isolated clean environment. Plugin autoload is disabled only for pytest
because an unrelated installed pytest_cases plugin is incompatible with its runtime.
No model weights, credentials, private course files or sealed competition data
are required for these saved-score checks.

## What the package can reproduce

The compact views retain only `exe_ans` for FinQA and `answer/answer_type/scale`
for TAT-QA, plus source/case identity. Every original paired score agrees with the
full native dictionaries locally. The manifest binds both actual and derived
ledgers, numerical reference readings, compact annotations, algorithms and saved
results. Quantities/units remain AI-reviewed proxies; a hash does not prove them true.

The strict original endpoint and later reference projection are separate. TAT
answer EM/F1 and scale remain individual channels. FinQA scalar/fraction sensitivity
is adapted JSON-answer grading, not official full-program accuracy. Replaying a
score does not validate the expression/evidence trace or reinterpret ambiguous text.

The later compact diagnostic replay separately reconstructs all 384 posthoc
numeric-recovery and whole-expression rows, checking exact JSONL bytes and every
aggregate against the full-input analysis. It uses unchanged compact native fields,
the frozen diagnostic functions and current extension inventory. It does not replace
the original full-input protocol or retroactively bind the omitted calculator hash.
The original `outputs/finance-document-diagnostics-v1/diagnose.py` still requires
the separately staged, hash-matching full source targets and its original freezes.
Its [report](../outputs/finance-document-diagnostics-v1/REPORT.md) preserves that
boundary. The new wrapper measures saved-score reproducibility, not expert semantics.

## Original review and fresh inference

Full corpora, original annotation dictionaries and original question/context
packets are excluded. Admission scripts and exact pins/hashes can reconstruct
inputs in a separate working copy, subject to the recorded source notices.
Reconstructing original reviewer judgments requires the retained original sheets;
new blind reviewers can disagree. The two AI reviews are not human expert approval.

The frozen collection runner refuses an existing ledger and has no rerun/retry
mode. Do not delete its ledger to restart it. Its interrupted final call is recorded
in `FINANCE_DOCUMENT_COLLECTION_CLOSURE_V1.md`; the normal-completion frozen analyzer
cannot process383 raw records. Saved-artifact replay uses the separately derived
384-attempt view, including the censored failure. The original input and output
hashes, raw provider records and all deviations remain intact.
