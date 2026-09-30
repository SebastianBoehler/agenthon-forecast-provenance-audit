## Executive summary (read this first)

The defensible contribution is a particular failure in released financial supervision and its observed grading consequences. Annotation repair, financial formula checking, unit/precision validation, visible-answer determinacy, interpreter assistance and scoring-policy sensitivity are established. The strongest evidence here is financing debt credited as a call price, including labels that pass the tested price bounds, with passing comparison families and unchanged-answer grading. The present follow-up does not establish an effective quantity-repair method or expert-certified financial truth.

This is a targeted primary-source review, not an exhaustive novelty search or an acceptance prediction. No manuscript, scientific input, result, freeze or bundle was changed. No model was called. Sources were checked on September 30, 2026; the review snapshot was taken after 13:57 UTC. Page references below distinguish one-based PDF pages from printed proceedings pages.

### Access and version record

The six works below have accessible full texts. I read their cited methods, evaluation and limitation passages, rather than relying only on abstracts. This does not claim a cover-to-cover review of every appendix.

| Work | Exact primary version inspected | Relevant full-text locations |
| --- | --- | --- |
| Tang et al., FinanceReasoning | [ACL 2025 publisher record](https://aclanthology.org/2025.acl-long.766/), DOI 10.18653/v1/2025.acl-long.766; [proceedings PDF](https://aclanthology.org/2025.acl-long.766.pdf) | §2.1, Table 1, Appendix C.1, limitations; PDF pp. 2–4, 9, 14; printed pp. 15721–15749 |
| Xie et al., FinChain | [ACL 2026 publisher record](https://aclanthology.org/2026.acl-long.662/), DOI 10.18653/v1/2026.acl-long.662; [proceedings PDF](https://aclanthology.org/2026.acl-long.662.pdf) | §3.2, §§4.1–4.2, A.3, B.2; PDF pp. 4, 15, 17; printed pp. 14529–14553 |
| Panda, FinVerBench | [Author preprint v1](https://arxiv.org/abs/2605.29586v1), submitted May 28, 2026; [PDF](https://arxiv.org/pdf/2605.29586v1), [HTML](https://arxiv.org/html/2605.29586v1) | §§3.5, 6.4–6.5, 7.1–7.2; PDF pp. 8, 22–23, 26–27 |
| Krumdick et al., BizBench | [ACL 2024 publisher record](https://aclanthology.org/2024.acl-long.452/), DOI 10.18653/v1/2024.acl-long.452; [proceedings PDF](https://aclanthology.org/2024.acl-long.452.pdf) | §3.1, limitations, A.1–A.2; PDF pp. 3–4, 9, 13; printed pp. 8309–8332 |
| Chang et al., Measurement Risk | [Author preprint v2](https://arxiv.org/abs/2604.27374v2), revised July 14, 2026; [PDF](https://arxiv.org/pdf/2604.27374v2), [HTML](https://arxiv.org/html/2604.27374v2) | §§4, 6.4, 7.1–7.4, 8–9, Appendix C; PDF p. 4 for §4 |
| Chen et al., Program of Thoughts (PoT) | [Author preprint v4](https://arxiv.org/abs/2211.12588v4), revised October 23, 2023; [PDF](https://arxiv.org/pdf/2211.12588v4), carrying the TMLR 2023 header | §2.2, financial evaluations, limitations; PDF pp. 4, 12 |

FinVerBench is cited as a preprint, without a peer-reviewed venue claim. Measurement Risk v2 is titled *Measurement Risk in Supervised Financial NLP*, whereas the [IEEE CIFEr record](https://doi.org/10.1109/CIFEr67845.2026.11692425) uses *LLM-Based Financial NLP*. The IEEE final text was not read; the inspected version must remain explicit. Its fourth author is Rongdong Chai. The PoT [publisher forum](https://openreview.net/forum?id=YfZ4ZPt8zd) presents an access challenge; the author v4 full text was read, without claiming byte identity with a publisher-final PDF.

The reader-gated Arcifa/Carra *Fair and cheap* manuscript remains an access gap inherited from the existing review: its abstract supports visible-answer determinacy, but exact experimental overlap is unresolved. This note does not upgrade abstract access to full-text access. The existing 29 bibliography entries are not all revalidated here.

### FinanceReasoning: annotation repair already occupies much of the apparent gap

Supporting excerpt, §2.1, printed p. 15724 / PDF p. 4:

> “specifying units, percentage formats, signs, and decimal places”

The paper separates unsolvable questions, ambiguity, incorrect answers and relaxed evaluation. Its repair actions disambiguate questions, elaborate Python solutions and correct answers. Table 1 reports corrections and question changes in CodeFinQA and CodeTAT-QA; Appendix C.1 also treats financial conceptual errors and precision mismatches. These are direct precedents for the present taxonomy. [Full text](https://aclanthology.org/2025.acl-long.766.pdf).

Our useful difference is an audit of unchanged, pinned training/preference releases and fixed saved answers, not the invention of financial annotation repair. FinanceReasoning's reannotated evaluation combines changed questions/solutions and stricter scoring; our paired comparison holds the observed response fixed. That contrast concerns the reported designs, not a claim that FinanceReasoning never scores shared predictions. The local provenance review finds 37/48 question-and-ordered-paragraph matches and two already repaired quantity faults. Those document cases corroborate prior repairs; they cannot carry first-discovery or independent-benchmark claims.

### FinChain: the closest collision with a generic financial contract checker

Supporting excerpts:

> “displayed values were rounded while computations used full precision”

A.3, printed p. 14543 / PDF p. 15.

> “financial framework and its implementation are correct”

B.2, printed p. 14545 / PDF p. 17.

FinChain reviews precision, units, completeness and reasoning steps. Its rubric checks formula/framework choice, mathematical implementation and representation, including rounding. It explicitly fixes displayed-value/full-precision mismatch. This is stronger prior art than merely noticing units. The paper describes expert review; this review does not independently certify those annotators' credentials. [Full text](https://aclanthology.org/2026.acl-long.662.pdf), [official code](https://github.com/mbzuai-nlp/finchain).

The incremental evidence here is a particular released debt-for-call label pattern, its survival of tested bounds, released preference implications, and reconstructed grading consequences. A general claim to introduce the first financial semantic validator, formula-aware verifier or precision contract would collide directly. Our AI-only document references also do not establish superior annotation authority. Prefer the exact description: FinChain checks units, precision and reasoning, and repairs mismatches between rounded displayed values and full-precision computations. The current shorthand is not a contradiction, but could sound like it retains that mismatch.

### FinVerBench: mathematical consistency does not establish visible financial meaning

Supporting excerpt, §7.1 / PDF p. 26:

> “the problem is not computational error”

The paper studies financial-statement verification, controlled numerical error injection, incomplete rendered statements and rounded inputs. It distinguishes benchmark-wide generation from a smaller model-evaluated diagnostic subset. Correct subtotal arithmetic can still misclassify a legitimate statement when omitted line items make the assumed identity incomplete. Its rounding analysis and limitations directly preclude novelty claims for information sufficiency or hidden precision. [Full text](https://arxiv.org/pdf/2605.29586v1).

The present defect is in naturally released synthetic supervision rather than author-injected statement faults. Reconstructing a different financial quantity is stronger than reporting raw gold disagreement, but it is not a new general math-versus-semantics principle. Keep the rounded-input feasibility category: a compatible latent-input explanation should prevent an unconditional wrong-label finding, even when the displayed-input calculation differs.

### BizBench: executed-answer agreement and its limits are established

Supporting excerpt, limitations / PDF p. 9:

> “We assumed that the code is correct if it produced an answer”

BizBench evaluates financially grounded code generation, document extraction and financial concepts. §3.1 uses numerical answer comparison; A.1–A.2 describe transformations from FinQA/TAT-QA. Its limitations expressly acknowledge that a correct numerical answer may arise from a wrong program, and that a valid program can miss the acceptance criterion. [Full text](https://aclanthology.org/2024.acl-long.452.pdf).

Our agreement failure concerns a generator and verifier sharing a wrong financial quantity, not just accidental correct-output code. That particular provenance chain adds an empirical example, not a new theorem about answer agreement. An adapted FinQA scalar endpoint must remain separate from native program equivalence. Derivative context overlap means more document questions alone do not establish an independent new source of novelty.

### Measurement Risk: changing the scoring ruler while fixing outputs is already explicit

Supporting excerpt, §4 / PDF p. 4:

> “which determines how those labels are compressed into a model ranking”

The author v2 separates inference policy from scoring policy, including metrics and ranking aggregation. It audits class support, baseline headroom and paired uncertainty, and limits pragmatic interpretation and close-ranking claims. Its task is ordinal financial-language classification, not algebraic option valuation. [Full text](https://arxiv.org/pdf/2604.27374v2).

Our increment is tying observed grader disagreements to specific released financial target defects. A subgroup ordering reversal illustrates the effect; it is neither a new sensitivity principle nor evidence that the overall model ranking, future deployment choice or training outcome reverses. Repeated questions and source-family census counts cannot be treated as independent population trials. For transfer effects, preserve paired discordances and the explicitly selected, AI-reference-eligible subset rather than using marginal percentages as efficacy evidence.

### Program of Thoughts: executing arithmetic is a precedent, not a new method here

Supporting excerpt, §2.2 / PDF p. 4:

> “PoT relegates some computation to an external process”

PoT separates semantic program generation from interpreter computation and evaluates financial tasks including FinQA/TAT-QA. It already motivates execution as a way to reduce numerical calculation errors while leaving reasoning in the language model. [Author full text](https://arxiv.org/pdf/2211.12588v4).

Our restricted, whole-expression execution is a narrower saved-output diagnostic. It does not verify operand grounding, requested quantity, financial assumptions, currency or evidence pointers. The 32-question follow-up has 14/22 versus 13/22 reported matches and 18/22 expression matches in both arms: this supports no observed reminder benefit. Numerical compatibility with provisional AI references must not become a semantic certification claim. PoT/PAL are baseline precedents; another architecture is not needed to explain this audit.

### What the released evidence adds, and the boundary on each claim

| Evidence in this paper | Contribution it can support | Claim it cannot support |
| --- | --- | --- |
| 975/1,000 call-label conflicts; all 1,000 match financing debt and pass tested bounds | A source-specific wrong-quantity mechanism missed by these particular sanity checks | All financial bounds fail; every verifier is coupled; exact original generation revision proven |
| 946/1,000 requested-whole-unit violations; rejected-answer controls | Output projection is needed for this released instruction; wider tolerances trade denials for false credits | First rounding audit; certified reasoning traces; a sophisticated new repair method |
| Seven passing comparison families and convention-dependent cases | The audit distinguishes defects from passing/compatible cases within selected releases | Representative prevalence across financial QA or independent replication of 12,655 mechanisms |
| 800 fixed responses; 55/136 strict-format, numerically valid DeepSeek answers denied | Paired reconstructed grading consequences, decomposed by quantity and rounding | Measured training damage, provider production-grader behavior or general model ability |
| Source inspections agree numerically with released debt labels | Separately pinned public code corroborates a consistent mechanism | A recovered execution trace of the release's original generator/verifier |
| New document and unused-group follow-ups | Bounded diagnostics and openly retained uncertainty/null outcomes | Expert adjudication, repaired-source firstness, a successful semantic intervention or broad V2 performance |

“Financing debt” must include the 25 compatible zero-value cases; do not describe all 1,000 as positive debt. Original-label cent scoring is a reconstructed comparator unless an operative released reward implementation is independently established. A numerically sound final answer and a financially sound derivation are separate claims.

### Concrete refinements within the same field

1. **Explain why the bound control can miss this quantity.** Under the declared one-period, non-dividend European-call convention, write gross factor `R = 1+r`, with `S>0`, `K>0` and `0<d<R<u`. When both expiry states are in the money (`K < dS`), replication gives `delta = 1`, positive borrowing amount `D = K/R`, and call price `C = S-D`. The standard bounds are `max(0,S-K/R) <= C <= S`. Substituting the wrong candidate `D` passes those bounds whenever `S/2 <= D <= S`. There is therefore a nontrivial region `S/2 < K/R < dS/R` when `d/R > 1/2`, with `D != C`. Both quantities have currency units. This elementary explanation follows the established [Cox–Ross–Rubinstein identity](https://doi.org/10.1016/0304-405X(79)90015-1), not a new option-pricing result. It illustrates possibility; it does not classify all selected rows or establish behavior at serialization boundaries. CRR's signed bond holding is `-D`, so its notation must not be copied with the borrowing sign reversed.

2. **Keep the simplest repair control visible.** The current integer-plus-original-label-half-unit baseline matches the complete numerical contract on the selected Gordon controls. State that result prominently. The stronger call finding needs the valuation identity/quantity check; neither a wider tolerance nor currency typing establishes it. This prevents a family-specific correctness rule from being presented as a newly competitive general method.

3. **Lead the grading result with the paired mechanism.** Keep quantity denials, rounding denials, strict-format failures, native representation conventions and numerical recovery separate. Retain passing families and source-authored rejected responses as controls. Exact set counts describe a selected finite census; generalization requires a specified sampling population and independent mechanisms, not a larger denominator of repeated templates. The follow-up's null intervention and failed evidence-pointer parsing are limitations of that extension, not counterexamples to the algebraic source audit.

4. **Make document follow-ups a qualified corroboration layer.** Cite FinanceReasoning beside its known repairs and retain derivative-overlap limits. Keep independent visible-answer sets, textual/executable source channels and faithful native metrics distinct. Qualified external adjudication would strengthen ambiguous financial interpretations; the existing AI-only review cannot supply that authority. A future held-out intervention needs identical executable-calculation fields and separately declared assumptions, avoiding the earlier prompt conflict. No new answers or review are commissioned by this note.

Suggested contribution wording: *A pinned audit of selected released financial supervision identifies a wrong-quantity label pattern that survives tested call-price bounds, instruction-rounding failures with passing controls, and paired reconstructed grading disagreements on saved answers.* Avoid firstness, universal verification claims, successful learning mitigation, an expert-validated document benchmark, and acceptance/main-track guarantees.

### Evidence and cache record

Canonical paper inspected: `paper/answer_contract_audit.tex`, 29 bibliography keys. Its byte hash is recorded below; this is a reporting snapshot, not a new scientific freeze. Local corroboration records include `docs/FINANCE_DOCUMENT_DERIVATIVE_OVERLAP_REVIEW_2026-09-30.md`, `docs/MAIN_TRACK_DOCUMENT_EXTENSION_REVIEW_2026-09-30.md` and the existing independent novelty review. No new target contents were needed.

| Existing PDF cache | SHA-256 |
| --- | --- |
| `literature/pdfs/financereasoning-acl2025.pdf` | `7edcadd778a4619b863247fe66a91b7d820115af367cf47bf6d05f72f353e60a` |
| `literature/pdfs/finchain-acl2026.pdf` | `20a4d354b7e76b6ca7ce5de7ee29b60f831eae9b1d1ab6fcac3aadb77f7f11c9` |
| `literature/pdfs/finverbench-2605.29586v1.pdf` | `32dff1ee0a4177957b6225395eeca58c15b7ffd1114bbc7fc1066c3488aa9bd4` |
| `literature/pdfs/extended-20260930-pot-author-v4.pdf` | `34aaf52e7e0ca5acd46e811fff318a9c99310c1921d2b759640361aa2d6165f1` |
| `literature/pdfs/citation-workspace/bizbench.pdf` | `09ecdd16751f8feebed9d76aa236d6e0d9f12d6913665f759bee2b566fc4f70d` |
| `literature/pdfs/citation-workspace/measurementrisk.pdf` | `cad1123721816cd67d026242448a5f8593fd07f91192d4e1f61c912f5876c75b` |

The first four caches were rechecked against fresh primary PDF bytes in memory during this review. The last two were acquired separately by the root CiteProof work; their local hashes and acquisition URLs were checked here. Root owns that sidecar. This note does not claim official publisher-final identity for an author preprint. Quotes total 8 / 16 / 6 / 12 / 11 / 8 words respectively; each work remains below 25 quoted words. All seven excerpts were checked against local PDF/text content; line wrapping and line-end hyphenation are normalized without changing wording.

Reporting snapshot: primary sources checked from `2026-09-30T13:57:33Z`, with final local paper check after 14:00 UTC. Canonical paper SHA-256: `c938578de9ea9a227dcd54aef1ab132d3657dc1e24b509b0a512f27cd200421a`. There is no actual organizer, professor or expert review in this note.
