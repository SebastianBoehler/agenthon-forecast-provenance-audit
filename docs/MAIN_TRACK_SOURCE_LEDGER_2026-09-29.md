## Executive summary (read this first)

FinQA and TAT-QA are useful independent annotation pipelines for financial
document transfer. FinChain supplies a separate executable template pipeline and
is a necessary prior-art baseline. These are **three candidate sources, not three
verified reinforcement-learning releases or three completed audits**. No defects
are presumed. This ledger prepares Stage 2 of the
[main-track roadmap](MAIN_TRACK_RESEARCH_ROADMAP_2026-09-29.md).

For example, answering a ratio question from an annual-report table tests evidence
selection and scale interpretation beyond our current Gordon/binomial/WACC tasks.
Replaying its annotated program establishes consistency with the annotation;
it does not independently establish that the program answers the financial question.

Subsequent [document-packet preparation](FINANCE_DOCUMENT_AUDIT_READINESS_V1.md)
has selected 48 FinQA and 48 TAT-QA cases without correctness checks. It verifies
identical FinQA raw/evaluator inputs and replaces the proposed TAT-QA native-UID
join with a declared exact context/question join. The source observations and
prospective plan below describe the earlier ledger stage; no additional financial
answer audit or expert adjudication is established by this update.

Checked 2026-09-29 using first-party papers, repository files and complete GitHub
tree metadata. Small README, license and evaluator files were inspected in memory.
No corpus was downloaded, instantiated, scored or labeled; no model was called.
All corpus counts below are published counts unless explicitly described as tree
counts. The current pilot and its frozen artifacts remain separate.

## Roles and revision pins

RLVR means reinforcement learning with verifiable rewards: a program assigns a
training reward. A source annotation is an author's answer/program; having an
executable annotation does not establish a released RLVR reward implementation.
Producer independence means separate question/annotation or generation pipelines,
not merely a different repository name or different operand values.

| Source and canonical paper | Current default-branch revision, checked live | Proposed role |
|---|---|---|
| [FinQA, EMNLP 2021](https://aclanthology.org/2021.emnlp-main.300/), [czyssrs/FinQA](https://github.com/czyssrs/FinQA) | `main`, `0f16e2867befa6840783e58be38c9efb9229d742`, 2022-06-06 UTC | Human-annotated report QA; transfer benchmark and annotation audit candidate. |
| [TAT-QA, ACL 2021](https://aclanthology.org/2021.acl-long.254/), [NExTplusplus/TAT-QA](https://github.com/NExTplusplus/TAT-QA) | `master`, `870accc41953dcde885aabeb963d94aabdc0fbc3`, 2024-12-09 UTC | Human-annotated table/text QA; scale-aware transfer benchmark and annotation audit candidate. |
| [FinChain, ACL 2026](https://aclanthology.org/2026.acl-long.662/), [mbzuai-nlp/finchain](https://github.com/mbzuai-nlp/finchain) | `main`, `9bd2942b85d992844b77094a8b822aa16832703c`, 2026-09-17 UTC | Symbolic generation/trace benchmark; baseline and independent audit candidate, pending artifact admission. |

Revision dates are commit timestamps, not dataset collection dates. Live checks:
[FinQA commit](https://api.github.com/repos/czyssrs/FinQA/commits/main),
[TAT-QA commit](https://api.github.com/repos/NExTplusplus/TAT-QA/commits/master),
[FinChain commit](https://api.github.com/repos/mbzuai-nlp/finchain/commits/main).
Subsequent experiments must use the pinned hashes rather than moving branches.

## FinQA: annotated report reasoning

The authors used FinTabNet's S&P 500 reports from 1999–2019 and eleven financial
professionals to create questions, supporting facts and reasoning programs.
Published splits contain 6,251 training, 883 validation and 1,147 test questions;
input reports are disjoint across those splits. This offers evidence retrieval,
ratios, differences and multi-step arithmetic beyond the current four families.
[Construction and splits](https://arxiv.org/html/2109.00122v3).

Public artifacts are `dataset/train.json`, `dev.json` and `test.json`.
`private_test.json` contains questions without gold references and is excluded
from the proposed audit. Preserve `id`, report/page provenance, table, pre/post
text, `qa.question`, `program`, `program_re`, `gold_inds` and `exe_ans`.
The official program format ends in `EOF`; an answer-only model needs a declared
adapter, not an undocumented comparison with program accuracy.
[Pinned README/schema](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/README.md).

The [official evaluator](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/code/evaluate/evaluate.py)
executes a restricted arithmetic/table language, rounds a numeric final result to
five decimal places and compares it with `exe_ans`; symbolic program equivalence
is a separate score. `%` operands are converted to fractions by `str_to_num`.
This is neither our cent tolerance nor a uniform percentage-point contract.
The evaluator's `code/evaluate/test.json` and `dataset/test.json` have different
Git blobs: their exact row/schema correspondence needs a future check.

Repository [LICENSE](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/LICENSE)
is MIT. Dataset provenance has an additional layer: the paper describes FinTabNet
as CDLA-Permissive but its footnote links a CDLA sharing URL. Retain that statement
and inspect the actual upstream dataset notice before redistributing report
content; the repository's code license is insufficient evidence for every asset.
[Paper licensing statement](https://arxiv.org/html/2109.00122v3).

The README reports a **fixed** May 2022 preprocessing label-leak issue and corrected
baseline results. That historical repair is not evidence of a current label defect.
[Repair notice](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/README.md).

## TAT-QA: annotated hybrid contexts and explicit scale

The authors independently collected reports from annualreports.com, constructed
table/paragraph contexts and used financial annotators plus two-round verification.
Published splits are 13,215/1,668/1,669 questions in 2,201/278/278 contexts.
Splits separate contexts; do not upgrade this to a report-disjoint guarantee.
Annotations include answer type/source, scale and arithmetic expressions or count
derivations. This permits unseen evidence-grounding and scale tasks.
[Construction and splits](https://arxiv.org/html/2105.07624v2).

Use `dataset_raw/tatqa_dataset_{train,dev,test}.json` and the separate public
`tatqa_dataset_test_gold.json` released in January 2024. Join by source question
UID and retain the complete table/paragraph context and original annotations.
`dataset_tagop` heuristically adds facts/mappings; these are derived preprocessing,
not an independent human trace. TAT-DQA extends TAT-QA and does not count as another
independent producer.
[Pinned README](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/README.md).

The [official CLI](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/tatqa_eval.py)
accepts UID-indexed answer/scale pairs. Its
[metric](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/tatqa_metric.py)
normalizes numeric answers with scale, compares exact match and token F1, and
records scale accuracy separately. Arithmetic/count F1 equals exact match.
Scales include thousand/million/billion/percent; a percent-normalization path can
accept an unscaled fraction for a percentage answer. Preserve the explicit scale
channel and audit its interaction with numeric validity rather than imposing our
current literal `currency`/`percent` wrapper unchanged.

The [code license](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/LICENSE)
is MIT; the current README explicitly names dataset CC BY 4.0. The older paper's
abstract says noncommercial use. Record the documentation discrepancy and retain
the current dataset-specific notice; do not silently treat the MIT code notice
as the dataset license. No redistribution decision is made here.
[Dataset notice](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/README.md),
[older wording](https://arxiv.org/html/2105.07624v2).

## FinChain: executable templates and close prior art

The published ACL 2026 work covers 58 topics in 12 financial domains and evaluates
financial reasoning traces with ChainEval. Treat it as a baseline for executable
financial verification and step evaluation, not just a source to inspect for faults.
It already occupies much of the proposed broad symbolic-finance benchmark space.
[Published paper](https://aclanthology.org/2026.acl-long.662/).

The README describes 2,900 instances: five templates per topic and ten seeds per
template. The complete current Git tree has **59 Python files** under
`data/templates/`, not an independently checked 58-topic/290-template manifest.
No instantiated JSON/JSONL corpus or frozen train/dev/test/seed bank was found in
that tree. Reconcile the extra file and paper snapshot before claiming reproduction.
[Pinned tree](https://api.github.com/repos/mbzuai-nlp/finchain/git/trees/9bd2942b85d992844b77094a8b822aa16832703c?recursive=1),
[release description](https://github.com/mbzuai-nlp/finchain/blob/9bd2942b85d992844b77094a8b822aa16832703c/readme.md).

For example, the [NPV template program](https://github.com/mbzuai-nlp/finchain/blob/9bd2942b85d992844b77094a8b822aa16832703c/data/templates/investment_analysis/npv.py)
returns question/solution strings. Its helper randomly creates seeds and records
seed, ID, topic/subtopic and difficulty. Running it would create a new instantiation,
not recover a demonstrated official test split. Future reproduction requires a
frozen seed bank, generator hash, Python/runtime version, template identity and
printed-input precision. An independently derived financial answer must be separate
from replaying the generator's own trace. None was generated in this pass.

Current [ChainEval code](https://github.com/mbzuai-nlp/finchain/blob/9bd2942b85d992844b77094a8b822aa16832703c/chaineval/evaluate_predictions.py)
reads reference `solution` and `model_generation`, extracts step/final values,
aligns textual steps and checks numeric agreement. Constants are 5% final relative
tolerance and 15% step-value tolerance; numeric denominator is `abs(gold)+1e-4`.
They are not exact formula execution or our cent-level financial score. Unit words
such as thousand/million/billion enter extraction; there is no TAT-QA-style mandatory
scale field. Pin and test sign, near-zero, percentage, unit and trace parsing before
using these scores as training rewards. Current code imports embedding/BERTScore
models at module load; inspection did not import it or fetch model weights.

The [README license statement](https://github.com/mbzuai-nlp/finchain/blob/9bd2942b85d992844b77094a8b822aa16832703c/readme.md)
expressly covers original source code, ChainEval and templates under Apache 2.0.
It preserves third-party notices. A separate instantiated-data grant was not found;
record that unresolved field before publishing derived question/solution files.
Use the ACL 2026 citation despite the README's older submission wording.

## Independence, overlap and admission boundaries

FinQA and TAT-QA have separately described annotation teams/pipelines; FinChain
describes construction from symbolic templates. That supports candidate producer
independence. It does **not** prove record or document disjointness. FinQA's
FinTabNet reports and TAT-QA's annual reports may share company/year/pages; shared
financial formulas may also overlap Cosimo or FinChain. These are unresolved
overlap hypotheses, not measured duplicates.

Before admission, compare source IDs, report/company/year identity, normalized
tables/paragraphs/questions, operand tuples and economic formula families across
all sources, the old 200 questions and the new pilot. Cluster derivatives with
their parents. An aggregator, reformatted copy, heuristic trace or TAT-DQA extension
does not add an independent producer. Public test labels also mean that “unseen”
can mean unseen by our optimizer, not guaranteed absent from model pretraining.

Current status: zero additional sources independently audited; two distinct
document-transfer candidates; one additional executable-generation candidate.
The roadmap's two-additional-producer audit gate remains incomplete. Any claim
about multiple released RLVR training verifiers additionally needs another genuine
release, or a narrower claim. FinQA/TAT-QA cannot silently fill that category.

## Next blind selection step: prospective, not executed

1. Pin the listed revisions, dataset/evaluator blob hashes and notices in an
   admission manifest. Resolve raw-versus-evaluator test identity, TAT-QA UID joins,
   and FinChain's topic/seed/split discrepancy. Missing identity stays excluded with
   its reason logged; do not substitute a convenient downstream copy.
2. Freeze an eligibility classifier based only on question/context, source metadata
   and topic names: numeric financial questions with available public evidence;
   preserve ambiguous precision as an auditable category. It must not inspect
   computed correctness, defect flags or actor outputs. Separate quantity, scale,
   requested precision and reasoning complexity rather than infer them from reward.
3. Proposed first packet: 48 FinQA public-test questions and 48 TAT-QA public-test
   arithmetic/count questions, at most one per hybrid context and grouped by report
   where identity permits. Select by a published salted SHA-256 order, recording
   exclusions and tie rules. Keep both corpora entirely outside adaptation feedback.
   Fix eligibility and counts before selecting records; report shortfalls honestly.
4. For FinChain, first freeze six eligible topics outside the existing financial
   families by the same hash rule, then two seeds per each of five documented
   templates: prospective maximum 60 generated cases. These would be **our seeded
   instantiations of released code**, not the paper's recovered test set. Complete
   provenance/license gates before generating them; never pick seeds by validity
   or actor success. Hold out whole topics/templates, not only seeds.
5. Freeze selected IDs/context hashes, generator/seed hashes and the review rubric
   before independent financial recomputation or defect review. Two independent
   reviewers assess requested quantity, visible inputs, acceptable units/precision,
   answer set and trace; preserve disagreements. Technical AI checks do not replace
   qualified human financial adjudication. Passing cases remain in the denominator.
6. Only after adjudication, compare native released scores with independent financial
   validity, including clean controls. Proceed to larger training only if a mechanism
   survives an additional producer or held-out financial task. If defects remain
   confined to Cosimo, retain the case-study boundary. No second producer of verified
   training rewards is claimed on the strength of this ledger.
