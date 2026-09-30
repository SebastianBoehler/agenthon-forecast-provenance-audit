## Executive summary (read this first)

Replay grading of the saved 800 model responses without inference or API spending.
The same 200 public questions were answered by four models. Preserve the original
three-model 600-response panel and its later 200-response size extension, the frozen
strict endpoint and the separately documented post hoc numeric sensitivity.
No model was trained, and no upstream reward or human review was executed.
The original label-audit protocol prohibited paid compute. The later user-authorized
model study permits a bounded OpenRouter run; the original protocol record is preserved.

## Replaying the released artifact

Use the audit runtime and pinned public data staging described in
`docs/ANSWER_CONTRACT_REPRODUCE.md`. Install
`experiments/review_requirements.txt` for the lightweight independent check and
focused tests. From the extracted artifact root:

```bash
PYTHONPATH=src .venv/bin/python scripts/stage_answer_contract.py
PYTHONPATH=src .venv/bin/python scripts/evaluate_model_grading.py
PYTHONPATH=src .venv/bin/python scripts/evaluate_model_grading_sensitivity.py
PYTHONPATH=src .venv/bin/python scripts/evaluate_model_grading_extension.py
PYTHONPATH=src .venv/bin/python scripts/analyze_model_grading_conventions.py
.venv/bin/python scripts/validate_model_grading_outputs.py
.venv/bin/python scripts/validate_model_grading_extension.py
.venv/bin/python scripts/validate_model_grading_conventions.py
.venv/bin/python scripts/census_model_grading_conventions.py
PYTHONPATH=src .venv/bin/python scripts/report_model_grading.py
.venv/bin/python scripts/render_answer_contract_tables.py --check
.venv/bin/python figures/model_grading.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=src .venv/bin/python -m pytest tests/test_answer_contract.py tests/test_model_grading.py tests/test_model_grading_sensitivity.py -q
```

The strict scorer verifies the original freeze, prompt hashes, panel completeness
and visible numerical values. Supplementary scoring verifies its corrected freeze.
The independent validator uses another parser and exact rational formulas; it
checks per-answer values, errors, unit states, policy decisions and aggregates.
All four models retain the same 200-question denominator; the original three-model panel remains separate. Truncated and malformed
responses remain failures. Raw response order is saved as collected; numerical
scores and results should reproduce byte-for-byte with the recorded runtime.

`scripts/render_answer_contract_tables.py` updates the standalone TeX source from
the saved audit and model results; `--check` verifies without modifying the file.
The independent review snapshot contains the exact response ledger hashes it read.
The integer-plus-original-half-unit policy is interpretable only for constructed
Gordon. Its mechanical values in other-family JSON records are not a valid
cross-family baseline.

## Fresh inference is a separate operation

The bundle already contains answers, so fresh inference is unnecessary for replay.
Local inference additionally needs the versions in
`experiments/model_grading_requirements.txt`, Apple MPS and the exact cached model
revisions listed in `selection_manifest.json`. Weight files are excluded from the
bundle. The local runner is offline and fails when the pinned cache is absent.

```bash
PYTHONPATH=src .venv/bin/python scripts/run_model_grading_local.py qwen3-1.7b
PYTHONPATH=src .venv/bin/python scripts/run_model_grading_local.py qwen2.5-coder-3b
PYTHONPATH=src .venv/bin/python scripts/run_model_grading_extension.py qwen3-4b
```

The API runner needs `OPENROUTER_API_KEY` and consumes credit only for missing
responses. Its fixed provider has fallback disabled; transport failures are
retained without retry. Do not put credentials in the artifact. A model identifier
does not guarantee immutable API weights. Original requests, returned provider,
usage cost and catalogue metadata are preserved. The original request cap was
1,024 output tokens and concurrency four. The original panel must not be silently
replaced by newly generated responses. Use a separate named study for replication.

## Endpoint history and review

The primary protocol precedes financial-model responses. The supplementary rule
was written after observing missing-unit and literal-placeholder output formats.
Both endpoints are reported together; numeric extraction is not evidence of full
response compliance or sound reasoning. Its initial implementation had one
conflicting-unit edge case, corrected and versioned before complete-panel scoring.
Original supplementary files and both freezes are retained.

The additional convention sensitivity keeps the primary `1+r` reference and
allows the union of its cent neighborhood and an independently computed `exp(r)`
price for binomial questions only. It is post hoc and uses unchanged outputs.
Its first timing claim was corrected explicitly: 14 Coder binomial answers
already existed at the first freeze, while no 4B answer existed. Both timing
records are retained. See `docs/MODEL_GRADING_CONVENTION_TIMING_CORRECTION.md`.

`outputs/model-grading-review` contains an anonymous 12-item human annotation
packet and a separate answer key. Its blank sheet is preparation, not completed
human validation. The technical reviewer read primary code before independently
implementing scoring, so this is an AI-assisted technical replication rather
than blind human conceptual review.
