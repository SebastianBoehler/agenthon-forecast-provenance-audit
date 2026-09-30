## Executive summary (read this first)

This prospective transfer study has 32 fixed questions, two fixed answer arms and
one label-free quantity judge for each arm/question. A complete run contains
exactly 64 answer calls and 64 judge calls. Malformed answers still reach the judge,
with an explicit requirement to return `unassessable`. The existing session
authorization permits up to $10 total; the study remains capped at $2. After
locked references, semantic approval, authored preflight and code checks,
collection proceeds within that authorization. A freeze records the gate.

The model and judge both use DeepSeek V3.2 on the fixed SiliconFlow FP8 route through
OpenRouter. This shared-model judge is a diagnostic proxy, not an independent
oracle or qualified human assessment. The provisional references are AI technical
readings. Their eligible subset must retain that qualification.

## Fixed comparison and measurement

`protocol.py` fixes model, provider, prices, temperature zero, nonthinking mode and
1,024 output tokens. Baseline and quantity reminder share exactly the same JSON
fields, typed units, scales and pure numerical arithmetic grammar. Their only
intended difference is the label-free quantity/entity/year/denominator/sign/unit
reminder. Context is evidence data, never instructions.

Each packet row has `case_id`, `source`, `question`, `original_context`,
`provisional_reference={eligible,value,unit,scale,calculation}`, and optionally
`native_target={value}`. IDs are distinct and membership is fixed before calls.
Neither reference nor native target enters either model prompt. The judge receives
the original context, raw candidate answer and parser-validity flag, with no arm
name, reference or score. Currency identity is outside this endpoint: the typed
unit and scale checks do not certify which dollar currency was intended.

Strict validity requires the exact JSON schema, finite decimal-string numeric
value, a recognized typed unit and scale, and an executable whole-string numeric
calculation. Abstention and Boolean answers require empty calculations. A Boolean
answer has `yes`/`no`, unit `boolean`, scale `none`; it is retained in attempts but
does not receive numerical credit. Rates, ratios and durations require scale
`none`. Monetary/count scales are single multipliers, never squared.

The primary reported-value endpoint compares only AI-provisional eligible cases,
with exact typed-unit equality after declared scale normalization. Its tolerance
is `max(1e-8, 1e-4*abs(reference))` in the normalized base unit. An independent
expression endpoint evaluates the saved arithmetic with the same typed-unit and
tolerance rules. Reported/expression consistency is a third diagnostic; none
certifies quantity grounding. The separate native channel compares the literal
numeric value with `Decimal(str(native_value))` equality, preserving the original
JSON scalar separately, without scaling, percent adaptation,
tolerance or semantic certification. It is not a reproduction of native evaluators.

All 64 answer and all 64 judge attempts remain planned denominators. Eligibility,
strict answer coverage, numerical matches and judge verdicts are separate counts.
Abstentions and parser failures receive no numerical credit. A malformed answer
has effective judge verdict `unassessable` even if the judge violates that rule;
the original judge response and violation remain saved. Invalid judge schema or
source pointers also give `unassessable`, never selective removal. Pointer checks
verify location existence; the loose operand-check objects do not mechanically
certify role binding or semantic grounding.

## Budget, errors and provenance

The study cap is **$2** and the shared follow-up ledger cap is **$10**, with initial
actual spend **$0**. Paid authored preflight calls use the same study and aggregate
ledger. Each call reserves its entire UTF-8-encoded request byte count plus 256
framing tokens at the fixed maximum prompt price, and the full maximum output at
the fixed completion price. This byte/framing/output bound must fit the pinned
163,840-token context limit. It is a conservative tokenizer heuristic, not a
provider tokenizer proof; `usage.cost` is the authoritative observed total.

The append-only ledger is process-locked and flushed to disk. A returned response
is saved before billing settlement. Strict `usage.cost`, including cost from a
raw response whose choice parsing failed, is persisted before any subsequent
call. Missing, negative, nonfinite or invalid cost stops all further calls. A
pending reservation also blocks continuation after interruption. An observed
cost above the reserve/cap stops the run and remains recorded. There are no
retries, provider fallbacks, alternative models or assumed-free transport errors.

Every call preserves request hash/body, case/arm/phase, target and returned model
and provider, completion/error metadata, raw response and candidate text. API keys
are never written in request headers; matching secret strings and credential keys
are redacted if echoed in a response. Run status retains unstarted/attempted/
recorded answer and judge states for the complete planned panel. A stop means an
incomplete execution, not a completed 64-judge result. Interrupted runs require
explicit reconciliation and are not automatically resumed or retried.

## Commands and freeze boundary

Authored-only local checks require no source packet, API credentials or model calls:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -p 'test_finance_quantity_transfer.py'
.venv/bin/python scripts/collect_finance_quantity_transfer.py preflight
```

After code review and joint-reference/semantic approval, freeze the real paths:

```bash
.venv/bin/python scripts/freeze_finance_quantity_transfer.py \
  --packet outputs/finance-quantity-transfer-v1/experiment_packet.jsonl \
  --reference-lock <locked-reference-record> \
  --comparison <locked-semantic-comparison> \
  --semantic-approval <approved-label-join-record> \
  --output outputs/finance-quantity-transfer-v1/experiment_freeze.json
```

The freeze binds packet, joint reference lock, semantic comparison/approval, all
study modules/scripts, shared review I/O and join dependencies, safe calculator,
provider catalogue, review/join receipts, this protocol, authored tests and Python
runtime. Collection verifies those identities before reading financial cases.
Authored paid preflight is separately available through `preflight --allow-paid-calls`
and uses existing session authorization; its four calls are never financial
transfer observations. No paid command was run while preparing this infrastructure.

The affirmative paid-call flag records existing session authorization:

```bash
.venv/bin/python scripts/collect_finance_quantity_transfer.py collect \
  --packet outputs/finance-quantity-transfer-v1/experiment_packet.jsonl \
  --freeze outputs/finance-quantity-transfer-v1/experiment_freeze.json \
  --allow-paid-calls
```

Case packets, raw calls, target channels and scoring outputs remain local under
ignored `outputs/`. Report paired counts and disagreements on the fixed panel;
do not claim expert adjudication, an independent judge, causal training effects,
representative financial benchmark prevalence or cross-model generalization.
