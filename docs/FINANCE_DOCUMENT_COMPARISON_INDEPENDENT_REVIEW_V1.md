## Executive summary (read this first)

The recorded locks and adapted/native scoring interfaces are internally consistent.
The study endpoint must be called **locked unrounded value / broad-unit match**.
It does not certify financial correctness, requested-quantity equivalence, evidence
grounding, or a reasoning trace. Native credit with a locked mismatch can reflect
legitimate rounding, sign or representation conventions. Twelve independently
authored controls reproduce the intended scoring behavior and its limitations.

This review is AI-assisted technical validation, not human expert adjudication.
It was performed after recorded native-target unblinding. Original blind review A,
its receipt, code freezes and source evidence were not changed. Collection was
incomplete during this review; no model-outcome or reminder-effect claim is made.

## Scope and chronology

Reviewed `comparison.py`, `native_metrics.py`, `units.py`, the model parser/client,
the analysis/collection scripts, comparison/model protocols, locks and inspected
pinned first-party scorer code. Selected native programs were **read**, not run.
No model/API calls, answer regeneration or source-label correction occurred.

The comparison protocol was frozen at 00:49:15 UTC on 30 September 2026.
The pre-target lock was created at 00:54:55 UTC; target opening was recorded at
00:55:28 UTC. Every file hash in the comparison-protocol, pre-target, model and
analysis-implementation manifests passed. The unblinding receipt binds the actual
pre-target lock and unchanged target-file hashes. All seven pinned code/notice
dependencies passed their hashes; original A review/receipt hashes still match.

The analysis implementation freeze is transparently later: 01:07:47 UTC, after
launch and unblinding, with 231 response rows available. Its receipt says selected
metric replay had not begun. This is an implementation checkpoint, not another
prospective preregistration or proof of unseen responses.

## Denominators and classification

There are 96 selected questions, 48 per source. The full panel plans four
model/condition cells of 96, hence 384 attempts. The analysis requires every
`(model, condition, case)` exactly once and verifies the completed response hash.
Failures and abstentions remain in the attempted-answer denominator.

The pre-target combined record contains 62 agreed determinate numerical/broad-unit
cases: 29 FinQA and 33 TAT-QA. It also retains 20 agreed conditional cases, five
numerical/unit disagreements, three agreed insufficient-information cases, one
information-sufficiency disagreement, one Boolean, one unresolved case and three
cases with unspecified scale. The other 34 must remain visible per cell.

Thus four cells would contain 248 eligible **attempts**, not 248 independent
questions. The remaining 136 attempts are outside the locked numerical subset.
The analysis's `locked_reference_cases` field counts eligible attempts within the
supplied aggregation. No prevalence interval or independent-replication claim
follows from this selected document panel.

Candidate/request failures within the subset enter `native_ineligible`, outside
the four credited/denied matrix cells. They still count in full-attempt credit
rates. A four-cell matrix alone must not obscure its missing/ineligible row.

## Endpoint fidelity and limits

**FinQA:** inspected official execution rounds the final numeric program result
to five decimals, then compares exactly with `exe_ans`. The scalar adapter
reproduces this result comparison but does not execute the model's JSON calculation
or test DSL/program equivalence. It ignores candidate unit and monetary scale.
Call it adapted literal execution-answer credit, not official full-program accuracy.

Dividing only declared percent/percentage-point candidates by 100 is a separate,
target-independent sensitivity. It is not a repair chosen per gold. Differences
between literal percentage-point JSON values and fraction execution scalars can
arise from the imposed interface; these alone establish no source-label fault.
Other monetary conversions are intentionally absent from the literal adapter.

**TAT-QA:** the adapter calls the hash-pinned actual `TaTQAEmAndF1`. Its numeric
normalization includes two-decimal rounding, magnitude scaling and percentage
normalization. `credited` means answer EM equals one. It does not require correct
scale, currency, percent-versus-percentage-point semantics or requested quantity.
Arithmetic/count F1 equals EM in the inspected native implementation.

Per-case results retain answer EM, F1 and scale score. The frozen aggregate only
sums answer-EM credit; it does not aggregate the latter channels. A separate
reporting supplement should show native EM, scale, and EM-and-scale conjunction.
The conjunction must not replace or be described as the original answer-EM metric.

The locked guard is `max(1e-8, abs(reference)*1e-7)` in the recorded answer unit.
It checks an unrounded numerical reference, not native two/five-decimal projection.
For exact one-third expressed as percent, `33.33 percent` fails this guard while
receiving TAT native EM and correct scale. This is a precision difference, not
an unconditional arithmetic error or proof of financial invalidity.

Likewise `74.371 percent` is a legitimate FinQA five-decimal fraction projection
of `472.7/635.6`; the fraction sensitivity credits it, while the unrounded guard
rejects it. Do not infer wrong finance solely from `mismatch_credited`.

## Broad-unit counterexamples

The frozen mapping keeps percent and percentage points distinct and converts
declared monetary scales. It is useful but does not implement full dimensions:

- A reference `2.5 years` and candidate `2.5 shares` both map to `count` and match.
- A reference `0.36 USD per share` and candidate `0.36 USD` both map to money and match.
- Unknown currency remains a wildcard when only one side names a currency.

These are authored boundary counterexamples, not observed model-error counts.
They undercut a strict dimensional or requested-quantity interpretation of this
endpoint. A future prospectively frozen type version should separate duration,
item counts and entity type, preserve per-share/per-year denominators, and mark
unknown currency/scale explicitly ineligible or unresolved. Do not retrofit this
run or relabel its already locked 62 cases.

## Reference-output diagnostic after unblinding

Passing each eligible unrounded reference through the declared interfaces yields
9/29 FinQA literal credits, 24/29 under percentage-as-fraction sensitivity, and
31/33 TAT answer-EM credits. These are **reference-output representation controls**,
not model results, source-defect prevalence, or certification of the references.
The new machine receipt preserves each candidate and original annotation projection.

Residuals merit separate semantic interpretation:

- JPM 2018 uses native `4630/46780`, whose denominator excludes CIB Markets;
  the locked question reading uses managed net interest income `51410`.
- SLG 2011 native `2728290/2912456` is an opening/closing ratio, while the
  locked reading asks for relative balance change. Its wording remains awkward.
- UA 2011 native signed decline versus the locked positive decrease magnitude
  is a sign convention, not automatically a source arithmetic error.
- PPG 2012 native `56-34=22` uses 2011/2010; the question asks 2011/2012,
  whose disclosed values give `122-56=66` million USD.
- ETFC native `2.3/0.5=4.6` uses 2011 collateral; the requested 2010 collateral
  is `19.3`, giving `19.3/0.5=38.6`. The borrowing denominator is correctly dated.
- TAT compensation-rate change uses `3.3-2.7=0.6` rather than the locked relative
  change; percent/percentage-point wording is the issue, not calculation failure.
- TAT advertising costs use an unsigned decrease of `1559`, whereas the locked
  change is `-1559`. Both describe the same decline under different sign conventions.

The PPG/ETFC year selections and JPM denominator are concrete candidate annotation
mechanisms under their visible readings. Keep original labels and post-unblinding
classification disagreements. Prior correction/provenance checks and semantic
review remain necessary before first-discovery or definite-fault claims.

## Collection cautions and validation

The 01:13 UTC partial snapshot held 288 responses with six request failures and
missing costs. Missing cost is not zero; final accounting must use the completed
receipt. Successful observed model identifiers matched requested configurations,
but the frozen client only enforces provider identity, not returned model identity.

Qwen's authored preflight computed `63` with status `non_numeric_answer` and unit
`count`; the frozen parser rejects it. DeepSeek's preflight passed. The collector
does not enforce preflight success before launch; no retry was made. Retain this
procedural limitation and strict schema failures instead of repairing status values.

Validation passed: 12 new rational controls; all 33 original authored controls,
16 official authored FinQA execution comparisons and 15 schema rejections.
No selected native program or annotation expression was executed.

Reproduce the new controls with the existing repository runtime and a new output:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python scripts/finance_document_review_independent_controls.py --output /tmp/document-controls-new.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -c 'from finance_document_review.native_metrics import replay_authored_controls; print(replay_authored_controls())'
```

New artifacts: `scripts/finance_document_review_independent_controls.py` (SHA256
`2c1cddeff461ec29948b618b5c36d28f676ccb9573fb69d5db4cfe6eebf1a86e`),
`outputs/finance-document-review-v1/independent_comparison_controls.json`
(`5007823b1706cc0d26edcd846c6a168435bfb55db3fb90a996a367ae1567abba`),
and `independent_source_endpoint_review.json`
(`391c389f006813c1a26f2c0737acc8d94bb4d025cba4ba50191510df084b88af`).
