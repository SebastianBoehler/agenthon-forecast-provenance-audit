## Executive summary (read this first)

This separate diagnostic adds exact evidence-pointer formats to the unchanged V1
quantity-judge prompt. It arose after V1 collection began, from two source-free
authored preflight failures: both judge responses used prose such as
`table: year 1 cost 120`, which the frozen location parser rejected. This is an
explicit amendment before selected V1 outcomes are inspected, not pristine
preregistration. Frozen V1 answers, judgments and primary endpoints stay intact.

The triggering authored run completed four calls for $0.000641655. Its two answers
strictly matched the authored reference; its two judges failed pointer parsing.
The amendment author inspected only that authored run and source code. Neither
the author nor the root agent has inspected selected financial outputs when this
plan is frozen; the latter is a session disclosure, not an access-control proof.

## Fixed delta and diagnostic scope

`finance_quantity_judge_v2.protocol.SYSTEM` is exactly V1 `JUDGE` plus one `FORMAT`
suffix. It gives these zero-based, original-context-relative pointer forms:

- FinQA and authored top-level table cells: `table[r][c]`.
- FinQA text: `pre_text[i]`, `post_text[i]`.
- TAT-QA nested table cells: `table.table[r][c]`.
- TAT-QA paragraph strings: `paragraphs[i].text`.

No financial semantics, judge rubric, output fields, parser, route, model,
sampling parameters or budget rule changes. The same loose `operand_checks`
object schema remains. Pointer existence does not certify semantic grounding.
The suffix requests whole-cell/paragraph pointers and forbids character indexing;
the unchanged V1 lookup parser does not itself enforce that stronger type rule.

V2 makes exactly 64 financial judge calls on the same 64 saved V1 answer texts,
including malformed candidates, using the original question/context. It makes
zero answer calls. Each malformed candidate retains the V1 parser flag and has
effective verdict `unassessable`, even if the judge violates the rule. No labels,
references, scores, case/source IDs or arm names enter judge prompts. Membership
uses all original case/arm pairs with no outcome filtering. Failed/invalid V2
judgments stay in the 64-attempt denominator and remain a same-model proxy.

Two separate paid authored V2 preflight judge calls reuse the two authored V1
answers. They assess pointer/schema transport, not financial task performance.
Their success or failure will be retained without tuning this frozen suffix.

## Accounting and timing

The shared ledger and `finance_quantity_transfer_v1` study ID remain unchanged:
all V1, V2 and authored calls count toward the same $2 study / $10 aggregate caps.
Call phase `judge_v2` creates distinct IDs and prevents overwriting/retrying V1
calls. The original client, conservative request reserve and strict durable
`usage.cost` settlement are reused. Unknown billing, pending reservation,
route mismatch or exhausted budget stops further calls. No retries/fallbacks.

The existing session authorization applies; only root executes paid commands.
All V2 outputs remain in ignored `outputs/finance-quantity-judge-v2/`. Before any
selected V1 outcomes are accessed, the plan freeze binds V2 code/protocol/tests,
unchanged V1 dependency hashes, the V1 experiment freeze, the authored trigger
records and Python runtime. Selected input bytes are bound in the V2 run receipt
after V1 finishes; their values are never used to change membership or this plan.

## Commands

Authored-only checks and the source-free freeze require zero model calls:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -p 'test_finance_quantity_judge_v2.py'
.venv/bin/python scripts/freeze_finance_quantity_judge_v2.py
```

After root review, the existing authorization permits two authored judges:

```bash
.venv/bin/python scripts/collect_finance_quantity_judge_v2.py authored-preflight --allow-paid-calls
```

After V1 completes, execute the unchanged diagnostic on all saved answers:

```bash
.venv/bin/python scripts/collect_finance_quantity_judge_v2.py collect --allow-paid-calls
```

Report V1 and V2 judge coverage/verdicts separately. An increase in parser coverage
would measure format compliance; it would not prove improved financial reasoning,
independent adjudication or a change in the primary answer-arm comparison.
