## Executive summary (read this first)

This is the final iteration's portable scalar replay artifact. It preserves 2,548
authored controls, the complete 500-reference eligibility ledger and 96 recorded
attempt projections. It establishes identity and fixed scalar scoring; it does
not certify full mathematical/financial meaning or reproduce upstream model scores.

From the research repository, with Python 3.11 or later:

```bash
PYTHONPATH=src python scripts/replay_grader_comparison.py
```

Expected: PASS, 2,548 control comparisons and 96 projected attempts. The pinned
native comparator's MIT notice and exact source fragments are in the sibling
`recursivemas-scoring-source-v1` directory. Source fragments reconstruct an
upstream file by its checksum; this is a restricted pure-definition replay, not
the complete RecursiveMAS inference CLI.

The MATH500 source manifest gives pinned acquisition URLs and hashes. Original
questions/solutions and generated explanatory prose are omitted. Full-response
extraction replay needs local original replies; fresh inference additionally
requires separately acquired data and checkpoint bytes. The original scientific
freeze is retained for identity, including paths absent from this projection.

The declared scalar grammar covers signed integers, finite decimals and simple
fractions. There are 368 admitted references and 132 abstentions. Controls contain
174 distinct reference values and 695 distinct numeric pairs. Repeated references
and three stochastic local repetitions are dependent; do not treat each row as
an independent experiment. Current native comparator behavior does not establish
which evaluator produced historical RecursiveMAS paper results.

`manifest.json` binds the projected data files. This README is explanatory prose
outside that immutable data manifest. The historical census used a salted order
digest under a misleading raw-hash field name; the projection names it explicitly.
The Qwen readiness amendment preceded every Qwen cohort call, after Gemma's arm
completed. Strict scientific extraction and scoring remained frozen.
