## Executive summary (read this first)

The prepared adaptation questions pass independent numerical and split validation.
All 152 cases were recalculated with exact fractions, including the 16 off-split
format checks. The source selection was independently reproduced from the pinned
public parquet. No question or exact financial operand tuple crosses a new split
or repeats an operand tuple from the earlier 200-question study. The 24 authored
transfer tuples are absent from the entire four-family source release.

The financial oracle is ready for this bounded pilot under its declared exact-input,
effective-period-rate assumptions. This is AI-assisted technical review, not
finance-expert human adjudication. It establishes implementation agreement and
limited specification consistency. It does not establish broad benchmark validity,
the absence of model pretraining exposure, or an adaptation consequence. No new
inference was run by this reviewer. The final full freeze must cover the corrected
wrapper, implementation, dependencies, data, protocol, prices and these artifacts.

## Evidence and independent method

The [independent validator](../scripts/finance_adaptation/independent_validation.py)
imports no primary formula, benchmark, selection, parser, optimizer or generator.
It reads the original parquet directly, implements selection separately, extracts
operands from the actual source and transfer wording, and computes financial
values using Python `Fraction`, an exact rational-number representation.
The validator compares the prepared 50-digit Decimal values with an absolute
numerical allowance of `1e-42`. It separately checks the declared cent allowance
of `0.005` and its arithmetic guard of `1e-20`.

The [152-case result](../outputs/finance-adaptation-v1/independent/benchmark_validation.json)
was produced at 2026-09-29 20:32:41 UTC. A separate
[boundary check](../scripts/finance_adaptation/check_oracle_boundaries.py) calls
the actual primary grading API with independently specified synthetic cases.
That second check tests software behavior; its artificial cases are not inserted
into the experiment and are not reported as observations.

| Partition | Total | Per family | Released CR Gordon invalid | Released binomial invalid |
|---|---:|---:|---:|---:|
| Train | 32 | 8 | 7 | 8 |
| Development | 32 | 8 | 6 | 8 |
| Source numerical test | 48 | 12 | 12 | 11 |
| Off-split format preflight | 16 | 4 | 3 | 4 |
| Authored wording transfer | 24 | 6 | No released label | No released label |

All selected ordinary Gordon and WACC released targets are numerically valid.
The selection did not condition on these disagreements. One selected binomial
source-test case has zero call payoff, so its released target is valid. Retaining
that case is consistent with unconditioned selection.

## Financial quantities, units and rounding

For both Gordon families, the printed dividend is already paid: it is `D0`.
The price is the next annual dividend divided by the required return minus
growth. Independent extraction confirms that every authored wording preserves
that timing. The constructed-response family requests a whole currency unit;
ordinary Gordon requests cent compatibility.

For every binomial case, the reviewer computed terminal positive call payoffs,
solved the stock-and-bond replication, and separately computed the discounted
risk-neutral expected payoff. The two exact values agree. Both terminal payoff
identities and no-arbitrage bounds hold. The financial quantity is the current
call price, rather than the financing debt. The pilot fixes the risk-free return
as effective over the same single period, with gross factor `1+r`; continuous
compounding is not an alternative acceptance convention in this new experiment.
All three transfer wordings now state European expiry and no dividend cashflows.
Source text inherits its original concise tree description; the fixed wrapper
supplies the prospectively declared convention.

For WACC, both financing weights use market values. The debt contribution applies
the marginal interest tax shield. The result is in percentage points: `7.25
percent` means a rate of `0.0725`, not `0.0725 percent`. Independent values lie
between the equity cost and the after-tax debt cost, as a positive weighted
average should. All transfer wordings preserve these roles and units.

None of the 152 selected cases is an exact whole-Gordon half tie. The unchanged
unconditioned source pool contains such ties, so absence in this selection is
not evidence that the branch is unnecessary. A separately specified Gordon
case with `D0=1`, growth `0%` and required return `8%` has exact value `12.5`.
The actual API accepts both `12` and `13`, rejects `12.5`, and rejects the tiny
fractional perturbation `12.004` under the whole-unit repaired objective.

The [boundary result](../outputs/finance-adaptation-v1/independent/oracle_boundary_checks.json)
also passes inclusive cent boundaries, percentage-point scaling, nonfinite
rejection, wrong/conflicting units, repeated markers, trailing text, and
truncation or transport-failure rejection. The strict endpoint checks the final
answer line; it does not measure compliance with every prose instruction.

The formula-centered cent oracle measures numerical compatibility. It does not
require that the numeric value itself lie on a cent grid or have exactly two
printed decimal places. Whole-unit integer membership is explicitly enforced.
Do not interpret cent-oracle validity as proof of literal cent serialization.

## Sampling, separation and template ownership

The source has 630, 905, 639 and 999 distinct prompts in CR Gordon, binomial,
ordinary Gordon and WACC respectively. Duplicate prompts have no conflicting
released numeric labels. The independent implementation reproduces the declared
smallest-ID representative, salted SHA256 rank and family order. It reproduces
all 128 source-case IDs and their partition assignment, including the next four
off-split cases per family used for preflight.

Canonical exact operands remove insignificant decimal zeros. Both Gordon
families share the same operand namespace, preventing the same financial
problem from entering different partitions under a different rounding wrapper.
All 152 prompt hashes and operand hashes are distinct. Every transfer operand
tuple is absent from all 4,000 rows in the four-family source release, the earlier
study and the new source splits. Transfer rows omit `source_gold` entirely.

The [authored template file](../src/finance_adaptation/transfer.py) supplies three
wordings and two operand tuples per wording for each family. There are twelve
family/template IDs; the two Gordon families share their three base descriptions
and differ in requested rounding. This means nine base wording structures, not
twelve unrelated financial mechanisms. These are AI-assisted researcher-authored
questions reviewed by another AI-assisted technical workflow. They are not
independent external source releases or human expert annotations.

The source numerical test changes operands within inherited source wording.
Only the 24 authored cases test changed wording, within the same three financial
calculations and four answer contracts. Original family discovery and actor
inspection preceded this pilot. The freeze makes subsequent rules prospective;
it cannot turn the family choice into a previously unseen hypothesis.

## Objective isolation and review fixes

The [adapter](../src/finance_adaptation/adapter.py) forwards only the assigned
objective view in both GEPA outputs and reflection trajectories. The installed
GEPA 0.1.1 reflective mutation code can consume outputs as well as trajectories;
limiting only the latter would leave a weaker isolation boundary. Full financial
and released-label decisions remain in local result ledgers for later analysis.

Released-target adaptation receives the released target, boolean reward,
declared tolerance and parser error. Repaired adaptation receives its assigned
repaired target and whole-unit requirement. The feedback fields have the same
schema. All actor conditions use the same wrapper and raw question. All final
strategies are selected on their assigned development reward before either
holdout is loaded for response collection.

Passing ordinary-Gordon and WACC objective targets are exactly unchanged across
arms. The independent validator confirms their financial validity. Defective
binomial repair uses the independent call price serialized to cents; whole
Gordon uses the admissible integer or integers. The serialized-target comparator
is distinct from the formula-centered financial oracle. Therefore a repaired
reward is not, by construction, identical to independent financial validity at
every sub-cent boundary. Preserve both measurements and disclose the geometry.

Review found and resolved a missing no-dividend clause in the first binomial
transfer wording, fractional whole-unit acceptance in the repaired comparator,
and unnecessary unassigned-oracle fields in GEPA outputs. A separate runner
review confirmed that new egress rechecks the elapsed-time limit after acquiring
the global four-call semaphore. Provider and returned model identifiers are
checked against the actual route's response conventions. These are pre-freeze
corrections; they do not alter the earlier audit or its frozen response ledgers.

## Reproduction and immutable checkpoints

Run from the dedicated research repository, without making API calls:

```bash
.venv/bin/python scripts/finance_adaptation/independent_validation.py
.venv/bin/python scripts/finance_adaptation/check_oracle_boundaries.py
```

The first command writes a timestamped validation result. A rerun changes its
timestamp and thus its file hash. Preserve the pre-inference result in the full
freeze; write later replays to a copied workspace rather than overwriting that
checkpoint.

| Artifact | SHA256 |
|---|---|
| Public source parquet | `afa7e9241e0f06df090916e289a8e39d7fc9c4245c3b21c0c0f1188edafb0abb` |
| Earlier 200-question selection | `75c5b694db2d9a174e089c594e3f756867e0f840f12ac4634e5dc20173acf0cc` |
| Preserved original 600-answer independent checkpoint | `51c753e90ce0bff459c88d4580275eb847b1dab5f73ee088ff1696ceafa5712a` |
| Independent Fraction validator | `a05fc8c579a62f6b7446c8c8c9bf90e840dd13e9e277d568b59353bf31371191` |
| Synthetic actual-API boundary script | `a1ece77bdd384d2e15ccfc0b40c1e098bda608fcac8df52565a287db216e63f5` |
| Independent 152-case result | `1e24b7b2d54b85fcf1e1e00243e5e5deabbc606e6c5e0ef4b2baa00e23b50f5a` |
| Synthetic actual-API boundary result | `be573fd010f0ff8187d0d9f8e92390df99f2db5652ca1e0b68b6a715a150267e` |
| Train JSONL | `f9ea5a3d74b5894ffdeb11b95757dccb6f016776598a87ded0b79b512fb92d23` |
| Development JSONL | `de6662d615fb020740f54d7752f06d505db263b3db3c332d0faa0aab7ee0cae2` |
| Source-test JSONL | `ff1a6651c6730d0f5d493c6571c07fd4bfc5f3071b9cf0ac0479e5c2f8c0b4d7` |
| Preflight JSONL | `fb100cd689b3665da95323e62189836d578dedef5305bc8fe06b415c4afc054c` |
| Transfer JSONL | `46a0ee04a3144e554a5d469009456c0d37ec8c8a4076a07e6d827123fbd3bedb` |

The result JSON records these hashes plus individual exact answers, identities,
template counts and the preparation-manifest hash. The preparation manifest is
explicitly unfrozen; its earlier draft code hashes are superseded by the final
full freeze. This review supplies readiness evidence, not permission to change
frozen artifacts or a claim that the adaptation success gates have passed.
