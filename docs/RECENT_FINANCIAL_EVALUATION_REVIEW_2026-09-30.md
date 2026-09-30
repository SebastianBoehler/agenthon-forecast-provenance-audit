## Executive summary (read this first)

All three leads are real September 2026 arXiv v1 preprints. Their titles and authors are verified below. No official NeurIPS 2026 acceptance record was located or verified; this does not establish rejection. Full text was accessible for all three, so the assessments extend beyond abstracts.

These papers occupy broad claims about separating agent proposals from evaluation, auditing financial-agent weaknesses, and distinguishing output reliability from useful financial outcomes. They do not directly establish the released financial QA quantity/precision failures and fixed-answer grading disagreements measured in this repository. That narrower empirical distinction remains defensible; a general new verification principle does not.

This is a bounded primary-source review, checked on 2026-09-30. The relevance judgments and proposed follow-ups are our inferences, not the papers' endorsements. No inference, paid compute, manuscript edits, or frozen-record changes were performed.

## Verified records and access

| Work | Exact authors | Verified version and submission UTC | Access and venue boundary |
|---|---|---|---|
| [Propose, Don't Judge: An Anytime-Valid Referee for LLM Agents That Mine Investment Factors](https://arxiv.org/abs/2609.27051v1) | Bo Qu; Mingguang Chen; Licheng Wang | v1; 2026-09-22 20:43:44 | [Full HTML](https://arxiv.org/html/2609.27051v1), including methods and limitations; no acceptance venue stated in the arXiv record. |
| [SoK: Trading Agents or Market Crashers? Dissecting Robustness and Security Failures in Academic Financial LLM Trading Schemes](https://arxiv.org/abs/2609.19705v1) | Mengxiao Wang; Nitesh Saxena | v1; 2026-09-17 04:59:08 | [Full PDF](https://arxiv.org/pdf/2609.19705v1), including codebook methodology and limitations; no acceptance venue stated in the arXiv record. |
| [The Price of Thought: Does Test-Time Reasoning Pay in LLM Trading?](https://arxiv.org/abs/2609.30705v1) | Jiayi Chen; Guiling Wang | v1; 2026-09-25 02:28:01 | [Full HTML](https://arxiv.org/html/2609.30705v1), including methods, appendices and limitations; no acceptance venue stated in the arXiv record. |

Only v1 appeared in each submission history at inspection. Exact-title searches restricted to NeurIPS, its proceedings, and OpenReview found no matching official acceptance record. The [NeurIPS 2026 paper listing](https://neurips.cc/virtual/2026/papers.html) and [official OpenReview group](https://openreview.net/group?id=NeurIPS.cc/2026/Conference) exposed incomplete JavaScript views to the retrieval tool; proceedings/API retrieval was unavailable. Accordingly, cite these as preprints unless an affirmative official record is subsequently verified. Posting dates alone establish no acceptance status. No full-text redistribution was made.

## Propose, Don't Judge

**What was inspected.** Sections 2–4, 7.3 and 9. A factor proposer faces a frozen statistical referee using post-submission evidence, online admission and retirement. Existing sequential-testing theory supplies the guarantees; this is not a claim of new e-process theory. Script, bandit and LLM proposers are compared with frozen and deliberately leaky referees, using synthetic truth and a CSI500 walk-forward study. [Primary full text](https://arxiv.org/html/2609.27051v1).

**Material limits.** Validity depends on information access and a conditional null; whitening does not prove the marginal-null guarantee. Real-market evidence comes from overlapping starts in one market. The realized label overlaps admission; post-admission rejudgment reduces the headline ratio by about a third. Some LLM comparison cells are absent. A patience-matched fixed-horizon comparator produces better portfolio results; certification is not investability. Code/calls are available on request and market data cannot be redistributed. Exact snippet, §9: “no held-out period beyond the walk-forward”. [Primary full text](https://arxiv.org/html/2609.27051v1).

**Collision and relevance — our assessment.** Agent-proposes/referee-judges separation is occupied. Our audit concerns whether the purported referee computes the requested quantity and whether released labels satisfy visible precision instructions; statistical admission validity is a different endpoint. Merely freezing a checker does not repair its quantity semantics. We cannot transfer their false-discovery guarantee to QA labels.

**One feasible follow-up.** Without new calls, compare reconstructed source rules and an independently authored quantity checker on the same saved answers, preserving passing-family controls. Report false credit and denial conditional on the declared reference, rather than implying formal sequential validity. This refines the existing mechanism evidence; it is not a new referee method.

## SoK / FARSIGHT

**What was inspected.** Sections 3–5 and 7. FARSIGHT is a codebook for published trading-system designs, not a fixed executable benchmark. Selection narrows 127 candidates to 40 full texts and 15 schemes, with inclusion through March 2026. It rates four robustness dimensions and three security surfaces. Its 80% robustness and 100% security headlines are scheme-level ratings, not measured live attack success rates across 15 deployed agents. [Primary PDF, pp. 3–6](https://arxiv.org/pdf/2609.19705v1).

**Material limits.** Section 7 says paper-based scoring cannot replace penetration testing or live red-teaming. A missing control may exist in released code or a later version. Discussion-level prototype/live-market assertions should not be conflated with empirical validation of all 15 schemes. Exact snippet, §7: “control is not evidenced”. [Primary PDF, pp. 13–14](https://arxiv.org/pdf/2609.19705v1).

**Collision and relevance — our assessment.** Broad systematic financial-agent weakness audits and external enforcement recommendations are occupied. Its security/design assessment does not establish our observed released-label mismatches. Conversely, our numerical audit establishes no prompt-injection resilience, market robustness, or live economic harm. AI review agreement is not a substitute for grounded financial adjudication.

**One feasible follow-up.** Add a small evidence matrix distinguishing published claim, separately pinned implementation, observed saved-record failure, and unknown original generation binding. Check any control claimed absent against accessible code before concluding absence. This guards against converting a documentation gap into a measured system defect.

## The Price of Thought

**What was inspected.** Sections 3–4, 6–8 and relevant appendices. Within-backbone reasoning-level comparisons hold information, prompt, schema and portfolio rule fixed across three providers and three information conditions. The study uses 241 return dates in a 2024 US-equity backtest, repeated generations, transaction costs and paired uncertainty estimates. Large prediction counts are not independent market observations. [Primary full text](https://arxiv.org/html/2609.30705v1).

**Material limits.** Reasoning labels represent unequal compute across providers. Schema reliability can improve without net-return improvement. Most primary intervals include meaningful gains and losses; detectable effects exceed the declared economic threshold. Masking cannot exclude latent historical knowledge. The simulator omits several live execution frictions, and the experiment does not identify hidden reasoning mechanisms. Exact snippet, §8: “not an equivalence claim”. [Primary full text](https://arxiv.org/html/2609.30705v1).

**Collision and relevance — our assessment.** Controlled financial reasoning ablations, cost accounting, and reliability/outcome separation are occupied. Our quantity reminder is not a provider reasoning-effort intervention. No observed gain on 22 provisional references supports neither universal ineffectiveness nor economic equivalence. Typed numeric matching, grounded quantity support, and portfolio value must remain separate endpoints.

**One feasible follow-up.** Use the existing ledger to display schema coverage, provisional typed matches, quantity support, and billing completeness side by side. Keep the unknown-cost reservation separate from observed spend. This needs no new inference and makes measurement losses visible; it does not test whether extra reasoning pays in trading.

## Consequence for this paper

Recommended contribution wording: **“We audit selected released financial supervision for quantity and precision inconsistencies, diagnose corresponding mechanisms in separately pinned public code, and measure how reconstructed graders score unchanged model answers. Passing controls and independently checked arithmetic bound the findings; document-reference semantics remain provisionally AI reviewed.”**

Do not equate the code diagnosis with a trace of the original dataset generation or upstream verifier execution. Do not imply first financial evaluation audit, first independent referee, a new contract-validation principle, causal training effects, expert-certified reference truth, or demonstrated investment harm.

These trading papers are useful adjacent comparisons. FinanceReasoning, FinChain and FinVerBench remain closer collisions for financial QA data repair and verification. Adding all three citations merely for recency would dilute the paper. Propose merits a specific evaluation-separation citation; Price merits a limitations citation if reliability-versus-value is discussed; FARSIGHT merits inclusion only for an explicit comparison of documentation audits with released-artifact evidence.

For a main-track claim, stronger evidence would need independently adjudicated quantity references and transfer across independently released pipelines/tasks, with repairs tested against unchanged controls. None of these three preprints removes those gaps, and none provides evidence of acceptance for our paper.
