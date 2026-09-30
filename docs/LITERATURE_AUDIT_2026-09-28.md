## Executive summary (read this first)

The initial cache contains **25 PDF files**, matching the September 27 ledger. This is enough to identify major novelty collisions, but it does not establish exhaustive landscape coverage or a defensible new contribution. The collection is concentrated in recent preprints and previously explored forecasting, rationale, and harness directions. The conditional simulator direction had primary-page checks but lacked the corresponding cached papers.

On September 28, this audit inspected the closest forecasting papers' references and retrieved eight additional primary full texts, including foundational faithfulness and scoring literature and three simulator predecessors. A saved PDF is an access result; it is not evidence that every section, experiment, or cited reference has been critically reviewed. The key remaining deliverable is a small, claim-specific comparison matrix tied to an achievable experiment.

## What was verified locally

- `literature/pdfs/` held 25 PDFs before this pass. The files named in `literature/README.md` are present.
- The `.gitignore` contains `/literature/pdfs/`; PDFs and extracted texts belong in that ignored directory.
- Text was extracted from TimeLitmus, Semantics or Structure, TFRBench, and What LLM Forecasters Know but Don't Say during this pass. The first two papers' related-work and reference sections were inspected directly.
- The existing ledger distinguishes library metadata/abstract access from obtained PDFs. Its ACM RecSys rationale-audit paper remains **abstract/catalogue only**, not full-text verified.
- No source from private competition evaluation units was used.
- No new IU/EBSCO authenticated-session access was performed in this audit. All eight additions below came from public primary full-text endpoints.

The 25 initial documents include seven CLMM/transaction/retry/trading items. Those are useful if that direction returns, but they should not be counted as deep coverage of forecasting or market-simulator novelty.

## Close forecasting papers: verified boundaries

| Source | Access and inspected material | What it establishes for our decision |
|---|---|---|
| [TimeLitmus](https://arxiv.org/html/2609.24677v1) | Existing PDF; full HTML; related work, formulation, diagnostic design, reference list | Controlled event/series pairs, shortcut checks, and behaviorally supported explanations already exist. Generic forecasting faithfulness audit is insufficient novelty. |
| [Semantics or Structure?](https://arxiv.org/html/2608.22321v1) | Existing PDF; full HTML; limitations, text-intervention design, bibliography | Direct text substitutions and numeric-side-channel explanations already exist. The stated limitation is three frozen-encoder architectures on Time-MMD; an extension needs a new mechanism/result, not only another model. |
| [TFRBench](https://arxiv.org/abs/2604.05364) | Existing PDF and newly extracted text; bibliography located | Available for comparison, but a complete extraction of its metric definitions, data construction, and overlaps is still required before any narrow reasoning-benchmark claim. |
| [What LLM Forecasters Know but Don't Say](https://arxiv.org/abs/2607.08046) | Existing PDF and newly extracted text; bibliography located | Available for comparison; detailed intervention/representation analysis is still required before distinguishing our proposal. |
| [RecSys counterfactual rationale audit](https://doi.org/10.1145/3773078.3841294) | Previously documented IU catalogue/abstract access; no cached PDF | A material gap in the provenance proposal's nearest-neighbor review. Its exact methods and limitations must be read before claiming construction-order novelty. |

These statements are novelty boundaries, not judgments that existing work is flawless or covers every possible question.

## Backward reference tracing performed today

Backward tracing means opening references cited by the closest papers, rather than merely searching similar titles.

TimeLitmus directly cites Jacovi and Goldberg (reference 24), Lanham et al. (33), Turpin et al. (47), and Context is Key (50). These sources were followed to their primary pages/PDFs and saved. Its related-work section also identifies a faithful-explanation survey, behavioral testing, context benchmark integrity, and newer task benchmarks. Those additional branches remain on the reading queue.

JAX-LOB's related-work section directly discusses ABIDES and MAXE. All three papers were saved. This gives a concrete predecessor chain for simulation acceleration. It does not prove that ABIDES-compatible exact trace preservation is new: code, version semantics, later papers, and benchmark workloads still need comparison.

## Newly obtained full texts

Each file below passed a PDF signature check and was successfully text-extracted. The table reports access and targeted reading separately. Public access is not an unrestricted redistribution license.

| Ignored filename | Primary source | Reading status / role |
|---|---|---|
| `1904.12066.pdf` | [ABIDES](https://arxiv.org/abs/1904.12066) | Full text accessible; architecture/related-work passages inspected; baseline foundation. |
| `2008.07871.pdf` | [MAXE](https://arxiv.org/abs/2008.07871) | Core implementation passages inspected: C++ core, Python API, agents/latency/matching. Preempts generic compiled simulator novelty. |
| `2308.13289.pdf` | [JAX-LOB](https://arxiv.org/html/2308.13289v1) | Introduction and related work inspected: GPU/vectorization and ABM versus market replay. Preempts generic accelerated LOB simulator novelty. |
| `jacovi-goldberg-2020.pdf` | [Faithfulness definitions and evaluation](https://aclanthology.org/2020.acl-main.386/) | Evaluation-guideline passages inspected; distinguishes human plausibility from model faithfulness. A human provenance-identification test cannot automatically be called a faithfulness test. |
| `2305.04388.pdf` | [Turpin et al., Unfaithful Explanations](https://arxiv.org/abs/2305.04388) | Downloaded and extracted; targeted detailed methods review remains. Foundational explanation intervention predecessor. |
| `2307.13702.pdf` | [Lanham et al., Measuring Faithfulness](https://arxiv.org/abs/2307.13702) | Downloaded and extracted; targeted detailed methods review remains. Reasoning intervention predecessor. |
| `2410.18959.pdf` | [Context is Key](https://arxiv.org/abs/2410.18959) | Downloaded and extracted; full protocol review remains. Reference-traced context forecasting benchmark. |
| `gneiting-raftery-2007.pdf` | [Gneiting and Raftery, JASA review](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf) | Public author-hosted journal PDF; initial scoring definition inspected. Foundational justification for probabilistic forecast scoring. |

The parallel pass also saved and text-extracted [Get Real: Realism Metrics for Robust Limit Order Book Market Simulations](https://arxiv.org/abs/1912.04941) as `get-real-1912.04941.pdf` and [Gould et al., Limit Order Books](https://people.maths.ox.ac.uk/porterm/papers/gould-qf-final.pdf) as `gould-limit-order-books-2013.pdf`. These are retrieved, not close-read in this audit. The Kalibera benchmarking PDF download failed; it is not cached here. Do not combine filenames into a total without checking unique sources; two filenames can refer to one paper.

## Missing evidence before topic selection

1. **A bounded search question.** Select the scientific capability or failure to explain. A broad list spanning forecasts, harnesses, world models, and simulators has no meaningful saturation criterion.
2. **A closest-work matrix.** Extract question, intervention, data, baseline, evaluation, result, limitation, and proposed difference for about five closest papers. Every absence claim must specify the inspected section/code and uncertainty.
3. **Foundation and survey branches.** Follow Lyu et al.'s 2024 *Computational Linguistics* faithful-explanation survey (TimeLitmus reference 37), CheckList, forecasting data-integrity references (Fidel-TS and Rethinking Multimodal Evaluation), and simulator-validity references. Verify bibliographic details before citation.
4. **Forward tracing.** This pass performed limited backward tracing. It did not complete a systematic forward-citation search, a second independent search, or an inclusion/exclusion log for all directions.
5. **Comparable simulator conditions.** Native CPU versus GPU replay versus multi-agent discrete-event simulation are different workloads. Existing speedups cannot be compared as interchangeable ratios. Define the timing boundary, hardware, agents, seeds, output contract, and baseline version before comparing.
6. **Contribution beyond artifact hygiene.** ARA-style histories support credibility. They do not alone establish a novel scientific question or substantive simulator improvement.
7. **A falsifiable pilot.** Require one experiment that could invalidate the proposed contribution. For simulation, this includes failed equivalence or lack of a meaningful complete-run speedup. For provenance, this includes a classifier responding to writing style instead of generation order.

## Practical conclusion

We have enough full text to stop proposing broad first-of-its-kind claims and enough access to begin a focused academic comparison. We do **not** yet have a completed, independently checked landscape map or empirical evidence warranting confident acceptance. The next step should be a one-page gap justification plus the comparison matrix and a frozen pilot protocol, following the user's supplied Prof. Lu feedback. Reading more is useful when it closes one of those named gaps; accumulating an arbitrary PDF count is not the objective.
