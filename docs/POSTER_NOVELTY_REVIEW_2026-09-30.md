## Executive summary (read this first)

**Verdict: defensibly distinct empirical evidence for a focused workshop poster,
with a modest novelty margin; insufficient evidence for a main-track contribution.**
The strongest result is a systematic wrong-quantity defect in released supervision,
its numerical match to inspected public generator code, and the grading disagreement
on unchanged answers. It becomes more than a single bug report through the census,
passing comparisons, independent valuation identities, source-authored error controls
and explicit comparator trade-offs. The general principles are established prior art.

The sentence “Our novelty is the source-traced evidence about these released pipelines
and its measured grading consequences” is directionally reasonable but underspecified.
It leaves the scientific information implicit and can overstate production provenance.
Replace it with the bounded contribution wording below. Prioritize evidential clarity,
not another rushed architecture, model or optimization experiment. Acceptance confidence
cannot be assigned from the current record: there is no calibrated acceptance model,
organizer feedback or representative accepted/rejected sample.

This is my independent skeptical review of the [canonical manuscript](../paper/answer_contract_audit.tex) and primary
sources. “Hennig/Lu-informed” means an inferred emphasis on falsifiability, measurement,
closest alternatives and claim support; neither professor supplied this review or an
endorsement. The organizer perspective below is inferred from the public call, not
private selection criteria. No private course quotation is reproduced.

## What a skeptical reviewer will ask

| Perspective | Strong objection | Evidence-backed response and remaining limit |
|---|---|---|
| Agenthon fit | Why should a finance-agent workshop care about one generator bug? | Machine-verifiable finance evaluation is directly relevant. A wrong financial quantity can satisfy basic bounds and the inspected regeneration check, then deny credit to valid answers. This is a concrete release/evaluation failure, not a claim about Agenthon's own scorer. |
| Hennig-informed measurement | What exactly is wrong, under which convention, and what is the independent unit? | Wrong quantity and explicit integer rounding are separate from hidden-precision ambiguity. Report rows and unique prompts within selected families. The binomial result survives both checked compounding conventions; repeated templates are not independent population samples. |
| Lu-informed contribution | What did readers learn beyond “labels can be wrong”? | Which released targets follow the wrong financial quantity, what public code implements, why elementary bounds miss the cases, how fixed-answer grading changes, and which cheap correction succeeds. General contract awareness and metric sensitivity are already known. |

The live [Agenthon call](https://www.agenthon.net/#call-for-papers), checked 30 September,
explicitly includes evaluation, verification and benchmarks for financial AI. It accepts
short/full papers in any format and length and is non-archival; accepted papers are posters.
It does not publish an acceptance probability or promise selection for a relevant topic.
Work accepted at other finance workshops is useful calibration, not Agenthon approval.

## Closest primary collisions

| Work inspected | Established overlap | Defensible difference here |
|---|---|---|
| [FinanceReasoning](https://aclanthology.org/2025.acl-long.766.pdf), §2.1 | Reannotates unsolvable/ambiguous questions and incorrect answers; enforces units, signs, decimal places and a 0.2% margin. | Our object is pinned released synthetic training/preference supervision and a code-inspected wrong-quantity pattern. Label repair and numerical evaluation are not new. |
| [FinChain](https://aclanthology.org/2026.acl-long.662.pdf), §3.2, Appendix A.3/B.2, Eqs. 4/7 | Explicitly identifies displayed-rounded/full-precision computation, units and representation errors; uses a 5% numeric comparator. | The debt-as-call release fingerprint and coupled public regeneration are the strongest additional evidence. Hidden precision is not our discovery; our comparator experiments do not describe FinChain's deployed grading. |
| [FinVerBench v1](https://arxiv.org/pdf/2605.29586v1), §§3.5, 5.4, 6.4–6.5 | Relabels hidden-field positives as insufficient information and measures rounded-rendering effects on financial verification. | We audit released supervision and preferred completions rather than inject statement errors. Observability-aware labels and consequential rendering studies already exist. |
| [Northcutt, Athalye and Mueller](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/f2217062e9a397a1dca429e7d70bc6ca-Abstract-round1.html), §§4–5 | Label-error audits can change evaluation; striking reversals concern error subsets or increased-noise settings, not every complete leaderboard. | Our numerical financial contracts and inspected generator formula differ. “We found label errors and a ranking reversal” alone is insufficient novelty. |
| [Measurement Risk v2](https://arxiv.org/html/2604.27374v2), §§1.2, 3.2, 4 | Audits financial rubric/metric/ranking sensitivity and metadata drift; explicitly separates inference policy from scoring policy on emitted outputs. | The audited synthetic numerical supervision and wrong-quantity code diagnosis differ. Holding responses fixed to examine scoring is sound design, not a new experimental principle. |
| [Fair and cheap](https://montanaresearch.org/publications/mrf-2026-04/) | Its official abstract requires graded answers to be determined by model-visible information. | Full manuscript remained reader-gated; exact experimental overlap is unresolved. No firstness claim should depend on that access gap. |

FinanceReasoning, FinChain, FinVerBench and Northcutt were rechecked in cached primary
full texts. Current official title pages returned HTTP 200 when checked directly;
the browsing tool failed to fetch the first three pages. Measurement Risk's author
v2 §§1.2/3.2/4 were read directly online; no final IEEE-version equivalence is assumed.
Fair and cheap remains abstract/open-data-only. This was a bounded collision check,
not a new exhaustive search or proof no earlier source contains these exact findings.

## Is it a trivial bug report?

The strongest skeptical argument is substantial: call valuation and integer rounding
are elementary; regenerating a template shares its errors; grading against a different
number predictably changes scores. A thousand samples of one template do not create a
thousand independent discoveries. The repair is largely the obvious correct formula
and rounding instruction, not a learned or automatic general validator.

The useful empirical information is nevertheless more specific than that argument:

- All 1,000 audited binomial golds match financing debt, while 975 fail option valuation
  under both checked conventions; only 25 happen to match the call value.
- All 1,000 golds pass elementary call bounds. Those invariants therefore cannot replace
  an independent financial identity for this particular semantic defect.
- Seven comparison families match their numerical labels, limiting a universal parser
  or serialization-bug explanation. Independent rational checks cover 5,935 rows.
- Actual chosen/rejected completions supply controls beyond invented mutations; 627
  Gordon/binomial pairs have neither side numerically valid. Swapping labels is insufficient.
- The strict model endpoint demonstrates 55 valid-answer denials among 136 valid DeepSeek
  answers. The supplementary Gordon ordering example is concrete but post hoc and bounded.
- Cheap controls have mixed outcomes: integer-plus-half-unit succeeds on Gordon;
  widening succeeds on the tested DCF controls but cannot correct the wrong quantity.

These observations support a useful forensic audit poster. They do not establish
the prevalence of shared verification faults in finance, a universal failure taxonomy,
new independence theory, or downstream learning harm. “New evidence” is a contribution
description, not an exemption from asking whether the particular evidence matters.

## Source tracing and causal boundaries

**Highest-priority wording risk:** dataset revision and source-code revision are separate.
The inspected code at
[20668622104bf8237837efd67debd1419f7bbe33](https://github.com/btech-software/cosimo/tree/20668622104bf8237837efd67debd1419f7bbe33/dataset)
contains the debt formula, integer-wrapper behavior and seeded regeneration mechanism.
The dataset fingerprint supports that diagnosis. It does not prove this is the exact
original release-generation commit, that every stored verification flag came from
this harness, or that the upstream verification process was replayed. The figure
caption already distinguishes illustration from an executed trace; add this revision
boundary to the main pinned-source paragraph and soften “source-level attribution.”

Changing the comparator while retaining answers identifies the mechanical effect of
those declared scoring policies on this fixed panel. It does not identify a deployed
upstream reward, a general model ordering, learning degradation, commercial loss, or
the financial performance of a trained agent. Strict parsing succeeds for 0/34/0/137
answers across the four models; the 4B numeric endpoint recovers only 90/200. Numerical
recovery cannot turn that panel into a clean capacity comparison or unit-understanding test.

The repaired targets and negative classifications share manually specified contracts.
Zero acceptance of tested errors is finite oracle consistency. Independent identities
and source-authored controls strengthen correctness, but do not estimate general
validator accuracy. The completed GEPA pilot retains the seed in every arm and passes
neither consequence nor repair gate; it supplies no optimization-induced effect.

## Recommended contribution wording

> Our contribution is a release-specific numerical audit: systematic wrong-quantity
> and rounding failures; diagnosis in separately pinned public generator/verifier code;
> and grading disagreements on unchanged model answers under explicitly reconstructed
> label comparators, with passing families and source-authored error controls.

Follow with: “The inspected code revision is not established as the original generation
commit. Hidden-input precision is reported conditionally, and neither a new verification
method nor a downstream training effect is claimed.” For the poster's spoken opening:
“A released call-price label follows financing debt; its public regeneration check
shares the computation. We measure what happens when that label grades fixed answers.”

## Ranked changes achievable within the deadline

1. **Repair provenance and novelty wording.** Make the separate code/data pins and
   unproven production revision explicit in the source paragraph. State the exact
   empirical contribution and closest collisions once, without asserting firstness.
2. **Make one scientific story dominant.** Lead with call price 12.72 versus debt 45.28,
   the 975/1,000 persistent discrepancies, and the independent identity/basic-bounds
   comparison. Keep hidden precision conditional and secondary to that clear example.
3. **Show the cost of the grader with honest coverage.** Keep the strict 200-answer
   partitions visible and the 55/136 denial result. Mark the Gordon 10-versus-2 to
   22-versus-50 ordering example supplementary, one family/two models, unchanged answers.
4. **Expose the cheapest alternatives.** Give integer-plus-half-unit and successful
   DCF widening equal visibility with the failure cases; distinguish wrong quantity
   from serialization and ambiguity. Avoid making obvious repair sound algorithmically new.
5. **Spend poster space on evidence.** Use example → grading consequence → controls.
   Keep the ARA-inspired history/negative GEPA record available through the artifact
   index rather than allowing unrelated failed directions to dominate the poster.
6. **Finish consistency checks and presenter defense.** Recheck figure/table source fields,
   exact denominators, convention labels and source pins. Prepare answers to “one bug?”,
   “actual reward?”, “independently reviewed?”, “why four models?” and “what did GEPA learn?”
   Do not add a hurried new inference study or imply the blank expert packet is validation.

## Main-track gap

Main-track ambition needs a significant transferable empirical explanation, not more
rows of the same generator. A credible next study would prospectively admit independent
maintainer/generator pipelines; independently adjudicate task semantics; test naturally
interacting quantity/precision/rounding failures against cheaper policies; and evaluate
repair on held-out source releases/tasks. If learning consequences are central, actual
successful objective adaptation or controlled training must precede harm/repair claims.
Controlled verifier-noise effects already have a close predecessor in
[Delay, Plateau, or Collapse](https://arxiv.org/abs/2605.02909v2).

The current main-track blocker is substantive breadth/significance and missing learning
evidence, not absence of fashionable architecture. An empirical discovery can be original
without a new algorithm, but its explanation and evidential reach must survive the
closest alternatives. The workshop poster can honestly present the current bounded result
while the main-track plan remains a separate research program.
