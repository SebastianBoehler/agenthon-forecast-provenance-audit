## Executive summary (read this first)

This is the working literature ledger for the Agenthon paper. Twenty-five full-text PDFs are cached locally under the ignored `literature/pdfs/` directory, including public preprints, a peer-reviewed proceedings paper, and an open-access published journal PDF. A second novelty pass finds the current report-level candidate is not yet distinct enough: adaptive selection bias, multivariate score reliability, and multi-objective forecasting already have substantial prior work. The [broader September 27 review](../docs/BROAD_TOPIC_REVIEW_2026-09-27.md) ranks an exact-semantics simulation study as the best conditional short-paper route and parks the CLMM example.

## Search and access record

**September 28 update:** the [full-text audit](../docs/LITERATURE_AUDIT_2026-09-28.md) verifies the initial 25 files and records ten additional primary PDFs and extracted texts. These include simulator predecessors, foundational faithfulness and scoring papers, a limit-order-book survey, and realism-evaluation work. Limited backward reference tracing was performed; comprehensive forward tracing and the focused comparison matrix remain incomplete. No new authenticated IU access occurred in this pass. The failed Kalibera retrieval is recorded separately and is not counted as an obtained PDF. Follow the [process reset](../docs/PROCESS_RESET_2026-09-28.md) before promoting a topic.

Searches were run in the user's IU EBSCO Discovery Service session on 2026-09-26 for (1) text/time-series forecasting and explanation faithfulness, (2) forecast rationale, counterfactual intervention and faithfulness, and (3) temporal validation and financial backtest overfitting. EBSCO returned a close RecSys '26 record, **How Faithful Is the Reasoning of LLM Recommenders? A Counterfactual Audit** (DOI: [10.1145/3773078.3841294](https://doi.org/10.1145/3773078.3841294)). Its abstract describes rationale edits and measuring recommendation changes. The linked ACM publisher page required sign-in for the PDF, so the full text was not obtained or bypassed. EBSCO also surfaced the ICML 2026 workshop paper **Semantics or Structure?**

The original eleven PDFs below were retrieved from public arXiv or JMLR full-text endpoints and text-extracted locally to inspect methods, findings, and limitations. They were not downloaded through EBSCO. Fourteen additional public PDFs were cached on September 27, including seven from the broader harness and finance-benchmark pass. The IU catalogue was used for the two peer-reviewed CLMM journal articles; this ledger separates verified full-text reading from catalogue/abstract-only access.

## Closest prior work and implications

### Evidence and rationale faithfulness are already crowded

**TimeLitmus** is the most important collision. It evaluates event-conditioned time-series prediction and explanations with controlled counterfactual and contrastive interventions, shortcut controls, evidence-targeted tests, and human annotations across Finance and Traffic. Its reported behavioral support can remain low even when a model cites the manipulated factor. It does not appear to ask our exact question—whether a reviewer can infer that a rationale was generated after an identical forecast was fixed—but it makes a broad claim about auditing forecast explanations or evidence faithfulness untenable. Treat the exact generation-order contrast as a hypothesis about a specific gap, not a proven first.

**Semantics or Structure?** directly intervenes on text in multimodal time-series forecasting. On Time-MMD it reports that replacing text often changes results very little and that numeric side channels can explain apparent multimodal lift. This closes off generic text ablation or “does context matter?” as a fresh contribution.

**TFRBench** studies reasoning-aware forecasting over ten datasets and five domains, including finance, and measures both forecast quality and reasoning. **What LLM Forecasters Know but Don’t Say** studies evidence sensitivity and rationale stability in forecasting, using internal representations as well as evidence interventions. Neither should be summarized as “the first forecasting reasoning benchmark.”

These comparisons lower the expected novelty of the current blinded provenance proposal. It remains a distinct construction-order question, but that difference needs direct verification against the ACM RecSys audit and wider CoT work. A 60-pair study with no cases or recruited reviewers yet is not an evidence-backed, high-confidence submission for the September 30 deadline.

### Forecast selection under time change is established, so keep the claim empirical

Rolling-origin validation, multiple test periods, regime-sensitive model selection, backtest overfitting, proper scoring, and temporal-generalization benchmarks all have prior literature. The IU search surfaced Tashman's established review of out-of-sample forecasting tests and a Knowledge-Based Systems paper comparing financial backtest validation methods under regime shifts. Public work also includes [Impermanent](https://arxiv.org/abs/2603.08707), a live benchmark for temporal generalization, and [Why Model Selection Fails in Time Series Forecasting](https://arxiv.org/abs/2605.01608), a 2026 preprint that directly studies ranking instability across data regimes using descriptor-based model selection.

Therefore the proposal must not claim that regime-aware validation, tail-aware forecasting evaluation, multiaxis scoring, or a new promotion gate is novel in general. Cawley and Talbot establish the general model-selection-overfitting mechanism; multi-objective forecasting research already treats accuracy/latency trade-offs; Marcotte et al. directly study finite-sample reliability of multivariate proper scores. The remaining Agenthon-specific report-history angle is not by itself a demonstrated scientific contribution. Current files do not support a complete dated candidate history, candidate-rank transfer, or quantifying predeclared-check effectiveness. The idea may be too incremental unless verified outputs reveal a non-obvious result.

The reports show different outcomes: historical episode replay selected on early calibration worsened later validation by 0.097863; an F4 scale change passed its reported calibration-to-validation gates, but that validation period was reused in Batch 12 design; an FX log-return change did better on a recent slice than on older calibration but was rejected by the older/tail check. Batch 15 is a follow-up to Batch 14, not independent confirmation. The 15 reports found use varied scopes and panels; they are not proven to cover every attempt. Audit chronology, overlap, and public-safe handling before analysis; the reports alone do not establish an independent or confirmatory study.

## Full texts cached locally

The original local PDFs are open-access copies from arXiv or JMLR. Every PDF path below is Git-ignored by `/literature/pdfs/`.

| Local PDF | Paper | Why it matters |
|---|---|---|
| `pdfs/2609.24677.pdf` | Gong et al. (2026), [TimeLitmus](https://arxiv.org/abs/2609.24677) | Closest evidence-faithfulness benchmark; materially weakens broad provenance/faithfulness novelty. |
| `pdfs/2608.22321.pdf` | [Semantics or Structure?](https://arxiv.org/abs/2608.22321), ICML 2026 workshop | Direct text-sensitivity interventions for multimodal time-series forecasting. |
| `pdfs/2604.05364.pdf` | [TFRBench](https://arxiv.org/abs/2604.05364), ICML 2026 | Reasoning-aware forecasting benchmark; finance included. |
| `pdfs/2607.08046.pdf` | [What LLM Forecasters Know but Don’t Say](https://arxiv.org/abs/2607.08046) | Forecast evidence sensitivity and rationale stability. |
| `pdfs/2605.11258.pdf` | Liu et al. (2026), [Unlocking LLM Creativity in Science through Analogical Reasoning](https://arxiv.org/abs/2605.11258) | User's requested reasoning method: structural analogy, comparative baselines, human validation, implementation on real tasks. |
| `pdfs/2604.24658.pdf` | Liu et al. (2026), [The Last Human-Written Paper: Agent-Native Research Artifacts](https://arxiv.org/abs/2604.24658) | Artifact-design reference; not our scientific novelty. |
| `pdfs/2609.11728.pdf` | Barba (2026), [Reproducibility in the Age of Agentic AI](https://arxiv.org/abs/2609.11728) | Repository history and reproducibility practice; not our scientific novelty. |
| `pdfs/2605.01608.pdf` | Akinci & Martinez-Morales (2026 preprint), [Why Model Selection Fails in Time Series Forecasting](https://arxiv.org/abs/2605.01608) | Directly studies model-selection instability across time-series regimes; key novelty boundary. |
| `pdfs/cawley10a.pdf` | Cawley & Talbot (2010), [On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation](https://jmlr.csail.mit.edu/papers/v11/cawley10a.html) | Establishes selection-criterion overfitting and performance-estimate bias as general problems. |
| `pdfs/2202.08485.pdf` | [Multi-Objective Model Selection for Time Series Forecasting](https://arxiv.org/abs/2202.08485) | Covers probabilistic nCRPS benchmarking and accuracy/latency Pareto selection; undermines novelty of scalar-versus-vector framing. |
| `pdfs/2304.09836.pdf` | Marcotte et al. (2023), [Regions of Reliability in the Evaluation of Multivariate Probabilistic Forecasts](https://arxiv.org/abs/2304.09836) | Directly studies finite-sample score discrimination for multivariate forecast errors. |

### Additional full texts cached September 27

| Local PDF | Paper and access route | Why it matters |
|---|---|---|
| `pdfs/pace-2608.17220.pdf` | [PACE](https://arxiv.org/abs/2608.17220), arXiv full text | Closest transaction-gate work; explicitly leaves policy-valid harmful multi-step sequences open. |
| `pdfs/ndss-lastx-intent-transaction.pdf` | [Auditable LLM Arbiter for DeFi Security](https://www.ndss-symposium.org/wp-content/uploads/lastx2026-46.pdf), NDSS LAST-X proceedings PDF | Intent–transaction alignment benchmark with 18,000 examples. |
| `pdfs/clmm-digital-finance-2026.pdf` | [Tung & Wang, *Digital Finance* (2026)](https://doi.org/10.1007/s42521-026-00198-z), Springer published open-access PDF found through IU EBSCO | Peer-reviewed CLMM economic model; not an agent evaluation. |
| `pdfs/clmm-rl-2608.19389.pdf` | [Chionas et al.](https://arxiv.org/abs/2608.19389), arXiv full text | RL and sophisticated baselines for dynamic CLMM allocation. |
| `pdfs/finance-risk-2502.15865.pdf` | [Chen et al.](https://arxiv.org/abs/2502.15865), arXiv full text | Finance-agent workflow and system-risk audit. |
| `pdfs/idempotencybench-arr-2026.pdf` | [IdempotencyBench](https://github.com/gssanjana4/idempotencybench), author-hosted PDF under ARR review | Duplicate side effects across retry modes; synthetic tools and limited plan depth. |
| `pdfs/trading-execution-audit-2606.08285.pdf` | [Yao & Zheng](https://arxiv.org/abs/2606.08285), arXiv full text | Trading execution realism and reproducibility review. |

### Broader harness and finance-benchmark full texts cached September 27

| Local PDF | Paper | Why it matters |
|---|---|---|
| `pdfs/2605.27922.pdf` | [Harness-Bench](https://arxiv.org/abs/2605.27922) | Multi-model, multi-harness benchmark; configuration effects alone are already studied. |
| `pdfs/2609.01437.pdf` | [HarnessDev](https://arxiv.org/abs/2609.01437) | Reports limited transfer of evolved harnesses and emphasizes active execution paths. |
| `pdfs/2605.22166.pdf` | [Life-Harness](https://arxiv.org/abs/2605.22166) | Contrasting evidence of harness transfer in deterministic environments. |
| `pdfs/2607.27853.pdf` | [FinanceHarness and FinanceGym](https://arxiv.org/abs/2607.27853) | Finance-specific research workflow harness and point-in-time benchmark. |
| `pdfs/2605.27333.pdf` | [FinHarness](https://arxiv.org/abs/2605.27333) | Lifecycle safety monitoring for finance LLM agents. |
| `pdfs/2606.03918.pdf` | [Hedge-Bench](https://arxiv.org/abs/2606.03918) | Expert financial-analysis tasks with deterministic checks. |
| `pdfs/2606.26350.pdf` | [OpenFinGym](https://arxiv.org/abs/2606.26350) | Multi-task financial AI environment; weakens generic “finance gym” novelty. |

The broader review also checked primary pages for [FORESIGHT-9](https://arxiv.org/abs/2608.29372), [JAX-LOB](https://arxiv.org/abs/2308.13289), [MAXE](https://arxiv.org/abs/2008.07871), [ABIDES Rust](https://github.com/mariotrerotola/abides-rs), and the [Agenthon CFP](https://www.agenthon.net/#call-for-papers). Their PDFs were not added to this cache in this pass, so do not treat them as full-text-verified here.

## Decision and next evidence needed

1. Do not submit the current provenance proposal as if it had results. Keep it as a follow-on study unless a real, adequately blinded dataset and reviewers can be assembled before the deadline.
2. Check whether the available T2 reports, outputs, and provenance can be analyzed and disclosed under competition rules, author permissions, and public/private firewall constraints.
3. Recover reproducible raw outputs and chronology where available. Do not imply the located 15 reports exhaust the development history.
4. Define a narrow empirical question before reanalysis. Continue only if recovered evidence supports a non-obvious finding distinct from existing model-selection and probabilistic-score studies.
5. Use claim-linked code, decisions, and evidence following ARA and Barba. Keep code evolution tracking as the reproducibility method, not as the paper's claimed novelty.

## Related primary sources

### September 28 novelty-page additions

Three additional PDFs were saved and successfully text-extracted in ignored `pdfs/`, bringing the cache from 35 to 38 PDFs. Source URLs and SHA-256 digests are recorded in `pdfs/novelty-sources-2026-09-28.json`. These are public primary full texts; no new authenticated IU session was used.

- [JaxMARL-HFT](https://arxiv.org/abs/2511.02136), `2511.02136.pdf`: §5.1 reviewed, including matched CPU-MARL and environment versus complete training comparisons.
- [Converted, Not Equivalent](https://arxiv.org/abs/2605.29054), `2605.29054.pdf`: introduction and observable contract formulation inspected. Contract-based codebase conversion is prior art, not a new principle of our proposed simulator study.
- [Rigorous Benchmarking in Reasonable Time](https://kar.kent.ac.uk/33611/45/p63-kaliber.pdf), `kalibera-jones-2013.pdf`: author manuscript now successfully retrieved, superseding the earlier failed download. Variation and repetition guidance inspected; not a claim that our pilot is powered.

The [novelty page](../docs/NOVELTY_JUSTIFICATION_2026-09-28.md) records the resulting bounded comparisons and remaining empirical gates.

- Tashman, L. J. (2000). [Out-of-sample tests of forecasting accuracy: An analysis and review](https://doi.org/10.1016/S0169-2070(00)00065-0). *International Journal of Forecasting*, 16(4), 437–450. EBSCO/publisher record inspected; downloadable library full text not confirmed in this pass.
- Arian, H., Norouzi Mobarakeh, D., & Seco, L. (2024). [Backtest overfitting in the machine learning era](https://doi.org/10.1016/j.knosys.2024.112477). *Knowledge-Based Systems*, 305, 112477. Publisher metadata/abstract inspected; full text not locally cached.
- Garza et al. (2026). [Impermanent: A Live Benchmark for Temporal Generalization in Time Series Forecasting](https://arxiv.org/abs/2603.08707). Full paper page inspected; PDF not cached in this batch.
- **How Faithful Is the Reasoning of LLM Recommenders? A Counterfactual Audit** (RecSys 2026). [ACM DOI](https://doi.org/10.1145/3773078.3841294). IU/EBSCO record and abstract inspected; publisher required sign-in for the PDF.
