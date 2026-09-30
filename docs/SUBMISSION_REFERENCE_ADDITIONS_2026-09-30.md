## Executive summary (read this first)

All four references have a specific role. CheckList is the closest addition for targeted behavioral controls; PAL is essential context for the saved-expression diagnostic and a future execution baseline. Datasheets and Pineau support the provenance and replay section. They narrow the novelty boundary: focused tests, interpreter assistance, dataset documentation and reproducibility reporting are established practices. The contribution remains the bounded, source-linked financial measurements.

This is a four-candidate primary-source check, not a systematic literature review or a submission-rule check. Full text was inspected for all four, with the Datasheets version limitation below. No manuscript, frozen study or inference was changed. Bibliographic metadata was checked against the linked official or author-institution records on 2026-09-30.

## 1. CheckList — targeted behavior, rather than aggregate accuracy alone

**Marco Tulio Ribeiro, Tongshuang Wu, Carlos Guestrin, Sameer Singh.** *Beyond Accuracy: Behavioral Testing of NLP Models with CheckList.* ACL 2020, pp. 4902–4912. DOI: **10.18653/v1/2020.acl-main.442**. [Official record](https://aclanthology.org/2020.acl-main.442/); [published full text](https://aclanthology.org/2020.acl-main.442.pdf).

**Inspected:** §§2.1–2.3, pp. 4903–4904; §3 task examples. The method organizes capabilities and test types: minimum functionality, invariance and directional expectation. It permits authored examples and perturbations; some tests assess relationships between outputs without a complete gold label.

**Supports:** motivating capability-specific numerical controls and preserving failure categories that an aggregate score conceals. Cite beside the distinction between quantity, rounding, representation and format tests.

**Does not support:** newness of behavioral testing, financial label correctness, representative defect prevalence, or the claim that our controls constitute a full CheckList evaluation. Inspecting source implementations is additional work, not this paper's black-box methodology. Our comparator changes are not automatically its input-invariance tests.

**Suggested claim-linked sentence:** “Targeted behavioral tests complement aggregate accuracy; we use numerical controls to distinguish the mechanisms behind observed grading discrepancies.” Do not imply use of its software or comprehensive capability coverage.

## 2. PAL — execution is an established control

**Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan, Graham Neubig.** *PAL: Program-aided Language Models.* ICML 2023, PMLR **202:10764–10799**. [Official record](https://proceedings.mlr.press/v202/gao23f.html); [published full text](https://proceedings.mlr.press/v202/gao23f/gao23f.pdf).

**Inspected:** §3, §6 and Appendix B/Table 6. PAL generates intermediate programs and delegates execution to an interpreter. Its ablations distinguish externally executing code from asking the model to produce the answer after code; they also vary program structure. The experiments cover mathematical, symbolic and algorithmic tasks, not this financial document panel.

**Supports:** separating semantic decomposition from arithmetic execution and requiring a cheap tool-assisted baseline. Cite with PoT beside our saved-expression diagnostic; PoT remains the closer financial-QA precedent.

**Does not support:** calling the 47/131 conditional recoveries a new reasoning method, a PAL replication, a prospective accuracy gain, or certified question grounding. Our restricted arithmetic strings differ from PAL's prompted intermediate programs. An interpreter cannot repair an incorrectly selected quantity.

**Next comparison:** use identical questions, output contracts and budgets for reported-number versus executed-program answers; retain syntax/runtime failures in the denominator. This is a proposed prospective baseline, not an experiment already completed.

## 3. Datasheets — document missing provenance explicitly

**Timnit Gebru, Jamie Morgenstern, Briana Vecchione, Jennifer Wortman Vaughan, Hanna Wallach, Hal Daumé III, Kate Crawford.** *Datasheets for Datasets.* Communications of the ACM **64(12):86–92**, December 2021. DOI: **10.1145/3458723**. [Author-institution publication record](https://www.microsoft.com/en-us/research/publication/datasheets-for-datasets/); [publisher route](https://cacm.acm.org/research/datasheets-for-datasets/).

**Access:** publisher route returned HTTP 403. Full-text support comes from [author preprint v8, 1 December 2021](https://arxiv.org/abs/1803.09010v8), [PDF](https://arxiv.org/pdf/1803.09010v8), not an inspected publisher-final PDF. Inspected §3, especially §§3.2, 3.4–3.7, and §4.

**Supports:** recording composition, sampling, preprocessing/labeling, intended uses, distribution conditions and maintenance. Its examples explicitly retain provenance unknown to third-party documenters. Cite beside pinned release identities, derivative lineage and missing original-generation history.

**Does not support:** treating hashes as label certification, a pinned code revision as proof of the original generation revision, or claiming formal datasheet compliance from an index and manifests. Documentation alone does not remove dataset risks.

**Suggested application:** “We document inspected release identities, derivative lineage and unresolved generation provenance.” Our [artifact index](../PAPER.md) is an evidence resource; it is not a replacement for the creators' missing records.

## 4. Pineau — report the level of reproduction achieved

**Joelle Pineau, Philippe Vincent-Lamarre, Koustuv Sinha, Vincent Lariviere, Alina Beygelzimer, Florence d'Alche-Buc, Emily Fox, Hugo Larochelle.** *Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program).* JMLR **22(164):1–20**, 2021. [Official record](https://jmlr.org/papers/v22/20-303.html); [published full text](https://jmlr.org/papers/volume22/20-303/20-303.pdf).

**Inspected:** §2.1, §§3–5 and §6. The report covers code submission, a reproduction challenge and a reporting checklist. It distinguishes same-data/same-tools reproduction from different-data replication and different-analysis robustness. Section 3 warns that available code can reproduce mistakes. Section 5 emphasizes specified metrics and variation; §6 explicitly stops short of causal evidence that the program improved paper quality.

**Supports:** explicit runtime/data/metric reporting and distinguishing saved-score replay from fresh inference, reimplementation and transfer. Cite in the artifact section, alongside the narrower ARA inspiration.

**Does not support:** newness of reproducibility packaging, independent scientific confirmation from a hash validator, acceptance guarantees, or any **2026** main-track/workshop requirement. Its acceptance associations do not establish an intervention effect.

**Suggested sentence:** “The artifact supports deterministic replay of saved-answer grading; fresh model inference and independent scientific reproduction remain separate checks.”

## Placement and limits

Add CheckList to the controls discussion, PAL beside the execution diagnostic, and Datasheets/Pineau to the artifact/provenance paragraph. Four local citations should support four concrete claims, not broaden the abstract or turn the bibliography count into a quality target. The canonical source remains [the manuscript](../paper/answer_contract_audit.tex).

Current NeurIPS and Agenthon format, anonymity, deadline and submission requirements require separate official **2026** sources. These historical research papers supply methodological context, not rules. None upgrades this bounded audit to a validated transferable repair method or establishes main-track readiness.
