## Executive summary (read this first)

The frozen analyzer correctly produced four V2 scored ledgers but saved their
summary in the V1 directory. Preserve that file, the frozen code and every
response. A reporting-only helper copies identical summary bytes into V2 and
records the correction. No generation, parser, numerical decision or aggregate
changes. V1 still has no selected-question response ledger or collection receipt.

## Cause and preserved evidence

The amended controller reassigns `analysis.OUT` before calling the original
analyzer. The analyzer's imported `write()` retains the original generator
module's V1 `OUT`, so its summary uses that directory. Its direct scored-file
writes use the reassigned V2 directory. This Python function-global routing bug
was missed during precollection review and found during independent postflight.
An analyzer exit code of zero therefore did not establish correct output placement.

`outputs/model-grading-lmstudio-v1/results.json` is the misplaced **V2** summary:
its embedded collection-freeze hash is
`2949178d43af5b3ffef701073f7df92d8fce1c0d33133c783b2d4e805e52d96a`.
It does not convert the failed V1 readiness gate into a completed study.

## Correction and verification boundary

`scripts/restore_lmstudio_v2_summary.py` verifies the V2 freeze identity and
completed 200-question accounting before an exclusive byte-copy. The original
and `outputs/model-grading-lmstudio-v2/results.json` both have SHA256
`ec1ab58b11a39a1aac7cd9b1e73eb08ceaf75e82b5fef00272b21bfcf4795015`.
The new `summary_path_correction.json` records both paths, hashes and helper hash.
Nothing is overwritten. The correction is after collection and analysis, and is
not represented as part of the original precollection freeze.

Independent score replay must still validate the four saved streams and family
aggregates. Identical copied bytes establish reporting identity, not numerical
correctness, semantic truth or causal model effects. A fresh execution of the
frozen controller still has the documented routing defect; the reporting helper
is required after analysis in a fresh output tree. Existing populated outputs
are intentionally protected against overwrite.
