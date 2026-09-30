## Executive summary (read this first)

**Working paper:** *What Does Execution Verification Verify? Answer Contracts in Financial Reasoning Data*. This is the strongest new-paper lead found so far for the [Agenthon 2026 workshop call](https://www.agenthon.net/#call-for-papers), which welcomes evaluation and verification research. Two independent public finance datasets exhibit distinct prompt–label contract problems: an answer not uniquely identifiable from displayed rounded inputs, and an output label that ignores the requested rounding. The paper claim is **conditional**: establish comparator consequences, adjudicate examples, validate a repair, and rule out obvious explanations before submitting. No acceptance probability can be established from this pilot.

## Motivation, research question, and geometry

An executable solution can faithfully calculate from hidden generator values while disagreeing with displayed values. If those values were rounded for display, the visible question may admit an interval of answers rather than one exact target. A generator can also calculate a raw answer while the question explicitly requests a rounded answer. In either case, code execution verifies the arithmetic but not the full question–answer contract.

Geometrically, the model sees a point or set in the space of financial inputs, and the question defines a projection onto admissible output answers. A label can miss the contract by evaluating a nearby hidden input point or by omitting the required output projection. The practical question is: **How often do execution-verified finance labels disagree with prompt-admissible answers, what grading/training decisions does this change, and can a source-aware repair restore consistency without accepting wrong calculations?**

## Observations already reproduced

| Independent source | Verified label claim | Prompt–label issue | Current evidence boundary |
|---|---|---|---|
| [Financial RLVR 10k Enterprise](https://huggingface.co/datasets/coslinedev/financial-rlvr-10k-enterprise), pinned revision `6cfa9a71e777026ba7242fbbb96c11c7dece5011` | Executed code and a stored gold number | 2,385 of 2,655 ordinary terminal-value prompts differ from the gold by over the dataset card's stated absolute tolerance of 1e-4 when recomputed using their displayed cash flow and rates. Yet all 2,655 golds lie within the result interval if both displayed rates were rounded to the nearest 0.1 percentage point. Median relative interval width is 2.22%. Example: displayed $740, 10.0%, 3.5% imply $11,384.62 if exact; gold is $11,402.16. | **Underdetermination, not proof of an incorrect gold.** The stated tolerance has been applied analytically; actual verifier code and model reward have not been run. [Auditor](../scripts/audit_rlvr_dcf.py). |
| [Cosimo CFA/FRM 71k](https://huggingface.co/datasets/btech-software/cosimo-cfa-frm-71k), pinned revision `42244d29c6b9912683213a08d1a9c5b0373b381b` | Answer marked reference-code verified | All 1,000 `cr_eq_gordon` questions request the nearest whole unit; 946 stored labels instead have a different cent-level value. Example: prompt-consistent $31 versus stored $30.94. All 1,000 raw formula values independently agree with cent-level labels, isolating the requested-rounding conflict. Among 337 released preference pairs in this template, 312 `chosen` answers likewise differ from the requested whole unit. | A real answer-format conflict within one template and its preference supervision, not a measured downstream model effect. [Auditor](../scripts/audit_cosimo_gordon.py). |

Counts are rows within two selected generator families, not prevalence across all finance datasets. The sources are training-oriented synthetic releases, so evaluation-only results must not be generalized to all deployed finance agents. The DCF interval assumes conventional rounding of both rates to the displayed tenth of a percentage point; if the source defines those rates as exact, the prompt-consistent answer is the displayed-input calculation instead.

## Nearest-work gap, stated narrowly

| Work | What it establishes | Remaining question for us |
|---|---|---|
| [FinVerBench](https://arxiv.org/html/2605.29586v1) | Financial-statement error verification; observable versus hidden fields; rounding can change measured model performance. | Does execution-verified **training supervision** match both visible numeric inputs and requested output precision? |
| [FinChain](https://aclanthology.org/2026.acl-long.662/) | Expert-reviewed symbolic finance templates and executable reasoning checks. | Are prompt–label contracts an independent validation layer, and do repairs change decisions beyond execution checks? FinChain can serve as a negative-control source if its labels pass. |
| [FinanceReasoning](https://aclanthology.org/2025.acl-long.766/) | Corrects many existing financial QA labels and supplies program-formatted solutions. | Which generator-to-prompt transformations cause *systematic*, measurable conflict, and how should a verifier repair them? |
| [Arcifa and Carra, *Fair and cheap*](https://montanaresearch.org/publications/mrf-2026-04/) | Its official abstract already frames graded-answer determinacy from model-visible information and reports collapsed quant-finance task designs. | Our distinction would be a cross-dataset empirical audit of two training-label mechanisms, measured comparator effects and validated repairs. Only the abstract/open-data record was accessible; full-text overlap remains unresolved. |

We cannot claim to invent answer determinacy, finance verification, rounding awareness, or executable benchmarks. A paper would need to establish the **consequential empirical mismatch and a reliable correction**, rather than rename existing checks.

## Methodology and falsifiers

Use a dataset-validity audit as the research design: freeze source revisions and case inclusion before further results; derive answer contracts from the question visible to a model; recompute with independent Decimal or stable formula implementations; adjudicate a stratified sample twice; then assess comparators and repairs. The unit is a unique question/template case, with uncertainty clustered by generator, not individual row only. Report family counts and clean families alongside failures.

1. **Original labels:** record hidden generator operands when available, displayed operands, requested rounding, stored label and chosen answer trace. Execute no untrusted upstream code to derive our independent oracle.
2. **Comparator consequences:** reproduce published comparator code if it exists. Otherwise evaluate an explicit sensitivity grid of exact match, absolute/relative numeric tolerances and rounding-aware acceptance, always labeling these as reconstructed comparators. Include valid answers and deliberately wrong arithmetic to estimate false rejection *and* false acceptance.
3. **Repair:** for exact displayed inputs, regenerate from displayed values. For rounded inputs, derive an admissible interval and test whether its width makes exact grading meaningless; otherwise clearly declare the intended exact-number convention. Honor requested output precision. Compare original and repaired contracts on untouched cases and clean negative controls.
4. **Model relevance:** if feasible, collect frozen outputs from at least two different model families on a stratified case sample. Measure how many scientifically valid outputs change grade under the corrected contract. Avoid a causal RL-training claim without matched training runs.
5. **Falsifiers:** abandon the headline if documented comparators already accept prompt-faithful answers, conflicts collapse under legitimate conventions, independent adjudicators disagree substantially, clean controls acquire false accepts, or [the determinacy preprint](https://montanaresearch.org/publications/mrf-2026-04/) already reports the same dataset-level mechanism and repair.

## Paper outline and deadline gate

1. Problem and two concrete contradictions.
2. Related work and exact non-overlap.
3. Visible-input answer-contract formalism and source audit protocol.
4. Dataset-family results, comparator consequences and false-acceptance controls.
5. Repair ablations and model-output case study, if completed.
6. Limitations, dataset rights and reproducible artifact record.

The call accepts short papers in any format and length; submissions are due **30 September 2026 at 23:59 AoE**. This direction merits a short paper only if comparator and repair evidence are ready by that deadline. Source PDFs/data remain local and ignored; publish only allowed code, derived counts, case IDs and necessary examples. Preserve failed analyses and code evolution as part of the research artifact, following the agent-native reproducibility principle without claiming that principle as our novelty.
