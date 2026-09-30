## Executive summary (read this first)

Select a focused **empirical audit of released financial reasoning supervision**,
provisionally titled *When Verified Answers Violate Their Questions*. The useful
contribution is new, reproducible evidence about which published training and
preference targets violate visible questions, which grading decisions change, and
which targeted corrections restore consistency. It is **not** a new concept of
answer determinacy, a first observation of hidden precision, or a new precision
validation method. Those claims collide directly with the primary literature.

This recommendation is conditional on consequential comparator/preference results
and a repair evaluated against erroneous-answer controls. The current two-template
counts justify executing that study; they do not alone justify a strong paper.
The strongest more ambitious alternative is learned-market response consistency,
but its completed pilot supplies no demonstrated defect. Do not revive its positive
headline. A decision-sufficiency study remains promising future work without
current empirical support. No broad brainstorming reset is warranted.

## Review scope and decision rule

This independent review read the handoff and the three requested comparison notes.
It then inspected the primary full texts of FinVerBench, FinanceReasoning and
FinChain, including their methods, precision policies, relevant appendices and
limitations. It rechecked *Fair and cheap* through its official abstract, reader
page, open-data README and public Zenodo file listing. Its manuscript was not
available without submitting identifying information. No reader form was submitted.

The review also inspected two actual accepted workshop PDFs and rechecked their
acceptance against the organizer's roster. It preserved the competition firewall,
changed no implementation or manuscript, and used only ignored storage for source
texts. No AGENTS.md existed in the dedicated paper repository during this pass.

The decision criterion is distinguishable scientific information, supported by
actual observations and a falsifiable comparison. Time alone should not select a
small idea. Equally, a more ambitious unsupported hypothesis should not displace
an observed failure merely because its narrative sounds more novel.

## Exact collisions in the nearest primary literature

| Primary work | Established result or procedure | Consequence for our claim |
|---|---|---|
| [FinVerBench](https://arxiv.org/html/2605.29586v1), Sections 3.5, 5.4, 6.4–6.5 | Hidden-field positives are relabeled as insufficient information. Rounded versus unrounded rendering changes verification performance. | Observability-aware labels and consequential rendering audits already exist. Our unit is released training/preference supervision, rather than statement-error detection. |
| [FinanceReasoning](https://aclanthology.org/2025.acl-long.766.pdf), Section 2.1 and Limitations | Revises unsolvable or ambiguous questions and wrong labels; specifies units, signs and decimal places; tightens numeric grading. | Cross-source label correction and answer-format enforcement alone are established. Distinguish a systematically traced generator-to-supervision failure with comparator and repair evidence. |
| [FinChain](https://aclanthology.org/2026.acl-long.662.pdf), Section 3.2, Appendix A.3 and B.2 | Explicitly identifies displayed rounded values computed at hidden full precision, and validates precision, units, completeness and representation. | The exact hidden-precision mechanism already appears in published work. Do not claim its discovery or a first contract layer. |
| [Arcifa and Carra, *Fair and cheap*](https://montanaresearch.org/publications/mrf-2026-04/) | Official abstract requires the graded answer to be determined by model-visible information; reports eight quant-finance designs failing its protocol. | Determinacy is direct conceptual prior. Full-text overlap remains unresolved; acknowledge that boundary instead of inferring novelty from unavailable pages. |

FinVerBench uses a 1,985-instance generated corpus and an observable 105-instance
LLM diagnostic subset. Its construct-validity conclusions include hidden-field
relabeling, false positives caused by omitted components, and a rendering ablation.
The calibrated model's recall changes from 100% to 79% after realistic rounding.
That is already empirical evidence that answer visibility and presentation can
change measured model behavior. The relevant difference for our study must be
the supervision being audited and the evidence about its consequences. It cannot
be the general slogan that execution or arithmetic is insufficient.
[Full paper](https://arxiv.org/pdf/2605.29586v1).

FinanceReasoning is broader than an arithmetic repair resource. It performs
disambiguation, elaboration and correction across existing sources, and enforces
an error margin of 0.2% together with answer units, percentage format, signs and
decimal places. Its limitations explicitly restrict evaluation to
perfect-information calculations and distinguish these from clarification under
insufficient conditions. Thus both prompt adequacy and requested output format
are already within the financial benchmark literature.
[Published paper](https://aclanthology.org/2025.acl-long.766.pdf).

FinChain is the sharpest collision. Appendix A.3's precision-mismatch criterion
describes the same displayed-rounded/hidden-full-precision discrepancy as our DCF
example. Appendix B.2 includes representation errors covering units and rounding.
Its numerical matching policy nevertheless permits 5% relative deviation in
Equations 4 and 7. Therefore the strict-tolerance discrepancy count cannot be
transferred into a claim that its actual benchmark rejects those answers. A clean
control drawn from FinChain must be independently checked; expert-reviewed
provenance is not sufficient to declare an instantiated case clean.
[Published paper](https://aclanthology.org/2026.acl-long.662.pdf).

*Fair and cheap*'s accessible material is direct prior for the concept. Its
[open-data README](https://raw.githubusercontent.com/Montana-Research-Foundation/open-data/main/experiments/MRF-2026-04-task-design-collapse/README.md)
states that seven designs never ran against a model and one had two rollouts.
Its [Zenodo record](https://zenodo.org/records/22285450) contains a data ZIP, not a
manuscript. These facts establish overlap and its disclosed evidence scale;
they do not establish the contents of all 39 manuscript pages.

## The remaining defensible contribution

An appropriate claim is:

> In audited families of two public synthetic financial training releases,
> verification metadata does not ensure that released numeric and preference
> targets satisfy the model-visible question. Independently traced failures at
> input rendering, financial computation and requested output precision have
> different consequences. Targeted repairs can be compared with tolerance
> widening using valid and invalid answer controls.

This statement intentionally describes a corpus audit and measured intervention.
It does not describe a new financial theorem, a general verifier, or demonstrated
learning degradation. Its empirical novelty is a judgment from the inspected
sources, not proof that no matching audit exists anywhere.

The handoff's DCF and Gordon-growth observations support distinct claims. The DCF
golds all fall within the intervals implied by conventional rounding of the
displayed rates. That supports ambiguity under rounded-input semantics, not
intrinsically wrong finance values. The Gordon-growth source explicitly requests
whole-unit answers while supplying cent-level targets, including preferred
answers. That is a stronger direct prompt–supervision conflict. The team's newly
identified binomial-call issue is exploratory until the full family is independently
checked; a wrong financial formula is another mechanism, not a new idea by itself.

The important explanatory structure is a commuting calculation: the displayed
question, its declared semantics and output projection should lead to the same
admissible answer as the release's label-generation path. Existing work already
checks pieces of this structure. Our paper must show how independently published
supervision violates it and whether the correction meaningfully changes outcomes.

## Priority experiments and interpretation gates

1. **Systematic source coverage.** Complete a declared family census or a fixed
   transparent sample, including passing families. Preserve the exploratory status
   of already discovered issues. Freeze further inclusion before inspecting more
   results. Report both unique prompts and rows; duplicates are not independent
   evidence. Two selected generators cannot estimate field-wide prevalence.
2. **Independent financial derivations.** Recompute from visible operands with
   separately implemented mathematics. For a binomial call, use both replication
   and risk-neutral expectation. Cox, Ross and Rubinstein's Section 3 gives
   `C = delta*S + B` and `C = (p*C_up + (1-p)*C_down)/R`, with
   `R = 1+r` and `p = (R-d)/(u-d)`; the bond component alone is not the call.
   [Original author paper, PDF pages 4–6](https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/7/36891/files/2017/07/CRR79-1yy8av8.pdf).
3. **Source-authored preference consequences.** Evaluate released chosen and
   rejected completions under the requested output contract and financial formula.
   Count chosen-only conflicts, valid rejected answers and true pair reversals
   separately. A chosen answer with wrong precision does not automatically imply
   that its rejected alternative is better. This experiment directly strengthens
   the training-supervision relevance without requiring model training.
4. **Honest comparator scope.** Reproduce released grading code when it exists.
   Otherwise label policies reconstructed. Include the source's advertised policy,
   exact/cent/whole-unit checks where relevant, and relative tolerances including
   0.2%, 1% and 5%. A local sensitivity analysis is not an observed upstream reward
   rejection. Final-answer admissibility is not reasoning-trace correctness.
5. **Repair versus blunt tolerance.** Compare operand-aligned recomputation,
   requested-output projection and ambiguity-aware handling with merely widening
   numeric tolerance. Measure false rejection of valid answers and false acceptance
   of known incorrect calculations. Include source-authored rejected responses and
   explicitly declared corrupted detector controls. Wrong units, signs, formula
   substitutions and boundary cases should remain discriminable where appropriate.
6. **Adjudication and limitations.** Review a stratified sample including conflicts,
   passing cases, singular formulas, rounding ties and near-zero answers. State
   exactly whether adjudication is human expert review, independent program review
   or model-assisted review. Do not describe two model reviewers as two finance
   experts. Preserve disagreements and exclusions in the artifact.

For explicitly rounded inputs, let `X(q)` denote all input vectors consistent
with visible question `q`. The admissible outputs are the requested projection
of `f(X(q))`. If that set contains several requested answers, picking its midpoint
does not create a unique ground truth. Either expose sufficient input precision,
change the requested answer to an interval, or mark the scalar task underdetermined.
Do not silently treat every printed number as uncertain. Conversely, if all
permitted inputs round to one requested answer, the task is determinate at that
precision even though the unrounded numeric value is uncertain.

An interval-only final-answer checker cannot reject every flawed derivation that
lands inside an admissible interval. False-accept controls must respect that
information limit. Broadening tolerance to include all possible values also does
not demonstrate that one particular hidden generator value was recoverable.

The headline fails if all consequential disagreements disappear under documented
policies, if sample inspection reveals parsing or legitimate formula alternatives,
or if repair merely accepts more wrong answers. An isolated source bug still
merits a reproducible audit note; it does not establish the desired contribution.

## Strongest alternatives, assessed without anchoring

**Learned-market response consistency** has the highest potential methodological
upside among the existing alternatives: show that observationally realistic
simulators have a reproducible action-response defect, then correct it while
preserving fidelity. However, the actual MarS pilot has 52 completed cycles,
eight initialization failures and one profitable cycle, with no demonstrated
causal defect. Profitable samples alone cannot distinguish randomness, legitimate
information, trading semantics and model errors. Its current positive claim is
unsupported. See the executed [pilot report (archived)](../artifacts/history/retired-branches-20260930.zip), rather than
the older proposal. Choosing the supervision audit is evidence-based; it does not
mean simulator research is uninteresting or intrinsically too expensive.

**Decision-sufficient evidence** asks whether uncertainty prevents a financial
action, rather than whether it prevents an exact answer. An NPV interval entirely
above zero can settle approval without settling the exact NPV. An interval spanning
zero motivates targeted information acquisition. That extension could be a
substantive study, but needs an acquisition-cost objective, action-loss metrics,
specialized interval baselines and held-out task families. Generic financial
missingness and safe abstention already collide with
[Graph-Bounded Financial Reasoning](https://aclanthology.org/2026.acl-long.1273.pdf),
whose Sections 3.3–4 and 5.3 constrain evidence and test counterfactual entity,
time and metric mismatches. Robust optimization and value-of-information principles
also predate the proposed extension. No project observation yet motivates a
specific new method here. Retain it as a possible follow-on, not a deadline reset.

## Calibration against actual accepted workshop papers

The [official NeurIPS 2025 Generative AI in Finance accepted roster](https://sites.google.com/view/neurips-25-gen-ai-in-finance/accepted-papers)
confirms the following titles. This is a comparable distinct workshop, not a
historical Agenthon acceptance sample.

| Accepted work, full PDF inspected | Evidence scale and practical lesson |
|---|---|
| [Are Foundation Models Useful for Bankruptcy Prediction?](https://arxiv.org/abs/2511.16375), 14 pages | Compares one LLM and TabPFN with five conventional models across five horizons on matched 20,000-case test subsets. Includes output reliability and timing. A negative comparison can be substantive without a new model. |
| [FinAgentBench](https://arxiv.org/abs/2508.14052), cached v4, 6 pages | Separates document-type and chunk ranking with expert labels, standard ranking metrics, three commercial backbones and a fine-tuning comparison. The missing measurement, annotation quality and relevant baselines matter more than a novel architecture. |

The FinAgentBench PDF is a revised ICAIF-formatted arXiv manuscript; its title is
confirmed on the workshop roster, but its exact bytes are not confirmed as the
workshop submission. Its revised scale must not be mixed with older abstracts.
These accepted examples support an empirical audit contribution type. They provide
neither acceptance probabilities nor an excuse to omit consequential comparisons.

The listed [The Losing Winner](https://openreview.net/pdf?id=FzahgVWy59) is an
additional negative-study precedent. This pass encountered OpenReview's browser
challenge, so did not count it as a freshly read full PDF. The author's
[poster](https://tikatoka.github.io/data/69.pdf) and earlier access record support
its relevance, but the stronger scale comparison above uses accessible full papers.

## Access and reproducibility record

All cache paths below are under ignored `literature/pdfs/`. Existing source PDFs
were reused where present; FinVerBench and the original binomial paper were added.

| Source | Access in this pass | Cache / SHA-256 |
|---|---|---|
| FinVerBench v1 | Public arXiv HTML and full PDF; 37 pages | `finverbench-2605.29586v1.pdf`; `32dff1ee0a4177957b6225395eeca58c15b7ffd1114bbc7fc1066c3488aa9bd4` |
| FinanceReasoning ACL 2025 | Published full PDF; 29 pages | `financereasoning-acl2025.pdf`; `7edcadd778a4619b863247fe66a91b7d820115af367cf47bf6d05f72f353e60a` |
| FinChain ACL 2026 | Published full PDF; 25 pages | `finchain-acl2026.pdf`; `20a4d354b7e76b6ca7ce5de7ee29b60f831eae9b1d1ab6fcac3aadb77f7f11c9` |
| *Fair and cheap* | Official abstract and open-data README; no full manuscript | `fair-cheap-open-data-readme.md`; [reader gate](https://montanaresearch.org/download/paper/mrf-2026-04), [data-only record](https://zenodo.org/records/22285450) |
| Cox, Ross and Rubinstein 1979 | University-hosted author manuscript, full PDF; 34 pages | `crr1979-author-osu.pdf`; `750757cc67e1c48b8d39c61416e16253f9bc2567e862bdfe758c9537b90b02f3` |
| Bankruptcy prediction | Public arXiv full PDF; 14 pages | `workshop2025_bankruptcy.pdf`; `8b5c0783c1ab3733d2758136457d3dcfdafa3c5cf5674ae37654e8846775ae72` |
| FinAgentBench v4 | Public arXiv full PDF; 6 pages | `workshop2025_finagentbench.pdf`; `5385544cfe74d2304f5fe8091effc3d69cc42d38131fc26d558f1dd02813817e` |

No IU-gated source was needed for the three accessible nearest papers. The
unavailable *Fair and cheap* manuscript remains an explicit overlap limitation.
No legal agreement, paid compute, submission, email or public release was performed.

The [live Agenthon call](https://www.agenthon.net/#call-for-papers), rechecked on
September 29, still specifies September 30 at 23:59 AoE, October 1 at 13:59 CEST.
It welcomes evaluation, verification and benchmarks, allows short or full
non-archival papers, and presents accepted papers as in-person posters in Atlanta.
The proposed corpus audit fits that stated scope. An ambitious but precise empirical
submission is defensible if the priority experiments substantiate it; a concept-only
contract proposal is not the recommended outcome.
