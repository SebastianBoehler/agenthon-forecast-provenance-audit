## Executive summary (read this first)

Preserve the primary binomial convention `R = 1 + r`. Add a transparently post hoc
sensitivity allowing either that one-period convention or `R = exp(r)` with one
period. The question leaves compounding implicit. Freeze before 4B financial
responses and Coder binomial responses, after inspecting the DeepSeek discrepancy.

## Definition and motivation

DeepSeek answers one question with 3.06 using continuous compounding, while the
declared simple-rate reference gives `64/21`. The alternative is financially
coherent. A question that does not specify a compounding convention cannot justify
calling that difference an unequivocal financial reasoning error.

For binomial prompts only, independently compute both call prices. Accept a
parsed final number within the cent allowance of either price, with the existing
numerical guard. This is the union of two tolerance neighborhoods, not every
value between them. A continuous interpretation violating no-arbitrage is not
an admissible alternative. Other families are unchanged.

Apply this sensitivity to the complete 800 saved responses, separately for the
unchanged strict parser and the corrected exploratory numeric extractor. Finish,
format and unit failures remain failures. Do not require a keyword in the
reasoning: final-answer compatibility is distinct from trace certification.
Original source-grader decisions stay fixed; validity-dependent false-rejection
and false-acceptance counts are recalculated against the expanded reference.

Also check all 1,000 audited source binomial labels against both conventions.
The source generator's financing-debt formula is a separate mechanism diagnosis;
coincident final values do not certify that formula. The literal exponential-text
census remains descriptive and is not the gate for this sensitivity.

## Provenance and boundaries

`convention_sensitivity_freeze.json` records timing, observed ledger counts and
the new script/document hashes. The original protocol, source oracle, model
answers and primary/supplementary results are untouched. Independent high-precision
calculations validate both alternative prices and final decisions.

This is exploratory robustness under two plausible conventions, not a claim
that every possible interpretation is covered. Any model ranking remains specific
to the stated question panel, parser and reference convention.
