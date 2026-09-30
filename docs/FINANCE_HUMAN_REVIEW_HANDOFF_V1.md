## Executive summary (read this first)

The local handoff contains all 32 unused-group questions for a qualified financial
reviewer. It omits AI reference answers, source labels, generated candidates,
intervention names and scores. No reviewer has been recruited or contacted and no
human annotations have been completed. This preparation closes a practical step;
it does not close the paper's expert-adjudication gap.

## Handoff and independence

Provide only `outputs/finance-human-review-v1/question_only_packet.jsonl`, the
blank review form and this instruction sheet. Keep the private case map and all
AI/reference/model files away from the reviewer. Context may reveal source
lineage; salted IDs do not guarantee freedom from benchmark familiarity or
pretraining exposure. The preparer has prior case exposure, disclosed in the
preparation receipt. A fresh reviewer must record relevant financial expertise,
prior exposure to these questions, tools used and actual start/end times.

Review all 32 questions, including missing or ambiguous ones, before seeing any
answer comparison. Do not restrict review to successful or disagreeing outputs.
Retain the completed original review and hash-lock it before unblinding. A second
reviewer or later adjudication should be recorded separately rather than editing
the original record to obtain agreement.

## What the reviewer records

For each `review_id`, interpret the original question and context:

1. Record the requested quantity, entity, year/period and denominator. State
   whether the source permits one determinate answer, an answer conditional on
   explicit assumptions, multiple defensible interpretations, or insufficient
   information. Use `determinate`, `conditional`, `ambiguous` or `insufficient`.
2. For a determinate numerical reading, give a decimal-string value, complete
   arithmetic expression, typed unit and declared scale. Units include currency,
   currency per share, percent, percentage points, ratio, count and duration;
   do not silently treat these as interchangeable. Record currency identity where
   supplied. Keep relative change separate from a percentage-point difference.
3. Bind each operand to a zero-based cell/paragraph pointer and explain its role.
   FinQA contexts use `table[r][c]`, `pre_text[i]`, `post_text[i]`; TAT-QA contexts
   use `table.table[r][c]` or `paragraphs[i].text`. Record sign conventions,
   gross/net choices, missing scale and approximate displayed inputs explicitly.
4. Preserve uncertainty and competing calculations. Do not infer an intended
   result from a plausible numerical match or an unseen official answer.

The review form is a blank handoff, not synthetic annotations. Human-versus-AI
agreement must be assessed after its lock using a separately documented rule;
neither an agreement rate nor financial correctness is predetermined here.

## Local preparation

Run once from the research repository:

```bash
.venv/bin/python scripts/prepare_finance_human_review.py
```

The script verifies the existing question-only packet's cohort commitment, retains
exactly all 32 cases and writes a separate packet, private map, blank form and
hash receipt. Full financial-report contexts remain local; they are not added to
the portable numerical-review ZIP. Contacting or sending materials to a reviewer
requires the author's explicit instruction.
