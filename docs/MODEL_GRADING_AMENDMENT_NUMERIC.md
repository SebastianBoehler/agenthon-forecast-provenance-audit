## Executive summary (read this first)

Add an explicitly exploratory numeric-final-line sensitivity analysis after
observing frequent unit-format failures. Preserve the frozen strict primary
endpoint, every original response, and the original 200-question denominator.
No response is regenerated. This amendment is not preregistered.

## Timing and reason

The original protocol was frozen at 2026-09-29 18:24:04 UTC. At 18:27:21 UTC,
the main-agent ledger inspection found 50 Qwen3 and 49 DeepSeek responses, still
in the constructed Gordon family. Earlier independent review of 28 local and
27 API responses had found final lines such as `Final: 16 <unit>` and `FINAL: 36`.
The original parser rejects these before numerical grading, even when a number
is stated as the final answer. No Qwen Coder study response had been collected.

The primary endpoint remains unchanged. A second analysis diagnoses the numerical
effect of released labels separately from the extra response-format requirement
we introduced. Its definition follows observation of output formats, so it must
be reported as exploratory even if later families and models were not yet seen.

## Added endpoint

Read only the last nonempty line, require exactly one case-insensitive `FINAL:`
marker in the response and exactly one numeric scalar. Permit an optional dollar
prefix, surrounding asterisks, and the suffixes currency, USD, dollar(s), percent,
%, or literal `<unit>`. A missing or placeholder unit is recorded explicitly.
Reject a unit explicitly inconsistent with the question's answer type. Do not
convert fractions into percentage points. Do not retrieve a number from the
reasoning, select among competing answers, or manually repair malformed outputs.
Unfinished responses and infrastructure failures remain failures.

Apply exactly the original frozen numerical comparator policies to the recovered
scalar, retaining units in the analysis record. This is numeric-only compatibility
with the visible question, not full response-contract compliance. Report strict
and numeric-only results together. The integer-plus-half-unit comparator has a
scientific interpretation only within constructed Gordon; do not present its
other-family or mixed-family aggregate as a meaningful baseline.

Freeze this amendment and its two analysis implementation files before running
their scoring. Record ledger counts and hashes at that freeze. Compare the results
against an independently implemented final-line parser and exact rational formulas.
No human review or original upstream reward execution is inferred.
