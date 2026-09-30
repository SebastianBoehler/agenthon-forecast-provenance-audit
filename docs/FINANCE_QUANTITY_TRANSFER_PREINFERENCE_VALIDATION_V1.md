## Executive summary (read this first)

**Technical verification passes, with explicit measurement limits.** All 32
question/context packets and unchanged native annotations match the pinned
releases. The locked comparison retains 22 provisional eligible cases and ten
uncertain cases. Offline serialization checks exclude reference/native channels
from actor and judge requests. Fourteen authored runtime tests pass.

This is AI-only technical verification, completed 2026-09-30 at
10:00:17 UTC. This agent authored reviewer A. Independently reconstructing joins,
hashes and arithmetic does **not** provide independent semantic adjudication or
qualified financial expertise. No financial model requests or outcomes were
examined, and this agent made no API calls or canonical-file edits.

The new receipt is
`outputs/finance-quantity-transfer-v1/preinference_validation.json`, SHA-256
`4bf25a8d486731d45f796972dbff4bf56af0fa29927d96785385707424a37323`.
It binds the reviewed data and 19 runtime source files. A later runtime change
requires a new review receipt rather than silently treating this snapshot as
verified.

A later metadata-only check verified the V1 inference freeze,
`3ad1042962889e9f7f92fe5e614a08ecbdbafc62890647dbffec044ac7090e6f`,
created at 09:59:50 UTC. Its 19 runtime entries exactly match this reviewed
snapshot. This receipt was written after that freeze; it is a technical
verification record, not prospective preregistration. No financial generation
contents were opened. The separately proposed V2 judge amendment is outside this
V1 code review and requires its own provenance and validation.

## Checks and provenance

The data checks independently reconstructed source joins and the A/B comparison
using standard-library code, without importing the preparation script's join or
comparison functions. There were 370 check groups covering 2,260 items. These are
engineering check counts, not independent observations or statistical evidence.

| Check | Verified result |
|---|---|
| Six row channels: packet, A, B, comparison, targets, experiment | Exactly 32 unique IDs, identical order |
| Cohort, reference-stage, joint and label-join freezes | Every linked hash matches |
| Receipt/output bindings | A/B outputs, targets, experiment and join freeze match |
| Recorded order | Cohort → reference protocol → reviews → joint lock → semantic comparison → join freeze → join receipt |
| Reference A | 28 primary expressions, 11 alternatives, 286 pointer checks |
| Reference B | 30 primary expressions, seven alternatives, 200 pointer checks |
| Primary literals | Every numerical magnitude has a declared binding |
| Combined candidates | Exactly 22: 11 FinQA and 11 TAT-QA; ten excluded retained |
| Complete original annotations and experiment construction | Exact equality for all 32 |

Primary numerical calculations were independently evaluated as exact rational
arithmetic and compared with stored 60-digit decimals at a relative bound of
`1e-55`, with the same absolute floor. Corpus programs were never executed.
Pointer checks establish that a cell/text location exists. Literal coverage and
arithmetic agreement do not establish the intended role, entity, year, operator
or denominator. Recorded timestamps establish internally recorded ordering,
not independent timestamp attestation.

The joint lock remains
`7ad42486e519d9d49a32c9e41ae71720647713193aea252db40780adbf45d984`.
The root's semantic comparison is separately disclosed and unchanged. Reviewer
B's RSG scale interpretation remains preserved; reviewer A's uncertainty prevents
that case from entering the primary set. Conditional numerical agreement was not
promoted. No selected question was replaced after review.

## Exact pinned-source joins

FinQA uses the original `dataset/test.json` QA object, not the distinct
`code/evaluate/test.json` representation. The verified revision is
[`0f16e2867befa6840783e58be38c9efb9229d742`](https://github.com/czyssrs/FinQA/tree/0f16e2867befa6840783e58be38c9efb9229d742).
All 16 selected original questions, `pre_text`/`table`/`post_text` fields, full
QA annotations and native `exe_ans` values agree exactly.

TAT-QA uses raw question/context packets and gold annotations at revision
[`870accc41953dcde885aabeb963d94aabdc0fbc3`](https://github.com/NExTplusplus/TAT-QA/tree/870accc41953dcde885aabeb963d94aabdc0fbc3).
The independent join hashes the exact table cells, ordered paragraph text and
question wording. It uses neither answers nor derivations. Across the entire
pinned inputs, 1,669 raw and 1,663 gold questions produce 1,626 unique exact joins;
43 raw and 37 gold questions are unmatched. Native question UID overlap is zero.
All 16 selected raw questions join uniquely to unchanged gold annotations.

The eight acquisition artifacts, including first-party notices/licenses, match
the existing ingestion manifest. This verification establishes release identity
and source preservation; it does not adjudicate label correctness, licensing of
underlying report text, or population-level benchmark defects.

## Runtime and label firewall

The latest fixed packet passes runtime validation without rewriting source
numbers: FinQA has 16 float labels; TAT-QA has 11 floats and five integer labels.
An earlier runtime rejection of these original scalar types was reproduced and
fixed by the runtime owner. The separate native scalar converter now uses
`Decimal(str(value))`, avoiding binary-float artifacts while preserving original
annotation files. The decimal-string requirement remains strict for actor output.

Offline checks covered 64 actor and 64 judge request shapes plus 32 metadata
canary cases, using authored placeholder candidate text. Actors receive only
original question/context. Judges additionally receive candidate text and parser
diagnostics; no native target, provisional reference, score, source ID or arm
name enters their serialized input. `client.answer` serializes this same body.
These checks verify construction, not delivery of future live requests.

The fixed provider catalogue agrees with the DeepSeek V3.2 SiliconFlow FP8 route,
prices and requested parameters. The runtime freeze binds that snapshot, shared
review IO, calculator, preparation/join code, protocol, tests and study modules.
Returned provider/model identities and observed billing must still be checked
after actual requests. The append-only billing ledger stops on unknown charges,
pending reservations or exceeded bounds; no automatic retry is implemented.

The authored endpoint controls preserve distinctions between reported value and
executed expression, relative percent and percentage points, monetary scales,
signs, tolerance boundaries, malformed JSON and unsupported expressions. A
malformed candidate forces an effective judge verdict of `unassessable`; its raw
judge violation is retained. Invalid top-level judge source pointers also fail.
The offline suite passed 14/14 with:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -p 'test_finance_quantity_transfer.py' -v
```

## Endpoint limits and interpretation

The primary outcome is a **typed numerical match to an AI-provisional reference**.
Safe execution is a second numerical endpoint. Neither checks currency identity,
entity/time grounding, operand roles or semantic equivalence. Matching the number
within `max(1e-8, 1e-4*abs(reference))` does not certify the requested quantity.

The native literal channel uses exact decimal equality with no unit, scale,
percent conversion or tolerance. For example, a native fractional rate and an
actor's percentage-point representation can disagree despite equivalent economic
meaning. Rounding also changes this equality. It reproduces neither official
FinQA program/execution scoring nor TAT-QA answer/scale EM/F1. Do not interpret
such disagreements as evaluator bugs or wrong source labels.

Authored controls explicitly confirmed that candidate evidence paths are not
resolved by the answer parser. The judge parser resolves its top-level evidence
paths but accepts empty evidence/operand lists and does not validate the semantic
content or subfield schema of operand-check objects. Thus `supported` is a
same-model judgment proxy, not machine-verified source grounding. A second call
to the same checkpoint can share actor or reference errors.

Baseline always precedes reminder, and each answer precedes its judge. Report
paired observed changes on this fixed cohort with that order limitation. One
checkpoint/provider, 22 provisional eligible questions and unknown TAT report/
company identities do not establish broad causal or population-level effects.
Keep all 32 questions and all 64 planned attempts visible, including the ten
uncertain cases and any incomplete execution. Human semantic adjudication and
live request/billing verification remain distinct later checks.
