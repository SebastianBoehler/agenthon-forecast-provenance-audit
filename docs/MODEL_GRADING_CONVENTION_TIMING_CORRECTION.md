## Executive summary (read this first)

Correct the convention-sensitivity timing claim, without changing the acceptance
rule or any model response. Its first freeze precedes every 4B financial answer
but follows 64 Coder answers, including 14 binomial questions. Preserve that
original freeze and document the correction separately.

## What the record actually shows

`convention_sensitivity_freeze.json`, frozen at 19:03:05 UTC, records 64 Coder,
200 Qwen3 1.7B and 200 DeepSeek responses. The first 50 questions are constructed
Gordon, followed by binomial questions. The original document and freeze's
executive summary incorrectly say the freeze preceded Coder binomial responses.
The earlier ledger inspected when planning this analysis was in the Gordon family;
collection continued while the new script was written. That is not evidence that
the answers were absent at freeze.

The analysis is post hoc, motivated by DeepSeek's completed convention mismatch.
It precedes every 4B response. Neither status changes, nor is the original
three-model primary experiment retrospectively preregistered.

## Version-two record

`convention_sensitivity_freeze_v2.json` hashes the current driver, original
sensitivity definition and this correction. It retains the original freeze hash.
The original driver is saved in `convention-original/`. The added output fields
separate simple-only, continuous-only, both, neither parsed and unparsed answers;
they do not change the already specified two-neighborhood acceptance rule.
Original strict and numeric scores remain untouched. No answer is regenerated.
