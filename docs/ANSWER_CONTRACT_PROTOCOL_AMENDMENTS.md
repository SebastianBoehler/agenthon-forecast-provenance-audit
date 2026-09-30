## Executive summary (read this first)

The frozen V1 protocol remains unchanged. These post-result refinements improve
interpretation and controls. They are exploratory amendments, not independent
confirmation. Prior results and code are preserved in ignored
`outputs/answer-contract-v1/snapshots/before-beta-only-amendment/`.

1. **CAPM interval, source-informed.** Independent source inspection found that
   the generator renders already-exact rates but rounds beta from three to two
   decimals. Narrow the ambiguity interval to beta ±0.005 with rates fixed.
   All 1,000 golds remain feasible after accounting for cent-output serialization.
   The original broad rate/beta interval was sufficient but unnecessarily loose.
2. **Nearest-integer ties.** The question does not specify a half-tie convention.
   Accept either adjacent integer for exact half ties. A materialized repaired
   dataset may declare half-up explicitly. There are 19 such source cases; their
   cent-level .50 answers violate either integer convention, so the 946 count
   does not depend on choosing one convention.
3. **Integer-formatted error controls.** Raw source rejected answers usually
   contain decimals; rejecting them could reflect format alone. Project all 337
   source Gordon rejected answers to whole integers before another comparator
   test. Thirty-four projected answers become numerically correct despite the
   erroneous D0 derivation. Analyze the remaining 303 as wrong final values.
   The 34 collisions demonstrate the limit of final-answer verification.
4. **Ablation correction.** Formula-only evaluation uses the source's cent-level
   serialization allowance, rather than inheriting the requested whole-unit
   interval. This prevents a broad ±0.5 allowance from masquerading as an output
   projection ablation. The full contract explicitly checks the integer target.
5. **Runtime repairs.** Install the editable package to make new modules visible.
   Isolate pytest from an unrelated globally installed pytest-cases plugin that
   crashes with the current pytest. This changes no scientific calculation.
6. **Materialized patch validation.** After review, compare all 5,935 independently
   derived rational values with the actual exported numerical patch records.
   This checks serialization and patch construction beyond comparing formula modules.

The numerical correction file is explicitly a patch artifact. It neither repairs
nor certifies the original reasoning traces or multiple-choice option letters.
It is not a drop-in certified DPO training dataset.
