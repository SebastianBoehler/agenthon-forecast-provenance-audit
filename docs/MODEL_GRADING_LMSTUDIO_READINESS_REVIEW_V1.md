## Executive summary (read this first)

**Implementation review finds concrete prefreeze gaps; launch is not yet certified.**
The native request preserves the original instructions and explicit decoding,
and seven focused tests pass. Raw responses and conservative at-cap rejection
are sound. Before freezing, complete the extraction/compounding sensitivity,
bind actual requests, reject contradictory zero-token statistics, and enforce
the declared loaded configuration. This review does not load a model, query the
server, run probes or collect financial answers. Original studies are untouched.

## Material findings sent before collection

1. **Incomplete sensitivity cross.** The analyzer computes strict and numeric
   scores, but applies the two-convention union only to strict scores. A value
   rejected by strict formatting but admitted by the prespecified numeric parser
   can therefore remain convention-misclassified in the numeric analysis. Import
   the unchanged `extended_record` for both saved score streams. Report both
   convention endpoints and per-family/compatibility cells without replacing
   nominal `1+r` primary results. No new numerical rule is needed.
2. **Actual requests are not bound per attempt.** `generate()` constructs its
   request from frozen `CONFIG` and the question, but stores only the reply.
   Preserve the exact request body and deterministic request hash, then verify
   system/config/input equality against the frozen question in analysis. This
   closes request provenance; code inspection alone documents intended messages.
3. **Contradictory counters are accepted.** An authored nonempty
   `FINAL: 21 currency` response with both `input_tokens` and
   `total_output_tokens` equal to zero currently normalizes to `stop`.
   Validate positive input counts for these nonempty requests and positive output
   counts for nonempty content. Keep an empty/no-answer return explicitly failed
   or unparsed rather than inventing completion. Existing type/nonnegative checks
   correctly reject booleans, missing counters, reasoning and over-cap output.
4. **Capture is not an initial configuration gate.** `prepare` captures
   `loaded_config`; `verify` rejects drift from that capture. Neither presently
   rejects a captured configuration violating the protocol's context 4096,
   parallelism one, full Metal offload or no speculative draft. Validate required
   effective fields before accepting the freeze, using actual exposed schema
   or a bound machine receipt where fields are unavailable. A hardcoded engine
   name does not itself prove the live instance used that engine.

Tighten analyzer integrity at the same boundary: require the intended `MODEL_KEY`,
collection indices 1..N, receipt scheduled count 200, exact unattempted suffix,
timestamps after the collection freeze, and selected prompt/formula equality
against reconstructed cases. The existing case-order/question-hash/receipt hashes
are useful but do not check every declared field. Preserve runtime errors and
their raw native evidence; successful normalization must not repair a failed record.

The wall guard currently stops **scheduling** after one hour. An already running
request may continue up to its 120-second timeout. Either say scheduling cutoff
explicitly or bound request timeout by remaining time. Timed-out server execution
is unresolved and must not trigger a retry or a fabricated output.

## Sound implementation choices and remaining measurement limits

The API body explicitly sets reasoning off, integrations empty, store false,
stream false, temperature zero, top-k one, top-p one, min-p zero, repeat penalty
one and a 1024-output-token cap. There is no previous-response identifier or
structured-output grammar. Sequential one-shot collection preserves every
attempt and stops after five consecutive runtime failures; the ledger/receipt
refuse overwrite and retain unattempted IDs separately. Neither answer quality
nor malformed final lines trigger a retry. Original scorers/formulas are imported.

Native normalization checks exact instance identity, one message item, no
reasoning/tool item, integer aggregate counters, zero reasoning tokens, the cap
and input-plus-cap context allowance. At-cap output remains `length` even with
a parseable final line. Below-cap `stop` is a declared adapter category for a
normally returned reply; it is **not an observed native finish/EOS**. No native
token IDs or exact stop reason are available. Do not imply identical token-level
termination or rendering to old PyTorch/OpenRouter runs. In particular, an
early server cancellation below the cap cannot be distinguished if no other
native status is exposed; the parser alone does not certify completion semantics.

Read the installed native `model.yaml`: it preserves a distinct system turn
and user turn, injects a thinking marker conditionally, and uses an empty thought
prefix when thinking is disabled. Its defaults are temperature 1, top-k 64,
top-p .95 and thinking enabled. Explicit request overrides therefore matter;
zero observed reasoning is useful execution evidence but does not independently
reconstruct server serialization. The local manifest's revision 4 identifies
the LM Studio virtual descriptor, not an upstream immutable GGUF revision.

The latest preparation code now hashes engine root binaries/libraries, concrete
GGUF files, native YAML/JSON/README, scientific imports, old selection manifest,
tests and the original precollection review. Root binary files are actually
present in the named engine directory. No multi-gigabyte hashes or effective
live configuration were independently verified here; the prospective preparation
and collection verifier must do so. Bind this supplement as well before probes.

The new three-correct-strict-final gate is stricter than the prior review's
runtime-only feasibility recommendation. It is permissible as an explicit
prospective gate on a fixed configuration, with all failed diagnostics retained.
It conditions any launched result on elementary arithmetic/format competence;
do not imply selection independent of that competence or hide a failed gate.
Three toy successes would not establish sustained 200-question feasibility.

## Verification and scope

Inspected the new protocol/module, preparation/collector/analyzer drivers,
tests and read-only installed model/engine metadata. Ran only authored controls:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=src .venv/bin/python -m pytest -q tests/test_model_grading_lmstudio.py
```

Result: `7 passed in 0.02s`. An additional in-memory authored counterexample
reproduced finding 3 without server access. Findings describe the inspected
prefreeze version and must be rechecked after fixes. Only this new supplement
was written; no new inference, server query or frozen modification occurred.
This is AI-assisted technical review, not human financial adjudication or a
prediction of checkpoint performance.
