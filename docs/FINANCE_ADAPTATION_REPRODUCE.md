## Executive summary (read this first)

The adaptation pilot uses official GEPA 0.1.1 and a separate prospective freeze.
Replay saved-answer grading without paid inference. Never run the API collection
command merely to reproduce the reported measurements. This is prompt adaptation,
not a trained financial model; the original 800-answer study is preserved.

The V1 collector stopped before holdouts because concurrent GEPA default loggers
interfered with process streams. Its files stay intact. The
[execution amendment](FINANCE_ADAPTATION_EXECUTION_AMENDMENT.md) defines the separate
V2 repeat with unchanged scientific rules and the remaining original budget/time.

## Files and runtime

Question partitions, source provenance, authored transfer targets and immutable
rules are in outputs/finance-adaptation-v1 and
[the protocol](FINANCE_ADAPTATION_PROTOCOL_V1.md). The preparation manifest is
historical and may contain hashes from before implementation review corrections;
freeze.json is the authoritative pre-inference record. Its 34 hashed files and
the 81 GEPA package-source hashes must agree before collection.

Use the base audit/review requirements, plus
experiments/finance_adaptation_requirements.txt. GEPA is pinned to 0.1.1.
The actor uses the catalogued DeepSeek V3.2 SiliconFlow FP8 route, with API fallback
disabled. An API identifier does not prove immutable weights. No weights or
credentials are included in the package.

## Replay without model calls

After staging the pinned public sources as in the audit guide:

```bash
PYTHONPATH=src python scripts/report_finance_adaptation.py
PYTHONPATH=src python scripts/finance_adaptation/validate_outputs.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=src python -m pytest tests/test_finance_adaptation.py -q
```

The report requires the complete six-strategy, 72-question holdout panel; partial
execution must not produce a completed result. Independent validation uses saved
exact Fraction oracles and a separate parser. Retain the timestamped preflight
review artifacts rather than overwriting them during reproduction.

Those V1 commands correctly refuse its incomplete panel. For completed V2 outputs,
use `scripts/report_finance_adaptation_v2.py` and
`scripts/finance_adaptation/validate_reexecution.py` as in the execution amendment.
Do not combine the two attempts' responses or overwrite the failed V1 files.

The completed V2 postflight exposed a frozen-checker bookkeeping assumption:
six legitimate repeated training-minibatch tags were collapsed. The original
checker still fails its uniqueness assertion. Use the disclosed occurrence
supplement for complete saved-output validation:

```bash
PYTHONPATH=src python scripts/report_finance_adaptation_v2.py
python scripts/validate_finance_adaptation_occurrences.py
```

It matches every saved occurrence to one raw API call, retaining all duplicates,
costs and failed attempts. Numerical/parser/selection rules remain unchanged.
See [independent results](FINANCE_ADAPTATION_INDEPENDENT_RESULTS.md). The completed
432-response panel retains the seed in every optimizer arm and passes neither
gate. Primary outputs are under `outputs/finance-adaptation-v2`; the frozen
report's historical V1 path wording is clarified by the execution note/review.

## Fresh inference

The original outputs directory contains a freeze and call ledger. The collector
refuses to overwrite them. A new collection is a separate experiment with a new
named output path, prospective protocol/review and freeze; changing the current
path or parser is not a replication of this frozen run.

The original collector was scripts/run_finance_adaptation.py. It requires
OPENROUTER_API_KEY in the process environment. It applies the strict extractor,
a 16-item format gate, two seeds for each of two objectives, the fixed manual/seed
baselines and all failed-attempt denominators. Global request concurrency is four,
the shared spending ceiling is $0.90, and new requests stop at three hours.

GEPA sees only its assigned feedback. Saved local records can contain both scores,
but unassigned financial or target information cannot enter source-arm reflection.
Selected strategies are saved before either held-out set is answered. Compare
trajectories only on the common 32-question development set, not changing minibatches.

## Claim and artifact boundaries

The 24 transfer questions are researcher-authored and independently calculated.
Their source-label reward is undefined. They cover four contracts over three
underlying calculations and nine base wording structures. Neither expert human
annotation nor a general financial benchmark is claimed.

The objective intervention changes target values and, for whole-unit Gordon, an
integer constraint/feedback flag. Passing-family target centering remains identical.
Equal call ceilings are not equal realized compute; retain actual calls, tokens,
elapsed time and costs by arm. A valid final number does not certify its derivation.
