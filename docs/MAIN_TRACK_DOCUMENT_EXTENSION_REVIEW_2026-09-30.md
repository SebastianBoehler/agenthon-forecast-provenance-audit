## Executive summary (read this first)

**Proceed as a falsification and diagnostic study; a stronger main-track contribution
remains conditional on what it finds.** Adding 48 FinQA and 48 TAT-QA cases, correcting
labels, or adding a quantity/unit reminder alone is incremental. The highest-value
question is whether *native scoring disagrees with independently established financial
validity even when source annotations are correct*, and whether a traced correction
fixes that disagreement without admitting financially wrong answers. Distinguish
annotation, question identifiability and evaluator behavior before assigning blame.

This review read the frozen protocol/configuration, readiness/reproduction reports,
existing novelty reviews, relevant primary full-text sections and pinned evaluator
code. It did **not** open `source_targets.jsonl`, either reviewer packet, or any selected
question content. No case was calculated, labeled, adjudicated or sent to a model.
The later blinded AI technical review is a separate ongoing stage, not completed human
expert review. Recommendations here do not amend any frozen protocol or result.

### Why these sources help, and what they do not establish

The [prepared cohort](FINANCE_DOCUMENT_AUDIT_READINESS_V1.md) comprises 48 FinQA
company/year report groups and 48 TAT-QA raw context UIDs. All selected exact contexts
are distinct; TAT-QA report identities and cross-source underlying-report overlap
remain unknown. Question-first hash ordering with a one-per-group cap is not uniform
report sampling. Future fractions describe this fixed selected set, not prevalence
in finance QA, all public-test rows, or independently sampled reports.

[FinQA](https://aclanthology.org/2021.emnlp-main.300.pdf) and
[TAT-QA](https://aclanthology.org/2021.acl-long.254.pdf) describe separate financial
annotation pipelines and evidence/program or derivation annotations. They add real
document grounding beyond the synthetic audit. Neither is thereby a verified RLVR
training-reward release. Public questions may be memorized by models; “held out”
means excluded from this experiment's adaptation/selection, not unseen in pretraining.
The TAT-QA raw/gold UID mismatch requires the already frozen exact question/context
join. Version mismatch alone is not a bad financial label.

### Direct prior-art collisions, checked in primary full texts

| Work and inspected sections | What is already occupied | Remaining conditional distinction |
|---|---|---|
| Tang et al., [FinanceReasoning, ACL 2025](https://aclanthology.org/2025.acl-long.766.pdf), §2.1, Table 1, Appendix C, Limitations | Reannotates CodeFinQA and CodeTAT-QA, separating answer corrections from question disambiguations; specifies units/signs/precision and a 0.2% margin. Table 1 reports 55 corrections/58 disambiguations among 795 CodeFinQA test cases, and 19/9 among 288 CodeTAT-QA cases. Perfect-information evaluation and proactive clarification are distinguished. | A blind audit of native sources and actual scoring layers could isolate causes that joint question/label/evaluation revisions do not isolate. Mere correction of these same source families is a direct collision. |
| Koncel-Kedziorski et al., [BizBench, ACL 2024](https://aclanthology.org/2024.acl-long.452.pdf), §3.1, Appendix A, Limitations | Python reformulations of FinQA/TAT-QA; code correctness inferred from answer agreement can admit wrong solutions or reject correct ones. CodeTAT-QA is a table-answerable subset, not the entire hybrid task. | New evidence must establish an actual mechanism and consequence beyond this explicitly recognized limitation. Program output agreement is not a new verification insight. |
| Xie et al., [FinChain, ACL 2026](https://aclanthology.org/2026.acl-long.662.pdf), §3.2, A.3, B.2 | Precision, unit consistency, incomplete inputs and representation errors are explicit validation categories; A.3 identifies displayed rounding versus hidden full precision. | Do not claim a first contract layer or first units/rounding audit. Native document-source/evaluator attribution is a different setting, not automatic novelty. |
| Panda, [FinVerBench v1](https://arxiv.org/html/2605.29586v1), §§3.5, 6.4–6.5, 7.2 | Hidden-field positives become insufficient-information cases; omitted statement components cause false alarms; realistic rendering changes verification performance. | Our hypothesis concerns original QA annotations and native acceptance of independent answers, not generated statement-error detection. Observability and partial-context mechanisms themselves are established. |
| Chang et al., [Measurement Risk v2](https://arxiv.org/html/2604.27374v2), §§4–5, 7–9 | Separates inference/rubric stimulus from scoring/aggregation; financial labels and rankings depend on evaluation policy; provenance and claim limits are audited. | A numerical, source-grounded mechanism can add evidence; generic financial metric/ranking sensitivity cannot be claimed new. This is the author preprint, not an independently compared IEEE final version. |

CodeFinQA/CodeTAT-QA are derivatives of these native sources. FinanceReasoning or
BizBench overlap must be checked by original IDs/context/question provenance later,
without selecting against known corrections. Do not count those derivatives as
additional producers or call previously corrected examples new defect discoveries.
The [earlier novelty assessment](INDEPENDENT_NOVELTY_REASSESSMENT_2026-09-29.md)
also records direct answer-determinacy overlap with *Fair and cheap*; its gated full
manuscript remains unread. This is targeted collision checking, not proof of firstness.

### Native scoring semantics independently verified

Sources are pinned to FinQA `0f16e2867befa6840783e58be38c9efb9229d742` and TAT-QA
`870accc41953dcde885aabeb963d94aabdc0fbc3`. Code was fetched directly from first-party
raw URLs into memory; no selected corpus or upstream evaluator was executed.

**FinQA:** [evaluate.py](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/code/evaluate/evaluate.py)
executes its restricted tokenized program, converts `%` operands to fractions,
rounds the final numerical result to five decimals and exactly compares it to
`qa.exe_ans`. Symbolic program equivalence is a separate endpoint. `process_row`
strips currency/parenthetical suffixes; these parsing rules warrant authored boundary
controls but do not establish selected-case faults. The batch evaluator iterates
prediction entries and divides by their count: enforce all unique cohort IDs outside
it to prevent omitted/duplicate predictions altering the denominator. This is a
pipeline integrity control, not a presumed financial defect.

An answer-only JSON study cannot claim native FinQA program accuracy. A scalar
comparator reproducing its final numeric equality is an **adapted execution-answer
condition**. A `calculation` string is not an official DSL program. Keep actual
program execution/equivalence, stored answer consistency and independent validity
as different tests. Do not insert the source answer into a fabricated program.

**TAT-QA:** [tatqa_eval.py](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/tatqa_eval.py)
expects UID-indexed answer/scale pairs and iterates gold questions; missing predictions
receive no credit. [tatqa_metric.py](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/tatqa_metric.py)
normalizes numerical answers, including two-decimal rounding before scale multiplication;
an additional percent path permits some fraction representations without a scale.
Arithmetic/count F1 equals exact match; scale accuracy is separate.
[tatqa_utils.py](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/tatqa_utils.py)
defines scale factors, accounting-parenthesis signs, percentage conversion and
four-decimal numeric normalization. Preserve every stage and the scale channel.

These are intended scoring conventions, not proven bugs. Rejecting an output outside
the declared native format is not a native evaluator error. Review the complete
model-visible task, including global output instructions, before defining alternatives.
An adapter that incorrectly converts percentages or monetary scale can manufacture
disagreement; test it separately from the native metric and semantic oracle.

### Falsifiable central hypothesis and attribution

**Proposed H:** On both native sources, a nontrivial subset of identified numerical
tasks has a native acceptance boundary inconsistent with the independently frozen
quantity/unit/precision contract, after faithful interface adaptation and annotation
consistency checks. Correcting labels alone leaves this disagreement; a frozen
contract-aware rule reduces it while retaining rejection of matched invalid controls.

This is a hypothesis, not a discovered mechanism or a new general verifier. The
strongest possible evidence would trace the same *failure principle* across sources
with different interfaces, show it on source-correct cases, reproduce it through
controlled transformations, and explain why label replacement or tolerance widening
does not resolve it. A normalization edge case alone is a software diagnostic.
If effects are only known label errors, missing output conventions or an adapter
mistake, H fails and the study remains an annotation/measurement extension.

| Category | Required evidence and permissible claim |
|---|---|
| Identified answer, wrong label | Evidence fixes quantity/operands/units; adjudicated source target lies outside admissible answers. Numerical/program replay alone is insufficient. |
| Multiple plausible interpretations | Preserve each quantity-tagged alternative and its assumptions. One plausible source answer is not necessarily wrong; do not silently choose the source interpretation. |
| Missing evidence / nonidentification | Show which necessary fact is absent and how admissible completions differ. Do not invent hidden exact operands or certify a unique numerical gold. |
| Units/rounding representation | Separate equivalent economic value from explicitly required serialization. Printed reporting precision is not automatically an uncertainty interval; document that assumption. |
| Quantity/evidence grounding | Trace entity, period, table cell/text and formula to the requested financial object. Coincident final numbers cannot certify a reasoning trace. |
| Native evaluator discrepancy | Reproduce actual pinned scoring after a faithful adapter, with an independently settled contract. Separate documented design choices from implementation/specification violations. |

Acceptable answers need structured quantity, value or discrete alternatives/interval,
unit, scale, precision, assumptions and evidence locations. Do not replace disconnected
interpretations by their min/max convex hull, or use a broad tolerance to hide an
unresolved question. Reviewers must freeze these records before seeing gold/derivation
or each other's sheets. Afterward preserve disagreements, use a separate adjudicator
and report unresolved cases. Independent AI processes remain technical checks with
possible shared errors/memorization; they do not constitute human financial expertise.

### Decisive endpoints and controls

Add a prospective scoring/analysis amendment before unblinding targets or observing
model outputs; retain the existing selection and review freezes. Keep all 48 per
source, including clean, ambiguous, unresolved and nonnumeric FinQA cases. A strict
numeric response cannot solve a native yes/no task; record output-schema ineligibility
from blind review before responses, rather than call that a model or label error.

1. **Audit endpoint:** source-specific counts of identified/correct, identified/wrong,
   ambiguous, insufficient, schema-ineligible and unresolved cases, with separate
   answer/derivation/execution consistency. Freeze attribution rules before gold.
2. **Paired scoring endpoint:** on each saved answer, independent validity versus
   native/adapted credit, separating false rejection of valid answers from credit
   to invalid answers. Keep conditional denominators and unresolved totals visible;
   publish conservative bounds when adjudication uncertainty changes the conclusion.
3. **Source-correct controls:** apply the same comparison to independently validated
   original annotations and ordinary passing cases. Source disagreements alone cannot
   isolate an evaluator mechanism. Include zero, negative, percentage and large-scale
   values in clearly labeled *researcher-authored* boundary tests, not released counts.
4. **Representation/financial mutations:** predeclare economic-value-preserving
   scale/percent/format alternatives only where the question permits them, and matched
   value-changing sign, factor-100/1,000, wrong-period/quantity controls. Hold numerical
   proximity fixed where possible; retain explicit-precision violations as invalid.
   Each variant inherits its case cluster and is not another independent observation.
5. **Repair comparison:** native scoring, label-only correction, declared tolerance
   widening and frozen typed/precision-aware comparison on the same responses/control
   bank. Track both error directions. Case-specific rules supplied by adjudicators
   establish manual audit practice, not automatic semantic validation or test transfer.
6. **Reference/evaluator mutation tests:** same native arithmetic expression must
   reproduce the stored result or report its failure; probe sign, rounding boundaries,
   percentage/scale serialization and valid equivalent expressions. Mutating a
   reference value or evaluator rule should change only the predicted scoring cases.
   Zero/missing/duplicate ID controls catch plumbing faults. Keep authored faults
   separate from evidence about faults in released questions.

### Proposed 384-answer intervention: useful, bounded

Two models × 96 questions × baseline versus a label-free quantity/unit/precision
reminder gives 384 responses if every case supports the frozen answer schema. A
strict JSON `value/unit/scale/calculation` wrapper must be identical across conditions;
freeze how null/abstention and nonnumeric answers are handled first. This is an
adapted answer study, not official FinQA program evaluation. The proposed fixed
DeepSeek V3.2/Qwen3.5-9B provider routes, reasoning-off, temperature-zero and 1,024-token
limit require execution manifests; a provider name or zero temperature does not
guarantee immutable weights or deterministic service behavior.

The primary measurement is financial/native-credit disagreement on identical saved
outputs. The reminder contrast is a separate prompt intervention: report parsing,
unit/scale, quantity grounding and numerical changes separately. Randomize/interleave
condition order, keep all failures, and prohibit target-conditioned retry/prompt
selection. Two checkpoints do not identify a size effect. Better formatting alone
is not improved financial reasoning; better source credit alone is not better truth.
This can strengthen an empirical extension, but does not demonstrate learning harm,
weight-training benefit, broad financial ability or new optimizer methodology.

### Meaningful evidence, stopping rule and limits

The 96 cases are a discovery/falsification cohort, not automatically a held-out test
of rules designed after its results. Any learned/general audit claim needs a frozen
rule tested on additional independent contexts/tasks or a later held-out source;
predeclare the smallest practically relevant effect and uncertainty analysis then.
Report per-source counts and paired effects first. FinQA report/company clustering
and TAT-QA's unknown report dependence preclude pretending 384 answers are 384
independent samples; context-level descriptive sensitivity is not population certainty.

**No-fault result:** if source targets are valid and native decisions agree after
faithful adaptation, report that comparison evidence. It weakens the proposed
cross-source failure hypothesis and prevents extrapolation from the synthetic audit.
Do not replace clean cases, cherry-pick disagreements or manufacture native prevalence
from authored perturbations. Ambiguity without wrong labels is a separate finding.

A substantial contribution requires a consequential, independently checked mechanism,
controls ruling out simpler explanations, and a transferable explanation or procedure
beyond the cited corrections and metrology precedents. Training is not mandatory for
a strong empirical insight; it is mandatory evidence for a training-consequence claim.
Merely adding datasets, reviewer agreement or reminder gains does not meet that bar.
Human domain adjudication, source overlap, publication notices and model contamination
remain material boundaries. This review does not decide publication eligibility or
main-track acceptance.

### Verification record

The four first-party code SHA256 hashes fetched in memory were:

| File | SHA256 |
|---|---|
| FinQA `code/evaluate/evaluate.py` | `845cd131cab843eceff256cf6d392978cc470a7da4a80107beb56027fdca5c13` |
| TAT-QA `tatqa_metric.py` | `2aeeac479f89f8c76300af1cc0e8d098eb86af84bc386b38b6ab4af484a6dea8` |
| TAT-QA `tatqa_utils.py` | `a84bb2f960737cf0a53733637a674cc4b20ef030a2be6a4b21dc2c4356f415ec` |
| TAT-QA `tatqa_eval.py` | `a4110626c477e7ed88f42b5edeb8449eaa9a4370740a627631b4a462bcf43762` |

Existing local primary text copies read: FinanceReasoning
`c24f795739f52517d9c3f233e37b7a3abc6f7ffb090430f40c538362d2e090ad`,
FinChain `bcbca9a2942b474e46de4a9d8e8e9f28cdbee4124db7884d8acad02705410a2d`,
FinVerBench `f08ab35cc0b4949d356d83353f3dba55ca4469135d07e83eecad1b1133179ee6`.
BizBench PDF and Measurement Risk v2 relevant full-text sections were read online.
No full-text exclusivity/firstness search, new adjudication, evaluator execution,
inference, spending, contact, manuscript edit or submission occurred.
