## Executive summary (read this first)

Frozen on 2026-09-29 before the expanded audit and comparator experiment. The selected
paper is **Verified Against What? Auditing Visible-Question Contracts in Financial
Reasoning Supervision**. The contribution is a reproducible external empirical audit
of released supervision, measured comparator trade-offs, and validated corrections.
Precision validation itself is established prior art, including FinChain Appendix A.3.
No experiment here estimates the effect of reinforcement learning or model training.

## Research design and discovery boundary

The two prior pilots examined 2,655 ordinary RLVR DCF rows and 1,000 Cosimo
constructed-response Gordon rows. Their counts were known before this freeze.
The first example from Cosimo's binomial family also revealed a likely bond-as-call
error. These are discovery analyses, not preregistered confirmation.
The expanded sample includes ten named families from the pinned CFA Level I split:
`cr_eq_gordon`, `eq_gordon`, `deriv_binomial_call`, `tvm_annuity_fv`,
`v_tvm_annuity_fv`, `corp_wacc`, `m_corp_wacc`, `port_capm`, `tvm_pv_lump`,
`tvm_eay`. All rows in these families are included; parser failures are fatal.
Selection reflects independent formula coverage, tractability, and the discovered
mechanisms. It is not random sampling of finance releases. Report every family,
including clean and surprising results. Count unique visible questions separately.

## Sources and units

Use RLVR revision `6cfa9a71e777026ba7242fbbb96c11c7dece5011` and Cosimo revision
`42244d29c6b9912683213a08d1a9c5b0373b381b`. Verify the existing local SHA256 hashes
before loading. Both dataset cards declare MIT licenses. Public data stay in this
dedicated research repository, never competition repositories. Source IDs and hashes
link each derived row to its release. Source code is inspected as text/AST; no upstream
code is executed. This audit is independent of the generators' self-verification.

## Answer contracts and calculations

Recompute formula values using Decimal arithmetic with 50-digit precision. For
binomial calls, compare risk-neutral expectation with replicating-portfolio valuation.
Check no-arbitrage bounds and parameter restrictions. For present/future values,
compare closed forms with independent discounted/accumulated cash-flow sums in review.
For requested whole-unit Gordon answers, use nearest integer. Report ties explicitly;
do not classify half-tie convention disagreements as defects. The source's cent labels
are tested within 0.005 unit plus 1e-20 numerical guard. A source serialization at two
decimals does not imply that the prompt demanded exactly two-decimal output.

RLVR DCF has two separately reported interpretations. With displayed inputs exact,
the target is FCF/(r-g). With rates rounded to the nearest 0.1 percentage point,
propagate their ±0.05 percentage-point intervals and check gold feasibility. This
second analysis diagnoses nonidentification; interval membership does not certify
an individual exact answer. Never silently replace ambiguity with a broad reward.

## Comparator experiment and controls

Evaluate original-label numeric equality, absolute tolerances 1e-4, 0.005, 0.5, 1,
and relative tolerances 0.1%, 1%, 5%. These are reconstructed comparator conditions,
not observed deployed rewards. RLVR's 1e-4 condition reproduces its card specification
analytically. FinChain's 5% comparator informs a sensitivity condition, but is not
claimed to grade these datasets. Test source gold, prompt-faithful formula/rounded
answers, source-authored chosen/rejected answers, and one targeted wrong-formula
candidate per row. Preserve numerator/denominator counts; exclude answer-colliding
wrong-formula candidates from false-accept denominators and report their count.

Repairs: (i) re-evaluate visible exact inputs, (ii) apply explicitly requested output
rounding, (iii) compose both. Ablate the rounding step and compare against tolerance
widening. Validate on source-authored rejected answers as an independent error control
in addition to constructed mutations. Report legitimate rejected answers and pairs
where neither side is correct; do not automatically flip such pairs. For multiple
choice, analyze numerical answer validity; option-letter repair is outside scope.
Preference results describe released supervision, not downstream learning effects.

## Uncertainty, validation, and falsifiers

This is a finite census of selected families. Report exact counts, deduplicated counts,
and family-level outcomes. Do not attach IID confidence intervals to synthetic rows
or infer field prevalence from two sources. An independent reviewer will inspect
deterministically sampled examples and the formulas; record review as AI-assisted
technical validation, not human expert annotation or inter-rater reliability.
Compare identities and source formulas rather than merely retesting the same code.
If tolerance widening already solves validity without error acceptance, say so.
If the repair accepts source mistakes or disagrees with independent identities,
repair it before making the reliability claim. If all consequential findings disappear,
retain the negative study and withdraw the positive headline.

## Artifact and submission boundaries

Persist the protocol hash, input hashes, implementation hashes, runtime versions,
row-level results, aggregate results, figure metadata, commands and review responses.
Record changed claims and failed paths in a dated evolution log. This follows the
agent-native research artifact practice, not a claim of methodological priority.
No paid compute, external submission, organizer email or public release is authorized.
The live CFP was checked 2026-09-29: deadline 2026-10-01 13:59 Europe/Berlin;
accepted papers require an in-person poster presenter in Atlanta on December 12.
