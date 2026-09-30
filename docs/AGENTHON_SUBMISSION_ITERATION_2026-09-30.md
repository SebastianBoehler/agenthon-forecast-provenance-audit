## Executive summary (read this first)

The strongest submission is a focused financial-evaluation paper: diagnose a
specific requested-quantity failure, trace its source, and measure its grading
consequence on unchanged answers. Anchor the document extension in **FinQA and
TAT-QA**, while keeping their native evaluation conventions separate from our
diagnostics. The most important remaining main-track gap is a useful procedure
that transfers to unseen, semantically adjudicated contexts beyond these selected
defects. Additional architectures or checkpoint counts alone do not fill it.

This is our research judgment from the current manuscript, retained evidence,
official venue pages and public organizer work. It is not actual organizer or
faculty feedback, a private rubric, an assigned-reviewer list or an acceptance
probability. Sebastian Böhler is the sole author and has confirmed attendance.

## What the venue actually asks for

The [official Agenthon CFP](https://www.agenthon.net/#call-for-papers) includes
evaluation, verification and benchmarks for financial AI. It welcomes short or
full papers, any format/length, submitted as one PDF. Accepted papers are posters;
the workshop is non-archival and at least one author presents in Atlanta on
December 12. Its competition science includes explaining failures, not just
ranking winners. This supports the audit topic; it does not require a new model.
No detailed paper-review rubric or acceptance rate is published there.

Deadline: September 30, 23:59 AoE = October 1, 13:59 Europe/Berlin. This is the
workshop/poster route. Main-track standards remain a research target, rather than
the status or deadline of this submission. The
[NeurIPS reviewing guidelines](https://neurips.cc/Conferences/2026/ReviewerGuidelines)
provide useful quality criteria: technical support, clarity, significance and
originality. Meeting formatting requirements cannot establish those properties.

## Who is listed, and how to use their work

All nine names are covered in the primary-source
[organizer/track-lead ledger](AGENTHON_ORGANIZER_RESEARCH_LENSES_2026-09-30.md)
and [industry ledger](AGENTHON_INDUSTRY_RESEARCH_LENSES_2026-09-30.md).
They are organizing roles, not established assignments to judge this manuscript.

| Listed person | Verified background lens | Concrete question for this manuscript |
|---|---|---|
| Pawel Polak | Computational statistics and financial learning | What is the independent evidence unit, and what transfers beyond discovery families? |
| Christos Koutsoyannis | Economics, investment and robust optimization | Is the claimed failure a wrong financial quantity or defensible convention uncertainty? |
| David Rosenberg | Statistics and domain-specific financial GenAI evaluation | Does the complete system measure the intended financial behavior after representation handling? |
| Gary Kazantsev | Financial NLP and cross-stage semantic/annotation errors | Where does the failure enter: interpretation, calculation, reporting, parsing or scoring? |
| Ioana Boier | Computer science, derivatives/risk and synthetic-data workflows | Do numerical constraints test financial meaning, and can the evidence be rerun? |
| Zhikang Dong | Constrained scientific learning and financial modeling | Why do the tested invariants miss the debt-versus-call defect? |
| Ruolan Sun | Preference-guided inference with scorer and matched-compute controls | Does improved proxy credit survive an independent check and matched conditions? |
| Haohan Xu | Preference-based financial execution | What downstream consequence is measured, and what training/trading effects remain unmeasured? |
| Mathew Thiel | Scientific financial workflows and discovery/validation separation | Which branches were exploratory, and did results influence selection or interpretation? |

These questions are our inferences from their public work. Four completed PhDs
are explicitly verified in this bounded review; the others' listed student or
professional status is not upgraded into a doctorate. Avoid citing organizer
papers solely to court reviewers: include a work in the paper only if it directly
helps explain or compare the scientific contribution.

Hennig's course standards and Lu's writing guidance, examined in earlier local
reviews, point to the same practical requirements: an interesting falsifiable
question, justified methodology, obvious baselines, honest uncertainty and claims
the author can defend. Their actual opinion of this paper is unknown. See the
[evidence-backed earlier assessment](POSTER_EVIDENCE_REVIEW_2026-09-30.md).

## Make the idea recognizable without changing the claim

[FinQA](https://aclanthology.org/2021.emnlp-main.300/) is the EMNLP 2021 financial
numerical-reasoning dataset with annotated programs.
[TAT-QA](https://aclanthology.org/2021.acl-long.254/) is the ACL-IJCNLP 2021
financial table/text QA benchmark. These are identifiable published benchmarks;
we do not claim a measured popularity ranking. We have already examined 48 cases
from each and retained the 384-attempt two-model panel.

Frame the current extension as an audit of selected original benchmark questions,
not official leaderboard performance or a replacement benchmark. Our FinQA JSON
scalar endpoint is adapted, not native program accuracy. TAT-QA uses pinned native
answer/F1/scale metrics. Preserve original labels, contexts, IDs and scores next
to any diagnostic reading, and credit FinanceReasoning's two known repairs.
No definite TAT-QA quantity contradiction has been established by this study.

The next benchmark resource can be a clearly marked audit/contrast extension on
these recognizable sources: same context, minimally changed requested year,
denominator, relative change versus percentage-point difference, or total versus
per-share quantity. Independently validate every target. Keep source questions
untouched and mark authored contrast questions separately. Original scores and
contrast consistency answer different questions. Recognition helps communication;
it does not supply novelty, clean train/test separation or semantic truth.

## The weaknesses that affect the contribution most

1. **Incremental novelty.** Label repair, precision checks, interpreter baselines
   and ranking sensitivity have substantial precedent. Our strongest distinct
   evidence is the debt-for-call mechanism in released synthetic supervision,
   its passing-bound controls and measured grading denials. Two document repairs
   were already published. The artifact supports trust; it is not new science alone.
2. **Reference semantics.** Two AI reviews and broad-unit matching cannot certify
   entity/year/denominator/per-share meanings. Existing ambiguous readings and the
   two later-corrected unit-parser disputes must remain visible.
3. **Measurement confounds.** Old strict output failures dominate small-model
   comparisons. The earlier reminder changes calculation-field instructions;
   the 47/131 expression transitions are conditional numerical consistency, not
   certified quantity grounding. No numerical change explains the old DeepSeek
   reminder's net +1 locked match.
4. **Transfer and consequence.** Selected families and discovery reports do not
   establish population error prevalence, an automatic audit's accuracy, actual
   deployed reward behavior, training harm or trading impact. The exact original
   dataset-generation commit is also unproven.

## Paper structure for an assessable argument

1. **Problem and claim:** call price versus financing debt; narrow research question;
   one sentence explaining what is new relative to financial label-repair work.
2. **Measurement layers:** visible task, source target, returned answer, evaluation
   convention. Define quantity, units, rounding and hidden input precision once.
3. **Source audit:** selection/provenance, independent valuation, distinct-question
   counts, passing families and source-authored error controls.
4. **Consequences:** paired fixed-answer grading, with all-attempt coverage and
   strict/exploratory channels. Lead with 55 strict DeepSeek denials: 48 quantity
   failures plus seven rounding failures; retain passing-family controls.
5. **Recognizable benchmark extension:** FinQA/TAT-QA, native/adapted scoring,
   known repairs, uncertain readings and matched prompt diagnostics.
6. **Implication and limits:** specific maintainer checks, reproducible artifact,
   boundaries of evidence and the held-out procedure test. Move branch detail and
   unsuccessful optimization into the appendix/artifact so it does not fragment
   the central argument.

This structure is appropriate for an empirical paper; a Method section naming a
new architecture would not strengthen it unless a method was actually developed
and tested. Keep the existing short, accurate title rather than making an
unsupported claim that shorter titles cause acceptance.

## Revised experimental priorities and decision rules

**Completed: separately frozen local 2×2 pilot, with failed feasibility.** Qwen3-1.7B and
SmolLM2-1.7B cross reminder/no reminder with compact/full output on the same 32
FinQA/TAT-QA questions. Within each schema, both arms require identical precision,
units and calculation grammar. Report all 256 scheduled attempts and the fixed
24-reference intersection. Separate availability, number, unit/scale and mixed
transitions. Compact/full changes requested content and possible reasoning, not
serializer mechanics alone. Native tokenizer parity is an execution check.
Both toy probes generated on FP16 MPS but failed their requested output schema;
these diagnostics are retained and do not change frozen models or prompts.

All 256 attempts are retained, but only 141 generations succeed: 128 Qwen and
13 Smol, followed by 115 Smol MPS out-of-memory failures. Every Smol TAT-QA
attempt fails. Strict numerical availability is zero in every arm; Qwen's six
status-only recoveries yield zero locked matches. The independent saved-artifact
check passes, but this does not establish a usable family comparison or an absence
of reminder effects. Separate source-free cache-cleanup diagnostics do not
establish a sustained-runtime fix. See the [results and scope](FINANCE_LOCAL_INTERFACE_RESULTS_V1.md).

**Completed: separately frozen Gemma checkpoint replication.** Cached Gemma 4
E2B Q4_K_M returns all original 200 synthetic answers, with two caps and no runtime
errors. Independent saved-record replay passes all four scoring channels. Strict
extraction admits 43 WACC answers and no monetary answers in the other families;
the prespecified numeric sensitivity admits 145 outputs. Its 22 whole-unit
rounding denials support a bounded consequence beyond the original checkpoints.
Two WACC denials are opposing comparator windows, not label faults. Only the
convention sensitivity admits one binomial final; an intermediate arithmetic slip
prevents trace certification. The failed V1 launch gate, source-free amendment and
summary-path reporting correction remain visible. This does not establish a
causal family/size effect or replace held-out semantic testing. See the
[new result report](MODEL_GRADING_LMSTUDIO_RESULTS_V2.md).

**Next substantive falsification: audit the 131 saved supported/reference-eligible
expressions.** Apply a disclosed posthoc rubric to passes and failures alike:
operand location, entity, time index, denominator and requested-unit meaning.
Ask how many of the 47 expression-match transitions remain defensible. Preserve
unresolved attribution, old scores and all unsupported attempts. This would test
an inference weakness; it has not yet been completed as an expert adjudication.

**Main-track experiment: freeze one procedure, then test it on unused groups.**
Admit original FinQA/TAT-QA report/context groups before finding defects and screen
derivative overlap. Develop only on the current discovery material. Obtain
qualified semantic adjudication for genuinely disputed targets before evaluation.
Use identical prompts/interfaces for final-answer, native representation,
execution, simple tolerance and quantity-aware checks. Report both false acceptance
and false rejection, coverage, unresolved cases, cost and group-level variation.
For FinQA official performance, emit/evaluate its actual program representation;
do not relabel our scalar adapter as native program accuracy.

A convincing contribution requires a consequential residual finding or useful
audit performance surviving those cheap baselines and transferring beyond hand
specified templates. Contrasts should be held out by report/source group, with
both members kept together. More model sizes/families can test robustness after
the measurement is valid, using matched interfaces without causal size claims.
Training source-versus-repaired policies is needed only for a learning claim;
GEPA, world models, looped transformers and PufferLib RL remain separate hypotheses.

## What is completed versus pending

Completed: live CFP/committee check, all-nine background ledgers, benchmark primary
source check, revised risks/structure/priorities, metadata-selected cohort, all
256 native token audits, two runtime probes and authored parser controls. Previous
source and document studies retain their validated records and archive.
Local collection and independent result replay are complete; its failed
feasibility is disclosed in the manuscript appendix. Four claim-linked sources
and the Gemma model card bring the bibliography to 28. The official NeurIPS
preprint style compiles, with the completed Gemma panel retained separately, while
rendered body-page count and the official full checklist remain unchecked.
Held-out procedure performance, expert reference
adjudication, broader prevalence and downstream learning effects remain unmeasured.
No submission receipt or acceptance exists from this preparation work.
