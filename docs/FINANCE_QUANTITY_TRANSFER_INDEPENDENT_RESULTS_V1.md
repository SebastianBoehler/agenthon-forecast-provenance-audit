## Executive summary (read this first)

Saved-output validation passes for the complete V1 panel and the closed, interrupted V2 judge diagnostic. All 32 questions and both arms remain in the accounting. The reminder does not improve either numerical endpoint: reported typed matches are 14/22 to 13/22; executed-expression typed matches are 18/22 to 18/22. These are agreements with locked AI provisional readings, not certified financial accuracy.

V1 has 128 financial calls. V2 stops after 23 of 64 planned financial judge calls because an HTTP 502 response has no `usage.cost`; 41 calls never start. The partial V2 results do not establish judge efficacy, a model ranking, or generalization to TAT-QA. The known shared subtotal is $0.061335771. One unresolved reservation is $0.002311197; the conditional accounted total is $0.063646968, assuming the unknown charge does not exceed its reservation. The complete observed bill is unknown.

### Verification scope

This is AI-assisted technical validation, not human expert adjudication. No inference, network access, retries, source-program execution, or frozen-file edits occurred. Earlier exposure to this repository's financial examples and technical reviews limits semantic independence. The numerical implementation uses a separately authored bounded AST evaluator with exact `Fraction` arithmetic; it does not import the frozen scorer or arithmetic implementation.

The full checker verifies all saved identities, fixed ordering, request bodies and hashes, source/context payload binding to the frozen packet, returned provider/model identity, raw response text and finish categories, saved parser/numerical/judge flags, runtime identity, and every spend-ledger event. V1 binds 19 source files and 9 input records. V2 binds 8 new source files, 19 unchanged V1 sources, and 4 input records. All hashes pass. This audit binds requests to the saved packet; it does not reacquire the financial corpora or independently certify every source interpretation.

Both phases use `deepseek/deepseek-v3.2`, pinned `siliconflow/fp8`, temperature 0, disabled reasoning, 1024 output tokens, and prohibited provider fallback. Requests contain the visible question/context and, for judges, the saved candidate and parser flag; no reference answer is sent to either answer or judge calls. Fifteen authored controls and compilation pass. Controls cover unit distinctions, scale multiplication, native scalar serialization, unsafe arithmetic, malformed candidates, invalid evidence, nullable usage metadata, the exact frozen judge instruction, and unknown billing.

### Numerical endpoints and denominators

The fixed panel contains 16 FinQA and 16 TAT-QA questions. Eleven per source have an eligible locked AI provisional reference; ten questions remain ineligible/unknown. There are 32 answer attempts per arm and 22 eligible comparisons per arm. The ten unknown references remain counted, and numerical nonmatches on them are not called errors.

The comparator requires the same declared numerical unit, applies the declared monetary/count scale once, and uses absolute tolerance `max(1e-8, 1e-4*abs(reference))`. It distinguishes total currency, currency per share, duration, count, ratio, percent, and percentage points. It does not certify currency identity or semantic grounding. All 22 eligible reference expressions independently agree with their serialized values within this tolerance; repeating fractions differ only at the reference's 60-digit decimal serialization.

| Endpoint | Baseline | Quantity reminder |
|---|---:|---:|
| Strict schema valid, all 32 | 30 | 30 |
| Strict numerical answer, all 32 | 29 | 27 |
| Reported typed match, eligible 22 | 14 | 13 |
| Executed-expression typed match, eligible 22 | 18 | 18 |
| Literal native equality, all 32 | 7 | 7 |
| Reported/expression consistency, all 32 | 23 | 22 |

| Source / eligible denominator per arm | Reported baseline → reminder | Expression baseline → reminder |
|---|---:|---:|
| FinQA / 11 | 9 → 9 | 10 → 10 |
| TAT-QA / 11 | 5 → 4 | 8 → 8 |

Within baseline, the `(reported match, expression match)` cells are `(false,false)=4`, `(false,true)=4`, `(true,false)=0`, `(true,true)=14`. Within reminder they are `4,5,0,13`. Executing the expression yields four and five additional provisional matches respectively, without replacing the reported-value endpoint.

Across arms, reported-value pairing has 13 matches in both, one loss, no gain, and eight nonmatches in both. Expression pairing has 17 matches in both, one gain, one loss, and three nonmatches in both. This supports a null/net-negative descriptive reminder result on this panel. It does not support a causal efficacy conclusion: one model/provider, fixed baseline-first ordering, shared source groups, and small provisional-reference coverage remain limits.

Literal native equality compares the unscaled decimal answer directly with the native scalar. It performs no percent/fraction conversion, monetary scaling, tolerance adjustment, or evaluator normalization. It is neither the official FinQA nor TAT-QA metric. A disagreement in that diagnostic does not establish a financially wrong answer.

Both arms prospectively require a pure arithmetic calculation string. The earlier document study's baseline arithmetic versus reminder assumption/prose grammar confound is not reused. Strict schema still checks the evidence field's type, not whether its paths identify actual source locations: 62/64 candidate evidence lists have invalid whole-cell/paragraph pointers under the separate typed-pointer audit. That finding does not retroactively change the frozen candidate parser or numerical scores.

### V1 judge availability

V1 completes 64 judges. Sixty fail the frozen judge parser through invalid evidence pointers. Effective verdicts over all 64 are 62 unassessable, one supported, and one contradicted. Both non-unassessable verdicts are outside the eligible 22 questions. There are zero supported judge verdicts on either eligible arm, so the primary judge channel offers no demonstrated residual utility on the eligible panel.

All V1 saved answer/judge finish categories are `stop`, with no runtime error. One baseline TAT-QA judge nevertheless records exactly 1024 completion tokens. Output-cap exposure is reported separately from `finish_reason='length'`; the saved category does not prove unlimited completion. No output was regenerated.

### Separate V2 diagnostic and interruption

V2 appends only an explicit zero-based source-pointer grammar to the unchanged judge instruction and reuses saved V1 answers. The prospective amendment froze at `2026-09-30T10:09:02.523144+00:00`, after V1 collection began, based on two authored pointer failures and before the preparers' disclosed selected-outcome inspection. This is a timing disclosure, not a technical access-control proof or pristine preregistration. V1 remains primary.

V2 financial judging starts at `2026-09-30T10:52:33.509775+00:00` and stops at `2026-09-30T11:04:03.005148+00:00`. It attempts the first 23 planned calls: 22 successful returns, one HTTP 502, and 41 not started. All attempted financial cases are FinQA; TAT-QA has no V2 judge coverage. All 64 planned case/arm rows are retained.

Twenty of the 22 successful returns pass the judge parser. Over the complete 64-row denominator, effective verdicts are 16 supported, two contradicted, and 46 unassessable. The latter include the transport failure, not-started calls, invalid-pointer replies, and valid replies forced unassessable by malformed candidates. Each arm has eight supported verdicts over its 32 planned rows. Those numbers are availability/accounting diagnostics, not accuracy or efficacy estimates for a completed panel.

The separate V2 summary carries the original 64 candidate rows and answer usage to compare unchanged numerical endpoints. These are reused V1 calls/costs, not additional V2 answer generations or charges; V2 provenance explicitly records `answer_calls=0`.

Among each arm's 22 eligible questions, five V2 supported verdicts agree with both cheap numerical baselines; one agrees with neither. The latter is `finqa:HUM/2017/page_118.pdf-1` in both arms: the locked reference uses positive decline magnitude `(77-75)/77*100`, while the candidate uses signed change `(75-77)/77*100`. The judge supports the negative computation. This is a concrete sign-interpretation disagreement with the provisional reference, not an expert-proven false financial acceptance or a reason to revise the frozen targets retrospectively.

Both contradicted verdicts concern ineligible references: `finqa:MKTX/2012/page_42.pdf-3` baseline and `finqa:RSG/2015/page_98.pdf-2` reminder. Both calculations execute and agree with their reported values. MKTX's judge flags an unspecified comparison period. RSG's judge is internally inconsistent: its parsed `verdict` is `contradicted`, while its reason endorses the operands/calculation and explicitly describes the verdict as supported. The fixed parsed enum is preserved. Neither case establishes incremental arithmetic-error detection or expert-verified semantic error detection.

Judge parser validity is not semantic certification. The frozen parser permits empty evidence/operand-check arrays and character indexing inside strings; the independent whole-cell pointer audit preserves these limitations separately. No supported V2 verdict has empty evidence, but two valid returned judgments have empty operand-check arrays. The V2 prompt asks for whole-cell/paragraph pointers; the frozen parser itself is unchanged.

### Costs, stopping, and preservation

V1 runs from `2026-09-30T09:59:50.065582+00:00` to `2026-09-30T10:49:59.690284+00:00`. Its 128 financial calls cost $0.049929495. Including four authored V1 preflight calls, its closure subtotal is $0.050571150 and exactly matches `run.json['spend']`. Later V2 costs are excluded from that closure-prefix check.

Two authored V2 preflight judges add $0.000499002. Twenty-two billed V2 financial returns add $0.010265619. The final shared ledger has 157 reserved and settled calls, no pending reservation, one settlement with unknown billing, and no subsequent reservation. The stop guard operates as specified: the unknown cost is retained, no retry occurs, and all remaining calls stay not started. Settlement completeness must not be confused with observed-cost completeness.

The missing-cost call is `finance_quantity_transfer_v1:finqa:SLB/2015/page_59.pdf-1:baseline:judge_v2`, request SHA256 `4248a40cb117212d3eab7dc82f47c3cf811d34f544a4ed471aa5aac8d83e2ceb`. Its reservation is $0.002311197. No generation identifier or usable raw response is present; the checker assigns neither zero cost nor a measured total charge. The $2 study and $10 aggregate caps are not crossed by known costs or the conditional reservation accounting.

### Reproduction and portable scope

Run from the repository root using the recorded existing `.venv` runtime:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -p 'test_finance_quantity_analysis.py'
.venv/bin/python -m py_compile scripts/analyze_finance_quantity_transfer.py src/finance_quantity_analysis/*.py
.venv/bin/python scripts/analyze_finance_quantity_transfer.py --judge-v2-dir outputs/finance-quantity-judge-v2
.venv/bin/python scripts/analyze_finance_quantity_transfer.py --portable-input outputs/finance-quantity-transfer-v1/independent-analysis/portable_numeric_packet.jsonl --output outputs/finance-quantity-transfer-v1/independent-analysis/portable-replay
```

Both analysis directories are created exclusively; rerunning requires a new `--output` path. No original output is overwritten. The full [receipt](../outputs/finance-quantity-transfer-v1/independent-analysis/receipt.json) records input, code, and result hashes. The [compact receipt](../outputs/finance-quantity-transfer-v1/independent-analysis/portable-replay/receipt.json) records the projected replay.

The compact packet retains model reply text, numerical reference/native scalars, and previously validated accounting flags. It excludes original contexts, questions, request bodies, raw responses, and judge rationale/operand text. The standard-library replay independently rechecks all 64 numerical/parser/native endpoints; it preserves validated judge/pointer accounting rather than rerunning source checks without contexts. Full pointer, request/source, and semantic review requires independently acquired original financial contexts.

Full and compact scientific summaries match exactly, including separate V2 accounting; only timestamps and provenance scope differ. All receipt code/output hashes verify.

| Artifact | SHA256 |
|---|---|
| V1 experiment freeze | `3ad1042962889e9f7f92fe5e614a08ecbdbafc62890647dbffec044ac7090e6f` |
| V2 plan freeze | `ead4bd31a01ff59ea50b60d03a172932403985939eb99ad3745b4359ddf02784` |
| Full results | `21e4436d1b8aa93a2171195a7a57e5bd3afe52df0adb87afdacd4a7edf354467` |
| Full receipt | `caac34099c80a05845f37ffb9d198d8df086e3747215291a61399aa4e4ec8e0d` |
| Portable packet | `9000d7e1d23359cf489458f693607a61824caeffe6a0c586afa6815c236cc32b` |
| Compact results | `fcf390607423570d6d06f8be045294da7aef1a971d1529194cee38cf1624df71` |
| Compact receipt | `68701d21f842e0928b220b0019e1095a6374905a156c0bc31188e5e664643a67` |

The independently reproduced result is complete V1 numerical agreement accounting, poor V1 judge availability, and an interrupted separate V2 format diagnostic. It is not validation of general financial competence, expert semantic truth, a successful reminder intervention, or a completed V2 comparison.
