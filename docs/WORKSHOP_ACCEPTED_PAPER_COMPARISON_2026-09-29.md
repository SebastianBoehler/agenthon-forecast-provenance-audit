## Executive summary (read this first)

The NeurIPS 2025 Generative AI in Finance workshop explicitly accepted datasets,
agent frameworks, and negative empirical studies. These are useful comparators for
contribution types. They do not establish Agenthon acceptance criteria or probabilities.
Six papers below were checked against primary acceptance records and full texts.
Five PDFs and extracted texts were saved in the ignored `literature/pdfs/` cache;
one OpenReview paper was available through indexed full text but its download was blocked.

## Acceptance evidence and scope

### 1. The Losing Winner: An LLM Agent that Predicts the Market but Loses Money

- Acceptance: named on the official [NeurIPS 2025 accepted list](https://sites.google.com/view/neurips-25-gen-ai-in-finance/accepted-papers).
- [Full text](https://openreview.net/pdf?id=FzahgVWy59); [author poster](https://tikatoka.github.io/data/69.pdf).
- Contribution: a negative empirical case study. Qwen2.5-3B receives supervised
  and reinforcement fine-tuning to classify next-day Bitcoin market states. Better
  classification is accompanied by worse simulated trading returns. The authors
  attribute this to mismatch between classification rewards and trading objectives.
- Evidence scope: one model and Bitcoin daily trading; this does not establish a
  universal result about RL or trading. Calling objective mismatch reward hacking
  does not itself identify a new mechanism.
- Lesson: an informative failure can be a workshop contribution. We cannot claim
  a first finance reward-mismatch study; this accepted paper already supplies one.
- Access: read indexed full-text methods and discussion; direct OpenReview PDF
  download returned 403. No full-paper PDF saved for this item.

### 2. Are Foundation Models Useful for Bankruptcy Prediction?

- Acceptance: named on the same official NeurIPS 2025 list.
- [Full text](https://arxiv.org/abs/2511.16375).
- Contribution: empirical comparison of Llama-3.3-70B and TabPFN against five
  classical methods across five bankruptcy horizons. Classical approaches win;
  the study also examines probability reliability and computational overhead.
- Evidence scope: Visegrád company records, with a 20,000-case test subset;
  limited LLM choice and API-returned probabilities restrict generalization.
- Lesson: useful head-to-head evidence can justify a paper without a new model.
  Appropriate specialized baselines and operational metrics matter.
- Cached: `workshop2025_bankruptcy.pdf` and `.txt` (14 pages).

### 3. FinAgentBench: A Benchmark Dataset for Agentic Retrieval in Financial Question Answering

- Acceptance: named on the same official NeurIPS 2025 list.
- [Full text](https://arxiv.org/abs/2508.14052).
- Contribution: expert-annotated financial retrieval benchmark separating document
  selection and passage ranking, plus reasoning-model evaluation and reinforcement
  fine-tuning. The full text includes nDCG, MAP, and MRR comparisons and gains
  from adapting GPT-o4-mini.
- Evidence scope: a retrieval-only setting, not an end-to-end financial agent.
  Random splits do not demonstrate arbitrary unseen-task generalization.
- Version caution: cached arXiv v4 is an ICAIF-formatted manuscript of a title
  independently confirmed on the NeurIPS workshop list. It is not proven to be
  byte-identical to the workshop submission. Dataset scale changed between versions;
  avoid mixing the older 3,429-example abstract with revised corpus descriptions.
- Lesson: a well-defined missing measurement with curated labels and baselines
  is substantive; benchmark size alone is insufficient.
- Cached: `workshop2025_finagentbench.pdf` and `.txt` (6 pages).

### 4. Structured Agentic Workflows for Financial Time-Series Modeling with LLMs and Reflective Feedback

- Acceptance: named on the same official NeurIPS 2025 list.
- [Full text](https://arxiv.org/abs/2508.13915).
- Contribution: TS-Agent combines model selection, code refinement, and tuning
  with structured knowledge banks and execution feedback. Experiments cover
  forecasting and synthetic generation using cryptocurrency, FX, and stock data;
  four LLM backbones are compared with agentic and AutoML baselines.
- Evidence scope: reported metrics average five runs. The model library and
  domain resources are substantive parts of the system, so superior results do
  not isolate a single harness mechanism automatically.
- Lesson: generic financial harnesses with reflective feedback already have an
  accepted predecessor. A new harness needs a distinguishable mechanism and
  controlled comparisons, not merely another workflow diagram.
- Cached: `workshop2025_ts_agent.pdf` and `.txt` (9 pages).

### 5. Secure and Scalable Horizontal Federated Learning for Bank Fraud Detection

- Acceptance: [ML Collective's primary project record](https://mlcollective.org/projects/)
  explicitly says published at Advances in Financial AI Workshop, ICLR 2025.
- [Full text hosted by the research collective](https://s.mlcollective.org/SecureandScalableHorizontalFederatedLearningforBankFraudDetection.pdf).
- Contribution: federated transformer versus federated MLP and centralized/local
  baselines on Bank Account Fraud data, with communication and timing measurements.
- Evidence scope: five simulated institutions, downsampled nonfraud examples,
  20 communication rounds; federated transformer ROC-AUC 0.87 versus centralized
  LightGBM 0.89. It is an operational trade-off study, not an absolute performance win.
- Caution: raw-data locality alone does not prove formal privacy or compliance;
  accepted manuscripts can still contain limitations and overclaims.
- Cached: `workshop2025_federated_fraud.pdf` and `.txt` (8 pages).

### 6. TWICE: What Advantages Can Low-Resource Domain-Specific Embedding Model Bring?

- Acceptance: [the authors' institution lists the work and ICLR 2025 Financial AI oral presentation](https://modulabs.co.kr/papershop).
  This is an institutional primary record, not an independently retrieved workshop roster.
- [Full text](https://arxiv.org/abs/2502.07131).
- Contribution: KorFinMTEB, native Korean financial evaluation across seven tasks
  and 26 datasets, compared with translated FinMTEB and eight embedding models.
- Evidence scope: performance differences measure distributions that differ in
  several ways; attributing them solely to cultural nuance requires stronger controls.
  Document-level reasoning and some niche financial sources remain limited.
- Lesson: a meaningful evaluation resource can support even an oral, but this
  example cannot establish Agenthon oral availability or selection standards.
- Cached: `workshop2025_twice.pdf` and `.txt` (10 pages).

## Source integrity corrections

The old ICLR 2025 Google Sites URL listed by OpenReview currently serves unrelated
content. It was not used as evidence of accepted papers.
`advancesinfinancialai.com` currently describes CIKM 2025; its accepted-paper list
must not be labeled ICLR 2025. The ICLR 2025 OpenReview venue exists but public
submission access was not recovered in this pass.

## Implications for our contribution decision

1. We should aim for one useful, distinguishable scientific result, mechanism, or
   evaluation artifact with empirical evidence, rather than requiring a new
   foundation model to justify a workshop paper.
2. Negative findings are viable contributions when the comparison identifies a
   consequential mismatch and supports its explanation.
3. Finance retrieval benchmarks, financial constraint evaluation, reflective
   harnesses, and RL reward mismatch are already occupied areas.
4. Accepted examples guide positioning; they cannot supply acceptance certainty.
   We have no representative rejected-paper sample or Agenthon acceptance rate.
5. The current financial training-versus-harness proposal still needs an exact
   gap against these predecessors. Acceptance of a similar topic elsewhere is
   evidence of relevance, not evidence that another version is novel.
