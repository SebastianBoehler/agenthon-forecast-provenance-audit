## Executive summary (read this first)

Generic financial fine-tuning, executable financial reasoning, and paired financial evidence benchmarks already have close predecessors. A stronger provisional direction is to audit whether verifiable financial rewards are actually computable from the information shown to a model. A pinned public dataset provides a concrete hidden-precision failure to investigate. This is preliminary evidence, not a novelty certificate or an acceptance prediction. No training, model inference, or upstream solution execution ran.

### Candidates compared

| Candidate | Closest work and collision | Potential substantial contribution | One–two day assessment |
|---|---|---|---|
| Financial SFT followed by GRPO | Fin-R1 already does finance SFT plus RL; DianJin-R1 and Fin-o1 further crowd the space. | A distinct reward mechanism with controlled generalization gains, rather than a new adapter. | High risk: training infrastructure, seeds, controls and held-out evaluation are unresolved. |
| Financial transformation-generalization benchmark | FinChain already generates parameterized financial tasks; GSM-Symbolic establishes perturbation evaluation; FinMirror covers paired financial evidence changes. | A validated held-out transformation study demonstrating which training or inference intervention transfers beyond trained relations. | Possible small diagnostic study, but a taxonomy alone would be incremental. |
| Matched-budget tools versus trained financial reasoning | FinanceReasoning already compares reasoning with executable programming and function retrieval. | A reproducible cost/reliability frontier, with failures attributed to extraction, formula selection and arithmetic, across several backbones. | Feasible only with available checkpoints and endpoints; an ordinary calculator comparison is insufficient. |
| Reward validity under rendered financial information | FinanceReasoning corrects existing labels; FinVerBench studies rounded financial statements; benchmark audits already exist. | An information-contract audit revealing when a valid execution rewards an answer that the visible prompt cannot justify, with measured false rejection, repair and independent validation. | Best evidence-led candidate from this scan, conditional on extending beyond one small dataset. |

### Closest full-text evidence

- **FinChain, ACL 2026:** Sections 3.1–3.2 and 5.3 describe expert-reviewed parameterized templates, input completeness and unit checks, and 2,900 generated evaluation cases. Its 58 topics and five templates per topic mean “a new executable finance benchmark” is already a broad collision. A useful difference would have to be the new evaluation question or finding. [Published paper](https://aclanthology.org/2026.acl-long.662.pdf) · [Code](https://github.com/mbzuai-nlp/finchain).
- **FinanceReasoning, ACL 2025:** Sections 3 and 4.4 cover corrected questions, a 3,133-function resource, and Reasoner-with-Programmer experiments. Its limitations explicitly distinguish perfect-information calculation from insufficient-information clarification and propose ambiguity injection as future work. That paragraph suggests a question; it does not establish that nobody subsequently answered it. [Published paper](https://aclanthology.org/2025.acl-long.766.pdf).
- **GBFR, ACL 2026:** Sections 3.3–4 implement graph-bounded calculation and counterfactual missing/mismatched entity, period and metric cases. Safe financial abstention with symbolic constraints is therefore already published. [Published paper](https://aclanthology.org/2026.acl-long.1273.pdf).
- **FinMirror:** The current source README specifies independent paired worlds, calculation and operand provenance, abstention, deterministic rewards, positive equivalence checks and local model baselines. It is a public engineering artifact rather than a verified peer-reviewed result. It nevertheless directly collides with a generic financial metamorphic harness. [Repository](https://github.com/faceWang753/finmirror).
- **FinVerBench:** Its full HTML reports changes caused by rounded rendering and incomplete observability. A reward audit must distinguish training-target validity from this already-studied statement-verification construct; neither “rounding matters” nor “benchmark validity matters” is a new claim. [Full text](https://arxiv.org/html/2605.29586v1).
- **AbstentionBench:** Full-text Sections 2–4 cover underspecified tasks and effects of reasoning post-training. It prevents presenting “reasoning can worsen abstention” as a new general finding. [Full text](https://arxiv.org/pdf/2506.09038).
- **Fin-R1:** The full text describes finance-specific data and SFT followed by GRPO. Domain training alone is insufficient differentiation. [Full text](https://arxiv.org/pdf/2503.16252).

### Concrete preliminary observation: execution can conceal invisible precision

Source: the public MIT-labelled `coslinedev/financial-rlvr-10k-enterprise` dataset, pinned revision `6cfa9a71e777026ba7242fbbb96c11c7dece5011`.

[Exact JSONL bytes](https://huggingface.co/datasets/coslinedev/financial-rlvr-10k-enterprise/resolve/6cfa9a71e777026ba7242fbbb96c11c7dece5011/financial_rlvr_10k_enterprise_verified.jsonl) · [Dataset card](https://huggingface.co/datasets/coslinedev/financial-rlvr-10k-enterprise).

Downloaded bytes have SHA-256 `86968a146a09e2ba1b19aac3a5ca2bec7e878358341a7972fddeb4b8cd7754af`. There are 10,000 rows, 9,205 distinct prompts, three formula domains and 2,030 edge-case rows. This is narrow coverage; the dataset had only 83 downloads and one like in the inspected API snapshot. It cannot stand in for financial RLVR generally.

Row `fin-rlvr-10k-00002` asks for terminal value with cash flow 740, discount rate **10.0%** and growth **3.5%**. Applying `740/(0.10-0.035)` to those visible values gives **11,384.6153846**. The supplied code instead uses **0.0995** and **0.0346**, yielding the stored gold **11,402.1572**. A solution that follows the stated input can therefore disagree with an execution-verified gold value.

A preliminary independent calculation screen parsed all 7,970 ordinary cases using prompt key–value pairs and separately written WACC, Gordon-growth and Black–Scholes formulas. It did not execute dataset code. At absolute tolerance `1e-4`:

| Formula domain | Ordinary rows | Prompt calculation differs from gold |
|---|---:|---:|
| WACC | 2,682 | 0 |
| Gordon-growth terminal value | 2,655 | 2,385 |
| European call pricing | 2,633 | 0 |

Among ordinary terminal-value rows, 2,218 exceed relative error `0.001`; 127 exceed `0.01`. Median relative discrepancy is about **0.00316**. This is not merely a count of floating-point discrepancies. The result still requires a second independent implementation and an adjudicated sample.

**Interpretation boundary:** the dataset card advertises numerical correctness within `±1e-4`, but the inspected repository exposes no verifier implementation. These counts are numerical mismatches, **not observed reward rejections or demonstrated training failures**. We have neither trained a model nor reproduced the claimed reward engine. A looser relative tolerance changes the result substantially. The exact-source formula, visible-input interpretation and evaluation tolerance must all be stated.

Edge cases also announce `[EDGE CASE]` in their prompt. That marker can offer a shortcut for a trap classifier. A zero-maturity call has a valid intrinsic payoff, which the supplied code actually calculates while emitting a trap string. We must distinguish a singular general formula, a valid boundary solution and an unanswerable problem; the mere trap label is not proof of a financial error.

### A defensible conditional contribution

Provisional question: **When does execution-verified financial supervision penalize solutions grounded in the rendered input, and can an explicit precision-and-domain contract eliminate those false penalties without accepting financially invalid answers?**

The artifact would connect each prompt-visible operand to its precision, units and formula domain, then test reward behavior against independently derived admissible solutions. The scientific contribution would be measured failure mechanisms and a validated repair, not the JSON schema itself. It should include multiple independent generators or datasets, clear negative controls, and held-out cases.

Distinguish two contracts: a stated number treated as exact, and a number explicitly declared rounded. For rounded inputs, propagate intervals and report when no unique requested answer exists. For exact inputs, recompute gold from the displayed values. Do not silently reinterpret every financial number as uncertain.

### Go/no-go before committing the deadline

1. Reproduce the observed hidden-precision discrepancy with Decimal arithmetic and independently inspect a stratified sample.
2. Audit at least one independent source/generator; do not inflate a low-use dataset bug into a field-wide conclusion.
3. Implement only the documented reward comparator or clearly label a comparator as our reconstruction. Report false rejection and false acceptance separately.
4. Add repaired versus original targets and positive controls that preserve valid boundary cases. Training consequences remain optional and cannot be claimed without a matched experiment.
5. If the effect is isolated, cannot survive realistic tolerances, or adds no distinction from FinVerBench, stop the paper claim. Release a reproducible audit note instead.

Five open primary PDFs were saved in the ignored `literature/pdfs/` cache: FinChain, FinanceReasoning, Fin-R1, AbstentionBench and GSM-Symbolic, with text extraction. GBFR and FinVerBench were read through primary full-text web pages. The pinned JSONL and numerical-screen summary are also in that ignored cache. No IU-gated access was used in this subtask.
