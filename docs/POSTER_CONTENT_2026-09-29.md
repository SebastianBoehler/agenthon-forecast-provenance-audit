## Executive summary (read this first)

The poster's single question is whether financial labels marked verified answer
the question the model actually sees. Lead with the wrong financial quantity,
then show that the same saved answers receive different grades. The content
below is a candidate story for the current manuscript, not a rendered poster or
an accepted presentation. The separate adaptation pilot completed with all seed
prompts retained; it supplies an inconclusive feasibility result.

## Title and opening claim

**When Verified Financial Labels Fail**

“A generator and its verifier can agree while answering the wrong question.”

One concrete example: a released one-period call-price question has independent
value 12.72, while the label is 45.28, the financing debt. The inspected verifier
regenerates the same template. Dataset and code revisions are separately pinned;
the code pin is not proven to be the original dataset-generation revision. This
is a code-consistent diagnosis, not an execution trace of the production process.

## Three evidence panels

1. **What is wrong?** In the selected Cosimo families, 975/1,000 binomial labels
   fail call valuation under both checked compounding conventions. All 1,000
   binomial labels match financing debt and pass the tested call-price bounds.
   Another 946/1,000 constructed Gordon labels omit requested
   integer rounding. Seven comparison families pass. Hidden precision in DCF
   and CAPM has a different interpretation: labels remain feasible if inputs
   were rounded, but the exact answer is unidentified.
2. **Why does it matter for NLP evaluation?** Models must identify the requested
   quantity, units and rounding instruction. In the strict endpoint, source-cent
   grading denies 55/136 numerically valid DeepSeek answers: 48 quantity and seven
   rounding denials, with zero from the two passing model-panel families. Admitting
   either checked compounding convention yields 56/137 in a disclosed post hoc
   sensitivity. On the supplementary
   constructed-Gordon endpoint, the same unchanged responses rank Qwen1.7B
   above DeepSeek under source-cent grading, 10/50 versus 2/50, and below it under
   integer validity, 22/50 versus 50/50. Mark this ordering example exploratory.
3. **What correction is sufficient?** Integer plus source-half-unit tolerance
   fixes the tested Gordon rounding family; call valuation needs the correct
   financial identity. A 5% tolerance succeeds on the tested DCF controls but
   accepts many errors elsewhere. Do not present widening tolerance as a universal
   failure or the repair as a new general algorithm.

## What the presenter should be ready to defend

- Family selection was exploratory and mechanism-driven; these are finite counts
  from two synthetic releases, not financial-AI prevalence estimates.
- The 800 answers cover four checkpoints and two model families. Format failures
  prevent a clean capacity ranking; the strict endpoint and post hoc extraction
  stay separate. Numerical agreement does not certify reasoning traces.
- Independent arithmetic checks and technical review are complete. The blank
  human-review packet is prepared, but no finance-expert adjudication is complete.
- The current paper measures label validity and grading. The separate 432-response
  adaptation pilot met neither consequence nor repair gate. It measures no weight
  training, market forecasting or monetary loss.
- Precision and visible-information validation are established prior work. The
  contribution is the release-specific numerical audit, diagnosis in separately
  pinned code, and paired grading consequences. Artifact history is supporting
  reproducibility evidence; it does not establish a new verification principle.

## Evidence and presentation constraints

Use the existing standalone manuscript's example, source census and grading
table. Keep every denominator and convention legible. If a final visual poster
is requested, use a readable three-panel layout, accessible colors, and a link
to the reproducibility artifact. Do not promise acceptance from title length.

The [official Agenthon call](https://www.agenthon.net/#call-for-papers) gives a
September 30, 23:59 AoE deadline: October 1, 2026 at 13:59 CEST. Accepted work
requires an author in Atlanta on December 12. Presenter eligibility remains a
submission prerequisite. Relevant scope and scientific care cannot guarantee selection.
