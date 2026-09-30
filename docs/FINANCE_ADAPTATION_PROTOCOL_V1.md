## Executive summary (read this first)

This prospective experiment compares prompt adaptation to released financial
targets with adaptation to independently calculated financial targets. It tests
financial correctness after changing prompts, not model-weight training or
investment performance. The unchanged earlier 200-question study is excluded.
No inference may begin until independent mathematical/specification review passes
and a freeze manifest hashes the complete protocol, data, runner, dependencies
and current provider-price snapshot. The preparation manifest alone is not a freeze.

## Questions, partitions and provenance

Use the pinned public Cosimo CFA Level I release recorded in
`answer_contract.sources.SOURCES['cosimo']`. Admit only `cr_eq_gordon`,
`deriv_binomial_call`, `eq_gordon` and `corp_wacc`. The latter two are passing
controls. Existing discoveries and family choice are exploratory; this protocol
prospectively freezes adaptation and evaluation rules.

Per family, select eight training, eight development and twelve source-test
questions: 32/32/48 source questions total. Exclude all exact prompts and canonical
operand tuples in the previous study before selection. Deduplicate prompts and
operand tuples globally across new partitions, including across the two Gordon
families. Canonical values remove insignificant zero padding. Rank by SHA256 of
`finance-adaptation-v1-20260929` plus the original question, then case ID. Assign
the first eight eligible questions to training, next eight to development and
next twelve to source test. Never select by discrepancy, actor success or score.
Use the next four eligible questions per family as 16 frozen off-split format
checks. They are disjoint from the earlier study and every experimental partition.
Deduplicate source prompts first, keeping the smallest case ID, and record any
duplicate-prompt released-label conflicts in the preparation manifest.

Source partitions retain the original question and released numeric target in
`source_gold`. No actor receives the case ID, family, source identity, target,
metadata or formula. The question is combined with the same fixed instructions
and format wrapper for every condition.

The transfer test has 24 researcher-authored questions: three new wording
templates per family, two new operand tuples per template. Transfer operands must
be absent from the entire four-family source release, the earlier study and all
new partitions. Wording changes preserve the financial calculation while asking
for the quantity through three distinct presentations. These questions are
limited financial-calculation transfer tests, not expert-authored professional
scenarios or an independently sourced financial benchmark.

Transfer rows omit `source_gold` entirely. Their only target is a financial answer
computed from their authored inputs. No source reward can be calculated for
transfer; principal transfer comparisons use financial validity exclusively.
Binomial transfer text explicitly states an effective single-period rate and no
dividends. Gordon text states that D0 was already paid and asks for the current
ex-dividend share value. Constructed Gordon requests a whole currency unit;
ordinary Gordon and binomial request 0.01 currency. WACC uses market-value weights,
deductible debt interest and percentage points to 0.01.

## Financial semantics and scoring

Every input is treated exactly as displayed. The fixed instruction wrapper
prospectively interprets every quoted one-period binomial rate as an effective
rate for that period, with gross factor `1+r`. This disambiguates the original
source wording without changing its bytes. It is a new explicit task assumption;
the old model study and its post hoc convention sensitivity remain unchanged.
The same wrapper assumes no dividends during the binomial period in every partition.

Reuse existing independent `answer_contract` mathematics at 50-digit Decimal
precision. Binomial call prices must agree between discounted risk-neutral
payoffs and replication. Gordon uses the next dividend, `D0*(1+g)`.
WACC is the market-weighted equity cost plus debt cost after the interest tax
shield. These definitions are independently reviewed before the first answer.

For whole-unit Gordon, accept exactly the nearest integer. At exact half ties,
either adjacent integer is admissible because no tie-breaking rule is supplied.
Every other family accepts a numerical error at most 0.005 in its declared unit,
with the existing `1e-20` arithmetic guard. Monetary values use `currency`;
WACC uses percentage points with unit `percent`. `grade_numeric` uses the frozen
admissible values or intervals, never a transfer source label.

The same strict `model_grading.protocol.parse_final` extractor applies to both
objectives. One marker must occur on the final nonempty line, in the declared
unit. Malformed, truncated, refused and failed responses stay in denominators;
no retry, post hoc numeric recovery or manual answer replacement is allowed.
The released-target objective is a reconstructed cent comparator, absolute error
at most 0.005 from `source_gold`. It is not an executable upstream reward.
The repaired adaptation objective uses the same 0.005 absolute comparator around
`repaired_objective_targets`. For defective binomial labels, serialize the
independently computed call price to cents. For whole-unit Gordon, use the requested
integer, including both integers at exact ties, and additionally require an
exact integer-valued answer for that family. For passing ordinary Gordon and
WACC, preserve `source_gold` as the repaired objective target and assert its
independent validity. Thus passing-family reward geometry is identical across
objectives. This serialized-target adaptation reward is distinct from the
formula-centered financial-validity oracle and its strict whole-integer rule.

## Prompt adaptation and leakage controls

Keep the actor, provider route, decoding and fixed wrapper identical across
conditions. The wrapper requires literal numeric units and a final line such as
`FINAL: 12.3456 currency` or `FINAL: 7.2500 percent`, with no Markdown or trailing
text. A concise calculation may precede it. Only the strategy instruction is
optimized; the parser, financial oracle, question and wrapper are immutable.

Use official GEPA 0.1.1, caching disabled, with optimizer seeds 0 and 1 per objective and a maximum of 256
metric evaluations per run, including training and development evaluations.
Record actual evaluation and reflection counts; 256 is not a reflection cap.
Keep the same seed prompt and compare with a frozen manual financial instruction.
Optimizer seeds control optimizer sampling, not immutable API-model randomness.
The actor uses temperature 0 and at most 512 output tokens. Reflection uses the
same provider at temperature 0.7 and at most 1,536 output tokens. Limit each run to
16 reflection calls and 40 optimizer iterations. Require a proposed strategy at
most 2,000 UTF-8 bytes; malformed or oversized candidates fail without actor calls.
Check available evaluation budget before a possible 3+3+32 evaluation batch. Select
the best candidate by its assigned score on the entire 32-question development
set, retaining the library's first-occurrence tie rule. Only full development
evaluations describe comparable optimization trajectories; minibatch rewards are
not the corresponding causal endpoint.

For released-target adaptation, reflection sees the raw question, generated
response, released target, assigned boolean reward, 0.005 tolerance and parse error. It never sees
the independent formula, financial target, correctness decision, defect annotation
or source metadata. For repaired adaptation, reflection sees the independently
calculated target and any permissible adjacent integer at a half tie. Saved
ledgers may contain both scores; unassigned scores are never fed to the optimizer.
Development chooses candidates under the assigned objective. Both test sets
remain inaccessible until candidate selection is complete.
Reflection records use only `Inputs`, `Generated Outputs` and `Feedback`, where
feedback contains `reward`, `target_values`, `absolute_tolerance` and
`integer_required`, plus `format_error`. Source feedback has its one released target; repaired feedback
has the serialized corrected target list. No independent-oracle fields enter
source-objective reflection.

## Freeze and execution gates

Prepare JSONLs and a manifest with status `prepared_unfrozen_pending_independent_review`.
Independent review must inspect operand extraction, exact-input semantics,
financial targets, half ties, transfer wording and global disjointness. Correct
errors before freezing; preserve old study freezes and outputs. After review,
freeze the complete new implementation and protocol, five question JSONLs, dependencies,
review report and a fresh price snapshot. Refuse modified frozen inputs.

The runner must enforce a shared $0.90 ceiling for this new experiment, including
health, optimization, baseline and test calls across actor and reflection. This
keeps the known previous study cost of about $0.028 plus this experiment below
the existing $1 cap. Use conservative input accounting and output-token limits. Record actual
provider usage and costs. No silent model/provider substitution is permitted.
The frozen run configuration must contain these financial limits before health
answers. Measure elapsed time and stop the optional pilot at three hours.

Require at least 15 of 16 off-split format checks to parse before optimization.
They cannot overlap any study prompt or operand tuple. If the gate fails, stop.
No selected financial answer may be generated before the freeze. Do not interpret
a formatting-only effect as a financial-reasoning consequence.

## Endpoints and interpretation

Report every attempt, strict parsing, financial validity and released-label
acceptance on source partitions. Transfer reports financial validity only.
Separate the 48 source-template numerical holdout from the 24 new-wording test.
Report errors involving the wrong financial quantity, integer rounding and passing
controls, with saved output evidence rather than reasoning-keyword gates.

An adaptation-consequence claim requires increasing source reward alongside
worsening financial validity on both holdouts in both source-objective seeds.
Concretely, each source run must improve its full-development assigned score,
increase released credits on the 48-question source test relative to the seed
prompt, and reduce financial validity relative to that prompt on both tests.
Repair must improve transfer validity relative to released-target adaptation
without harming either passing family relative to the seed prompt on either test.
Each repaired run is compared with its corresponding source-objective seed.
These finite pilot gates are decision
rules, not population-level significance tests. If assigned reward never improves,
the optimizer test is inconclusive. Preserve null and opposite-direction effects.

The manual baseline may match optimized repaired prompting. That would support
the importance of the objective rather than an optimizer-specific advance.
Shared templates and one actor/provider limit external validity. No new-method,
weight-training degradation, general verifier accuracy, investor-loss or broad
financial benchmark claim follows from this pilot alone.
