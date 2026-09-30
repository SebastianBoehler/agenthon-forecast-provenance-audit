## Executive summary (read this first)

An independently implemented exact-rational audit agrees with the primary numeric
calculation on **5,935 released rows**. It confirms three distinct interpretations:
the constructed-response Gordon wrapper omits its requested whole-unit rounding;
the binomial generator returns bond financing rather than the call value; and CAPM
labels are compatible with hidden beta precision. RLVR DCF labels are compatible
with rounded displayed rates. These are different mechanisms and should remain
separate in the paper.

This is **AI-assisted technical validation**, not human expert annotation or a
blind inter-rater study. The validator read the protocol and main formula code,
then wrote separate calculations using Python `Fraction`. It imports no primary
audit module and executes no upstream solution, generator or verifier. Reading
the primary implementation limits claims of conceptual independence; exact
arithmetic, different cash-flow identities and source inspection supply additional
technical checks.

## Scope, sampling and arithmetic

The pinned Cosimo CFA Level I release and ordinary RLVR DCF subset were loaded only
after checking their complete-file SHA256 hashes. The independent implementation
checks all 1,000 constructed-response Gordon rows, all 1,000 binomial rows, all
1,000 CAPM rows and all 2,655 ordinary DCF rows. It checks 40 rows from each of the
other seven Cosimo families: 20 with source preference pairs and 20 without.
Sampling sorts SHA256(`independent-contract-v1:<row id>`) within each stratum.
There is no sampling based on the primary audit's findings.

A separate 440-row review file contains 40 rows per Cosimo family, stratified by
preference availability, plus 40 DCF rows stratified by visible rate spread below
five percentage points versus at least five. This file is an executable arithmetic
review sample, not a claim that 440 examples received human annotation.

All displayed decimal operands become exact rational numbers. Annuity values use
the successive account balance `balance = balance * monthly_gross + payment`;
they also agree exactly with the geometric-series closed form. Present values use
successive annual discounting and satisfy `PV * gross**years == cash`. CAPM uses
the equivalent expression `beta * market + (1-beta) * risk_free`. Effective rates
use successive compounding. WACC values are in percentage points, matching the
source percentage answers. Multiple-choice checks cover numeric values, not
option-letter repair.

The raw-formula serialization check allows 0.005 unit (or 0.005 percentage point
for percentage answers). A cent label alone does not establish that the prompt
demanded exactly two decimal places. Explicit nearest-whole instructions instead
require an integer. At exact half ties both adjacent integers are acceptable.

| Cosimo family | Checked rows | Unique questions | Gold valid under displayed-exact contract | Preference pairs | Chosen valid |
|---|---:|---:|---:|---:|---:|
| `cr_eq_gordon` | 1,000 | 630 | 54 | 337 | 25 |
| `eq_gordon` | 40 | 39 | 40 | 20 | 20 |
| `deriv_binomial_call` | 1,000 | 905 | 25 | 326 | 11 |
| `tvm_annuity_fv` | 40 | 40 | 40 | 20 | 20 |
| `v_tvm_annuity_fv` | 40 | 40 | 40 | 20 | 20 |
| `corp_wacc` | 40 | 40 | 40 | 20 | 20 |
| `m_corp_wacc` | 40 | 40 | 40 | 20 | 20 |
| `port_capm` | 1,000 | 991 | 158 | 353 | 65 |
| `tvm_pv_lump` | 40 | 40 | 40 | 20 | 20 |
| `tvm_eay` | 40 | 17 | 40 | 20 | 20 |

The seven sampled control families have zero sampled gold mismatches. This is not
an independent full-census validation of those families. All 1,156 raw source
rejected answers encountered across the checked Cosimo rows fail the final-answer
contract; the rounding control below makes that observation more informative.

## Source inspection and mechanisms

The public MIT-licensed generator repository was accessed successfully and pinned
to revision `20668622104bf8237837efd67debd1419f7bbe33`. Source text is cached under
ignored `literature/pdfs/cosimo-source-20668622104b/`. This Git revision is separate
from the Hugging Face dataset revision. It demonstrates that the inspected public
implementation contains the mechanism; it is not asserted to be the exact commit
used to generate the pinned release.

In [the binomial implementation](https://github.com/btech-software/cosimo/blob/20668622104bf8237837efd67debd1419f7bbe33/dataset/pipelines/templates/cfa_l1.py#L441),
line 451 assigns `c = (h*su - cu)/(1+rf)`. That is positive bond debt. A replicating
portfolio instead holds `h` shares and a signed risk-free bond, with call value
`h*S0 + signed_bond`. The validator solves both terminal payoff equations and
checks exact agreement with risk-neutral expectation on every row. All 1,000 golds
match positive bond debt within cent serialization. Only 25 match the call price;
975 differ, spanning 888 of 905 unique questions. There are 315 preference pairs
whose chosen numeric answer is invalid and whose rejected answer is also invalid.
All 1,000 source golds nevertheless satisfy the elementary call lower/upper bounds.
Thus those bounds alone do not detect this particular semantic error.
Every audited binomial row is marked verified. The inspected
[verification harness](https://github.com/btech-software/cosimo/blob/20668622104bf8237837efd67debd1419f7bbe33/dataset/verification/run_verify.py#L47)
regenerates the selected template from its seed and compares its answer. This
checks reproducibility of the generator rather than an independent pricing identity.

In [the constructed-response wrapper](https://github.com/btech-software/cosimo/blob/20668622104bf8237837efd67debd1419f7bbe33/dataset/pipelines/templates/wrappers.py#L30),
the added nearest-whole instruction is followed by copying the underlying answer.
The independent census reproduces 946 invalid final golds, spanning 594 of 630
unique questions. All 1,000 golds agree with the unrounded formula to cent
serialization. There are 19 exact half ties; the stored fractional half values
are invalid under either neighboring-integer convention. Half-up versus half-even
is therefore not an explanation for the reported label count.

Quantizing the 337 source-authored Gordon rejected answers produces **34 numerically
valid integer answers** despite their wrong dividend trace. These are trace-blind
final-answer collisions, not invalid-final negatives. The remaining 303 integer
answers provide the stronger rounding control. Quantizing the 337 chosen answers
produces 337 valid integers. A numerical repair cannot establish trace correctness.

In [the CAPM implementation](https://github.com/btech-software/cosimo/blob/20668622104bf8237837efd67debd1419f7bbe33/dataset/pipelines/templates/cfa_l1.py#L519),
rates are sampled to three decimals as proportions, exactly representable at the
displayed one decimal percentage precision. Beta is sampled to three decimals and
displayed to two. The rounding function is confirmed in
[the RNG implementation](https://github.com/btech-software/cosimo/blob/20668622104bf8237837efd67debd1419f7bbe33/dataset/pipelines/core.py#L212).
All 1,000 CAPM golds are feasible with displayed rates held fixed, beta allowed
within ±0.005, and cent-answer serialization within ±0.005 percentage point.
The independent census reproduces 842 exact-visible-input mismatches, spanning
836 of 991 unique questions. The raw interval width is 0.041–0.099 percentage point.
This supports beta precision loss rather than an incorrect CAPM formula.

For the 2,655 ordinary RLVR DCF rows, exact visible inputs produce 2,385 misses at
the advertised absolute 0.0001 condition, 2,220 differences over 0.1%, and 128 over
1%. If each displayed rate is rounded to 0.1 percentage point, all 2,655 golds are
feasible after allowing the gold's four-decimal serialization. The median relative
feasible-interval width is exactly `180/8099`, approximately 2.2225%. Feasibility
does not identify a unique target or justify rewarding every feasible candidate.
No deployed reward or trained-model consequence was tested.

## Concrete checked examples

- Gordon row `cosimo_CFA_Level_I_257594_44f6d3da2ba5930c`: `D0=5`, `g=6.1%`,
  `r=12%` gives `5305/59 ≈ 89.9153`. The gold is 89.92, while the requested integer is 90.
- Binomial row `cosimo_CFA_Level_I_1081729_515a22eb37c94a76`: `S0=59`, `u=1.25`,
  `d=0.80`, `K=54`, `rf=4%` gives call value `395/39 ≈ 10.1282`. The source gold
  33.76 matches bond debt `3950/117 ≈ 33.7607`.
- CAPM row `cosimo_CFA_Level_I_630879_0ba67a2fd2368e4e`: visible operands give
  9.33%, while the gold is 9.34%. Allowing beta ±0.005 yields `[9.299%, 9.361%]`.
- Gordon row `cosimo_CFA_Level_I_833594_065b1ef61675cca9`: the correct value is 13,
  while the source rejected D0 calculation gives 12.50. Half-up integer rounding
  produces 13; correct final output therefore does not validate its reasoning.

## Agreement, revisions and limits

After independent results were computed, they were compared with the primary
row artifact. All 5,935 formula values agree within absolute `1e-35`; all 3,280
checked Cosimo gold decisions, all 1,156 chosen decisions and all 1,156 rejected
decisions agree. These comparisons are additional consistency checks, not the
method used to generate independent values or choose sample rows.

Review prompted two clarifications: accept both neighboring integers at exact
half ties, and distinguish the narrower source-supported beta-only CAPM interval
from an interpretation that also rounds its rates. The rounded-rejected Gordon
control was added to exclude 34 valid-final collisions from the invalid-final
denominator. No confirmed formula disagreement remains.

The sources and families are purposively selected. Counts do not estimate the
prevalence of finance-data defects. This review checks scalar financial formulas
and stated rounding, not all language, trace quality or alternative conventions.
No source generator was run, so no end-to-end reproduction of its publication
pipeline or claim of training degradation is made.

## Materialized patch validation

A post-review check compares the actual 5,935 exported patch answers against
independent Fraction calculations, including declared half-up rounding and source
serialization precision. All checked patches pass. This tests exported numerical
corrections; it does not certify a reasoning trace or downstream learning effect.

## Reproduction and artifact hashes

Run from the dedicated research repository after staging the two pinned datasets,
the source cache and the primary `outputs/answer-contract-v1/rows.jsonl` artifact:

```bash
cd /Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit
.venv/bin/python scripts/independent_contract_validation.py
.venv/bin/python -m py_compile scripts/independent_contract_validation.py
```

To recreate the legally accessible source cache:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path
import hashlib, json, urllib.request
revision = '20668622104bf8237837efd67debd1419f7bbe33'
paths = ['LICENSE', 'dataset/pipelines/templates/cfa_l1.py',
         'dataset/pipelines/templates/wrappers.py', 'dataset/pipelines/core.py',
         'dataset/verification/run_verify.py', 'dataset/verification/nums.py']
files = []
for path in paths:
    url = f'https://raw.githubusercontent.com/btech-software/cosimo/{revision}/{path}'
    raw = urllib.request.urlopen(url).read()
    destination = Path('literature/pdfs') / f'cosimo-source-{revision[:12]}' / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(raw)
    files.append({'path': path, 'local_path': str(destination),
                  'sha256': hashlib.sha256(raw).hexdigest(),
                  'url': f'https://github.com/btech-software/cosimo/blob/{revision}/{path}'})
Path('literature/pdfs/cosimo-source-manifest.json').write_text(
    json.dumps({'revision': revision, 'files': files}, indent=2) + '\n')
PY
```

The script is 286 lines. Python was 3.13.2 and pandas 2.3.1. The executable
`summary.json` records runtime, protocol, input, source, primary-comparison and
output hashes. `rows.jsonl` preserves exact fractions alongside display floats;
`review_sample.jsonl` preserves the 440 selected review rows. Display floats never
drive an acceptance decision.

| Artifact | SHA256 |
|---|---|
| Independent script | `80d89eb50510f5c2a8d198bc840477b0f1a1d56f2591ebf8610dd12f40c74b95` |
| Independent row results | `cb551463abbd0a47c50392f492a05bdd84cf6ce43a841697132807c974c320dd` |
| Review sample | `b06ea91f935b821f5497e1c857dffb52ea2a2e61445f5ebec5e1bf833b0f51df` |
| Cosimo dataset | `afa7e9241e0f06df090916e289a8e39d7fc9c4245c3b21c0c0f1188edafb0abb` |
| RLVR dataset | `86968a146a09e2ba1b19aac3a5ca2bec7e878358341a7972fddeb4b8cd7754af` |
| Public CFA generator source | `440447b60a75d37479bf2d4ec4cf8921748e2b76f0fb40f87a690d164622d43e` |
| Public wrapper source | `41da0325c6775f3d1e5cecc7dce242d4fac2e236009b7727e7834f41b4c1c51a` |

The summary's protocol and primary-file hashes identify the exact compared snapshot;
rerunning after a protocol amendment legitimately updates those two identifiers.
