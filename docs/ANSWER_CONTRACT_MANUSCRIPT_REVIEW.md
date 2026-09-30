## Executive summary (read this first)

The manuscript supports a **bounded empirical data-quality paper**, with substantial
new corpus-specific evidence and modest methodological novelty. Its main counts,
two valuation identities, preference interpretation and passing-family comparisons
agree with the reviewed outputs. It correctly avoids claiming preference reversal,
upstream reward loss, trained-model degradation, or a new validation principle.

Three clarifications should be completed before treating the draft as final:
make rounded-input nonidentification explicitly conditional; identify full-contract
zero acceptance as reference-oracle consistency rather than measured general
validator performance; and give accurate complete bibliography entries. The main
author reported these revisions in progress during review. They do not require a
new experiment campaign or abandoning the topic.

## Scope and reviewed artifacts

This review inspected `paper/answer_contract_audit.tex`, the primary
`outputs/answer-contract-v1/results.json`, the independent rational-arithmetic
validation report, the protocol and amendments, and the relevant formula,
comparison and patch code. It also inspected the cached public Cosimo generator,
wrapper and verification harness. No manuscript or implementation was edited by
this reviewer. The review did not compile or export the paper; those checks belong
to the main drafting task.

Primary literature was checked against the earlier full-text reassessment. The
official *Fair and cheap* page was rechecked live for full title and authors. Its
full manuscript remains reader-gated. No quotation from its inaccessible text is
present in the reviewed draft.

At the numerical cross-check, the results SHA256 was
`d44c2cfca0609b70d44f6499f1d2269a851ab064c1e86b19ea20a4f32828067c`.
The manuscript SHA256 was
`9721f02b6df35d410a4c79b8929b6a6398a31d8904e95f5623d2aa28cd9ba9f6`.
Further drafting revisions may legitimately change the latter.

## Actionable findings

### P1: Separate source-supported rendering from question-declared semantics

The abstract says rounding feasibility establishes nonidentification. Section 3,
however, defines intervals for explicitly rounded inputs, while the audited source
questions do not explicitly declare rounded-input semantics. Source code shows why
a generator's hidden operands can differ; it does not make that convention visible
to the learner. Both interpretations must remain explicit:

- If displayed operands are exact, the computed visible-input target is identified
  and conflicting labels fail that contract.
- If displayed operands are rounded, hidden-label feasibility and multiple
  admissible output values imply conditional nonidentification.

Suggested abstract phrasing: “Under a rounded-input interpretation, discrepant
RLVR and CAPM labels remain feasible; their exact hidden targets are not identified
by the displayed operands.” Preserve the exact-input interpretation in the table
caption and the explicit task-specification change in the numerical patches.
This issue was acknowledged by the main author during review.

### P1: Full-contract zero acceptance is oracle-defined

In the experiment code, an error is included in the invalid-answer denominator
only when `case.accepts(error)` is false. The full-contract condition then applies
the same predicate. Its zero acceptance of those errors follows directly from the
definition. The rounded-negative control likewise excludes the 34 numerically
valid collisions with that predicate before measuring the full-contract count.
The corrected positive target is also generated from the same formula and output
projection used to score it.

This does not invalidate the corpus audit or the tolerance-policy comparisons.
Different comparators genuinely disagree with the reference classification, and
the independent rational calculations validate arithmetic and source mechanisms.
But source authorship of negatives alone does not make their correctness labeling
independent of the reference checker. A skeptical reviewer can reject a claim that
zero demonstrates general repair reliability or general false-accept performance.

Explicitly call the full-contract row a **manually specified reference oracle**,
and state that its zero entries are internal consistency by construction.
Independent arithmetic and source inspection support the oracle's family-specific
validity; they do not turn the experiment into a learned-validator evaluation.
The existing limitation discusses constructed-positive acceptance but should cover
negative classification as well. The main author reported this clarification in
progress.

### P2: Put the simpler Gordon baseline in the visual comparison

The prose correctly reports that an integer constraint plus original-label ±0.5
tolerance accepts all valid integer targets and rejects all 303 incorrect projected
integers. This is an adequate simple baseline for the examined Gordon family.
The dominant full-contract bars in the main figure and table can nevertheless
suggest an algorithmic advantage to a reader scanning visuals.

Prefer an additional baseline row/bar, or a caption sentence saying that the
integer-plus-half-unit baseline attains the same tested Gordon result. This is a
presentation improvement, not a requirement for more model training. Preserve the
successful RLVR 5% tolerance result as a counterexample to the claim that widening
tolerance always causes harmful false acceptance.

### P2: Foreground the concrete common-mode verification mechanism

The public Cosimo verification harness regenerates the same template from its seed
and compares the result. It therefore checks generator reproducibility without an
independent financial valuation. This is more informative than the generic opening
slogan that code execution is insufficient. Include a short explanation and a
pinned source citation near the binomial result:
[published harness](https://github.com/btech-software/cosimo/blob/20668622104bf8237837efd67debd1419f7bbe33/dataset/verification/run_verify.py#L47).

The binomial generator returns bond financing rather than the full replicating
portfolio. All 1,000 source golds match that quantity to cent serialization, while
975 fail the call value. That source-to-label agreement and two independent pricing
identities make a specific reproducible finding. Preserve the disclosed limit that
the inspected Git commit is not proven to be the dataset's generation commit.

### P2: Clarify the introduction's dividend timing

The example yielding 30.94 uses the current dividend `D0=2`, so
`2*(1+0.052)/(0.12-0.052)=30.941176...`. A next-year dividend of 2 would instead
give 29.41. State “current dividend D0=2” explicitly. The implementation and
independent report already use D0 correctly; this is a wording correction.

### P2: Complete bibliography metadata

Use the exact primary entries:

- Silu Panda. *FinVerBench: Benchmark Validity and Calibration in Large Language
  Model Financial Statement Verification*. arXiv:2605.29586, 2026.
  [Primary paper](https://arxiv.org/abs/2605.29586).
- Ricardo Arcifa and Francieli Carra. *Fair and cheap: eight task designs for
  frontier evaluation in quantitative finance*. Montana Research Foundation
  preprint MRF-2026-04, September 2026. DOI 10.5281/zenodo.22285450.
  [Official abstract and citation](https://montanaresearch.org/publications/mrf-2026-04/).

The FinVerBench entry was already corrected during this review. The ARA citation
has the correct first author, Jiachen Liu, and title according to its cached v3
first page. FinanceReasoning and FinChain titles and ACL links match their primary
papers. The full-text access limitation for *Fair and cheap* is correctly disclosed;
do not erase it after expanding the bibliography entry.

## Numerical and preference cross-check

The following claims match the revised executable result file:

| Claim | Checked value |
|---|---:|
| Selected rows / distinct within-family questions | 12,655 / 10,476 |
| Seven passing Cosimo comparison families | 7,000 rows / 5,297 questions |
| Constructed Gordon conflicts | 946/1,000 rows; 594/630 questions |
| Binomial conflicts | 975/1,000 rows; 888/905 questions |
| CAPM exact-input conflicts | 842/1,000 rows; 836/991 questions |
| RLVR exact-input conflicts | 2,385/2,655 rows; 2,383/2,653 questions |
| Gordon chosen-invalid/rejected-invalid pairs | 312/337 |
| Binomial chosen-invalid/rejected-invalid pairs | 315/326 |
| Combined pairs requiring a valid chosen replacement | 627 |
| CAPM chosen disagreement under exact-input semantics | 288/353 |
| Gordon projected source negatives becoming valid | 34/337 |
| Remaining incorrect integer controls | 303 |
| 5% original-label acceptance of incorrect integers | 173/303 |
| Independent arithmetic coverage | 5,935 rows |

At the beginning of review, CAPM unique conflicts differed between the primary
artifact (833) and independent prose (836). The primary code counted the first
row for a duplicated prompt; hidden precision made that ordering consequential.
The main author changed the aggregation to count unique prompts with any invalid
label. The revised artifact now reports 836. This definition should remain stated
in the protocol/results metadata; duplicate questions with different targets are
not equivalent to duplicate prompt–label pairs.

The independent coverage is `2655 + 3*1000 + 7*40 = 5935`. It is not a second
full census of all passing families. The manuscript now states seven additional
sampled families and correctly identifies AI-assisted technical validation.

The binomial worked example is correct: `S=58,u=1.15,d=.85,K=48,r=.06` gives
12.716981..., while bond debt is 45.283018.... The DCF example's rounded-rate
extrema are 11,212.1212... and 11,562.5. Main comparator numerators 23/337,
217/337 and 20/326 match the result file, as do the reported zero/error counts.
The figure percentages agree with those finite denominators.

The manuscript correctly distinguishes preferred-answer invalidity from reversal:
the rejected alternatives in the 627 highlighted pairs are also invalid. It does
not propose swapping those pairs. The raw rejected answers and their subsequently
rounded versions must retain different denominators; 34 of the latter are valid
final answers despite bad derivations.

## Novelty, suitability and evidence limits

The related-work section accurately concedes the closest collisions.
[FinChain](https://aclanthology.org/2026.acl-long.662.pdf) Appendix A.3 states the
hidden-precision mechanism and Section 3.2 validates precision and completeness.
[FinanceReasoning](https://aclanthology.org/2025.acl-long.766.pdf) already revises
ambiguity, labels, units and decimal places across sources.
[FinVerBench](https://arxiv.org/html/2605.29586v1) already studies observable labels
and rendering-induced grading consequences. The manuscript consequently cannot
advertise a new contract framework or a first failure of execution verification.
Its novelty is the new external audit, common-mode source attribution and measured
preference/comparator evidence for these releases.

For the [Agenthon workshop call](https://www.agenthon.net/#call-for-papers), that is
a defensible empirical submission type. Actual accepted comparable workshop
papers include negative comparisons and curated evaluation resources. This does
not establish an acceptance probability. The finding is useful but narrow; the
source/template selection and availability of public supervision limit significance
relative to a widely adopted benchmark or a demonstrated downstream model effect.

No new training campaign is necessary to support the present title and claims.
Training would be necessary to claim model degradation or learning improvements.
The stated limitations already cover purposive sampling, duplicate prompts, no
human expert review, no upstream reward execution, manually specified formulas,
uncertified traces and multiple-choice letters, and local artifact status.

Remaining finalization checks are operational: author metadata, native compilation,
export, legible figures/tables, a reproduction command and accessible artifact
instructions. Compilation was not performed by this reviewer. Submission and
public release remain human authorization actions, not outcomes of this review.
