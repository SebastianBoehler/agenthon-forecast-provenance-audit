## Executive summary (read this first)

This repository supports **When Verified Financial Labels Fail**, a sole-author,
AI-assisted audit of selected released financial labels and their grading effects.
The [submission draft](paper/answer_contract_voice_draft.tex) is the current paper.
The [evidence index](PAPER.md) connects its claims to protocols and replay records.
The code is MIT licensed; third-party fragments retain their original notices.

We inspect 12,655 rows, representing 10,476 distinct questions within family.
The clearest findings are financing debt used as a call-price reference and missed
whole-unit rounding instructions. Convention-dependent differences remain separate
from confirmed errors. This is a release-specific study, not a benchmark-wide error
estimate, causal model-size comparison or experiment on training harm.

## Reproduce without inference or API spending

From a fresh checkout, Python 3.11–3.13 and its standard library suffice for these
included evidence banks:

```bash
PYTHONPATH=src python scripts/replay_grader_comparison.py
PYTHONPATH=src python scripts/replay_independent_finance.py
PYTHONPATH=src python scripts/replay_final_extensions.py
```

The first checks 2,548 authored controls and 96 saved scalar attempt projections.
The second regenerates 300 native FinChain-template questions and solutions.
The third replays 96 final GLM/Llama replies and recorded API usage. None supplies
financial-expert judgment.
Full-response extraction and fresh model inference require separately acquired
inputs and the recorded model/runtime settings. See [reproduction scope](docs/REPRODUCIBILITY.md).

## Tests and primary audit

```bash
python -m venv .venv
.venv/bin/python -m pip install '.[audit,citations,validation]'
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=src:scripts .venv/bin/python -m pytest tests --ignore=tests/test_finance_adaptation.py
```

The excluded module requires its separately prepared study inputs; it is not a
substitute for the included public checks. GitHub Actions runs the declared checks
on Python 3.11, 3.12 and 3.13. To reacquire the pinned public datasets and rerun the
12,655-row census, use the [audit guide](docs/ANSWER_CONTRACT_REPRODUCE.md).

## What is retained

- `paper/` — current author-led draft and the fuller technical research record.
- `artifacts/` — hash-bound scalar banks, licensed source fragments and retired branches.
- `src/`, `scripts/`, `tests/` — numerical checks, collection, replay and focused controls.
- `docs/`, `experiments/` — protocols, amendments and results needed to interpret the evidence.
- `literature/citations/` — primary-source catalogues; downloaded full texts stay local.

Abandoned forecasting, simulator and blinded-packet code has been removed from the
active tree. Its [archive](artifacts/history/README.md) preserves the code and recorded
outcomes; Git retains the earlier revisions. Failures are not repackaged as findings.

Credentials, local datasets, model weights and private review packets are ignored.
No sealed Agenthon questions or realized competition outcomes belong here. The
repository is being prepared for public release; publication and workshop submission
are separate actions. Qualified-human financial adjudication and causal training
consequences remain absent.
