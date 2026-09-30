## Executive summary (read this first)

Three complete included model/template banks replay without internet, model inference or paid APIs.
The primary dataset audit can be recalculated after acquiring pinned public inputs.
Fresh inference and expert financial adjudication are separate from these checks.

## Included offline banks

Run from the repository root with Python 3.11–3.13:

```bash
PYTHONPATH=src python scripts/replay_grader_comparison.py
PYTHONPATH=src python scripts/replay_independent_finance.py
PYTHONPATH=src python scripts/replay_final_extensions.py
```

The grader bank contains 2,548 authored controls and 96 scalar response projections,
source revisions, control-generation metadata and scoring counts. It excludes the
original MATH500 question/solution texts and explanatory model replies. Its manifest
checks bytes; replay recalculates the included scoring decisions. Full-response
extraction therefore requires the original inputs and raw replies.

The independent financial bank contains 300 native questions and solutions from
three licensed FinChain functions. Replay checks source fragments, regenerates seeds
0–99 for each function and recomputes exact-input and source-rounding endpoints.
It does not recover historical FinChain paper instances or run ChainEval.

The final extension bank replays 96 GLM/Llama scalar attempts on the same cohort,
including nondecisions and recorded API usage. Its failed Llama readiness stage and
amendment are retained. The financial-audit summary bank binds the recorded census
and comparator aggregates; it is a consistency record rather than recalculation.

## Primary audit and fresh inference

Follow [ANSWER_CONTRACT_REPRODUCE.md](ANSWER_CONTRACT_REPRODUCE.md) to stage the
pinned public datasets, verify their hashes and recalculate the census. Downloads
are deliberately not bundled as unrestricted new datasets. The 800-answer panel
uses [recorded local and API settings](MODEL_GRADING_REPRODUCE.md); model weights
are not included, and a hosted model name cannot guarantee immutable weights.

The local grader panel uses native templates and recorded quantized checkpoints.
Unseeded repetitions permit exact scoring replay of saved answers, not identical
sample regeneration. API extensions similarly retain requests, provider metadata,
usage, amendments and nondecisions. They do not identify a capacity effect.

Citation review uses the public, pinned CiteProof dependency. Full source PDFs and
exact extraction caches remain local; manifest/excerpt identity checks establish
locations, not semantic support. The author reports completing the cited-source
review; the separate [dated review note](FINAL_BOUNDED_REVIEW_2026-09-30.md) records
that statement without changing immutable automated reports. Qualified independent
financial adjudication has not been completed.

## Code evolution and publication

[The retired-branch archive](../artifacts/history/README.md) preserves code and
recorded outcomes before cleanup, with a per-file manifest and Git checkpoint.
Use its historical entry points against its historical inputs; do not overlay new
files onto an older frozen experiment and claim that its old hash check still passes.
Current scalar banks and the current manuscript have their own revision identities.

The author-led submission package also retains the unchanged earlier research ZIP.
The current paper is `paper/answer_contract_voice_draft.tex`; the fuller research
record remains `paper/answer_contract_audit.tex`. Export the current editor preview
after checking pagination. A successful source compile is not a layout review.
