## Executive summary (read this first)

**PASS for saved diagnostic consistency, with explicit scope limits.** Independent
recovery and arithmetic checks agree on all 384 rows and the recorded counts:
DeepSeek recovered 88/87 answers and supported 72/39 whole calculations;
Qwen recovered 57/17 and supported 56/12. These are baseline/reminder counts out
of 96 attempts per arm. Recovery is posthoc; expression support is a selected
representation subset. Neither constitutes strict compliance, semantic truth,
a new execution method, or a causal reminder effect.

The initial diagnostic implementation freeze omitted `arithmetic.py`, contrary
to its protocol. That original freeze and all results are preserved. The later
dependency receipt establishes a present hash and replay agreement only; it does
not prove pre-result binding. The reminder's assumption-prose instruction also
conflicts with the whole-expression grammar. Reduced support cannot imply worse
arithmetic. No inference, network calls or original-artifact edits occurred.

## Verified coverage and recovery

Checked all 384 unique `(model, condition, case)` identities, original order and
ledger-line indices, all saved original strict fields, and every recovered value.
Each configuration retains 96 attempts, 48 per source; the 383 original records,
seven returned transport errors and one censored event stay in denominators.
The original 62-reference subset produces 248 eligible attempts across four
arms. It is not 248 independent questions or semantically adjudicated cases.

Own recovery checks accept only one complete JSON object, unique keys at every
depth, all six original fields, an existing unit/scale, and a finite literal
number. No aliases, prose salvage, missing-field fills or source-guided choice.
All 74 newly recovered panel records change only their status tag. Actual panel
recovery changes no value type or extra fields. Calculations/evidence remain
uncertified. The 135 failures are 83 missing-field, 28 nonnumeric-literal,
14 missing/nonstring-unit, two invalid-object and eight request/censored events.
All 83 missing-field cases lack calculation: 21 Qwen baseline, 62 reminder.

Own 34 runnable authored controls pass, including nested duplicates, missing
fields, Boolean/null/decorated values, numeric versus string exponents, NaN,
Markdown/prose, unsupported equations/calls and arithmetic power/operator rules.
The original 33 saved control records report PASS but do not preserve every
input fixture; this review does not claim to rerun those exact injections.

## Arithmetic and normalization denominators

| Endpoint | Verified count | Relevant denominator |
|---|---:|---|
| Recovered numeric availability |249|384 attempts|
| Whole-expression support |179|384 attempts; 249 recovered|
| Exact final-number agreement |62|179 supported expressions|
| Exact final-number disagreement |117|179 supported expressions|
| Supported with original locked reference |131|179 supported expressions|
| Reported mismatch → executed match |47|131 supported/eligible attempts|
| Reported match → executed match |41|131 supported/eligible attempts|
| Reported mismatch → executed mismatch |43|131 supported/eligible attempts|
| Reported match → executed mismatch |0|131 supported/eligible attempts|
| Supported TAT-QA calculations |86|179 supported expressions|
| TAT-QA native normalization eligible |85|86 supported TAT-QA calculations|
| Different reported/executed TAT-QA values |49|85 normalization-eligible calculations|
| Equal primary normalized strings despite different values |28|49 different-value calculations|
| Native credited among those collapses |24|28 collapsed representations|
| Also executed-match/reported-mismatch under locked proxy |15|24 credited collapses|

The normalization exclusion is a percent candidate with scale `thousand`, case
`tatqa:50c60658-c81f-482f-8b97-8a00965be958`, which the unchanged native adapter
rejects. The 28/24/15 counts are conditional saved
response diagnostics, not counts of released-label defects or wrong finance.
Pinned normalization first rounds numeric conversion to four places, then its
primary representation to two places before scaling/serialization. Independent
float normalization agrees with every recorded primary-string comparison.
Primary-string equality does not characterize every native acceptance path or
replace separate scale scoring. Exact disagreement also includes ordinary
finite precision; repeating division follows Decimal precision 60, not an exact
rational answer requirement.

Whole strings are evaluated by an independently implemented restricted AST
interpreter; no subexpression is extracted. All 179 executed values agree with
the saved Decimal results. Independent Fraction guards reproduce recovered and
executed locked matches. The native TAT adapter is shared and hash-verified;
FinQA scalar credits are independently checked. Every model/arm/source aggregate
and paired result reproduces from the independently verified rows.

Both-supported pairs number 38 DeepSeek and nine Qwen; only 29/eight respectively
have locked references. They do not provide all-96 arithmetic comparisons.
The baseline asks for a numeric expression; the reminder asks for assumption
prose in calculation. Its lower 39/12 support counts therefore mix representation
with availability. The 47 within-response transitions show proxy consistency of
saved expressions, not a prospective intervention or requested-quantity validity.

## Integrity, commands and reproducibility boundary

Read-only original replay reproduced exact `rows.jsonl` bytes and every aggregate.
All original diagnostic/input bindings match. Arithmetic's supplementary hash
is `9cf4ca91990bb3eb8f3c54f18b377f3d0d96fcd23fb6a28859f2b47a4b7e9bde`,
verified after results; pre-result dependency completeness remains unestablished.
The protocol, implementation and results timestamps are respectively
`2026-09-30T01:36:42.750410+00:00`, `01:45:20.989195+00:00` and
`01:45:21.515234+00:00`; the supplemental dependency receipt is `01:52:35.021532+00:00`.
All are later than observed panel outputs and do not create preregistration.

Commands used the existing repository runtime:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python outputs/finance-document-diagnostics-v1/diagnose.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python scripts/validate_finance_document_diagnostics.py --output outputs/finance-document-diagnostics-independent-v1/validation.json
```

The original script and this check of its complete freeze registry require
staged `source_targets.jsonl` and other original bound inputs; the compact ZIP
alone does not satisfy that route. No selected annotation program was executed.
A newly added compact diagnostic replay is a separate route, outside this check.
Independent receipts use exclusive creation; choose a new output path for reruns.
The 228-line [independent script](../scripts/validate_finance_document_diagnostics.py)
reuses the previous independent matcher's locked readings, not a third semantic
review. Its [new receipt](../outputs/finance-document-diagnostics-independent-v1/validation.json)
preserves full authored inputs/results and dependency hashes.

Saved rows SHA256: `9e151545e1003d391fa75fdb4a81251278d0d905be042fd96867df6b657ef0f1`.
Saved results: `922028e7037abff233f906b073ae14c62e36a6c139c37cc95588e8135d236756`.
Independent script: `09c558860b8c83ff94b7dae30e008ffec27da6df89fabdbd3bee6d1d784bc551`.
Independent receipt: `97a284f34e68da59796c01c044dbbfa40c89d0008c163d0d88524c04c57ca0d0`.
