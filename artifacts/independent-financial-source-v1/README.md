## Executive summary (read this first)

This complete 300-instance bank is newly generated from three pinned FinChain
functions. It is a current-code comparison, not FinChain's historical published
corpus, original model scores, expert reference set or complete reasoning audit.
The source's intermediate-rounding convention admits all 300 native final values;
the exact visible-input endpoint admits 82/100 calls and 100/100 each WACC and
compound-interest values. Preserve both endpoints rather than declaring 18 errors.

The [manifest](manifest.json) binds the [prospective freeze](freeze.json), all
[attempts](attempts.jsonl), [analysis](analysis.json) and collection receipt. Native
questions and solutions are retained verbatim alongside derived scalar and oracle
fields. The [FinChain source fragments](../finchain-source-v1/README.md) preserve
the author's current Apache-2.0 license and notices. Generated records come from
those declared executable templates, not a redistributable historical dataset
download. Adapter/reference fields are explicitly our derived research metadata.

```bash
PYTHONPATH=src python scripts/replay_independent_finance.py
```

The standard-library replay reassembles hash-checked original code, regenerates
every seed, checks exact original question/solution bytes and recalculates all
scalars and summaries. The collection runtime is Python 3.13.2; cross-version
regeneration is tested on Python 3.11–3.13. Numeric compatibility uses half-cent or
half-hundredth percentage-point distance; intermediate-rounding alternatives are
separate. No foreign imports, upstream main program, model or paid call executes.

See the [protocol](../../docs/INDEPENDENT_FINCHAIN_CODE_PROTOCOL_V1.md),
[result interpretation](../../docs/INDEPENDENT_FINCHAIN_CODE_RESULTS_V1.md) and
[source readiness](../../docs/INDEPENDENT_FINANCIAL_SOURCE_READINESS_2026-09-30.md).
Hashes and regeneration establish source identity and deterministic numerical
replay; they do not supply human financial adjudication or historical replication.
