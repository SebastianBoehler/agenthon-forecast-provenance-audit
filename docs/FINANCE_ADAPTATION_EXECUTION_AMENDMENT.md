## Executive summary (read this first)

The first frozen GEPA collection stopped with a process-stream logging error before
any held-out answers. Preserve that incomplete attempt. Repeat all four searches
under a separate execution freeze using isolated logs; do not change the questions,
objectives, methods, budgets per arm or success gates to obtain an appealing result.
The complete repeat remains a finite exploratory feasibility study.

## What failed and what is retained

GEPA 0.1.1's default Logger context redirects process-global stdout and stderr.
Its exit closes the arm's files. Four overlapping optimizer threads can leave a
remaining optimizer writing through a Tee into a closed handle. The collector
exited 120 with `ValueError: I/O operation on closed file.`

The original 152 questions, 34-file scientific freeze, 81-package-source hashes,
459-call ledger, evaluations and available result files stay unchanged under
outputs/finance-adaptation-v1. The attempted calls cost $0.089236560; 63 were
reflection calls. Repaired 0/1 result files retained the seed strategy, while
source 0/1 result files are absent. No holdout answers exist. This is an incomplete
execution, not a measured adaptation effect or successful null hypothesis test.

The interruption record is execution_failure.json. The new freeze additionally
hashes that record, the ledger and available evaluation/result files. It preserves
all initial failures rather than selecting successful arms for continuation.

## Operational changes in the repeat

Use outputs/finance-adaptation-v2 with a prospective execution freeze. Restart
all four searches; no best strategy or response from the incomplete attempt is
used to initialize them. The original scientific adapter, reward functions,
final-line parser, targets, questions, seeds, manual strategy, candidate length
limit, reflection and actor limits, selection rule and API settings stay unchanged.

The V2 runner supplies GEPA's official LoggerProtocol with an arm-local file
logger. It never redirects or closes process streams. The inherited API client
also records egress-slot entry/exit intervals through a bounded semaphore of 4.
These intervals bound actual request concurrency; they are not HTTP wire times.
The logger concurrency regression must pass before the new freeze.

V2 reserves only the remaining $0.810763440 of the original shared $0.90 ceiling.
Per-attempt indices start at 1; report the two costs separately and cumulatively.
The absolute request cutoff remains three hours from the original start,
2026-09-29T20:33:58.526883+00:00, so the request cutoff is
2026-09-29T23:33:58.526883+00:00. Time lost to failure/review is included. New calls
must not reset that cutoff, and transport responses can finish after it.

The original frozen report's metrics and gates are reused with only its output
directory rebound. The independent postflight parser/calculator is likewise reused
without changing its financial interpretation. The V2 wrapper additionally verifies
the interrupted-attempt evidence, unchanged questions/rules, cumulative accounting,
prospective execution hashes and egress intervals.

## Interpretation and reproduction

The repeat freeze occurs after partial development outputs were observed. It is
an operationally repaired feasibility rerun, not an independent confirmatory study.
Original optimizer outcomes and candidate failures remain reported. Neither a
null rerun nor an optimizer's failure to find an improving strategy establishes
that flawed supervision cannot cause harm. No model weights change.

When complete, replay without model calls:

```bash
PYTHONPATH=src python scripts/report_finance_adaptation_v2.py
PYTHONPATH=src python scripts/finance_adaptation/validate_reexecution.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=src:scripts python -m pytest tests/test_finance_adaptation_logging.py -q
```

No first-attempt primary files or freezes should be overwritten during replay.
The failed default logger's source and fix are inspected in the installed official
GEPA package; no upstream package patch, provider fallback or silent retry is used.
