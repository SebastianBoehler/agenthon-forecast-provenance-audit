## Executive summary (read this first)

Independent review confirms the frozen census, all 2,548 control equality labels, eight financial reference computations, both completed local arms, and the recorded scoring endpoints. No discrepancy was found in the actual frozen inputs or saved responses. All 96 scheduled cohort attempts returned; eight replies at the output-token cap and two other strict-final nondecisions remain separately accounted for.

The result is bounded: the frozen native grader fails targeted equivalent/unequal controls, but neither local model supplies an observed unequal-value credit on this eight-question MATH panel. Financial original-label scoring denies 16 of 28 contract-compatible answers across repeated responses to eight questions. This is numerical grading evidence, not general semantic validation, historical RecursiveMAS score inflation, or a model ranking result.

This is an AI technical review, not human expert adjudication, actual Hennig feedback, or an acceptance prediction. No model endpoint was called, and no frozen code, protocol, output, or manuscript was edited.

### What was checked independently

- Read the frozen [protocol](GRADER_COMPARISON_PROTOCOL_V1.md), preparation script, all `src/grader_comparison/` modules, original freeze, census, controls and cohort. Every original freeze file checksum matches.
- Reparsed the 500 references and all control candidates with a separately written Decimal/Fraction parser under the admitted grammar, without importing the production scalar parser. Checked equality, intended positive/negative roles, denominators and zero handling. No binary-floating-point arithmetic or executed corpus/model expressions were used.
- Replayed all 2,548 native control decisions through the hash-checked upstream definitions and independently recomposed the normalization ablations. No recorded control or ablation discrepancy occurred.
- Recomputed all eight financial unrounded targets directly from visible operands with Fraction arithmetic: Gordon, risk-neutral binomial valuation under the added simple-compounding instruction, and WACC. They match the frozen exact references and high-precision Decimal formulas; the constructed-Gordon rounded targets also match.
- Reconstructed the MATH hash selection and checked the financial original-question hashes against the earlier 200-question exclusion manifest. The selected cohort is exactly eight MATH and eight financial questions, with two financial questions per family.
- Independently scored all 96 saved responses, validated every request against frozen prompt/config/model fields, checked raw-message/stat consistency, and verified both collection-receipt hashes. Independent values agree with the production row endpoints. A fresh in-memory production analysis also agrees with every field of persisted `analysis.json`.

The independent checker was a temporary local script; the frozen production analysis and [portable replay](../scripts/replay_grader_comparison.py) supply the retained execution paths. This review does not claim a new isolated environment or independent conceptual discovery.

### Census and authored controls

All 500 IDs are present once in the reference census: 368 grammar-eligible and 132 excluded. Seven admitted cases carry the keyword flags, leaving 361 eligible without flags. Grammar eligibility is not a semantic adjudication of every question. The flag regex is a narrow wording screen, not an exhaustive approximation detector.

The 368 admitted questions contain **174 distinct exact reference values**. The 2,548 control rows contain **695 distinct numerical reference/candidate pairs**; distinct representations and repeated values remain in the row count. These are grouped stress tests, not independent observations of natural model errors.

| Transformation | Rows | Independent value relation |
|---|---:|---|
| Identity | 368 | Equal |
| Canonical rational | 368 | Equal |
| Unreduced fraction | 368 | Equal |
| Terminating decimal | 347 | Equal |
| Shift by one tenth | 368 | Unequal |
| Shift by one | 368 | Unequal |
| Nonzero sign flip | 361 | Unequal |
| Total | 2,548 | 1,451 equal; 1,097 unequal |

| Frozen comparator | Unequal controls accepted / 1,097 | Equal controls rejected / 1,451 |
|---|---:|---:|
| Native | 354 | 372 |
| Without integer-part branch | 354 | 406 |
| Without digits-only branch | 0 | 420 |
| Without both branches | 0 | 456 |
| Literal string equality | 0 | 456 |
| Exact rational equality | 0 | 0 |

All 354 false accepts in this factory are sign flips. Native false rejects comprise 361 unreduced fractions, seven canonical representations and four terminating decimals. Every identity is accepted. Exact equality's zero errors establish consistency on the admitted domain; equality and those control labels are not independent expert truths about source solutions.

**Coverage limitation:** both shifted negatives use canonical `p/q` rendering. A decimal-form shift can expose an integer-part collision that this representation does not. Thus unchanged false-accept counts after removing the integer-part branch do not establish that branch's general safety. Prior authored decimal counterexamples remain separate evidence; do not silently add different controls to this frozen denominator.

### Completed local model endpoints

Three unseeded stochastic repetitions give 24 scheduled MATH and 24 scheduled financial responses per model. Both checkpoints use the recorded Q4_K_M/native-template settings; their families, total/effective size and training differ. The eight MATH references comprise seven integers and one noninteger fraction. These are repeated responses to a tiny hash-selected panel, not 24 distinct mathematical tasks per model.

| Model / domain | Scheduled and returned | Strict final admitted | At cap | Other final nondecision | Exact/contract matches | Original/native full credit |
|---|---:|---:|---:|---:|---:|---:|
| Gemma / MATH | 24 | 22 | 2 | 0 | 20 | 20 |
| Qwen / MATH | 24 | 20 | 3 | 1 | 17 | 18 |
| Gemma / finance | 24 | 21 | 3 | 0 | 13 | 6 |
| Qwen / finance | 24 | 23 | 0 | 1 | 15 | 6 |

MATH matches mean exact agreement with an annotated scalar. Financial matches mean agreement with the declared numerical target/tolerance and requested integer rounding; units are fixed by family. Final admission does not certify the entire explanation or every formatting instruction.

Native and exact equality have **zero false accepts and zero false rejects on the shared, admitted MATH scalars**. Native full extraction additionally credits one numerically equal Qwen scalar outside the strict final-line parser. Its 18 versus 17 difference is extraction/format coverage, not an unequal-value credit. Across all admitted native extracted scalars, observed unequal-value credit is zero.

Removing both lossy normalization branches reduces shared MATH credit to 17 for Gemma and 14 for Qwen, losing three equivalent answers per model. Exact rational parsing preserves those values. This is a useful counterexample to treating stricter literal normalization as sufficient equivalence checking.

Financial complete-contract matches are 13 and 15, versus six original-label credits each. All 12 original-label credits satisfy the audited contract. The **16 valid-value denials** comprise 12 constructed-Gordon rounding denials and four call-price denials. The corrected-unrounded-cent ablation credits seven Gemma and nine Qwen answers; applying the requested whole-unit output contract adds six per model. This distinguishes quantity/reference repair from rounding compliance on this finite panel.

Report denominators together: 16 unique questions, 96 scheduled/returned attempts, 86 strict-final admissions, eight cap nondecisions, two other final nondecisions, and 28 financial contract matches. Do not turn 16/28 into an estimate for financial AI generally or pool controls with natural responses.

### Qwen continuation and timing

The original Qwen readiness gate stopped before any cohort call: all three authored arithmetic values were correct, but the first placed its final marker inline and failed strict admission. The [separate continuation](../scripts/continue_grader_comparison_qwen.py) permits a trailing literal marker only for the three preserved source-free readiness probes. It reruns no probe, replaces no question, and keeps the scientific parser, prompts, configuration and scorers frozen.

Its saved amendment was declared **2026-09-30 15:30:48.971224 UTC**, after Gemma completed 48 responses and before every inspected Qwen cohort start. Original probe and continuation-code hashes match the amendment. This is a disclosed post-gate readiness change, not pristine preregistration or proof of strict-format reliability. It is appropriate for allowing collection while retaining subsequent format failures.

### Implementation and reporting limits

No implementation defect affecting the frozen control truths or these 96 scores was found. Retain these narrower limits:

- Native grading is the pinned RecursiveMAS public endpoint, not the official MATH/PRM800K evaluator or a proven historical paper evaluator. Financial original-label comparators are reconstructed sensitivities, not reproduced upstream reward execution.
- The frozen census field `problem_sha256` is a salted selection digest, not a raw problem-byte checksum. The portable projection's `salted_problem_order_sha256` names it correctly. Original source byte hashes provide identity; preserve the historical field unchanged.
- The scalar helper lacks an explicit length/digit guard. An authored 5,000-digit scalar raises ValueError rather than returning unsupported. This did not occur in the admitted source/control/saved-output checks. Do not advertise unrestricted parser robustness; any future fix must be versioned separately.
- At-cap classification means exactly 1,024 recorded output tokens; no native finish reason is available. Preserve the conservative frozen censoring rule without claiming that every such response is conclusively truncated.
- The analyzer's request validation is narrower than the independent check performed here. It also assumes the valid frozen model/repetition schedule. Preserve receipt/hash checks and the complete schedule when replaying or projecting records.
- The portable artifact retains extracted scalars and accounting but omits prompts/raw prose. Its replay cannot independently reconstruct full-response extraction, financial semantics or fresh generations. The in-memory full-record checks in this review cover more than that portable scope.

### Evidence binding and final scientific judgment

Original scientific freeze SHA256: `bec1da3047f061ebc80a8dc0029470e0595fd26ae6059f3daa1c346e27ea45b1`.

Validated persisted analysis SHA256: `bc8a58fa42d5ce0ec5b2d63abb9a34619ee9219b088538b5884bbb19fba77f6d`.

Defensible wording: **“A pinned released mathematical grader fails targeted exact-value controls, while the tested natural scalar panel shows no unequal-value credit; financial reconstructed original-label grading denies 16 of 28 numerically contract-compatible saved answers.”**

This strengthens a bounded empirical audit by adding an actual public grading endpoint, controls, a stricter-equivalence tradeoff and new saved local answers. It does not establish a new semantic-verification method or remove the main-track gaps in breadth, independent financial adjudication and downstream effects. Retain the negative natural-MATH finding as prominently as the authored failures.
