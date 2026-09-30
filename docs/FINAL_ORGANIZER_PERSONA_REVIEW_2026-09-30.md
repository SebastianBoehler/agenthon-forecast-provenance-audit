## Executive summary (read this first)

The current draft has a defensible workshop contribution: a source-traced
financial quantity error that survives the tested price bounds, a distinct
requested-rounding failure, and paired grading consequences on unchanged model
answers. The best final addition is a controlled comparison of a pinned released
grader with an explicitly scoped numerical-equivalence checker, using a frozen
MATH500 sample and the financial cases. A small local-model run can establish
whether the failure occurs in observed outputs rather than only authored
counterexamples. This improves evidence and transfer; it does not certify
main-track readiness or predict acceptance.

This is a hypothetical organizer/quantitative-finance PhD review inferred from
the public venue and scientific evidence. No organizer reviewed the paper; no
reviewer assignment, personal opinion, endorsement, or acceptance probability is
known. The author is solo and can attend Atlanta, as confirmed by the user.
Checked September 30, 2026. No code, manuscript, frozen artifact, submission,
paid compute, or external communication was changed by this review.

### What the venue actually requires

The [official Agenthon CFP](https://www.agenthon.net/#call-for-papers) welcomes
financial evaluation/verification/benchmarks and high-quality AI work more
broadly. It accepts a single PDF, full or short papers of any format/length,
is non-archival, and requires an author to present a poster in Atlanta on
December 12. Its deadline is September 30 at 23:59 AoE, equivalent to October 1
at 13:59 in Berlin. It publishes no paper-specific judging rubric or assigned
reviewers. A nine-page NeurIPS paper is a useful discipline we choose, not a
workshop formatting requirement.

For the requested main-track quality target, the
[2026 NeurIPS reviewer guidelines](https://neurips.cc/Conferences/2026/ReviewerGuidelines)
evaluate quality, clarity, significance and originality. The use-inspired
guidance permits simple methods when justified by the application and expects
comparison with relevant established approaches. Negative results require
informative analysis rather than an unsuccessful experiment alone. These are
quality lenses, not a claim that this workshop uses that exact review form.

The [2026 E&D guidelines](https://neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines)
explicitly recognize reproducibility/auditing/stress-testing and data-centric
empirical analysis. Their relevant standards are systematic evidence,
independently assessable claims, meaningful evaluation insights and transparent
artifacts. This is a natural intellectual framing for the present work; it does
not turn this workshop submission into an E&D/main-track submission.

The [2026 main-track handbook](https://neurips.cc/Conferences/2026/MainTrackHandbook)
specifies nine content pages plus references/appendices/checklist, the year's
template and author responsibility for accuracy. Its formatting requirements
are useful preparation for a later submission. They should not be presented as
mandatory requirements of the Agenthon CFP.

### Evidence reviewed and limits

The draft reviewed was `paper/answer_contract_audit.tex`, SHA256
`c938578de9ea9a227dcd54aef1ab132d3657dc1e24b509b0a512f27cd200421a`.
The review also reads the existing
[organizer research lenses](AGENTHON_ORGANIZER_RESEARCH_LENSES_2026-09-30.md),
[fresh scientific audit](SCIENTIFIC_BASE_AUDIT_2026-09-30.md),
[close-source contribution review](CITATION_CONTRIBUTION_REVIEW_2026-09-30.md),
and [RecursiveMAS code/primary-paper review](RECURSIVEMAS_RELEVANCE_REVIEW_2026-09-30.md).
The current-count statements below rely on those replay receipts and manuscript,
not a new independent execution by this persona review.

### Hypothetical review

**Summary.** The study audits selected synthetic financial supervision releases,
traces a call-price/financing-debt error to separately pinned public code, and
holds observed model responses fixed while comparing numerical grading. It
also tests document transfer and inexpensive arithmetic execution, retaining
null interventions and uncertain AI references.

**Strengths.** The call example is concrete, independently checkable and
financially consequential at the target-definition level. Of 1,000 selected
call rows, 975 disagree with valuation, all 1,000 match financing debt, and
none violate the tested bounds. Seven passing comparison families make a
universal parser failure implausible. The 946 integer-output violations expose
a separate mechanism. The strict DeepSeek comparison decomposes 55/136 valid
answer denials into 48 quantity and seven rounding denials. These are stronger
than unexplained mismatch totals. Discovery history, failed branches and source
revision uncertainty are disclosed rather than converted into inflated claims.

**Major concerns.** A reviewer can agree that the release is defective while
asking whether this advances understanding beyond a careful bug report.
Formula/unit/precision checks and fixed-output scoring sensitivity have close
prior art. Two synthetic releases and repeated templates do not establish
prevalence. The document cases include known prior repairs and derivative
overlap; AI agreement is not domain-expert adjudication. The reminder has no
demonstrated benefit. The paper measures reconstructed grading, not historical
training harm or deployed reward behavior. These limits remain after one more
local run.

**Presentation concern.** The main draft presently gives substantial space to
several inconclusive extensions. For a poster reviewer, the debt-for-call result,
passing bounds, unchanged-answer grading and source provenance should remain
the central line. The MATH500 addition should supply one transfer question, not
replace the financial study with a new broad architecture story. Prior failed
model interfaces and most diagnostic endpoint details belong in the appendix.

**Workshop assessment.** Topic fit is strong and the financial defect is
inspectable. My hypothetical recommendation would depend on exact claim scope,
replay accessibility and a concise contribution statement, rather than a new
neural architecture or claimed leaderboard position. No confidence percentage
or simulated numerical reviewer score would be evidentially grounded.

### Final experiment: acceptance semantics on fixed outputs

The testable question is: does the released answer-normalization policy credit
numerically unequal observed answers, and can a small, explicit equivalence
checker expose those cases without rejecting admissible equivalent answers?
An equivalence checker compares numbers or admitted representations. It does
not establish that a supplied source label names the right financial quantity.
Keep label validity and comparator validity as two separate axes.

| Component | Required design | What would falsify an attractive claim |
| --- | --- | --- |
| MATH500 admission | Freeze release revision, seed/order and sample IDs before inspecting numerical targets; retain every sampled case | Selecting decimal/sign failures after target inspection would only support a selected diagnostic, not natural prevalence |
| Scoped scalar checker | Declare accepted integers, decimals, signs, rational/LaTeX forms, optional units and percent policy before scoring | Missing algebraic, vector or interval support can be a parser abstention, not an answer error |
| Representation controls | Include identical values, equivalent fractions/decimals, signed equivalents and allowed formatting; preserve explicit unit semantics | Rejecting legitimate equivalents would show that strictness trades false credits for false denials |
| Negative controls | Include nearby decimals, sign changes, distinct fractions and changed units where the task requires them | If the released comparator rejects them, the proposed collision mechanism fails on those controls |
| Local outputs | Use a cached model, native tokenizer/chat template, fixed generation budget and unchanged saved responses | If no adjudicated collisions occur, report zero in this panel; toy controls still do not establish natural impact |
| Financial comparison | Reuse pinned questions, passing families and independently checked target values; retain source-label and corrected-target scoring separately | A checker that only compares to a wrong label cannot repair the debt-for-call defect |
| Adjudication | Resolve each disagreement with exact arithmetic/source question inspection; preserve ambiguous and unsupported cases | A strict-parser rejection alone cannot be counted as a released-grader false acceptance |

Report full sampled denominator, answer-type eligible denominator, returned
response coverage, format/parse failures and adjudicated false-credit/false-denial
counts separately. Apply every policy to the same saved output. A one-cell score
difference is not enough: expose the disagreement matrix and representative
accepted/rejected examples. Authored mutation controls and naturally generated
outputs need distinct tables because their selection and denominators differ.

For ablations, include exact numeric equality, the pinned released comparator,
and the checker with individual sign/decimal/unit constraints removed. Reuse
only supported parsing rules; do not add silent repair or answer extraction
after seeing failures. Compare against a simple standard baseline wherever one
is available, rather than presenting a restricted parser as a new general
mathematical judge. Any native dispatch test must bind the exact code revision.

One deterministic local pass can establish feasibility and observed behavior.
Additional checkpoints help robustness if settings and budgets are fixed; a
few small runs do not establish causal model-size scaling. Repeating the same
greedy configuration produces no independent sample of the experiment. Save
model revision, quantization, chat template/tokenizer hash, prompts, token
limits, raw outputs, timings, failures and grader receipts. No paid inference
is required to test the present hypothesis.

### Tiny NN, RL and benchmark gaming

A local reward-exploitation experiment could eventually be relevant: optimize
against the flawed comparator, then independently measure numerical validity.
Its scientific target would be divergence between rewarded score and intended
correctness, not an apparent leaderboard win. A source-target-dependent mutation
is an authored adversarial control, not a question-solving policy; calling it
a superior model would be misleading. A learned policy requires held-out
question groups and targets, matched reward/compute budgets, repeated seeds,
a simple rule baseline and evaluation under a protected independent target.

For this last iteration, a new PufferLib environment or tiny NN adds integration
and learning confounds to a question already testable with fixed outputs.
If a deterministic exploit reproduces the phenomenon, RL would need to answer
a further question such as learned discoverability, transfer to an unseen
grader, or training-induced degradation. No such necessity has yet been shown.
Preserve the idea in future work; prioritize the approved grader comparison and
local run. Do not claim an official benchmark rank from local diagnostic scores.

### Essential writing changes after the run

1. State the concrete financial failure and strongest finite evidence first.
   Cite FinanceReasoning/FinChain and explicitly separate existing verification
   principles from this release-specific empirical contribution.
2. Define requested quantity, label, output representation and grading policy.
   Separate wrong target from normalization that merges unequal values.
3. Include a compact new comparison only if the result survives admissible
   equivalence controls and explicit adjudication. Report a null natural-output
   result honestly if that is what the local run yields.
4. Retain the seven passing families, simplest integer/tolerance baseline,
   rounded-input feasibility and nonbeneficial reminder. These make the study
   credible; they are not obstacles to hide.
5. Provide a flat replay entry point with exact input/code/output hashes and
   figure/table provenance. Source excerpts verify citation location; they do
   not alone certify entailment. Hashes verify identity; they do not certify
   correctness. Keep AI reference authority explicit.
6. Do the user's section-by-section co-drafting after the evidence is frozen.
   Keep the title factual and concise; no acceptance benefit of title length
   has been established for this venue.

### Main-track strength still missing after this iteration

The largest outstanding gains are financial-expert adjudication, a frozen audit
procedure tested on previously uninspected independent producer/task lineages,
and a demonstrated practical consequence beyond reconstructed fixed-answer
grading. Depending on the eventual claim, that consequence could be a reliable
audit/repair workflow or a causal training/reward experiment. A general new
benchmark needs a justified sampling/population design and governed references.
More source citations, model families or an accepted-paper architecture cannot
substitute for those evidence requirements.

The final addition can strengthen a good workshop submission and the foundation
of a later audit/evaluation paper. It should not be described as closing every
main-track gap, as demonstrating historical RecursiveMAS score inflation, or as
guaranteeing an accepted poster.

### Final-result addendum: controlled failures and natural-output limits

The completed local study is recorded in
[analysis.json](../artifacts/grader-comparison-v1/analysis.json) and the
[projection manifest](../artifacts/grader-comparison-v1/manifest.json).
I read the resulting counts and record-level Boolean decisions; this addendum
does not independently execute inference or reconstruct full response extraction.
Analysis SHA256 is
`bc8a58fa42d5ce0ec5b2d63abb9a34619ee9219b088538b5884bbb19fba77f6d`.
The earlier draft review remains a timestamped assessment of its stated hash.

The frozen MATH500 reference census admits 368 of 500 answers under the declared
scalar grammar; 132 are excluded. Its 2,548 authored controls contain 1,451
equivalent and 1,097 unequal pairs. The released comparator credits 354 unequal
controls and denies 372 equivalent controls. Removing digit-only normalization
eliminates the 354 false credits but raises false denials to 420; removing both
digit-only and integer-part normalization raises them to 456. Exact rational
comparison has zero errors on these admitted controls. That is a restricted
control-suite result, not validation as a general mathematical judge. There
are 174 distinct reference values and 695 distinct numeric control pairs;
2,548 controls are not independent discoveries or natural model mistakes.

All 96 scheduled attempts returned records: two local Q4_K_M checkpoints,
Gemma 4 E2B and Qwen3.5-9B, each used three unseeded repetitions on the same
16 questions (eight financial, eight MATH500). Eight output caps and two final
scalar parsing nondecisions remain accounted for. Saved-answer replay is exact;
fresh stochastic generation is not bitwise reproducible. The repeats do not
turn 16 questions into 96 independent problems or support a causal size claim.

On MATH500, 42 of 48 attempts admit a common strict final scalar. The native comparator
has zero observed false credits or false denials on that subset, with 37 exact
matches. Removing both permissive normalizations loses six correct credits,
leaving 31. Full native extraction admits 43/48 and credits 38/48, including one correct Qwen
answer recovered outside the shared final-line endpoint. Thus the natural panel
does **not** reproduce incorrect-answer inflation; stricter deletion demonstrably
costs legitimate credits. Full extraction and common-scalar scoring remain
different endpoints. Neither a eight-question null nor a controlled collision
establishes historical paper-score inflation or full-benchmark prevalence.
The local mathematical subset contains seven integer references and one
fraction, so its null provides limited coverage of decimal/sign-sensitive
natural failures. The paper now states that selection limit explicitly.

On the 48 financial attempts, complete numerical-contract grading credits 28,
while original-label cent grading credits 12. The 16 valid-answer denials split
into 12 whole-unit-rounding and four call-price cases. This extends the concrete
financial scoring consequence to two local checkpoints; it is not a learning
or deployed-reward experiment.

**Suggested concise contribution update:** We document released financial
target failures and audit acceptance semantics in a pinned MATH500 evaluator.
Controlled sign-changing perturbations reveal false credits, while local outputs
show that deleting permissive normalization can instead lose correct credits;
the financial panel reproduces correct-answer denials under source-label grading.

This balanced outcome strengthens the workshop story: verification must preserve
both intended quantities and valid representations. It closes the authored-only
comparison weakness for natural financial denials and supplies an informative
MATH null plus counterproductive-ablation result. It does not establish a new
general grader, historical RecursiveMAS score inflation, a trained exploit,
expert financial truth, independent financial producer replication, or a
leaderboard gain. Keep this as one compact supplementary comparison in the
financial manuscript, with control/local denominators visible. No additional RL
architecture is needed to make the completed evidence publishable at workshop
scope; main-track sufficiency remains unestablished for the reasons above.
