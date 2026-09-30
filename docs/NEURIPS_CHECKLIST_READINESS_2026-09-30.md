## Executive summary (read this first)

This is a **voluntary workshop readiness audit**, not a completed official
submission checklist or an attestation of NeurIPS compliance. The current paper
supports its narrow audit claims and discusses substantial limitations. Public
artifact access, complete licensing and complete compute reporting remain
incomplete. A later source check below verifies the added two-sided impact
discussion and closed V1 transfer results. Qualified financial adjudication has
not occurred.

All 16 questions in the actual 2026 template are covered below in their original
order, with proposed answers and bounded justifications; item 9 remains unresolved.
The initial snapshot is retained below; the later consistency note records
specific changed answers, closed V1 and stopped partial V2. V2 generated outcomes
were not read, and the manuscript was not edited or compiled.
No rendered nine-page compliance, submission, acceptance or ethics approval is
claimed. A No is a disclosure of a gap, not an acceptance prediction.

## Official source and inspected snapshot

The [current official CFP](https://neurips.cc/Conferences/2026/CallForPapers)
links the [2026 template ZIP](https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip).
Its cached local copy is `outputs/neurips-format-2026/official-template.zip`,
SHA-256 `82473931e3ef710fcd3f4a8cd4119b9de32e56825f90f9e5a6d55f2d01b817d9`.
`outputs/neurips-format-2026/checklist.tex` is byte-identical to the ZIP member;
SHA-256 `780ba13c480f652dcc42e69ed61a752ce0ea270f15d332d4a45b059dabad84f6`.
Its 16 question entries and all guidelines were read, not inferred from an older
year or a generic checklist.

The [2026 handbook, V2026.3](https://neurips.cc/Conferences/2026/MainTrackHandbook)
requires an official checklist for a main-track submission. Agenthon's
[workshop CFP](https://www.agenthon.net/#call-for-papers) does not state that
requirement; its rules remain the actual submission route. See the verified
[format comparison](SUBMISSION_FORMAT_2026-09-30.md). For a real main-track paper,
use the unchanged official questions/guidelines and answer macros after supporting
material; this Markdown paraphrase is not a substitute.

Official pages were checked September 30, 2026. Local snapshot checks finished
at 10:33:45 UTC. The inspected manuscript is `paper/answer_contract_audit.tex`,
SHA-256 `4ab67499614e95ac62ba258ab91a50184b74bc085274ec1707b37e3cda8a1af9`.
Its embedded style matches the official style exactly, SHA-256
`c3fc2894e83d2517ca18b66741d6c595986d97957dc08ec08bb2125a7ec4555a`.
The source has no completed checklist section. Source shortening does not prove
rendered page count. Later manuscript/results changes need a fresh consistency
check, especially for the transfer study and its separately versioned judge.

## Proposed answers to all official questions

Question descriptions below are concise paraphrases; the source above is
authoritative. Each item's specific official NA definition governs its use;
NA is not a blanket substitute for missing evidence or an experimental shortfall.

**1. Claim scope — Yes.** The abstract/introduction describe selected released
families, the debt-for-call and integer-rounding mechanisms, and grading unchanged
answers; they do not claim training harm, representative prevalence or a new
general verification principle. The separately pinned source-generation link
remains explicitly unproven; do not upgrade a completed transfer panel into
financial-expert truth when adding it.

**2. Limitations — Yes.** The dedicated Limitations section and appendices explain
mechanism-driven selection, template dependence, convention uncertainty, AI-review
dependence, parser/provider confounds and unsuccessful branches. Their explicit
scope restrictions are supported by the preserved protocols and reviews.

**3. Proofs and theoretical assumptions — NA.** No new theoretical result is
claimed. Established valuation identities are cited and used as numerical checks;
their rate/input assumptions must remain visible, rather than treating empirical
agreement as a theorem about every financial question.

**4. Information sufficient for reproduction — No, currently incomplete for an
external reader.** Pinned inputs, exact formulas, saved-response ledgers and
successful local replays exist, but the current PDF does not itself deliver an
accessible complete set of exact commands, prompts, manifests and dependencies.
Supply the review artifact and a resolvable replay index; separate deterministic
saved-score verification from fresh inference on mutable API weights. Evidence:
[audit replay](ANSWER_CONTRACT_REPRODUCE.md), [model replay](MODEL_GRADING_REPRODUCE.md),
[tested extracted package](FINAL_ARTIFACT_REPLAY_2026-09-30.md) and
[document replay](FINANCE_DOCUMENT_REPRODUCE_V1.md). This is a delivery gap, not
a claim that the demonstrated local replay failed.

**5. Open code/data with reproduction instructions — No.** The artifact remains
local and the paper provides no live public study-code/data access point. Public
upstream sources and a local ZIP do not make our analyses openly available; review
access and public release are distinct, and full report contexts/weights are
excluded with acquisition prerequisites documented.

**6. Experimental settings — Yes for the completed reported studies.** Selection,
endpoints, prompts/formats, model/provider settings, precision, caps, optimizer
seeds and amendments are recorded in the methods, appendices and linked freezes.
No weight training is claimed. Retain the original discovery-stage calculation
confound and post-start judge amendment when incorporating new results.

**7. Statistical uncertainty/significance — No.** The paper reports finite census
counts and paired decisions, without confidence intervals, error bars or formal
significance tests. Rows sharing templates/reports and repeated outputs are
dependent, and family selection is not population sampling; attaching an iid
binomial interval to 12,655 rows would create misleading certainty. This No is
appropriate disclosure, not a demand for invented intervals. Any later inference
needs an explicit estimand, independent grouping and justified variability model.

**8. Per-experiment compute — No, incomplete.** The later source includes
Appendix `app:compute-accounting`, supported by the
[closed-study inventory](CLOSED_STUDY_COMPUTE_ACCOUNTING_2026-09-30.md). It records
MPS/FP16, local hardware/runtime details, token totals, measured collection spans,
overlapping request latencies, failed runs, API-reported charges and conservative
unknown-billing debits. Complete preliminary/project-total accounting and
continuous memory/power measurements remain absent; remote accelerator
specifications and some charges are unavailable. This is substantial partial
reporting, not complete resource disclosure or a claim that missing costs are zero.

**9. Code-of-Ethics conformity — unresolved (Yes/No/NA awaits the author's own
review).** The
[official Code](https://neurips.cc/public/EthicsGuidelines) was read for this AI
audit; the human author's review state is unknown. The official item defines NA
as the authors not having reviewed the Code, so unavailable attestation alone
does not justify assigning NA. After that review, Yes requires a justified
conformity statement; No requires explaining any deviation. This remains a
voluntary readiness question, not a permission gate, finding of misconduct or
ethics approval; asset-term documentation also remains incomplete.

**10. Positive and negative broader impacts — Yes at the later snapshot.** The
actual `Broader implications` paragraph explains accountability benefits and the
harm of applying numerical patches without preserving assumptions, units or
legitimate conventions: defensible answers can be erased and new grading errors
introduced. It limits patches to numerical research evidence and leaves effects
on trained models/downstream financial decisions unmeasured. The initial
10:33:45 UTC snapshot lacked this paragraph and received No; that historical
assessment is not retrospectively changed into an earlier Yes.

**11. Safeguards for high-risk releases — NA.** No new trained generative model,
weights, high-risk personal dataset or sealed competition answers are released.
The artifact's exclusion rules for credentials, full third-party contexts and
protected competition/private course materials still matter; this answer does
not waive provenance, security or licensing checks.

**12. Existing-asset attribution and terms — No, incomplete.** Original producers
are cited, synthetic cards declare MIT and pinned notices are retained. However,
FinQA inherited report/FinTabNet notices, TAT-QA code versus dataset terms and its
historical wording discrepancy remain explicit unknowns; a complete model/API/
code/data term matrix is not in the paper/package. See the
[source protocol](FINANCE_DOCUMENT_AUDIT_PROTOCOL_V1.md). No unqualified corpus
redistribution permission or legal violation is inferred from these unknowns.

**13. Documentation accompanying new assets — No, not fully release-ready.** The
local protocols, claim graph, patches, deviations and replay instructions are
substantial companion documentation. Explicit release terms for newly authored
code/derived assets and the complete final inventory/access path are still
unresolved; no root project LICENSE was found in the inspected workspace. Document
intended use, limitations and upstream restrictions before calling the package a
fully documented released resource. A new benchmark or formal ARA compliance is
not claimed.

**14. Human/crowdsourcing instructions and compensation — NA.** No human-subject
or crowdsourcing experiment was performed. AI technical reviewers and blank human
review packets are not completed human expertise or paid participant labor.

**15. Human-participant risks and IRB/equivalent review — NA.** There were no
human research participants in these studies. No IRB approval or institutional
ethics assessment was obtained or implied; a later human study would need its own
applicable procedure.

**16. Substantive LLM use — Yes.** Methods/appendices disclose generated answers,
prompt adaptation, AI technical references and assisted analysis/implementation,
including correlated-error and prior-exposure limits. These uses affect the
research, not only wording. The later snapshot names the same-model judge and
its V1/V2 amendments/limitations; do not portray agents as authors or financial
experts. The [2026 author policy](https://neurips.cc/Conferences/2026/MainTrackHandbook)
keeps responsibility with the human author.

## Actions ranked by practical value

1. Deliver an inspectable, correctly inventoried review artifact and exact replay
   index. Keep unchanged historical archives separate from the current package;
   audit source reconstruction, saved-score replay and fresh inference separately.
2. Complete the asset/license matrix and remaining compute gaps. The added impact
   paragraph and available compute inventory are verified below; preserve unknown
   costs/hardware and third-party access restrictions.
3. Keep qualified adjudication explicitly pending. It is not an official universal
   requirement to recruit experts, but AI reference/judge agreement cannot support
   an expert-semantic accuracy claim. Retain uncertain cases and distinguish
   quantity grounding from numerical/unit matching and native conventions.
4. Preserve the closed V1 transfer results and the stopped partial V2 judge stage.
   Retain unstarted attempts and unknown billing. Neither matching grammar nor a
   corrected pointer instruction establishes improved quantity selection itself.

## Later consistency check: closed V1 and V2 status updates

The canonical source was rechecked September 30 at **11:06:37 UTC**, SHA-256
`e9631b1cdf726050c1f58e92ccf2e8628d879ea6587f67c2b726300552dcfe1c`.
This is source inspection, not rendered page-count or compilation verification.
The original snapshot/hash above is retained. V2 generated outcomes were not
opened; pending status is supplied by the study lead, not inferred from V1.

The shorter abstract retains the synthetic census and 55/136 strict denials.
Discovery-document protocol/full endpoints now appear in the existing appendix;
the main text presents the unused-group test. No new-method, training-harm,
reminder-efficacy, expert-reference or contamination-free claim is established.
Items 6/16 have explicit closed V1 settings/AI-judge disclosures, without making
the pending V2 diagnostic a completed result. Item 9 stays unresolved.

In-paper count identities reconcile 12,655 rows and 10,476 questions counted within
family; 5,935 rational checks; 48 quantity plus seven rounding denials = 55;
800 original answers, 200 separate Gemma answers and 432 GEPA heldouts. Discovery
retains 96 cases/384 attempts and 62 numerical readings plus 34 other cases.
The local pilot retains 256 attempts = 141 successes plus 115 failures. Transfer
retains 32 cases = 22 eligible plus ten uncertain, and 64 answers plus 64 judges.
Its reported pairs are 13 both/one baseline-only/zero reminder-only/eight neither,
giving **14/22 versus 13/22**. Expression pairs are 17 both/one per arm/three
neither, giving **18/22 in each arm**; within-arm additions are four/five. No
numerical count conflict was found. All 23 labels are unique and all 22 `ref`/
`eqref` occurrences resolve; this is a source check, not visual layout assurance.

Three material clarifications were identified in these snapshots and resolved
by the final source check below; none required changing frozen data:

1. **Version/status visibility.** The transfer table does not name V1. At the
   11:06 snapshot, V2's present-tense description did not explicitly state pending
   status; the closure update below verifies its partial stop disclosure. Label
   the table V1 and make planned versus attempted V2 scope explicit. Preserve
   the post-V1-start, pre-selected-output-inspection amendment provenance.
2. **Endpoint comparability.** Discovery uses broad units and relative allowance
   `10^-7`; transfer uses typed units and `10^-4`, with the same absolute floor.
   The relative component is three orders larger. These documented endpoints are
   different; the main table should explicitly discourage interpreting 14/22
   versus old 25/62 as improvement. Within-V1 baseline/reminder comparisons share
   their endpoint, and neither the cohort change nor tolerance changes prove repair.
3. **Numerical agreement versus grounding.** Main text reports 60/64 judge parser
   failures, while the appendix records 62/64 effectively unassessable and no
   assessable verdict on the 44 eligible instances; 62/64 candidate evidence lists
   also fail the separate type-aware audit. Bring the effective failure and zero
   eligible grounding verdicts into the main paragraph. The 18/22 interpreter
   matches demonstrate agreement under the provisional numerical endpoint, not
   successful pointer grounding or repaired financial quantity selection.

At **11:09:40 UTC**, source SHA-256
`22d0cf1c4f273798581edce4579998305c17ff4e63bc090cd56650cac8e94aa9`
adds the stopped V2 scope: **23** attempted judgments, **22** returned judgments
plus one HTTP 502 without billing metadata, and **41** planned judgments
unstarted. The observed prefix is FinQA-only; no TAT-QA or full-cohort judge
performance is claimed. These are source/lead-supplied accounting facts, not an
independent replay of selected V2 verdicts; those outputs remained unopened.

The source correctly preserves V1 and explains that missing billing stops
further calls. It reports **USD 0.061335771 known**, plus **USD 0.002311197
reserved** = **USD 0.063646968 accounted**, and explicitly denies a complete
observed-invoice interpretation. No complete project-cost claim was found.
At that snapshot the appendix said “It rejudges all 64 saved answers” before
the 23-attempt stop disclosure. Replace that sentence with planned scope, e.g.,
“It was planned to rejudge all 64 saved answers.” This resolves a completion
implication without changing any results. Items 8/9/10 remain No/unresolved/Yes.
The first two inspected hashes/times above are historical checks, not final-PDF
or current-after-every-edit certification. Compilation remains unverified here.

The **11:12:50 UTC** source check, SHA-256
`17719e28e62e15cd9f4fa48fc6b6636c3978fbf8bba3e9d479f443fc92b9bf0b`,
verifies all three corrections: the table names V1; the main paragraph explicitly
distinguishes discovery/transfer tolerances and avoids common-accuracy comparison;
the main text states 62/64 effective unassessable judgments, including every
eligible candidate; and V2 is **planned**, rather than claimed completed, over
64 answers. Partial V2/unknown-billing limits remain explicit. No further material
count/claim contradiction was found in this targeted source check. Twelve
in-paper count/accounting identities pass; this does not replace independent
raw-result validation, qualified adjudication or compilation/rendered review.

For actual main-track submission, the official checklist, anonymous review assets
and measured rendered format are additional formal gates. For this workshop they
remain a voluntary rigor/format target; no question here assigns an acceptance
probability or replaces Agenthon's own requirements.

## Final source binding

The final native-compiled source is bound by
`outputs/submission-iteration-20260930/semantic_transfer_manuscript_check.json`,
created at 11:20:24 UTC. Paper SHA-256:
`c938578de9ea9a227dcd54aef1ab132d3657dc1e24b509b0a512f27cd200421a`.
It verifies 29 unique cited bibliography entries, no unresolved references, the
unchanged official style, sole-author preprint mode and the corrected hash-bound
semantic-review figure. Later additions retain the partial judge counts, enum/
rationale disagreement, measured tokens/timing and incomplete observed billing.
The native compiler succeeds; rendered page count remains unverified.
