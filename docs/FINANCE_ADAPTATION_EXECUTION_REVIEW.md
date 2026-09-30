## Executive summary (read this first)

The proposed V2 operational repeat is ready to freeze. The original failure is
reproducible without model calls. The replacement logger avoids the confirmed
process-stream interference. Inspection and an abstract-syntax comparison find
unchanged GEPA optimization arguments apart from the logger. All four arms
restart from the original seed strategy. No surviving V1 strategy is carried
forward. No V2 responses have been inspected for this review.

The first attempt is incomplete: 459 API calls cost $0.089236560; 63 were
reflection calls; no holdout answers were collected. The repeat has at most
$0.810763440 remaining under the original cumulative $0.90 cap. Its absolute
request cutoff remains **2026-09-29T23:33:58.526883+00:00**. The repeat is an
exploratory feasibility execution after observed partial development results.
It is not an independent confirmatory replication or evidence of an adaptation
effect. This is AI-assisted technical validation, not human annotation or
expert financial adjudication.

### Confirmed failure and preserved evidence

The pinned GEPA0.1.1 [Logger implementation](../.venv/lib/python3.13/site-packages/gepa/logging/logger.py)
replaces global `sys.stdout` and `sys.stderr` when entering a context
(lines52–57), restores captured streams and closes its own files on exit
(lines60–65), and forwards writes through a `Tee` to retained streams
(lines17–23). Interleaved contexts can therefore restore a stream that refers
to another context's closed file. The pinned [GEPA API](../.venv/lib/python3.13/site-packages/gepa/api.py)
constructs this logger by default when a run directory is supplied (lines274–279)
and enters its context around the engine (lines411–416).

An isolated, deterministic interleaving reproduced `ValueError: I/O operation
on closed file.` without threads, network, or model calls. This establishes the
failure mechanism. The recorded exit120 and crash time are operator evidence
in [execution_failure.json](../outputs/finance-adaptation-v1/execution_failure.json).
They are not independently reconstructed from an operating-system exit log.

The original 34 frozen files and all 81 installed GEPA source hashes still
match their pins. Independent rescoring agrees for all503 saved optimizer
evaluations: 377 completed responses and126 overlong-candidate placeholders.
All63 reflection prompts match assigned-objective-only feedback reconstructed
from their saved training evaluations. All16 off-split preflight responses also
agree with the separate parser and Fraction references.

The396 nonreflection calls comprise16 preflight calls,377 optimizer responses
with saved evaluation rows, and **three completed actor calls without saved
evaluation rows** at interruption. These raw calls remain in the immutable API
ledger and their costs remain charged. Repaired0/1 have result files;
source0/1 do not. There are no V1 holdout responses. Partial development
outcomes cannot establish either the consequence gate or its absence.

### Review of the operational amendment

[run_finance_adaptation_v2.py](../scripts/run_finance_adaptation_v2.py) supplies a
structural `LoggerProtocol` implementation with one private file per arm. It
does not inherit concrete GEPA `Logger`, alter global streams, or patch the
installed package. GEPA therefore takes its existing noncontext logger branch.
A four-thread regression passed and confirms that logging preserves both
global stream identities and all four private output files.

The independently compared optimization keyword syntax is identical after
removing `logger=logger`. The same scientific adapter, candidate seed,
source/repaired objectives,32-row common development set, first-best tie rule,
256 metric-call cap,16-reflection cap, seeds0/1, and fixed actor/reflection
settings remain in force. All four jobs use fresh V2 directories and restart
from `SEED`. The V2 runner reuses the untouched V1 answer-panel function.
It saves all six selected strategies before loading or collecting holdouts.

[ObservedBudgetClient](../src/finance_adaptation/observed_client.py) inherits the
untouched API client. Its gate retains a bounded semaphore of4 and records
per-thread slot entry/exit. Request payloads, fixed provider, no-fallback
setting, conservative reservations, transport-error handling and billing
accounting are inherited. These intervals contain the actual HTTP operation;
they bound request overlap and do not measure precise wire start/end times.

The client monotonic start is rebased to the original freeze timestamp, so
time lost to the failure and review consumes the original three-hour window.
The inherited time check occurs both before reservation and after acquiring
an egress slot. Calls may finish after the cutoff if sent before it. The V2
manifest must record the exact cutoff above, original start
`2026-09-29T20:33:58.526883+00:00`, prior cost, remaining cap and cumulative cap.
The helper freezes the failure, raw V1 ledger, four partial evaluation ledgers,
two result files, unchanged original files, V2 byte copies and new drivers.

The repeat reporter reuses the frozen scientific reporter. Its report filename
retains scientific protocol version V1 while the appended execution note
identifies the V2 attempt. No completed first-attempt scientific report exists
to overwrite. The separate output directories remain the authoritative
distinction between attempts.

### Independent postflight acceptance checks

[validate_reexecution.py](../scripts/finance_adaptation/validate_reexecution.py)
first verifies preservation of V1, the disclosed interruption, all81 dependency
hashes, exact prior accounting, and unchanged optimization keywords. It then
checks V2 manifest hashes and all ten byte copies, the exact absolute cutoff,
same scientific caps/seeds/settings, attempt-local and cumulative billing,
and the observed egress-slot peak. It imports only independent validation
helpers, not the primary oracle, rewards, parser or runner.

Only the input directory and freeze verifier are rebound when it invokes the
unchanged V1 independent postflight validator. The preserved parser and exact
Fraction references independently recompute every saved response's financial,
source and repaired decisions. Passing-family rewards must be identical and
whole-Gordon repaired answers must be exact integers. Completion requires all
432 holdouts (six strategies times72 cases), all four optimizer results,
assigned-only reflection feedback, the common32 development cases, first-best
selection, fixed request wrappers/model route, and agreement with primary
aggregates and declared gates. V1 is never rewritten.

The full V2 validator cannot run before a prospective freeze and completed
responses. A PASS here means operational freeze readiness; postflight PASS
will be written separately to V2 `independent/response_validation.json`.

### Commands and identity evidence

Commands run from the research repository, with no API requests:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=src:scripts .venv/bin/python -m pytest tests/test_finance_adaptation_logging.py -q
PYTHONPATH=scripts/finance_adaptation .venv/bin/python - <<'PY'
import json
from validate_reexecution import verify_original
_, evidence = verify_original()
print(json.dumps(evidence, indent=2))
PY
```

The regression passed (1test). Original verification passed for34 frozen
files,81 source hashes,459 calls,503 evaluations and63 reflection prompts.
Exact no-model reproduction command:

```bash
.venv/bin/python - <<'PY'
import io, json, sys, tempfile
from pathlib import Path
from gepa.logging.logger import Logger
saved = sys.stdout, sys.stderr
caught = None
with tempfile.TemporaryDirectory() as tmp:
    try:
        sys.stdout = sys.stderr = io.StringIO()
        a = Logger(str(Path(tmp) / 'a.log'))
        b = Logger(str(Path(tmp) / 'b.log'))
        a.__enter__(); b.__enter__()
        a.__exit__(None, None, None); b.__exit__(None, None, None)
        try: sys.stdout.write('after parallel logger contexts')
        except ValueError as exc: caught = str(exc)
    finally: sys.stdout, sys.stderr = saved
assert caught == 'I/O operation on closed file.'
print(json.dumps({'status': 'reproduced', 'exception': caught, 'model_calls': 0}))
PY
```

Full saved-output validation after collection and primary scoring:

```bash
PYTHONPATH=scripts/finance_adaptation .venv/bin/python scripts/finance_adaptation/validate_reexecution.py
```

SHA256 identities at review:

| Artifact | SHA256 |
| --- | --- |
| V1 freeze | `2b4728f21b4890b6bdf9ebb33dd89c9b83c105d6de021beb3435343e4bdddd24` |
| V1 API ledger | `ca6d73475cb12c326090dff5488801651a65b3c9fcc8bbb8e0b55c8b2ffec2e1` |
| V1 failure record | `23b050498101328e0c195f28666d7fa0e378227d7336f4ccdc4d6f55d47cad3c` |
| Unchanged independent parser/support | `9c49923e61d1738dd8b27db7f736e42c837aba145e9ef4c50c36bb5c02fb4f69` |
| Unchanged independent V1 postflight validator | `879696c44775abc18d673068e87cd202649ff58e3244b0a174a143c08f2e3f55` |
| New V2 independent wrapper | `d3d92719167c53b0ff006bcd9d6cd585b3270844c643e02900118296b053e263` |
| New V2 runner | `a57d5457a00ab4d3511283acad07530be6835b6921168e6caf8e8dc26d6577bb` |
| New observed client | `0f773cb3d172b073350c77776f4bc4acf7f83a80298b70f6a5d5dc5f0d7cfec3` |
| Logger regression | `1acf8fb59f319dec9bb13541db6c39e2d187c788b27fc96b656091ebcb3692ae` |

The prospective V2 manifest will pin this review and all execution drivers.
Partial-ledger hashes are emitted by `verify_original()` and will also be
pinned in that manifest. No first-attempt ledger or preflight report was
regenerated for this review.
