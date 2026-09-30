## Executive summary (read this first)

Long appendices are permitted and occur in accepted NeurIPS papers. Their existence does not establish AI authorship or poor quality. Our appendix should nevertheless be shortened when it repeats the main text or carries secondary analyses that distract from the central claim. Keep enough information to interpret and reproduce the reported comparisons; preserve the full audit trail in the research artifact.

## Official requirements checked on 30 September 2026

The live NeurIPS 2026 Main Track Handbook, version V2026.3, specifies **nine submitted content pages**, including figures and tables, with **one additional content page for the accepted camera-ready version**. References, optional technical appendices, and the mandatory checklist do not count toward that limit. The suggested single-PDF order is paper, references, appendices, checklist. This is not a ten-page submitted-paper rule. [Official handbook](https://neurips.cc/Conferences/2026/MainTrackHandbook).

Agenthon's current call permits full or short papers in any format and length, submitted as one PDF. It is non-archival and requires an author to present in person. Therefore, the main-track page budget is a voluntary editing target for this workshop, not its stated constraint. [Agenthon CFP](https://www.agenthon.net/#call-for-papers).

## Three accepted 2025 examples

These are deliberately selected reasoning/evaluation examples, not a representative sample or evidence about the typical appendix length. Counts use one-based physical PDF pages from the proceedings PDFs. The checklist is counted separately from technical appendix pages, even where it appears before the appendix.

| Accepted paper | Track | Total PDF pages | Technical appendix pages | What the appendix supplies |
|---|---|---:|---|---|
| ThinkBench | Datasets and Benchmarks | 31 | 23–31: 9 pages | Dataset detail, additional task results, leakage analysis, adaptive comparison, process reward models, case studies |
| TTRL | Main conference | 25 | 22–25: 4 pages | Limitations, failure cases, reward pseudocode, additional results, training metrics, terminology |
| Reason-RFT | Main conference | 51 | 24–51: 28 pages | Evaluation tasks, training settings, extra results, data construction, reasoning-quality analysis, visual examples |

Primary proceedings records confirm acceptance/track, and their linked PDFs establish the page counts:

- [ThinkBench proceedings record](https://proceedings.neurips.cc/paper_files/paper/2025/hash/4da4f3c0dd1b907c48e2119afb2e2fde-Abstract-Datasets_and_Benchmarks_Track.html), [PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/4da4f3c0dd1b907c48e2119afb2e2fde-Paper-Datasets_and_Benchmarks_Track.pdf).
- [TTRL proceedings record](https://proceedings.neurips.cc/paper_files/paper/2025/hash/be690ea16f005c174f6c4102a5970e67-Abstract-Conference.html), [PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/be690ea16f005c174f6c4102a5970e67-Paper-Conference.pdf).
- [Reason-RFT proceedings record](https://proceedings.neurips.cc/paper_files/paper/2025/hash/08d70284b013c03ba89cd2b642bc864b-Abstract-Conference.html), [PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/08d70284b013c03ba89cd2b642bc864b-Paper-Conference.pdf).

Checklist pages in these PDFs are respectively 16–22, 15–21, and 17–23. References are not appendix pages either. These distinctions matter when comparing total PDF length with supporting material.

## Application to our paper: editorial recommendation

Aim for a compact appendix organized around two reader questions: exactly which response/scoring protocol produced the results, and exactly what can be reproduced from the artifact. A two-to-three-page target is a judgment for this paper, not a NeurIPS standard.

Keep model identities and decoding budgets, sample/denominator definitions, extraction/comparison rules, source-code revision distinctions, exact arithmetic conventions, and replay entry points. Consolidate the repeated protocol descriptions into one compact table and short explanatory paragraphs. Put the full prompt-adaptation feasibility and unused-group follow-up in the preserved artifact if they are not necessary for a main-text claim; revise main-text cross-references accordingly. Do not delete evidence or obscure failed/provisional branches.

The proceedings examples show that auxiliary material can have legitimate uses. They do not show that longer appendices improve acceptance, that a particular length is customary, or that padding is helpful. The actual editorial test is whether each retained section answers an identifiable reviewer question.
