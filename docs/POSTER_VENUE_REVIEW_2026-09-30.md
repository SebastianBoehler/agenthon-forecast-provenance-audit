## Executive summary (read this first)

**Hypothetical verdict: recommend poster acceptance as a bounded empirical audit,
conditional on final claim/evidence consistency and presentation eligibility.**
This is our professional assessment, not feedback from an organizer, an acceptance
prediction, or a guarantee. The strongest case is concrete financial supervision
defects plus their consequences for grading unchanged answers. The strongest
objection is that selected synthetic templates support a useful case study, not a
general new verification method or demonstrated learning harm.

Reviewed 2026-09-30, Europe/Berlin; primary-source verification completed at
2026-09-30T00:06 UTC. Inspected manuscript: `paper/answer_contract_audit.tex`,
SHA256 `9116a4a630a34fc3a9816f9f2bab588b19025809ab47ca0e3f1d6f5b1d5d73f8`.
This unfrozen review concerns that draft; later edits need a final consistency check.

### Verified venue requirements

The [official CFP](https://www.agenthon.net/#call-for-papers) accepts one PDF of
any format or length, including short papers. It is non-archival and welcomes
work published or under review elsewhere. Competition participation is optional.
Accepted papers become posters; an author must present in person in Atlanta on
December 12, 2026. The form uses Google sign-in and requests the presenting author's
NeurIPS-account email. Deadline: September 30, 23:59 AoE; decisions: October 2,
23:59 AoE. The reviewed public CFP gives no detailed scoring rubric or acceptance
rate. Its evaluation/verification/benchmark topic directly covers this paper.

AoE means UTC−12. The stated deadline converts to **October 1, 2026, 11:59 UTC /
13:59 Europe/Berlin (CEST)**. Conversion was checked with Python `zoneinfo`;
the site specifies minute precision. Eligibility and topic fit do not establish
acceptance. No account or submission action was performed.

### Verified scholarly lens, without impersonation

Pawel Polak is listed as a lead organizer by the
[official committee](https://www.agenthon.net/#call-for-papers). His
[Stony Brook faculty profile](https://www.stonybrook.edu/ams/faculty/faculty-profiles/pawel-polak.html)
identifies him as Assistant Professor of Applied Mathematics and Statistics,
with a 2014 Ph.D. in computational statistics from the Swiss Finance Institute.
His [university biography](https://ai.stonybrook.edu/node/262794) also identifies
the University of Zurich and research in statistical learning and quantitative
finance. His [own current page](https://sites.google.com/view/pawelpolak/home)
describes recent agentic-modeling and reinforcement-learning work.

Two verified research examples ground a financial ML lens:

| Primary research record inspected | Methodological connection we infer |
|---|---|
| Miao and Polak, [Online Ensemble Learning for Sector Rotation: A Gradient-Free Framework](https://arxiv.org/abs/2304.09947v2), v2 November 12, 2025. Abstract specifies rolling prediction, out-of-sample R-squared and comparisons against constituent models and ensemble baselines. | Distinguish the reported metric from the property being claimed; use matched comparisons and respect the scope of held-out evidence. |
| Xu, Bohne, Polak, Byrd, Rosenberg and Kazantsev, [Learning to Trade with Preferences: Interpretable Execution via Mixture-of-Experts](https://researchconnect.stonybrook.edu/en/publications/learning-to-trade-with-preferences-interpretable-execution-via-mi/), ICAIF 2025, pp. 762–770, DOI [10.1145/3768292.3770390](https://doi.org/10.1145/3768292.3770390). University abstract describes preference optimization of simulated execution trajectories and financial-cost evaluation. | Financial meaning, supervisory signals and evaluation outcomes must be distinguished. A supervision audit is relevant even before a training-consequence study succeeds. |

These are methodological inferences from research topics, not inferred personal
preferences or opinions about our paper. Access here was faculty/author pages,
research metadata and abstracts; no full-text methodological review of those two
papers is claimed. Rosenberg and Kazantsev's coauthorship is verified by the second
record, but we do not reconstruct their individual views or qualifications.

### Assessment of the inspected paper

The financial example is persuasive: the released call target can be the financing
debt rather than the option value. Replication and risk-neutral identities make
the distinction independently inspectable. Whole-unit rounding is another direct
contract defect. Hidden precision is conditional on the input convention and
should retain that qualification.

The 12,655-row audit is a census of selected families from two synthetic releases.
Passing families, explicit source revisions, independent rational calculations
and numerical patches make it more useful than a collection of anecdotes. The
800-answer experiment adds practical evidence: under reconstructed original-label
cent grading, 55 of 136 strictly formatted and numerically valid DeepSeek answers
lose credit. These are paired grading decisions on fixed responses, not measured
upstream reward execution or a causal model-training effect.

The strongest objection remains novelty and external validity. Label errors,
answer determinacy, financial precision checks and evaluator integrity already
have close prior art. Repeated templates and mechanism-driven selection prevent
field-wide prevalence inference. The contribution should remain the pinned
release-specific evidence, source diagnosis and replayable grading disagreement.
The inspected draft already states this boundary; preserve it through editing.

Three points deserve explicit defense at the poster:

1. **Independence:** the separate rational implementation is AI-assisted technical
   validation, with the primary code already seen; it is not blind expert review.
   Regeneration in inspected source is not proof of the upstream verification run.
2. **Model endpoints:** strict formatting heavily constrains comparisons; recovered
   numeric answers are a separately reported post hoc endpoint. The panel cannot
   rank latent financial ability or isolate parameter-count effects.
3. **Attempted adaptation:** all four GEPA searches retain the seed prompt. The 432
   held-out answers do not demonstrate adaptation harm or repair benefit. Preserve
   the logging failure and inconclusive repeat as bounded feasibility evidence;
   their honest retention strengthens provenance, not methodological novelty.

The 13-claim artifact improves inspectability and supports saved-output replay.
Hash/DAG checks do not establish financial truth, complete historical coverage,
fresh reproducibility or official ARA compliance. The 96 document packets remain
preparation only; they add no reviewed defect findings or independent-source result.

### Concrete readiness checks before submission

| Check | Current review finding / action |
|---|---|
| Scientific presentation | Lead with the released target/financial quantity mismatch and fixed-answer grading evidence. Keep prior-art boundaries and finite selected-family scope visible. |
| Final PDF | Check author/affiliation metadata, compilation, legibility and consistency of abstract, figures, tables, captions and retained negative results. This review does not certify the final PDF. |
| Reproducible evidence | Identify which claims replay offline and which need external data, weights or provider access. Verify final package receipts after edits; do not imply an already public artifact URL. |
| Source safety | Use only admitted public study evidence; retain attribution and notices. No sealed competition outcomes or restricted document corpora should enter the submission artifact. |
| Presenter | Confirm an author can attend Atlanta and supply the correct NeurIPS-account email; this review has no evidence that those conditions are met. |
| Deadline | Submit before the converted deadline with time for upload errors. No submission receipt or acceptance is currently evidenced by this review. |

No polishing strategy can supply certainty about an unpublished review decision.
The justified recommendation is to submit this carefully bounded audit for poster
consideration; pursue main-track breadth and learning consequences as separate,
prospectively gated research.
