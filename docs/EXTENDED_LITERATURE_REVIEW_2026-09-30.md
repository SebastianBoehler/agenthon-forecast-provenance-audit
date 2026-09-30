## Executive summary (read this first)

The strongest additions to the current paper are Northcutt et al. on test-label errors, Bowman–Dahl
on annotation validity, and Knight–Leveson on independence assumptions, with the latter's full-text
access limitation stated below. Add Skalse et al. if discussing potential reward misalignment. For
the planned document-QA extension, cite the original FinQA/TAT-QA papers and PoT/PAL as established
program-assisted baselines. Frénay–Verleysen is useful taxonomy; the remaining surveys are optional
background, not evidence for this paper's measured defects.

These sources strengthen the motivation and narrow the contribution. Label-error audits,
ambiguous-answer handling, nonrandom noise and offloading arithmetic to code are established. The
defensible contribution remains source-traced financial quantity/precision/rounding failures and
their bounded grading consequences. The unchanged-prompt GEPA pilot does not establish
optimization-induced harm.

This note independently checked primary sources outside the parent's IU EBSCO browser search. It is
not an EBSCO search log or a systematic review. Eleven candidate full texts were accessible,
sometimes as author-posted versions; one candidate was inspected only through primary
bibliographic/abstract records. No manuscript, frozen artifact or bundle was edited. Full texts are
local in ignored `literature/pdfs/extended-20260930-*`, not redistributed with this note.

## Verified candidates and source roles

### 1. Test-label errors and unstable evaluation — add now

**Curtis G. Northcutt, Anish Athalye, Jonas Mueller.** *Pervasive Label Errors in Test Sets
Destabilize Machine Learning Benchmarks.* NeurIPS **Datasets and Benchmarks** 2021, round 1; not the
main conference track. [Official
proceedings](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/f2217062e9a397a1dca429e7d70bc6ca-Abstract-round1.html).
**Access:** official proceedings PDF inspected, 13 pages.

The paper audits naturally occurring test-label errors across ten image, language and audio
datasets, screens candidates algorithmically and validates corrections with humans. Sections 4–5
distinguish original and corrected accuracy. Crucially, full-benchmark rankings are largely
unchanged after correction; pronounced changes occur on correctable-error subsets and when their
prevalence is increased. Corrections are explicitly imperfect even with unanimous annotator
agreement (PDF pp. 2, 6–9). **Collision/limit:** a label audit plus a ranking reversal is not itself
new. Their categorical human-label study is not a financial answer-contract audit, and its error
rates cannot be transferred to our sources. Cite it beside the bounded family-level reversal,
preserving the subset and comparator qualifiers.

### 2. Probabilistic label-error detection — background, not a ready baseline

**Curtis G. Northcutt, Lu Jiang, Isaac L. Chuang.** *Confident Learning: Estimating Uncertainty in
Dataset Labels.* JAIR **70:1373–1411**, 2021. [Publisher, DOI
10.1613/jair.1.12125](https://jair.org/index.php/jair/article/view/12125). **Access:** final JAIR
PDF inspected, 39 pages; publication header verified.

Section 2 assumes a latent categorical true label, independent class-conditional corruption and
observed error-free inputs. Section 3 uses out-of-sample predicted class probabilities to estimate
the noisy/latent-label joint distribution (PDF pp. 3–6). **Collision/limit:** label-error
identification is established, but this estimator does not directly supply a numeric finance oracle.
Our input rounding, multiple acceptable answers and shared generator bugs do not automatically
satisfy its assumptions. Do not discretize prices and call cleanlab an adequate control without
validating that new measurement model. Include only if contrasting detection assumptions with
source-grounded recomputation.

### 3. Nonrandom label noise — useful if the main-track paper claims structure

**Benoît Frénay, Michel Verleysen.** *Classification in the Presence of Label Noise: A Survey.* IEEE
TNNLS **25(5):845–869**, 2014. [DOI
10.1109/TNNLS.2013.2292894](https://doi.org/10.1109/TNNLS.2013.2292894), [institutional
publication/peer-review
record](https://researchportal.unamur.be/en/publications/classification-in-the-presence-of-label-noise-a-survey/).
**Access:** [author-posted
manuscript](https://bfrenay.wordpress.com/wp-content/uploads/2014/08/classification-in-the-presence-of-label-noise-a-survey.pdf)
inspected, 26 PDF pages; journal metadata separately verified. Cite manuscript sections rather than
silently treating its pagination as the final journal pages.

Section II identifies insufficient information, labeling mistakes, subjectivity and encoding
problems; its taxonomy already includes class- and feature-dependent noise. Section II-A assumes
stochastic, mutually independent labeling errors. **Collision/limit:** “first structured noise” and
“first labels inconsistent with available information” are untenable broad claims. Shared
computational faults are not necessarily independent stochastic label flips. This survey motivates
explicit mechanism and dependence descriptions, not a claim that our faults instantiate its model or
that classical noise-robust classifiers repair them.

### 4. Dataset construction and gold-label interpretation — optional background

**Amandalynne Paullada, Inioluwa Deborah Raji, Emily M. Bender, Emily Denton, Alex Hanna.** *Data
and its (dis)contents: A survey of dataset development and use in machine learning research.*
**Patterns 2(11):100336**, 2021. [Publisher DOI](https://doi.org/10.1016/j.patter.2021.100336),
[author record and version](https://arxiv.org/abs/2012.05345). **Correction:** this is not a *Big
Data & Society* article. **Access:** author preprint v1, December 2020, full text inspected;
publisher PDF returned HTTP 403. Publication identity is verified; final-text changes were not
compared.

Section 3.4 discusses annotation as interpretive work, the distinction between gold labels and
ground truth, documentation and reproducibility. It provides context for reviewing labels against
task meaning rather than treating annotation as an unquestionable oracle. **Limit:** a survey's
general critique neither demonstrates a defect in FinQA/TAT-QA nor validates our repaired numerical
targets. Use one short motivation citation if useful; it is less direct than Northcutt or
Bowman–Dahl.

### 5. Reliable, unambiguous NLU evaluation — add now

**Samuel R. Bowman, George Dahl.** *What Will it Take to Fix Benchmarking in Natural Language
Understanding?* NAACL-HLT 2021, **4843–4855**. [Official ACL record, DOI
10.18653/v1/2021.naacl-main.385](https://aclanthology.org/2021.naacl-main.385/). **Access:**
official conference PDF inspected, 13 pages; published position paper.

Sections 3.2 and 4.2 distinguish mislabeled examples, unclear guidelines and legitimate
disagreement; they discuss validation and alternatives to assigning one discrete label to ambiguous
examples. Sections 3.3/4.3 require adequate statistical power (PDF pp. 5, 7). **Collision/limit:**
information-sensitive acceptable answers and annotation validity are established evaluation
concerns. Our contribution must be their concrete financial instantiation and measured consequences.
This paper supports retaining ambiguity and insufficiency categories during independent review; it
does not prescribe our intervals, cent boundaries or financial conventions.

### 6. General benchmark claims and construct validity — optional, avoid redundancy

**Inioluwa Deborah Raji, Emily Denton, Emily M. Bender, Alex Hanna, Amandalynne Paullada**
(proceedings author order). *AI and the Everything in the Whole Wide World Benchmark.* NeurIPS
**Datasets and Benchmarks** 2021, round 2; published position paper, not the main conference track.
[Official
proceedings](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/084b6fbb10729ed4da8c3d3f5a3ae7c9-Abstract-round2.html).
**Access:** official proceedings PDF inspected, 17 pages.

Section 2.3 separates reproducibility/reliability from whether the benchmark measures the intended
construct. The analysis challenges treating specific datasets and metrics as general capability
measures. **Role/limit:** supports the distinction between generator reproducibility and financial
validity, and the restraint against calling four templates “financial reasoning ability.” It is
conceptual context, not evidence about our releases. Choose it or Paullada for a short background
sentence; adding both is unnecessary.

### 7. Original financial document QA — cite when the extension is described

**Zhiyu Chen, Wenhu Chen, Charese Smiley, Sameena Shah, Iana Borova, Dylan Langdon, Reema Moussa,
Matt Beane, Ting-Hao Huang, Bryan Routledge, William Yang Wang.** *FinQA: A Dataset of Numerical
Reasoning over Financial Data.* EMNLP 2021, **3697–3711**. [Official ACL record, DOI
10.18653/v1/2021.emnlp-main.300](https://aclanthology.org/2021.emnlp-main.300/). **Access:**
official current ACL PDF inspected, 14 pages; conference identity verified.

Sections 3/4 describe executable reasoning programs, eleven finance-background annotators and
external professional checks on 200 examples. Section 3 already warns that execution accuracy can
reward chance numerical matches and program accuracy can reject alternative correct programs (PDF
pp. 3–4). **Collision/limit:** program-grounded financial QA and distinction between numerical
agreement and reasoning validity are established. This is an independently described annotation
pipeline, not evidence of a current RLVR reward implementation or new defects. The paper's
report-disjoint split claim does not establish disjointness between our selected FinQA and TAT-QA
packets.

### 8. Hybrid financial QA and explicit scale — cite when the extension is described

**Fengbin Zhu, Wenqiang Lei, Youcheng Huang, Chao Wang, Shuo Zhang, Jiancheng Lv, Fuli Feng,
Tat-Seng Chua.** *TAT-QA: A Question Answering Benchmark on a Hybrid of Tabular and Textual Content
in Finance.* ACL-IJCNLP 2021, **3277–3287**. [Official ACL record, DOI
10.18653/v1/2021.acl-long.254](https://aclanthology.org/2021.acl-long.254/). **Access:** official
conference PDF inspected, 11 pages.

Sections 2.2/2.3 describe finance-background annotators, scale and derivation annotations, and
checking/approval by two different verifiers. Section 3.3 models scale explicitly. Section 2.4
splits by hybrid context (PDF pp. 3–5). **Collision/limit:** units/scale handling and verification
are not new. A pair of distinct reviewers is a process description, not proof of statistically
independent errors. Context splits are not guaranteed report splits. These publications justify
document QA as a new empirical setting; our still-blank packets establish no label defects, expert
agreement or supervision/training effect.

### 9. Proxy reward versus true reward — add for a precisely bounded motivation

**Joar Skalse, Nikolaus H. R. Howe, Dmitrii Krasheninnikov, David Krueger.** NeurIPS 2022 main
conference, Advances in NIPS **35**. [Official
proceedings](https://proceedings.neurips.cc/paper_files/paper/2022/hash/3d719fee332caa23d5038b8a90e81796-Abstract-Conference.html)
titles it *Defining and Characterizing Reward Gaming*; the [official
PDF](https://proceedings.neurips.cc/paper_files/paper/2022/file/3d719fee332caa23d5038b8a90e81796-Paper-Conference.pdf)
is titled *Defining and Characterizing Reward Hacking*. Preserve this source discrepancy.
**Access:** official PDF inspected, 12 pages.

Section 4.2 defines hackability through opposite reward preferences over policies, relative to an
environment and policy set; Section 5 studies conditions on those sets. It supplies a formal
distinction between the reward proxy and intended return. **Collision/limit:** reward preference
mismatch is established. Rejecting a valid saved answer demonstrates grading error, not an optimizer
exploiting it. The unchanged-prompt pilot provides no observed proxy-improvement/true-performance
decline. Neither our comparator repair nor this citation proves an unhackability guarantee outside
the specified finite evaluation and financial assumptions.

### 10. Program of Thoughts — strongest prospective numerical-QA control

**Wenhu Chen, Xueguang Ma, Xinyi Wang, William W. Cohen.** *Program of Thoughts Prompting:
Disentangling Computation from Reasoning for Numerical Reasoning Tasks.* **TMLR, October 2023**.
[Official OpenReview publication](https://openreview.net/forum?id=YfZ4ZPt8zd), [author version
v4](https://arxiv.org/abs/2211.12588v4). **Access:** OpenReview full PDF was
browser-verification/HTTP-403 gated; author v4 full text inspected, with the TMLR publication
header. It is not merely an unreviewed 2022 preprint.

Section 3.1/Table 1 evaluates FinQA test, ConvFinQA test and TAT-QA **dev**. The controls include
direct answers, CoT and CoT-plus-calculator. Programs execute with Python/SymPy. Its metric section
relaxes FinQA CoT matching using relative tolerance 0.001 (PDF pp. 5–6). **Role/limit:** use a
frozen, matched program-assisted baseline for future document QA; do not assume published gains
transfer to our models. Apply the same grading policies to all strategies. Executable code can still
implement the wrong quantity, inputs or convention; it is not an independent correctness
certificate.

### 11. PAL — complementary established control, not finance-specific evidence

**Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan, Graham
Neubig.** *PAL: Program-aided Language Models.* ICML 2023, **PMLR 202:10764–10799**. [Official
proceedings and PDF](https://proceedings.mlr.press/v202/gao23f.html). **Access:** official
proceedings PDF inspected, 36 pages.

Section 3 interleaves natural-language decomposition and code, then delegates execution to an
interpreter. Experiments cover mathematical, symbolic and algorithmic tasks; PoT is the closer
financial-QA precedent. **Role/limit:** motivates separating calculation from interpretation and
making a program-assisted control cheap. Do not label an invented calculator prompt an exact PAL
reproduction. Match inputs, models, output budgets, exemplars and evaluation; record syntax/runtime
failures. Neither PAL nor execution solves ambiguity or guarantees that displayed precision supports
a unique numerical answer.

### 12. Implementation independence — valuable citation, access incomplete

**John C. Knight, Nancy G. Leveson.** *An Experimental Evaluation of the Assumption of Independence
in Multiversion Programming.* IEEE TSE **SE-12(1):96–109**, January 1986. [Publisher DOI
10.1109/TSE.1986.6312924](https://doi.org/10.1109/TSE.1986.6312924). **Access:** publisher-deposited
bibliographic metadata verified. IEEE presented browser verification; the author-hosted
`sunnyday.mit.edu/papers/nver-tse.pdf` timed out. The [official UVA 1985 technical-report record and
abstract](https://libraopen.library.virginia.edu/entities/publication/4ac33eeb-79b4-46e4-aef9-f6ec56a62286)
were inspected; **the journal/report full texts were not inspected**.

That primary abstract describes independently prepared versions of the same specification and more
coincident failures than independence would predict. **Role/limit:** motivates documenting actual
diversity of independently authored checks instead of assuming independence from separate
implementations or agents. Our generator/verifier reuse is a direct shared-computation mechanism,
not their experiment on independently written versions. Do not import their numerical failure rates
or claim they prove AI-assisted checks are correlated. Add the citation with this narrow scope;
fuller experimental interpretation needs full text.

## Consequences for the present paper and next protocol

Keep the existing financial comparators central: FinanceReasoning already repairs questions/labels,
FinChain covers precision/units and rounded inputs, and FinVerBench covers observability. The new
sources supply historical context and stronger controls; they do not remove those closest
collisions. See the existing primary-source [novelty
reassessment](/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/docs/INDEPENDENT_NOVELTY_REASSESSMENT_2026-09-29.md).

For future numerical/document experiments, the bounded comparison is direct answer, CoT and one
clearly specified program-assisted condition, optionally CoT plus calculator if needed to isolate
arithmetic assistance. Freeze one semantic contract, one source-comparator panel and matched
extraction rules across conditions. Keep the source gold/program hidden from independent annotation
and solver prompts; report ambiguous/insufficient cases separately. Establish independent financial
targets before interpreting source-versus-repaired scores. These are prospective controls, not
experiments conducted in this literature review.
