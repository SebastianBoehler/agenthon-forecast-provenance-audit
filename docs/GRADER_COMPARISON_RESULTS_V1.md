## Executive summary (read this first)

The final iteration adds a restricted, familiar-benchmark comparator audit and
96 local attempts. It supports the financial grading consequence and a distinction
between false credit and equivalent-answer rejection. It does not demonstrate
natural MATH500 score inflation, a new universal verifier or a training effect.
No paid inference was used.

### Complete reference census and authored controls

All 500 MATH500 references are censused: 368 enter the declared exact-rational
grammar and 132 abstain. Seven admitted questions have approximate/rounding wording
flags, leaving 361 for salted local selection. Eight selected references comprise
seven integers and one fraction. The wording filter is incomplete and does not
certify answer determinacy.

The 2,548 authored controls contain 1,451 equivalent and 1,097 unequal pairs,
but only 174 distinct reference values and 695 distinct numeric pairs.

| Comparator | Unequal credit | Equivalent rejection |
| --- | ---: | ---: |
| Pinned native | 354 | 372 |
| Remove integer-part | 354 | 406 |
| Remove digits-only | 0 | 420 |
| Remove both | 0 | 456 |
| Literal equality | 0 | 456 |
| Exact rational equality | 0 | 0 |

All 354 false credits are sign flips. False rejections comprise 361 unreduced,
seven canonical and four terminating-decimal equivalents. Fraction-form shifts
do not cover all integer-part collisions possible under decimal representations;
the earlier authored diagnostic demonstrates those separately. Zero exact-baseline
errors verify control consistency within the grammar, not universal semantic truth.

### Paired local observations

Gemma 4 E2B and Qwen3.5 9B each receive three unseeded repetitions over eight
mathematical and eight financial questions. The latter are two unused question
groups per family in four families. Every one of 96 scheduled requests returns.

| Panel, 24 scheduled each | Strict scalars | Released/native shared credit | Corrected credit | Valid denied |
| --- | ---: | ---: | ---: | ---: |
| Gemma financial | 21 | 6 | 13 | 7 |
| Qwen financial | 23 | 6 | 15 | 9 |
| Gemma mathematical | 22 | 20 | 20 | 0 |
| Qwen mathematical | 20 | 17 | 17 | 0 |

Financial scoring rejects 16 of 28 contract-valid responses: 12 requested-integer
Gordon and four call-price answers. Correcting targets under unrounded cent
tolerance gives 7 Gemma and 9 Qwen credits; complete rounding compliance gives
13 and 15. Per-repeat complete credits are 5/4/4 and 4/6/5, against 2/2/2 under
released-label scoring for either model. These are dependent finite observations.

On 42 strict mathematical scalars, exact and native shared-extraction scores
agree on 37 credits. Removing both normalizers gives 31, losing six correct
fraction representations. Native full extraction admits 43 and credits 38, recovering
one correct inline Qwen final answer. No natural unequal-value credit is observed.
This small reference-type panel cannot establish benchmark-wide absence of errors.

Eight exactly-cap responses are conservatively censored: five mathematical and
three financial. Native statistics supply no stop reason proving truncation.
Two additional strict-final nondecisions affect one Qwen case in each domain.
No runtime error, retry, replacement or additional paid call occurred.

### Amendments, validation and contribution

Qwen's original readiness gate stopped on an inline final marker in a correct
source-free probe. A timestamped readiness-only continuation was declared after
Gemma completed, before any Qwen cohort call. The three preserved probes were
not rerun; scientific instructions, strict parsing and all endpoints stayed frozen.
The original timing and failed gate remain in the artifact.

Independent replay checked all source/freeze/collection hashes, all control truths,
the eight exact financial targets and all 96 saved score records. The portable
projection additionally replays 2,548 controls and 96 scalar attempts without
original questions or explanatory prose. Full extraction replay requires local
originals. A prospective projection corrects the historical salted-order hash's
misleading field name; historical frozen files are not overwritten.

The novelty claim is implementation-specific evidence connecting verification
metadata, requested financial quantities and observed grading consequences,
strengthened by controlled equivalence/extraction decomposition. Exact arithmetic,
label-error audits and behavioral controls are established methods. Main-track
gaps still include expert financial adjudication and independently produced
financial source replication. A tiny NN/RL policy that rediscovers a known scalar
collision would add little; learned discovery or held-out transfer needs its own
protocol and analytic exploit baseline.
