## Executive summary (read this first)

**PASS for the bounded prefreeze implementation recheck.** The previously found
failure-scoring and JSON-constant gaps are fixed, and status-only recovery now
requires a string status. All four authored tests pass independently. No new
material launch blocker was found in the runtime, collector or analyzer reviewed
here. This does not certify future financial results, model quality or full
instruction compliance. The original precollection review remains unchanged.

## Fixes and accounting

`score()` rejects candidates whenever an error is present or runtime/token gates
are not explicitly true, including scoreable text retained on a failed record.
Both strict and status-only channels receive an explicit failure reason.
`candidate()` rejects NaN/Infinity at every JSON depth; duplicate keys also fail.
Nonstring status is not repaired. Missing fields, values, units and scale remain
unchanged. Compact adapter trace fields stay empty and unobserved. Prose in full
calculation can still pass typed schema and is deliberately assessed separately
for execution; the four tests include that boundary.

The collector refuses an existing ledger, verifies frozen inputs and checkpoint
files before load, and uses audited native encoded tensors directly. It compares
runtime prompt lengths, ID hashes and rendered hashes with the frozen audit.
Generation exceptions become failed attempted records with empty text and false
runtime/token flags; they are retained and are not retried. Each of 32 cases has
all four conditions once. Cyclic order gives each condition eight appearances in
each position across the 32 cases. Sequential model launches remain an
orchestration requirement to verify from actual run timestamps later.

The analyzer requires all 256 unique expected model/condition/case keys and
checks completed ledger and freeze hashes. It preserves the fixed 24-reference
intersection (11 FinQA, 13 TAT-QA) and eight outside cases per condition. Primary,
status-only, native, reference-projection and full-expression channels stay
separate. Its four paired comparisons classify availability versus raw numeric,
unit/scale or mixed changes; none constitutes semantic truth or family causality.

## Runtime and prospective freeze boundary

Reviewed runtime loading verifies MPS availability, rejects enabled CPU fallback,
loads cached native models as FP16 on MPS and checks every parameter's device/dtype.
Inference uses evaluation/inference mode, native chat options, native EOS tokens,
greedy decoding and a 512-token selected-answer cap. Only generated continuation
tokens are decoded. Exhausted budgets retain finish reason `length`.
The previously reproduced 256 token audits and context budgets remain applicable.

Read both saved source-free MPS probes. Qwen's `invalid_non_numeric_answer` and
Smol's `invalid_fields` are preserved diagnostic outputs, not exclusion gates.
Their runtime/token checks pass, and neither contains a selected financial answer.
The initial inherited CPU-fallback failure occurred at the explicit load guard
before model loading/generation; the separate deviation receipt preserves it.
No probe was repeated or model generated as part of this review.

The freeze helper refuses existing financial ledgers, hashes actual complete
checkpoint files and code/native dependencies, including imported arithmetic,
and binds both probe and environment-deviation records. I have not invoked it
or independently rehashed the multi-gigabyte weights; successful prospective
freeze/verification remains the collector's required gate. Include the original
review and this supplement in that freeze to preserve review chronology.
Original studies, selected financial answers and original review were untouched.

Independent narrow verification:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=src .venv/bin/python -m pytest -q tests/test_finance_local_interface.py
```

Result: `4 passed in 0.01s`. Read-only inspection covered local scoring/runtime/
manifest, probe/collector/analyzer/freeze drivers, tests and saved preflight records.
Only this new supplement was written. No network, selected inference, source
correction or frozen mutation. This remains AI-assisted technical readiness review.
