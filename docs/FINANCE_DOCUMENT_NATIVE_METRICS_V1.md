## Executive summary (read this first)

The adapter implements the actual pinned TAT-QA answer and scale channels and an
explicitly adapted FinQA literal execution-answer comparator. It reads no corpus,
selected question, reviewer sheet or target file by itself. The authored controls
are interface checks, not evidence of defects in the 96 selected cases.

The implementation is `src/finance_document_review/native_metrics.py`. Its fixed
source dependency is `outputs/finance-document-native-v1/`; all seven code/notice
files are hash checked before scoring, including when an imported module is cached.
Missing files, changed hashes, unsupported schemas and missing dependencies fail
with an error. There is no download, fallback or annotation-expression evaluation.

### First-party code and notices

`source_manifest.json` records exact URLs, commit revisions, SHA256, Git blob SHA1,
byte lengths and acquisition timestamps for three code files and four notices.
The repository revisions are those already configured for the document audit.

- FinQA: `0f16e2867befa6840783e58be38c9efb9229d742`,
  [official evaluate.py](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/code/evaluate/evaluate.py).
- TAT-QA: `870accc41953dcde885aabeb963d94aabdc0fbc3`,
  [official metric](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/tatqa_metric.py) and
  [official utilities](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/tatqa_utils.py).

Both pinned repositories carry MIT code licenses, retained unchanged with their
README files. This source-only artifact does not resolve report-content or
FinTabNet redistribution notices. TAT-QA's pinned README names dataset CC BY 4.0;
the previously recorded older-paper noncommercial discrepancy remains explicit.
No corpus was downloaded for this adapter preparation.

### Input and output contract

Both scorers accept a plain native annotation dictionary and a candidate dictionary
with `value`, `unit`, `scale`, and optional `status`. Answer values are finite plain
decimal strings; scale is `none`, `thousand`, `million` or `billion`. The default
status is `answer`. `insufficient_information` requires null value. FinQA also
accepts `non_numeric_answer` with literal `yes`/`no`, unit `boolean`, scale `none`.

`score_finqa_scalar` requires unchanged native `exe_ans`. Numeric candidate values
are converted to float and rounded to five decimal places, then compared exactly
to that original value, matching the inspected post-execution endpoint. It does
not round or reinterpret `exe_ans`, and it performs no percent or scale conversion.
Returned `unit_ignored` and `scale_ignored` disclose its unit blindness;
`program_equivalence` is null. An answer emitted without FinQA's domain-specific
programming language (DSL) is not an official full FinQA submission. Different
literal scalar representations therefore do not establish an evaluator bug.

`score_tatqa` requires native `answer_type` (`arithmetic`/`count`), `answer`, `scale`.
It calls the actual `TaTQAEmAndF1` once and returns its exact answer EM (exact match),
F1 and `scale_score` channels. `none` maps to native empty scale; named magnitude
scales are retained. `percent` and `percentage_points` both map to native `percent`.
Their independent financial meaning remains distinct. The native metric may
accept an unscaled percentage fraction or a rescaled amount in its answer channel
while failing its scale channel; both results are retained. Currency code,
requested quantity and the percent/percentage-point distinction are not verified
by these channels. Financial validity must be scored separately by the root study.

### Authored checks and replay

`authored_controls.json` records 33 authored fixtures and 15 schema rejections,
plus six source-inspection/in-memory integrity checks performed at creation.
Sixteen fixtures run actual official FinQA candidate programs and compare their
execution endpoint to the adapted scalar endpoint. These are candidate test
programs, never fabricated reference programs or program-equivalence claims.
Signs, zeros, yes/no, precision boundaries, percentages, scale rescaling and
unit/quantity blindness are covered. Expected values were declared before scoring.

Replay the 33 fixtures, 16 official execution comparisons and 15 schema rejections:

```bash
PYTHONPATH=src .venv/bin/python -c 'import json; from finance_document_review.native_metrics import replay_authored_controls; print(json.dumps(replay_authored_controls(), sort_keys=True))'
```

The saved receipt also binds the adapter/source-manifest hashes and installed
dependency versions. Its six creation-time checks include source AST conditions,
corrupted cached-source rejection, a missing-file rejection and missing-dependency
rejection; the replay function does not repeat those injections. TAT-QA's unchanged
utilities emit upstream Python 3.13 escape-sequence warnings. Actual metric results
passed; no selected-case correctness, defect prevalence or model performance was
measured here.
