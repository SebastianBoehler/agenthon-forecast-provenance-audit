## Executive summary (read this first)

RecursiveMAS has official NeurIPS 2026 poster-listing evidence. Its latent collaboration architecture does not resolve our financial-supervision audit's scientific gaps. The closer connection is an inspected public scoring endpoint: authored unequal MATH500 answers can receive credit after decimal truncation or sign removal. This is a reproducible current-code finding, not evidence that the paper's historical scores were inflated. No benchmark answers, model inference, training or paid services were used.

### Acceptance and primary access

Checked September 30, 2026, after 14:20 UTC. The user supplied an [author announcement](https://x.com/jiaru_zou/status/2104964430564086189); this tool could not read it directly. The [author project](https://recursivemas.github.io/) and repository also identify NeurIPS 2026. Independently, the [official conference downloads page](https://neurips.cc/Downloads/2026) lists the exact title as a `Poster`, linking [poster 153292](https://neurips.cc/virtual/2026/poster/153292). That confirms conference poster listing; it is not evidence of an award or actual reviewer opinions. The individual poster page was inaccessible in this check.

The author-controlled citation supplies [OpenReview ML0KFwGcPG](https://openreview.net/forum?id=ML0KFwGcPG). Its page/API were inaccessible (API HTTP 403); no official decision text or reviews were read. The official downloads listing supplies the independent confirmation despite that access gap.

Primary full text: Zou et al., [*Recursive Multi-Agent Systems*, arXiv:2604.25917v2](https://arxiv.org/abs/2604.25917v2), revised July 13, 2026; [HTML](https://arxiv.org/html/2604.25917v2), [PDF](https://arxiv.org/pdf/2604.25917v2). Methods, experiments, ablations and Appendix B.3 were read. The PDF was inspected in memory: 36 pages, 13,240,657 bytes, SHA-256 `465fa33e185f2bf2b9338878359035c5ef5b3d993d024e61f29547c27cbc6098`. This is the author preprint, not a separately verified camera-ready version. No full PDF was added to the artifact.

### What was actually evaluated

The [paper, §5 and B.1–B.3](https://arxiv.org/html/2604.25917v2#S5) evaluates MATH500, AIME2025/2026, GPQA-Diamond, MedQA, LiveCodeBench-v6, MBPP Plus, HotpotQA and Bamboogle. AIME uses pass@10. Four collaboration patterns use frozen backbones with trained inner/outer links. Training draws from s1K, m1K, OpenCodeReasoning and ARPO-SFT; reported means span five runs. These are author-reported results, not independently reproduced here.

| Evidence | Exact paper locator | Interpretation |
| --- | --- | --- |
| Text-MAS, single-agent LoRA/full-SFT, MoA, TextGrad and LoopLM comparisons | Tables 2–3, PDF pp. 9–10 | Structured comparison; no financial label audit |
| Depth and training/inference recursion sweeps | §5.1, Figure 1 | Recursion control |
| One/two-layer links with/without residuals | Table 4, PDF p. 12 | Module ablation |
| Latent lengths 0–128 | Table 9, PDF p. 27 | Budget ablation |
| 1.2–2.4× speedup; 34.6–75.6% fewer tokens | §5.4 | Relative to text-MAS; token counts exclude latent computation as tokens |
| 15.29 GB, 13.12M trainable, $4.27 estimated; LoRA 21.67 GB/$6.64 | Table 5, PDF p. 13 | Scaled-sequential cost analysis, described as per-agent memory; not total project billing |

Appendix B.3 / PDF pp. 24–25 reports H100/A100 execution, batch four, maximum training length 4,096, and task-specific generation budgets. The $4.27 estimate is not a quote for our hardware or clouds; full costing/reproduction is unverified. The theorem's assumptions do not establish financial target validity. [Full text](https://arxiv.org/pdf/2604.25917v2).

The [project's displayed six-column table](https://recursivemas.github.io/) yields approximately 8.3% mean *relative* improvement over each column's strongest baseline (about 5.7 percentage points from its displayed values). Do not rewrite the headline as +8.3 percentage points or a finance result. The project's five supported configurations include light/scaled sequential variants; the paper counts four collaboration patterns.

### Pinned code and actual dispatch

The [official implementation](https://github.com/RecursiveMAS/RecursiveMAS/tree/cbfcaab56c9a8f660a9be598750b4ff3cd762056) was pinned to `cbfcaab56c9a8f660a9be598750b4ff3cd762056` (September 28 commit). Its [README](https://github.com/RecursiveMAS/RecursiveMAS/blob/cbfcaab56c9a8f660a9be598750b4ff3cd762056/README.md) says reference checkpoints do not replace task-specific paper training. Code is MIT licensed; base-model/data licenses remain separate. No checkpoints or corpora were downloaded.

Static inspection verifies this public path:

1. `inference/load_from_repo.py` maps sequential light/scaled styles to the sequential family.
2. `inference/run.py:303–332` returns `inference_mas`; `284–299` invokes its `main`.
3. `inference_mas.py:165–187` resolves `math500` to `HuggingFaceH4/MATH-500`; `397–411` passes native answers through without numerical repair.
4. `2010–2025` and the imported dataset predicates route MATH500 into non-code evaluation.
5. `3079–3088` calls `compare_answers` on each generated output and increments the reported correct count from its Boolean result.

The [comparator, lines 442–469](https://github.com/RecursiveMAS/RecursiveMAS/blob/cbfcaab56c9a8f660a9be598750b4ff3cd762056/inference/inference_utils/answer_utils.py#L442), accepts a match under **any** of integer-part, LaTeX-text, whitespace-stripped or digit-only normalization. Decimal truncation appears at `348–369`; digit-only normalization removes signs at `285–295`. This is stronger than a lower-level helper observation: the public post-generation counting block uses the same result. The full model-loading CLI was not executed.

Paper Appendix B.3 / PDF p. 25 says:

> “if the two values are mathematically equivalent”

That stated criterion is stricter than these current-code authored examples. We have not established which evaluator revision produced the historical paper tables.

### Authored controls, separate from natural benchmark effects

These controls were designed **after** inspecting the code. They are not prospectively preregistered, naturally selected benchmark cases or source-label findings. Every control uses MATH500 routing; fractional/decimal and sign controls are not presented as valid AIME tasks, which expect nonnegative integer answers.

| Authored target | Authored `Final Answer:` value | Current native counting block | Diagnostic |
| --- | --- | --- | --- |
| 12 | 12 | Accept | Identity |
| 12 | 13 | Reject | Unequal integer negative control |
| 1.2 | 1.8 | Accept | Integer-part collision |
| 1/2 in LaTeX | 4/5 in LaTeX | Accept | Both truncate to zero |
| −1 | +1 | Accept | Digit-only sign collision |
| −1.2 | −1.8 | Accept | Negative integer-part collision |
| 12 dollars | 12 years | Accept | Unit-blind representation diagnostic |
| 12 | Empty final value | Reject | Missing-value negative control |

All eight run through the inspected helper and the **unchanged native post-generation scoring statements**, wrapped with authored lists instead of model generation. Three recognized MATH500 aliases give 24 consistent checks. Four exact numerical inequivalences and the unit diagnostic receive credit. Unit blindness is not itself proof of a financially defective natural case. Neither toy frequency nor acceptance counts estimate real score inflation, model behavior or benchmark prevalence.

Replay, standard library only:

```bash
python3 scripts/validate_recursivemas_authored_controls.py
```

Result: `PASS`, six source files, 18 exact source fragments, eight controls, 24 native-block checks. The comparator is preserved verbatim in three contiguous parts (each at most 180 lines), reconstructed and checked against its original SHA. Dispatch excerpts preserve exact original line intervals. Only inspected pure definitions and scoring statements are compiled; no Torch import, corpus loading, network call, judge or model code runs. A full-CLI integration test remains unperformed.

Artifact: `outputs/recursivemas-code-review-v1/source_manifest.json` records URLs, revision, full-file hashes and fragment intervals; `source/` includes the MIT notice; `authored_control_receipt.json` binds script/source hashes, timing and exact results. Snapshot capture was `2026-09-30T14:34:40.971368Z`, after initial controls were observed. This is a reporting/replay artifact, not a new scientific freeze or a reproduction of RecursiveMAS performance.

### Relevance and next-step boundary

The architectural paper assumes supplied targets during optimization; recursion does not independently establish the target's requested financial quantity, rounding or units. Nothing here shows RecursiveMAS learned the Cosimo debt-for-call error or repairs it. Its latent-state interface also requires access to local model internals, so it cannot simply be inserted into our existing opaque provider endpoints. Mac feasibility and task-specific retraining are untested.

The grounded connection is **acceptance-set loss**: current released normalization can merge numerically distinct answers. That complements our source-label defect, output-rounding and paired-grading evidence without claiming a new verification principle. It is a future cross-domain comparator/control candidate, not an immediate new benchmark or architecture experiment.

For our present paper, prioritize the requested-quantity identity, passing bounds/comparison controls and paired grading decomposition. Preserve the null reminder result, AI-only reference authority and unmeasured training/downstream effects. If later investigating this external endpoint, freeze revisions and admissible representations before selecting natural cases, then compare saved outputs under original versus equivalence-preserving scoring. Historical evaluator provenance and raw-output access would be prerequisites for a claim about published scores. This report launches none of that work.

Official acceptance of this work does not imply an opinion about our submission, an acceptance guarantee or a requirement to adopt its architecture. No manuscript, prior freezes, scientific results or bundles were changed.
