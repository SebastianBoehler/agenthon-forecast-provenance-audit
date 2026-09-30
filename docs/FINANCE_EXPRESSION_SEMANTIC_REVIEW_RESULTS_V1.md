## Executive summary (read this first)

Of the original 47 saved numeric mismatch → executed-expression match transitions,
41 expressions across 22 questions are supported by both AI technical reviewers
under their recorded assumptions. Six expressions across two questions retain an
interpretation disagreement. Neither reviewer contradicts any of the 47. This is
conditional evidence of grounded computation, not 47 certified financially correct
answers, human adjudication, or improvement by a prospective method.

Across all 131 reviewed expressions from 58 questions, both reviewers support 104,
both contradict 14, both mark three ambiguous, and ten have A-ambiguous/B-supported
status disagreement. All original 384 attempts remain the study denominator; 253
attempts lie outside this review subset. Original outputs, endpoints and reviews
were not edited. No model calls or network access occurred.

## Lock and actual provenance

B passed the structural validator: 131 identities and 1,049 context pointers. Both
reviews and their receipts were then bound with the packet, protocol, preparation,
validator, shared IO, arithmetic helper, original packet freeze and structural
validations in a 13-file [joint lock](../outputs/finance-expression-review-v1/joint_review_lock.json).
It was exclusively created and made read-only at
`2026-09-30T09:29:19.367406+00:00`, before reading private join-key or diagnostic
outcome contents during this review. Its SHA256 is
`06e6066f4d030f21a59e69c1358830169ff5bcf366cb2587d7a4a9454834cc6e`.

Both reviewers disclose prior study exposure. B previously performed the original
question review, unblinding and diagnostic checks. Current masking cannot remove
remembered cases, references or outcomes, establish independent conceptual errors,
or create human expertise. Neither current review was revised after outcome
unmasking. B did not read current A judgments until after this joint lock.

The [analysis](../scripts/analyze_finance_expression_review.py) began at
`2026-09-30T09:35:03.942295+00:00`, after an exploratory post-lock join. It verifies
all 13 lock hashes and original freeze hashes, exact selected membership, salted
IDs, case/ledger joins and unchanged expression/unit/scale/evidence. All 131 saved
executed arithmetic values were independently recomputed with the existing safe
Decimal helper; no corpus program was executed. This new posthoc binding does not
retroactively repair the earlier diagnostic implementation registry's omitted
arithmetic dependency.

## All-expression and transition accounting

Rows are expression instances, not independent question samples. The full status
cross-table has A as rows and B as columns:

| A \ B | Supported | Contradicted | Ambiguous | Unresolved |
|---|---:|---:|---:|---:|
| Supported | 104 | 0 | 0 | 0 |
| Contradicted | 0 | 14 | 0 | 0 |
| Ambiguous | 10 | 0 | 3 | 0 |
| Unresolved | 0 | 0 | 0 | 0 |

Binary support tables preserve the uncertainty distinction in the full table:

| Subset | Both supported | A supported / B otherwise | A otherwise / B supported | Neither supported |
|---|---:|---:|---:|---:|
| All 131 | 104 | 0 | 10 | 17 |
| Original 47 transitions | 41 | 0 | 6 | 0 |
| Other 84 reviewed records | 63 | 0 | 4 | 17 |

The original locked numerical endpoint is an unrounded-value / broad-unit match,
not semantic truth. Its reported-value versus expression-value cells remain:

| Numeric reported → executed | Expressions | Questions | Both supported | Contradicted either | Ambiguous or disagreement |
|---|---:|---:|---:|---:|---:|
| False → True | 47 | 24 | 41 | 0 | 6 |
| True → True | 41 | 22 | 39 | 0 | 2 |
| False → False | 43 | 27 | 24 | 14 | 5 |

Thus all 14 consensus contradictions were already numeric False → False. This
review does not demonstrate new semantic false accepts among the original 47
transitions. Conversely, 24 False → False expressions receive consensus support:
semantic support under stated precision/interpretation assumptions and agreement
with the locked comparator are different outcomes. For example, direct lookup
`368` is a displayed rounded change for other-affiliate earnings; the visible
3,711 and 793 imply an unrounded change of `(3711-793)/793*100`. Neither a rounded
lookup nor an unrounded computation alone establishes the uniquely intended
precision policy.

## Question clustering and retained disagreement

The 58 question clusters contain 12 single-expression, 25 two-expression, 15
three-expression and six four-expression clusters. Forty-two clusters have all
reviewed instances supported by both. Fifty-one have at least one such instance,
12 have a contradicted instance, and five have an ambiguous or status-disagreement
instance. These latter counts overlap; they are not an exhaustive partition of
questions. Twenty-four transition questions and 47 other-record questions also
overlap. No independence-based confidence interval is inferred from 131 records.

The six uncertain transitions are two instances for
`finqa:AWK/2012/page_117.pdf-4` and four for
`finqa:SLG/2011/page_91.pdf-6`. Both reviewers recognize a defensible computation,
but A retains ambiguity while B supports the explicitly stated contextual reading:

- AWK: `74360/180993*100` is a share of gross **tax** liabilities. `post_text[0]`
  supplies the classification and `table[6][1]` the ending gross tax-liability
  balance. The question instead says company gross liabilities more broadly.
- SLG: `(2912456-2728290)/2728290*100` is conventional end-to-end balance growth;
  `table[4][1]`, `table[4][2]` and `table[1][1]` ground it. The phrase “percent of the
  change” does not uniquely identify the denominator. No judgment is overwritten.

The other four A-ambiguous/B-supported records concern signed percentage decrease,
two relative changes of a percentage-valued compensation assumption, and
structured-commercial-loan vehicle stocks versus “issued” wording. Three
consensus-ambiguous records use percentage-point differences where the question
may request relative percent change.

## Concrete counterexamples retained

All 14 contradictions are retained below, grouped into 12 question clusters.
Pointers are relative to each row's original visible context. The complete joined
records preserve exact review IDs, case IDs, ledger lines, both rationales and
reference expressions in [semantic_joined_rows.jsonl](../outputs/finance-expression-review-v1/semantic_joined_rows.jsonl).

| Expressions | Question / saved expression | Original evidence and explicit conflict |
|---:|---|---|
| 1 | UA interest-rate decrease: `(5.3-3.5)/5.3`, unit percentage_points | `pre_text[20]`: ratio is a fraction, not a point difference. |
| 1 | G&A qualifying-year count: `2` | `table.table[6][1]`, `table.table[6][2]`, `table.table[6][3]`: 1,827 / 2,144 / 1,993; only one exceeds 2,000. |
| 2 | Priceline minus benchmark returns using `216.54` or `277.56` | `table[6][2]` is NASDAQ; `table[6][4]` is RDG Internet; S&P 500 is `table[6][3]` = 198.18. Percent conversion is also absent. |
| 1 | Noncurrent-liability change: `(39398-32621)/32621`, unit percent | `table.table[4][1]`, `table.table[4][2]`: correct quantities, omitted factor 100. |
| 2 | 2017 CIB share: `3087/55687*100` | `table[2][1]`, `table[1][1]` are 2018; requested 2017 is `table[2][2]` = 4,630 and `table[1][2]` = 51,410. |
| 1 | Agiletics goodwill share: `3999/17015`, unit percent | `paragraphs[3].text`: grounded operands, omitted percent conversion. |
| 1 | Foreign-income change: `88527-75487`, unit count | `paragraphs[8].text`, `table.table[3][1]`, `table.table[3][2]`: monetary income in thousands, not count. |
| 1 | Current-year interim average: `(45+50)/2` | `table.table[4][1]` = 45 and `table.table[4][4]` = 43; 50 is prior-year final at `table.table[5][1]` / `table.table[5][4]`. |
| 1 | Finished-goods ratio: `6356/9801`, scale thousand | `table.table[3][1]`, `table.table[4][1]`: monetary input scale cancels in the ratio. |
| 1 | Basic-minus-diluted EPS: `0.36-0.36`, unit ratio | `table.table[5][1]`, `table.table[6][1]`: zero at displayed precision remains dollars per share, not a dimensionless ratio. |
| 1 | Canada share: `9815/363800*100`, scale thousand | `table.table[5][1]`, `table.table[8][1]`: thousand-currency scale cancels; cannot scale the resulting percent. |
| 1 | Debt share: `(10558+6426)/23556`, unit percent | `table[3][7]`, `table[4][7]`, `table[8][7]`: grounded totals, omitted percent conversion. |

## Reproduction and claim adjustment

Exact commands executed from the repository using its existing runtime:

```sh
PYTHONPATH=src .venv/bin/python scripts/validate_finance_expression_review.py b
PYTHONPATH=src .venv/bin/python scripts/analyze_finance_expression_review.py
```

These commands exclusively create receipts/results; they deliberately refuse an
in-place overwrite. Replay must use a separate working copy with only the new
derived receipts/results absent. Verify the retained lock before recomputation.
The analysis joins `private_join_key.jsonl` to the unchanged original diagnostic
`rows.jsonl` by `effective_ledger_line` and asserts matching `case_id`. All 384
original lines and the exact 131 selected lines are checked. No new eligibility,
normalization, scoring or review policy is introduced.

Recommended claim: “Executing saved expressions changes 47 locked numerical
mismatches into matches. Posthoc outcome-masked AI review supports 41 of those
instances, across 22 questions, under stated assumptions; six instances across
two questions retain interpretation disagreement.” Do not claim expert-confirmed
correctness, 47 independent corrections, a causal reminder benefit, or a new
prospectively validated answer-repair method. The baseline/reminder calculation
representation confound and selective 131-of-384 review coverage remain.

[Machine results](../outputs/finance-expression-review-v1/semantic_results.json)
SHA256: `5632ff7d882598975fc85ca1f5594012ffbba29ac498c9e1b47d0bca6d9c5377`.
[Analysis receipt](../outputs/finance-expression-review-v1/semantic_analysis_receipt.json)
SHA256: `49bf5092e018ce75f4bd67d9bc067bc9ae28929c8e8eace1efb7e6661031a9b9`.
Code SHA256: `3af8cef614fa2b20e1cf9002a5403ac321733847ba746e78392f0564dd5605e8`.
