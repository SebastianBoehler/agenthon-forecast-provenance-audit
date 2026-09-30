## Executive summary (read this first)

A convention sensitivity is scientifically appropriate because the binomial prompts
quote a risk-free rate without explicitly naming its compounding convention. Keep
the frozen `1 + r` primary reference. In an explicitly post hoc analysis, admit
prices consistent with either a simple effective one-period rate or a continuously
compounded one-period rate. Compare unchanged saved numeric answers under both
references; do not regenerate answers or condition acceptance on reasoning keywords.

The broader numerical answer set improves fairness of the checkpoint comparison,
but remains a declared two-convention sensitivity. It neither establishes that all
other interpretations are invalid nor certifies the reasoning trace. The source's
debt-as-call computation is a separate mechanism; measure its robust mismatch count
against both conventions rather than assuming the original 975 count is unchanged.

## Admissible financial prices

For the existing one-period setup, use the original effective-rate gross return
`R_simple = 1 + r` and the alternative continuous-rate gross return
`R_continuous = exp(r)` with period length one. Independently calculate the call
under each gross return using risk-neutral discounted payoff and portfolio
replication. A branch requires `d < R < u`; an infeasible branch must not enlarge
the admissible set.

Accept the union of the two existing cent-serialization neighborhoods around the
unrounded high-precision prices. This is two price neighborhoods, not every price
between the two answers. Do not round an oracle to cents and then add another
half-cent allowance; that changes the numerical boundary twice. Retain the original
high-precision arithmetic guard consistently if one is used in the frozen reference.

Independent high-precision validation matters for the continuous branch because
the exponential cannot be checked by an exact rational calculation alone. Check
the exponential with a separately implemented high-precision path and the two
financial identities. The identities share the compounding convention, so their
agreement alone cannot prove which interpretation the source question intended.

This review interprets “no text-marker prerequisite” as no requirement that the
reasoning contain `exp`, `e^` or “continuous” before a final numeric price may meet
the alternative reference. Keep completed-response handling and the existing
final-line extraction fixed. The literal-marker census remains descriptive; a
keyword does not prove a consistent calculation, and its absence does not prove
simple compounding. If extraction itself is changed, that needs a separately
specified sensitivity rather than being hidden inside the convention analysis.

## What changes, and what remains fixed

The model response, extracted value and source-policy decision remain fixed.
Only reference admissibility expands. Therefore recalculate both the validity
classification and reference-relative false-rejection/false-acceptance counts.
An answer newly valid under continuous compounding must not remain in an invalid
error pool. Save branch membership as simple only, continuous only, both or neither.

Other model-panel families retain their original numerical references. Apply the
same two-convention rule to every eligible binomial prompt and every model, without
choosing a preferred convention per model. The raw question gives eligibility;
the model's prose or performance does not.

Score all 1,000 audited source binomial labels under both conventions, including
the 25 numerical coincidences under the original reference. Report membership
counts and the “neither convention” source-conflict count. Keep the exact original
`1 + r` count identifiable. A numerical coincidence does not repair the generator's
wrong-quantity formula, and a generator-level diagnosis does not prove every
individual serialized label is numerically wrong under every convention.

For model outputs, compare the expanded reference with the already fixed numeric
extractor. This isolates convention sensitivity from recovery of missing units.
If strict extraction is also scored under the union, identify it as a separate
post hoc condition. Do not compare strict/simple and recovered/union scores as
though their difference came only from compounding.

## Timing and inference boundary

This review initially assessed the planning claim that the freeze would precede
Coder binomial responses. The recorded first freeze at 19:03:05 UTC instead
followed 64 Coder answers, including 14 binomial answers, plus completed Qwen3-1.7B
and DeepSeek runs. It preceded every 4B financial response. The
[timing correction](MODEL_GRADING_CONVENTION_TIMING_CORRECTION.md) explains that
collection continued during script preparation; the
[original freeze](../outputs/model-grading-v1/convention_sensitivity_freeze.json)
and its incorrect summary remain preserved. The version-two record at 19:04:31
UTC follows 71 Coder responses and documents the correction without changing the
acceptance rule.

The sensitivity is post hoc for the observed original-model outputs. Its rule was
fixed before the 4B outputs, but that does not make the complete comparison an
initially preregistered experiment. Preserve the primary freeze, extraction
amendment, size-extension freeze and convention amendment as distinct events.
Do not describe the convention analysis as preceding all Coder binomial answers.

Report fixed-set outcomes without population confidence claims. A within-Qwen3
ordering may depend on how ambiguous rates are interpreted. Show that dependence
rather than treating the original simple-reference ranking as universal financial
correctness. The source-grading consequence can be robust even when a model's
reference-validity count is convention-sensitive.

## Suggested manuscript prose

Methods:

> The binomial primary reference interprets the quoted risk-free rate as an
> effective one-period return, with gross return `1 + r`. Because the original
> questions do not explicitly specify compounding, we add a post hoc sensitivity
> accepting prices under either this convention or continuous one-period
> compounding. We retain the stored answers, extractor and source comparators;
> only the admissible financial price set changes. We apply the rule equally to
> all models and audited source labels, without requiring a reasoning keyword.

Results, after execution:

> Some apparent disagreements with the primary reference reflect an unspecified
> compounding convention. We therefore distinguish primary-reference agreement
> from agreement with either declared convention. The source-label grading
> comparison uses the same model outputs under each reference; its counts are
> reported separately from strict formatting failures.

Use actual branch counts and the robust source-conflict count after scoring. If
the broadened reference rescues an answer, call it convention-compatible, not
“correct reasoning recovered.” If the answer satisfies neither convention, call
it disagreement with both tested references; the experiment still does not audit
every possible derivation or interpretation. Do not silently substitute union
counts for the original frozen primary numbers in the abstract.

No new diagram, model generation, manuscript edit or separate PDF compilation was
performed for this review.
