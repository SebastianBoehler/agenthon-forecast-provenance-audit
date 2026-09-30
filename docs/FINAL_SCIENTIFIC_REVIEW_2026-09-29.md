## Executive summary (read this first)

The completed 800-response study supports a bounded audit and observed grading disagreement, not a new verification method, broad model ranking, or training-harm claim. The main DeepSeek result is sound: source-cent comparison denies 55 of 136 numerically valid strict-format answers. The selected Gordon ordering reversal is confined to post hoc extraction.

One additional attribution issue is confirmed: two Qwen3 4B denials occur in passing WACC, because the acceptance neighborhoods around the exact formula and rounded source label differ. They are comparator-centering effects, not defective-label effects. The planned GEPA pilot must prevent that nuisance difference from changing its passing-control rewards.

Before freezing the pilot, specify identical rate conventions across all splits, reward serialization, feedback fields, selection rules, and transfer-label provenance. These are substantive controls, not optional presentation improvements. This review edits no manuscript, frozen record, or implementation and performs no inference, publication, contact, or editor action.

### Basis and review lens

Reviewed the completed [manuscript](/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/paper/answer_contract_audit.tex), [independent result checks](/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/docs/MODEL_GRADING_INDEPENDENT_RESULTS.md), saved 800-response aggregates and relevant rows, [expansion triage](/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/docs/RESEARCH_EXPANSION_TRIAGE_2026-09-29.md), and primary prior-art sources. This is a claims review, not a replacement numerical scorer.

The Hennig/Lu lens is explicitly inferred from examined teaching and thesis-writing guidance: ask an interesting, falsifiable question; justify the method; compare the obvious alternative; distinguish established knowledge from contribution; and make results traceable. This is **not faculty feedback, endorsement, or a predicted grade**. No private course quotations are included; supporting course-specific notes remain private and unbundled.

### Confirmed manuscript issues, in priority order

**P1 — Numerical validity and comparator agreement are different measurements.** The Qwen3 4B WACC value 9.4667 lies within 0.005 of the independent value 9.4636734694, but outside 0.005 of the correct source label 9.46. Likewise, 9.4333 is close enough to 9.4350602410 but not its source label 9.44. Thus 38 recovered-valid 4B denials comprise 36 constructed-Gordon cases and two passing WACC cases. Keep the counts; explain that denial counts need not all arise from defective targets. The DeepSeek 55/136 and 97/199 headlines do not contain this WACC effect.

**P1 — Coverage prevents a capability or size ranking.** The primary parser admits 0, 34, 0, and 137 answers in manuscript roster order. Post hoc recovery admits 189, 90, 192, and 200; the 4B recovery rates differ drastically by family. Comparing 46/90 with 41/189 would compare selected subsets. Comparing 46/200 with 41/200 is an all-attempt endpoint comparison, not isolated financial ability or parameter-count benefit. Root's planned prominent coverage statement is necessary.

**P1 — Preserve the reversal's exact scope.** On the 50 constructed-Gordon questions, source-cent credit is Qwen3 1.7B 10 versus DeepSeek two; reference integer credit is 22 versus 50. This reverses ordering only under the exploratory numeric-final-line endpoint and this comparator/family. The current sentence has those qualifiers. It must not become an abstract claim of general model misranking.

**P2 — Keep the controls that limit novelty.** Integer plus original-label half-unit tolerance solves tested Gordon separation, including the observed model answers. DCF 5% widening succeeds against its tested omission controls. These successes strengthen the diagnosis and rule out sweeping claims that arithmetic checks or tolerance widening cannot work. Final-value collisions still prevent certifying reasoning.

**P2 — Keep source and interpretation boundaries attached to the result.** Inspection identifies a wrong debt quantity and generator–verifier coupling; it does not reproduce upstream verifier execution or prove the public code pin is the dataset's exact generation commit. Hidden-precision discrepancies are conditional on exact-input semantics. DeepSeek's 3.06 binomial answer is continuous-compounding compatible, not an unequivocal arithmetic error. The union sensitivity preserves all 975 source conflicts but does not certify reasoning.

No new aggregate-number discrepancy was found. Independent validation records agreement across the original 600, added 200, combined endpoints, and convention scores. Numerical agreement does not remove the interpretation issues above.

### Pilot blockers to resolve before freezing

1. **Remove compounding ambiguity everywhere.** The triage explicitly specifies the effective one-period rate only in authored transfer questions. Apply the same declaration in the immutable wrapper or every binomial optimization/development/numerical-holdout question. Preserve original source wording separately and record the specification patch. Otherwise “financial deterioration” can mix wrong quantity with a defensible alternative convention.
2. **Hold reward geometry fixed.** Freeze output serialization and comparator semantics. For passing ordinary Gordon and WACC, source and repaired objectives should give identical decisions on the same candidate outputs; assert this on boundary candidate grids. Using rounded-source-centered versus exact-formula-centered neighborhoods changes controls even with correct labels. If that change is intentional, it is a second intervention requiring separate attribution. Keep the independent financial-validity oracle separate.
3. **Freeze the feedback intervention.** Specify whether reflection receives a binary score, numerical assigned target, error distance, or explanatory text. Use the same schema and information budget in both objectives. Source-objective reflection must not receive the repaired target, financial-validity score, source diagnosis, or an oracle-generated correct explanation. Different target values may be legitimate supervision; then call the experiment adaptation under label feedback, not reward-only optimization.
4. **Freeze prompt selection without test access.** Final prompts must be selected by their assigned objective on the declared development set, with a fixed tie rule. Neither numerical holdout nor transfer validity may choose prompts, seeds, stopping points, or preferred results. Pair optimizer seeds across objectives and show each seed separately. Two seeds demonstrate only limited optimizer robustness, not independent datasets or population significance.
5. **Compare trajectories on common questions.** Changing optimization minibatches can manufacture apparent reward/validity movement. Score a candidate's same saved development answers under both objectives for descriptive trajectories; keep the holdouts sealed for the final comparison. Compare final source/repaired prompts with the unchanged seed and frozen manual baseline on all 72 holdout attempts per prompt, separated into 48 source and 24 transfer questions.
6. **Label authored transfer correctly.** The 24 authored questions have no released labels. A source-style reward there extrapolates the traced debt or unrounded-Gordon rule; it is researcher-generated. Independently check both values and report that provenance. New wording and operand tuples within four known formulas demonstrate limited wording/operand transfer, not unseen financial mechanisms or independent-source generalization.
7. **Separate format learning from financial changes.** Freeze the wrapper/parser before the off-split format gate. Report all-attempt coverage and quantity/rounding errors separately. If format alone improves, do not call it financial harm or repair. Retain failed preflights and do not repeatedly adjust extraction until held-out results look favorable.
8. **Make the cap an implemented stopping rule.** `max_metric_calls` is not a money/token/time bound. Pin the GEPA version, actor/reflector routes, all call types, caching policy, and actual completed counts. Count validation and reflection work too. If caps truncate search or the assigned objective never improves, the pilot is inconclusive about adaptation consequences; do not infer that corruption is harmless.

The manual baseline may contain correct formulas and rounding instructions, so document its privileged information. If it matches the repaired GEPA result, the useful finding concerns objective fidelity, not optimizer superiority. API temperature zero does not guarantee deterministic serving or immutable weights; retain request identities and time/order, and avoid stronger causal language than this controlled prompt-adaptation experiment supports.

### Novelty blockers and defensible contribution

The triage is appropriately skeptical. [FinanceReasoning](https://aclanthology.org/2025.acl-long.766.pdf), [FinChain](https://aclanthology.org/2026.acl-long.662.pdf), and [FinVerBench](https://arxiv.org/html/2605.29586v1) already cover financial label repair, precision, and observability consequences. They block firstness for a general answer-contract principle.

The proposed adaptation effect also has direct antecedents. [Delay, Plateau, or Collapse](https://arxiv.org/html/2605.02909v2), especially §§4.2–4.6, studies systematic verifier errors, differing optimization dynamics, and oracle mitigation. [EPO-Safe](https://arxiv.org/html/2604.23210v1), §§2.4–3.3, already contrasts reward-only reflective adaptation with an independent corrective channel. [GEPA](https://arxiv.org/abs/2507.19457) is an existing reflective optimizer. A positive pilot would not establish a new overoptimization phenomenon or optimizer.

The exact defensible addition is: **a bounded prompt-adaptation experiment grounded in traced defects from released financial supervision, with independent formula checks, passing controls, and new-operand/authored-wording evaluation**. That goes beyond changing grades on fixed outputs if actual prompts change behavior. It remains a case study with one actor, four formula families, and a reconstructed source objective.

### Required bounded claim wording

| Evidence | Wording that the evidence permits |
|---|---|
| Completed audit and fixed-response study | “In selected pinned financial supervision families, source labels conflict with independent valuation or explicit rounding. Reconstructed source-label grading denies numerically valid observed answers.” |
| Source code inspection | “The inspected generator computes financing debt as the call price; the inspected verifier regenerates that template, allowing a shared computation error.” |
| Selected-family reversal | “For these 50 constructed-Gordon questions under post hoc numeric extraction, source-cent and integer-contract grading reverse the two models' ordering.” |
| Positive pilot meeting all frozen gates | “For this actor and GEPA configuration, adaptation to the reconstructed source objective increased its reward while reducing independently assessed numerical validity on held-out operands and authored wording; the repaired-objective run avoided that deterioration.” Include both seeds and family counts. |
| Null/inconclusive pilot | “The bounded pilot did not demonstrate the specified adaptation consequence.” Distinguish no search progress, format changes, and genuine objective/validity outcomes. |

Do not write “verified data cause model degradation,” “repair improves training,” “GEPA discovers financial truth,” or “general financial benchmark.” The pilot updates prompts, not weights; the existing 800 responses measure grading only. Keep those experiments separate even if both appear in one paper.

### Decision

Proceed with a precisely frozen pilot only after the controls above are concrete and independently checked. Preserve the completed audit as the submission-ready scientific core; add the pilot only after full scoring and verification, including unfavorable seeds. The workshop contribution is credible at this scope. Main-conference significance still requires evidence that the lesson transfers beyond these already understood sources and formulas; another architecture or a positive two-seed demonstration does not by itself establish it.
