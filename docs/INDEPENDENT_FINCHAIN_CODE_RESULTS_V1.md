## Executive summary (read this first)

A prospectively frozen bank of 300 newly generated FinChain-template instances
adds an independently authored code comparison. All 300 native final values are
compatible with their source's intermediate-rounding convention. Eighteen of 100
call prices fall outside half-cent compatibility with exact visible-input values;
none falls outside both declared conventions. This is convention sensitivity and
source specificity, not replication of the debt-for-call defect or a historical
FinChain benchmark reproduction. No new model or paid compute call was made.

### Frozen source and complete membership

The [protocol](INDEPENDENT_FINCHAIN_CODE_PROTOCOL_V1.md), source fragments, adapters,
analysis, parser, tests and runtime were frozen at **16:13:51.976774 UTC on
September 30, 2026**, before any native instance generation. Python 3.13.2 executes
the inspected FinChain commit `9bd2942b85d992844b77094a8b822aa16832703c`.

The three original functions each receive all seeds 0–99, with a separate
`random.Random(seed)`. Every question and solution is preserved verbatim and
hashed. There are 100 unique questions per family, 300 assessed attempts, zero
nondecisions, retries or replacements. Mechanisms are clustered within three
functions from one additional authoring pipeline; the seeds are not independent
replications of a newly discovered mechanism. This is not uniform topic coverage.

| Original native function, 100 scheduled each | Exact visible-input compatibility | Source-rounding compatibility | Wrong-quantity control accepted |
| --- | ---: | ---: | ---: |
| One-period binomial call | 82 | 100 | 13 |
| Basic WACC | 100 | 100 | 0 |
| Annual compound interest | 100 | 100 | 0 |

Compatibility is within half of one hundredth currency unit or percentage point.
References use exact Fraction arithmetic from untouched question operands, checked
by independently expressed financial identities. A separate endpoint preserves
the source's cent-rounded call-state prices, four-decimal WACC weights and rounded
compound amount. Both nearest alternatives are retained at exact ties. We inspect
final scalars only; no ChainEval, trace-validity or model-performance score is used.

### What the differences mean

All 18 call differences are compatible with source-rounded terminal states. The
largest exact/native distance is approximately 0.008390 currency units. One case
(`binomial_call/40`) returns 39.36 while the exact lower bound and exact price are
`52163/1325`, approximately 39.368302. The difference exceeds half a cent, but the
native answer matches the rounded-state calculation. We do not recast this as a
wrong-quantity defect. Exact-model bounds and source-rounded evaluation require
different interpretations; a validator should make that choice explicit.

The authored controls substitute financing debt, omit the WACC tax adjustment or
use future amount rather than compound interest. All 13 accepted call/debt controls
have zero call payoffs and zero financing debt, so they are nondiagnostic numeric
collisions. The other 87 call controls and all 200 WACC/interest controls are
rejected. These are deliberately constructed controls, not native error rates.

The new producer does not reproduce the audited debt-for-call mechanism in this
bank. That negative comparison makes the release-specific claim more credible and
prevents generic claims about all financial generators. Different author teams
and repositories do not prove statistical or conceptual independence.

### Replay and remaining boundary

The [portable bank](../artifacts/independent-financial-source-v1/README.md) contains
all 300 original generated question/solution pairs, extracted values, exact and
source-rounded references, control decisions and source/code/runtime receipts.
The author's current Apache-2.0 source/notices are preserved separately; no
historical published instances, original benchmark outputs or weights are implied.

```bash
PYTHONPATH=src python scripts/replay_independent_finance.py
```

Replay checks original source bytes, seed membership, generated text, financial
values and all summary counts. It does not establish expert authority or causal
learning consequences. Qualified-human adjudication remains absent, and further
work requiring it is not included in this iteration. The source expansion partially
addresses breadth while historical financial-release replication remains open.
