## Executive summary (read this first)

The selected study has executed: **12,655 rows, 10,476 distinct visible questions
within family**, two pinned public training releases, ten Cosimo families and one
RLVR family. Independent rational calculations agree on 5,935 checked rows.
The strongest contribution is the external supervision audit and traced common-mode
verification failure. No new verification concept, trained-model degradation,
field-wide prevalence or acceptance guarantee is claimed.

## Findings and their interpretation

| Family | Rows / distinct questions | Result |
|---|---:|---|
| Constructed-response Gordon | 1,000 / 630 | 946 labels violate requested whole-unit output; 594 distinct prompts have a violating label. All raw formula values match cent labels. |
| Binomial call | 1,000 / 905 | 975 labels disagree with option valuation; 888 distinct prompts affected. All 1,000 golds instead match positive bond financing. |
| CAPM | 1,000 / 991 | 842 disagree with exact displayed inputs; all 1,000 are feasible under hidden beta precision. This is conditional ambiguity, not unconditional wrong finance. |
| Seven Cosimo comparisons | 7,000 / 5,297 | No cent-serialization discrepancies: ordinary Gordon, WACC, MCQ WACC numeric values, annuity, vignette annuity, present value, effective annual rate. |
| RLVR DCF | 2,655 / 2,653 | 2,385 exact-visible results miss the advertised absolute 1e-4 condition. All golds match stored hidden literals and all remain possible under rounded-rate semantics. |

Counts concern these selected families. Distinct affected prompts mean prompts with
**any** conflicting released label; hidden parameters can give different labels
for the same displayed question. The published source generator revision is separate
from the pinned dataset revision; it is not proven to be the original generation commit.

## Comparator consequences and simpler baselines

On whole-unit Gordon, original-label ±0.005 rejects 946/1,000 valid integer answers.
±0.5 accepts every valid answer but accepts 23/337 raw source rejected answers.
5% accepts every valid answer and 217/337 rejected answers. The complete numerical
contract accepts valid targets and rejects all 337 tested raw errors. Formula-only
recomputation still rejects 946 valid integer answers: the output instruction matters.

After rounding rejected answers to integers, 34/337 become numerically correct
despite their incorrect D0 derivation. Those 34 are not wrong-final-value negatives.
Of the other 303, 5% tolerance accepts 173; the numerical contract accepts zero.
An **integer constraint plus original-label ±0.5** also accepts every valid target
and rejects these 303. This simpler baseline succeeds; no new repair algorithm is needed
for this particular instruction conflict. A format-only integer checker accepts all
303 wrong integers and therefore is insufficient by itself.

In the binomial family, 5% rejects 975/1,000 correct formula answers and accepts
20/326 source rejected answers. Re-evaluating the correct formula is necessary.
All 1,000 source golds satisfy elementary call bounds; those invariants alone miss
the defect. The inspected verifier regenerates the same template from the seed:
generator agreement verifies reproducibility while sharing its formula error.

For DCF, 5% accepts every correct displayed-input value and rejects all tested
growth-omission errors. This is a successful tolerance-widening control, not a
universal failure. An interval checker cannot identify hidden targets; the rounded
DCF interval also contains a deliberately shifted +1% answer in 1,769/2,655 cases.
That statistic illustrates nonidentification, not false acceptance under interval semantics.

## Preference supervision and numerical patches

The unambiguous source conflicts include 312/337 chosen Gordon answers and 315/326
chosen binomial answers. Their rejected alternatives are also invalid: **627 pairs
need replacement chosen completions, not automatic swaps**. CAPM contributes another
288/353 exact-input chosen disagreements, conditional on the exact-input convention.
None of this measures downstream model learning or deployed rewards.

`outputs/answer-contract-v1/numerical-patches.jsonl` materializes 12,655 numerical
patch records. For ambiguous families, patches explicitly declare exact inputs.
They do not restore the original hidden precision. Reasoning traces and MCQ letters
are not certified or regenerated; this file is not a ready-to-use DPO training corpus.
Acceptance and negative classification share specified mathematical oracles.
Zero acceptance is finite consistency on the tested controls, not general validator accuracy.

## Execution and evidence

```bash
cd /Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit
.venv/bin/python -m pip install --no-deps --no-build-isolation -e .
.venv/bin/python scripts/stage_answer_contract.py
.venv/bin/python scripts/run_answer_contract.py
.venv/bin/python scripts/independent_contract_validation.py
.venv/bin/python figures/answer_contract.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/python -m pytest tests/test_answer_contract.py -q
```

The focused five tests pass. Plugin autoload is disabled because an unrelated global
pytest-cases installation crashes against pytest 9.1.1. The native LaTeX compiler
successfully compiled `paper/answer_contract_audit.tex`; local TeX exports the same
source to a six-page PDF. The final two-pass export has no undefined-reference or
overfull-box warnings after review edits.
Git status is unavailable because Apple's Git requires accepting the Xcode agreement;
no legal agreement was accepted and no commit/push was requested or performed.

Inputs, code/protocol/amendment hashes, runtime versions and output hashes are in
`outputs/answer-contract-v1/manifest.json`. Independent fractions, a 440-row review
sample and source hashes are in `outputs/answer-contract-independent/`. Figures have
their own metadata. The [independent validation](ANSWER_CONTRACT_INDEPENDENT_VALIDATION.md)
and [literature reassessment](INDEPENDENT_NOVELTY_REASSESSMENT_2026-09-29.md) distinguish
technical validation, full-text access, conceptual overlap and remaining limits.
