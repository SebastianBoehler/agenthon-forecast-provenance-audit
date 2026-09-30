## Executive summary (read this first)

The completed V2 pilot passes independent saved-output validation with a
disclosed reporting-only bookkeeping supplement. All 541 optimizer evaluations,
16 preflight responses and 432 holdout responses agree with the unchanged
independent parser and exact Fraction references. All 64 reflection prompts use
assigned-objective-only feedback. Every raw actor call is accounted for.

Neither source-objective arm improved its development reward. All four
optimizer arms selected the original seed strategy. The declared adaptation
consequence and repair gates are **false for both seeds**. This pilot does not
establish optimization-induced financial degradation or repair efficacy. The
same seed prompt was independently queried for each selected arm, so differences
among those holdout rows are response/provider variation, not learned-strategy
effects. The observed source-label grading errors remain directly measurable.

This is AI-assisted technical validation, not human annotation or expert
semantic adjudication. No additional inference, retries, model calls or changes
to frozen scientific code were performed during validation.

### Frozen-checker failure and reporting supplement

The frozen checker failed at its nonreflection-tag uniqueness assertion. It
expected 878 raw actor calls to have 878 distinct tags; there are 872 distinct
tags. Six training evaluation tags each occur twice. The saved minibatches also
contain both occurrences. No holdout or development question was duplicated.

The pinned GEPA0.1.1 [epoch sampler](../.venv/lib/python3.13/site-packages/gepa/strategies/batch_sampler.py)
pads the 32-case training set to a multiple of the minibatch size 3 using a
previously selected ID (lines46–55). Its last three-item batch can therefore
contain a repeated ID. The tag uses run, evaluation and case ID, so it cannot
uniquely distinguish those legitimate occurrences. The frozen checker also
collapsed them in an actor dictionary. This is an invalid checker assumption,
not evidence of duplicate source questions or omitted calls in the collector.

The authorized postflight supplement
[validate_finance_adaptation_occurrences.py](../scripts/validate_finance_adaptation_occurrences.py)
matches the full multiset of saved occurrences to raw calls by original tag,
exact request messages, exact response text and finish reason. It then gives
private in-memory copies unique API-index identifiers for the unchanged frozen
request, cost and feedback checks. Identical responses are exchangeable; no
unsaved occurrence index is inferred. All 878 actor calls match one-to-one.
No duplicate occurrence is removed from denominators or billing.

The independent parser, financial formulas, reward tolerances, rounding rules,
selection rule, primary results and raw ledgers are unchanged. Both frozen
validators remain byte-for-byte intact. The supplement produces a separate
[response_validation_occurrences.json](../outputs/finance-adaptation-review/response_validation_occurrences.json)
whose status explicitly reads `PASS_WITH_DISCLOSED_REPORTING_SUPPLEMENT`.
The original frozen checker continues to fail without that supplement.

### Completed holdouts and gates

All 432 holdouts parsed successfully. Each strategy has 48 fresh released-source
questions and 24 researcher-authored transfer questions. Transfer has no source
gold label; source acceptance there is undefined.

| Selected strategy/run | Source valid/48 | Source credits/48 | Transfer valid/24 |
| --- | ---: | ---: | ---: |
| Seed | 47 | 24 | 23 |
| Manual | 48 | 25 | 23 |
| Source0, seed retained | 47 | 24 | 23 |
| Source1, seed retained | 48 | 25 | 23 |
| Repaired0, seed retained | 47 | 24 | 21 |
| Repaired1, seed retained | 48 | 25 | 22 |

Recomputed consequence gates are `{0: false, 1: false}`. Recomputed repair
gates are `{0: false, 1: false}`. Primary aggregates, family counts and gates
agree with the independent calculations. Actual completed outputs are under
`outputs/finance-adaptation-v2`; V1 contains the interrupted attempt.

Across the repeated source panels, 285/288 answers are financially valid but
147/288 receive released-label credit. All 72 whole-Gordon responses are valid
integers and receive no source credit. All 72 source-binomial responses are
financially valid, with only 6 source credits from the one compatible zero-price
case per panel. The three remaining invalid source answers are WACC responses.
No financially invalid wrong-quantity answer receives source credit in these
holdouts. These are six repeated response panels over 48 questions, not 288
independent questions.

Across transfer, 135/144 responses are valid. The nine errors are binomial
answers; all other families pass. There are no whole-Gordon rounding violations.
Financial and repaired acceptance coincide on these realized holdouts, although
their comparator geometries are distinct by design. Passing-family source and
repaired rewards are identical on every saved response with source gold.

### Optimization, failure accounting and interpretation

| Arm | Metric rows | Actual actor calls | Reflection attempts | Overlong proposals | Best development reward |
| --- | ---: | ---: | ---: | ---: | ---: |
| Source0 | 125 | 107 | 16 | 6 | 17/32 |
| Source1 | 128 | 98 | 16 | 10 | 18/32 |
| Repaired0 | 128 | 101 | 16 | 9 | 30/32 |
| Repaired1 | 160 | 124 | 16 | 12 | 31/32 |

All best indices equal 0. Repaired 1's 1388-byte candidate ties the seed at 31/32;
the frozen first-maximum rule retains the 73-byte seed. All candidate development
evaluations use the same 32 questions, and saved per-case scores, assigned
feedback and selected strategies agree independently.

There are 37 overlong proposal batches, generating 111 retained three-case
placeholders without API calls. Their strategies range from 2005 to 4605 UTF-8
bytes against the 2000-byte cap. There are three actor read timeouts and one
reflection read timeout, with no retry. Their conservative unknown-billing
debits total $0.003331419 and remain charged. All 432 holdout calls finish normally.
The fixed compute ceilings are equal; actual actor compute is unequal.

The finite pilot has a strong explicit financial wrapper and a high-validity
seed baseline, little room for improvement, frequent overlong proposals, one
actor/provider, two optimizer seeds, and a narrow template/family sample.
Its failure to improve the assigned objective is an optimization limitation;
it is not evidence that defective rewards cannot harm learning. The intervention
also includes the repaired whole-integer feedback constraint and target values,
so even a successful contrast would not identify a numeric-label-only effect.
Repaired financial targets and AI-authored transfer templates have independent
math checks but no external human semantic review. No training or generalization
claim follows from this completed feasibility pilot.

### Timeline, cost and preservation

V1 froze at 2026-09-29T20:33:58.526883+00:00 and failed before holdouts, retaining
459 API calls, 63 reflection calls and $0.089236560 in accounted cost. Its 34
original frozen files, partial ledgers, two surviving result files and failure
metadata are unchanged. The three completed actor calls without saved V1
evaluation rows remain preserved and billed.

V2 froze prospectively at 2026-09-29T21:28:24.489599+00:00. Its first egress-slot
entry is 21:28:30.911126 UTC. Optimizer egress ends 22:08:11.851176 UTC;
holdout egress begins 22:08:11.859013 UTC, after all selected strategies were
saved by the frozen runner. The final egress-slot exit is 22:35:08.442698 UTC.
All requests precede the original 23:33:58.526883 UTC cutoff. Recorded egress
slots bound actual HTTP operations and have a verified peak overlap of 4;
they do not measure exact wire transmission times.

V2's 942 calls comprise 16 preflight, 430 optimizer actor, 64 reflection and 432
holdout calls. Their accounted costs are respectively $0.001949220,
$0.066855796, $0.036953833 and $0.057054312. V2 totals $0.162813161;
both attempts total $0.252049721 under the cumulative $0.90 cap. Unknown billing
uses reserved worst-case cost, so these totals are accounted costs.

All 65 V2 frozen-file hashes and 81 installed GEPA source hashes match. The
original 600 independent-result checkpoint remains
`51c753e90ce0bff459c88d4580275eb847b1dab5f73ee088ff1696ceafa5712a`.
The original 800-answer study and its selection remain separate from this pilot.

### Reproduction and result identities

Run from the research repository, with its pinned GEPA0.1.1 environment:

```bash
.venv/bin/python scripts/validate_finance_adaptation_occurrences.py
```

The complete result retains the occurrence matches, per-family outcomes,
development trajectories, gates, API usage and freeze evidence. No primary
oracle, parser or reward function is imported. SHA256 at this completed review:

| Artifact | SHA256 |
| --- | --- |
| New reporting supplement | `234248af068261c1b7dd8c3abe1c7c4a3c8f67c0802cee3cc5e428169e7ebb7c` |
| Independent complete result | `a25c30fe18dea420e18163407a2de6e651076e58de6773cfb047c2458f661d5f` |
| V2 prospective freeze | `47832ac0ccc4540b4820b914890104b10edfe5dfb9520daa72ef6227ed47c1f2` |
| V2 raw API ledger | `d8eb659fc733384cc581fc223a44afd67d9306a76dd36688ea39bfde15fe554f` |
| V2 raw holdouts | `8733f50323a21245dfa5c9bfc82d4b311126d4f427c722e04282258f4acf064d` |
| Primary V2 result | `a597add5b288a9d376e15c9f3fd883895edf573abffbff59c8f498b1e44d5fee` |

Clean extracted-bundle replay is a separate pending verification. No portability
claim is made by the local saved-output checks alone.
