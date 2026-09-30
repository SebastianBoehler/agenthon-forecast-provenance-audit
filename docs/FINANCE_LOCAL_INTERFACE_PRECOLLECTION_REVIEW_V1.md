## Executive summary (read this first)

The proposed 2×2 local pilot has a defensible bounded design. Salted selection
and all 256 native-token audits pass independently, without financial inference.
Its factors are requested response content/burden and quantity instructions;
tokenization is plumbing, not novelty. Two checkpoints on the same backend do
not identify causal model-family or size effects. This is a discovery-cohort
pilot with reused AI-assisted numerical references, not a fresh semantic test.

**Resolve failure accounting and strict JSON parsing before the scientific
freeze.** At the reviewed state, `score()` can credit retained valid text on an
error-marked record, and `candidate()` accepts nonstandard `NaN` within evidence.
These are authored boundary controls, not observed financial outcomes. Complete
model/runtime and collector gates also remain outside this read-only review.
No frozen code, original study or model output was changed or generated here.

## Independent checks completed

Read the new protocol, `protocol.py`, `tokenization.py`, `scoring.py` and
`prepare_finance_local_interface.py`. Recomputed salted ranks from the original
96-case packet: exactly the first 16 FinQA and 16 TAT-QA IDs are selected. Every
prompt projects only question and original context; no native target, reviewer
status, prior answer or outcome filter enters selection/prompt construction.
The selected original-reference intersection is **24 questions: 11 FinQA and
13 TAT-QA**. Each condition therefore needs 32 attempted answers, 24 eligible
references and eight explicit exclusions; across eight model/condition cells,
256 attempts and 192 eligible attempts are repeated observations, not new cases.

Independently loaded both cached native tokenizers offline and recomputed every
prompt's native chat IDs, rendered-text hash, explicit-retokenization IDs and
legacy-default comparison. All 256 saved audits agree. Maximum input lengths
are 2,237 Qwen and 2,283 Smol tokens; native context limits are 40,960 and 8,192.
All inputs plus 512 completion tokens fit. Additional-special-token-disabled
IDs equal native IDs. **Legacy default IDs also equal native IDs in all 256
cases**, so these checkpoints provide no measured legacy token duplication.
Tokenizer-file hashes match preparation metadata. No model was loaded/generated.
Weight filenames/sizes were observed; complete checkpoint hashes and MPS runtime
success were not independently established by this tokenizer-only check.

## Material prefreeze findings

1. **Failure records must be ineligible regardless of retained text.** A source-free
   compact response containing valid `63 count` plus an authored runtime error
   receives a locked match from current `score()`. The scorer ignores error flags.
   Make both strict and status-only candidates absent on failed/censored attempts
   and retain an explicit failure reason, or establish an enforced collector
   invariant that failed records never carry scoreable text. Test valid-text-plus-
   error and empty-text failures before freezing. Preserve failures in denominators.
2. **Reject nonstandard JSON constants in the local parser.** Full text with
   `evidence:[NaN]` receives a strict numeric candidate. Python's default loader
   permits NaN/Infinity; list typing does not reject them. A local `parse_constant`
   rejection can fix the new interface without editing the old frozen parser.
   Exercise constants nested inside evidence, duplicate keys and trailing content.
3. **Define the status-only boundary.** Current normalization changes even a
   nonstring status `false` into `answer` when the original value is a numeric
   string. If the intended sensitivity repairs string status tags, require an
   original string and record its tag. If broader status-type repair is intended,
   declare and count that deviation explicitly before answers. Missing fields,
   numeric JSON value types, units and scale must remain unrepaired as specified.
4. **Name strict coverage precisely.** Full `calculation:"Assume annual; 7*9"`
   passes the unchanged typed parser. Strict schema availability does not enforce
   the requested arithmetic grammar or evidence validity. Keep whole-expression
   support separate, as the protocol proposes; do not describe it as complete
   instruction/trace compliance. Compact empty adapter fields are unobserved,
   not successful calculations or evidence. Full grammar is consistent across
   both reminders, removing the previous prose-in-calculation confound.

## Collector and freeze success checks

The collector was not part of the supplied implementation, so the protocol's
order, backend and completion-accounting claims are not yet execution evidence.
Before selected inference, freeze its actual driver, this review, all imported
scoring/native/projection/arithmetic dependencies, package versions and complete
model/tokenizer/config hashes. Avoid the earlier omitted-import binding gap.
Require successful pinned model loading on MPS with actual FP16 tensors, no
silent CPU/other-checkpoint substitution, and matching runtime prompt-ID hashes.
Use the audited native encoded dictionary directly in generation; preserve masks,
input length, generated-token count, stop reason, elapsed time and errors.

Verify greedy inference, evaluation/no-gradient mode, output-only decoding and
actual 512-token cap. Never truncate a financial context. Runtime availability,
token/context identity and parser-control success are gates. Toy answer/schema
failure remains a disclosed diagnostic and must not justify changing checkpoints
or prompts after observing outcomes. No toy financial outcome is a launch gate.

Validate exactly one record for each of two fixed models, four known conditions
and 32 cases. Rotation must balance condition positions and be recorded, not
only promised. Sequential model order can mix checkpoint and device/time effects;
report it and avoid family-causal claims. Exhausted generation budgets are
retained, even if compact/full token needs differ; that interaction is part of
output burden, not an isolated serializer effect. A stopped run is partial and
must not become a 256-record result by inserting fabricated responses or retries.

## Interpretation and verification scope

Within each schema, classify reminder discordances by availability, number,
unit/scale or mixed change; within each reminder, do the same for schema changes.
Report the all-32 primary coverage and fixed-24 locked denominator alongside
native and precision channels. Native credit and broad-unit agreement remain
distinct from semantic truth. An evidence/calculation request can change the
reasoning process as well as output format; schema effects are content/burden
effects. Full expression coverage has no observed compact counterpart.

The shared numerical instructions and no-prose arithmetic requirement are sound.
Salt selection was chosen after observing the earlier cohort; transparent
unfiltered hashing does not turn it into an unseen generalization sample.
Nulls, parser failures, previously documented repairs and ambiguous readings
must remain visible. Encoding checks cannot support an encoding-method novelty
claim or an old-tokenizer-defect claim when all observed legacy IDs match.

Checks used existing `.venv` Python with `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=src`,
`USE_TF=0`, `USE_FLAX=0`, `TOKENIZERS_PARALLELISM=false`, offline native tokenizer
loading and source-free parser/scorer controls. No network or financial inference.
Selection SHA256: `f173c740a1a721e91cb29a0fd26ca24e11d61b640632c509bd33fdd50b82758b`.
Original packet: `7cd3c12033bf97bd6fa4fc59277f06be01b83ee23d155a12b91bb1a7787553b0`.
This is AI-assisted precollection review, not human expert certification.
Offline token checks do not substitute for actual runtime/parser gate evidence.
