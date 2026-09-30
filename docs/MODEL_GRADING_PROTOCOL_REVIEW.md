## Executive summary (read this first)

The 200-question extension measures grading consequences on
actual responses in the audited families. The same frozen response must be scored
by both the original-label comparator and a visible-question oracle. This is a
paired evaluation of released labels; it does not estimate causal training harm,
field prevalence, or transfer to unseen financial templates.

This review is AI-assisted methodological and technical validation. A blinded
human-review packet is prepared separately under ignored storage. Preparing
that packet is not human annotation, financial-expert adjudication or contact with
any reviewer. Execution findings will be added after checking the actual artifacts.

## Source evidence and appropriate contrast

The pinned Cosimo CFA Level I release has 1,000 rows in each proposed family.
There are 630 distinct constructed-response Gordon questions, 905 binomial
questions, 639 ordinary Gordon questions and 999 WACC questions. A 50-question
sample is feasible for all four. These are template families from a known audited
release, so the extension should be described as an observed-output consequence
study rather than an independently discovered transfer result.
An independent full-pool metadata check found no duplicate-question gold conflicts
in these four families. CR and ordinary Gordon share 395 operand-identical prompts
after removing the CR prefix and its whole-unit instruction. This dependence
should be checked again in the selected 200-question set.

The [public binomial generator](https://github.com/btech-software/cosimo/blob/20668622104bf8237837efd67debd1419f7bbe33/dataset/pipelines/templates/cfa_l1.py#L441)
calculates positive bond debt and stores it as the call value. The
[constructed-response wrapper](https://github.com/btech-software/cosimo/blob/20668622104bf8237837efd67debd1419f7bbe33/dataset/pipelines/templates/wrappers.py#L30)
adds a whole-unit instruction while copying a cent answer. Ordinary Gordon and
WACC supply passing comparison families under independently checked formulas.
Consequently, the contrast has a substantive quantity error, an output-precision
conflict, and two controls. It is not a random four-family finance sample.

The Data Literacy and Lu review recommends measuring an actual decision change,
checking metadata before trusting it and keeping sampling assumptions explicit.
These requirements follow the local
[course-grounded review](/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/outputs/course-review/DATA_LITERACY_AND_LU_REVIEW_2026-09-29.md).
No professor's endorsement or feedback on this paper is inferred.

## Selection requirements

1. Deduplicate exact visible questions within each family before selecting. If
   duplicate rows disagree about source labels, preserve that conflict explicitly;
   a representative row must not silently remove inconsistent supervision.
2. Select 50 questions per family using a fixed, recorded hash namespace or random
   seed. Freeze IDs, exact prompt text, representative-row rule, source hashes and
   selection hash before inspecting new responses. Do not select for a label error,
   price regime, successful parsing or dramatic grading change.
3. Keep all 200 questions for every model. A failed request, empty completion,
   parse failure or truncated response remains visible. Retrying a transport
   failure requires logging the attempt and why no usable answer existed. Do not
   regenerate a valid but inconvenient response.
4. Preserve original questions and explicit whole-unit instructions. A common
   formatting instruction may request a final value, but must not supply the
   correct formula, answer, source solution, verification metadata or source gold.
5. Report within-family uniqueness and cross-family operand overlap. CR and
   ordinary Gordon share an underlying formula; matching operands are related
   cases even when their output instructions differ. Equal family weights estimate
   this balanced design, not the source's natural population mixture.

## Response extraction and units

Freeze extraction before inference. A schema-constrained final-answer field or a
strict final marker is preferable to taking the first or last number anywhere in
a reasoning trace. Preserve raw text and any structured value. Numbers inside
equations, examples, confidence statements or self-corrections are not interchangeable
with the model's declared final answer. Ambiguous final values require an explicit
extraction failure, followed by a separately recorded blind review if performed.

WACC is expressed in percentage points in the source: 8.51% means the scalar
8.51 for the numeric comparator, whereas 0.0851 as a proportion denotes the same
economic rate only if its unit is explicit. Predeclare unit parsing and normalization.
Do not interpret a unitless 0.0851 as 8.51 merely because doing so improves accuracy.
Report unit failures separately from arithmetic failures. Currency results share
one currency unit; do not silently interpret a value as thousands or millions.

A whole-unit answer is a numerical integer. Rendering 31 as 31.0 or 31.00 does
not change the represented value. The validator should distinguish numerical
rounding from textual formatting. Conversely, it must not round a model answer
30.94 to 31 on the model's behalf. Scientific notation, thousands separators,
currency marks, percent signs and negative signs need predeclared treatment.

Pin named model versions, endpoint/provider, exact system and user messages,
generation limits, temperature and other supported settings. Record timestamps,
returned model identifiers, response IDs, usage and finish reasons. Temperature
zero alone does not certify deterministic API behavior. A serving alias is not
equivalent to an immutable weight revision; state any unavailable version pin.

## Oracle requirements

- Constructed-response Gordon: calculate `D0*(1+g)/(r-g)` from displayed operands,
  then compare the model's numerical final answer with the nearest whole value.
  At an exact half tie, accept either adjacent integer because the original prompt
  names no tie convention. Track arithmetic-only correctness separately if useful.
- Ordinary Gordon: use the same financial formula without imposing an unstated
  whole-unit requirement. The stored cent answer supports a declared 0.005-unit
  serialization allowance; it does not make all additional decimals invalid.
- Binomial: use risk-neutral valuation and check exact agreement with a portfolio
  reproducing both terminal payoffs. Elementary bounds alone are insufficient:
  all 1,000 audited source bond-debt labels passed those bounds. Enforce `d<1+rf<u`
  and record spot, up/down factors, strike, interest convention and payoffs.
- WACC: combine market-value equity/debt weights and apply the tax shield to debt
  cost. Keep the output in percentage points. Its cent-percentage allowance is
  0.005 percentage point, not 0.005 as an unnormalized rate proportion.

The oracle depends on a financial specification independently checked with exact
fractions. It is not a generic learned judge, a proof that every model trace is
correct, or a new general-purpose verifier. Incorrect reasoning can collide with
a correct final integer; the 34 rounded Gordon rejected-answer collisions already
demonstrate that limit. Model trace assessment must remain a separate outcome.

CAPM and DCF should remain supplementary ambiguity examples in the human packet,
outside the 200-case primary test. Their intervals are identification bounds from
rounded inputs, not confidence intervals. A feasible source gold is not a uniquely
identifiable exact target. Introducing an interval reward would change the task.

## Paired grading outcomes and interpretation

For every model and family, report attempted, completed, parsed, oracle-correct,
and source-comparator-correct counts. For each declared policy give the paired
four-cell table: both accept; oracle only; source comparator only; neither accepts.
The oracle-only cell measures valid observed answers denied credit. The source-only
cell measures invalid observed answers receiving credit under that comparator.
Give exact denominators as well as percentages, with failure handling visible.

Original-label absolute and relative tolerances are reconstructed policies. They
do not reproduce a deployed Cosimo reward. Policies from the earlier audit may be
reused as declared sensitivity conditions; do not choose a new threshold after
seeing model answers to maximize a headline. For relative policies, document which
value supplies the denominator, including zero-label behavior.

Every model answers the same selected questions. Any claimed model-order reversal
must use the same completed-case/failure convention and policy, and report the
actual scores and family decomposition. A finite score difference on 50 templated
questions is not a broad superiority ranking. Question-level paired resampling can
describe sensitivity within this sample; it cannot turn family selection into
population prevalence or remove shared-generator dependence.

The headline should follow observed results. If few real responses change grading,
report that result even when constructed candidates showed large effects. If a
simple tolerance policy resolves the output-precision conflict without accepting
the observed errors, keep that successful control prominent. Regardless of outcome,
this extension measures evaluation distortion, not RL reward loss during training.

## Prospective human-review packet

The small packet should contain anonymous prompt IDs, unmodified question text,
blank fields for the reviewer's assumptions, formula, final value and output
precision, plus explicit uncertainty fields. Include affected families, passing
controls and supplementary rounded-input examples. Do not display source labels,
verification flags, defect status, model names or this study's expected conclusion.
The source IDs, exact-rational calculations and ambiguity intervals belong in a
separate key. When model responses are available, append anonymized candidate
responses while retaining the original raw answers for audit.

Question wording necessarily reveals financial content and sometimes response
format. “Blinded” therefore means blind to source labels, defect classification
and model identity; it does not mean blind to the question's family. Record who
actually reviewed the packet, their relevant expertise, reviewed case IDs,
disagreements and any adjudication. Until then, report only packet preparation.

## Execution review status

No model-grading execution artifact was available at initial review. The current
draft subsequently named two local Qwen models and a third, provider-pinned
DeepSeek API configuration. The roster must be described as three configurations
if all are executed, rather than the initial two-model proposal. Exact identifiers
and serving limitations are recorded in the main V1 protocol.

Pre-inference extraction probes confirmed numeric-integer equivalence, standard
scientific notation, valid thousands separators and explicit WACC unit rejection.
They also identified an uncaught extreme-exponent Decimal exception, and ambiguity
between a strict one-marker policy and counting only uppercase line-leading
markers. These were flagged before inference; the probe artifact preserves the
tested code hash. Any corrected parser must be frozen before observing responses.

The frozen selection at `2026-09-29T18:24:04.060820+00:00` has SHA256
`75c5b694db2d9a174e089c594e3f756867e0f840f12ac4634e5dc20173acf0cc`.
Separate source-based sampling reproduced all selected IDs and prompts. Exact
rational calculations agree with every selected formula and target. There are
50 distinct questions per family, three shared Gordon operand sets and one exact
half tie. The selected source golds are invalid for 48 CR questions and all 50
binomial questions; both 50-question control families pass their source-label check.

The twelve-prompt human packet now uses eight questions from this actual selected
panel plus two supplementary CAPM and two DCF questions. Anonymous prompts and
blank review fields are in ignored `outputs/model-grading-review/BLINDED_PACKET.md`;
labels, identities and exact-rational calculations are separately stored in
`ANSWER_KEY.json`. The packet hash is
`fa9f5a2495d0bb5032b9b114787fa78af557d4438da316d924e834a3e33af789`.
Its source selection is recorded in the separate manifest. No human review or
reviewer contact has occurred.

The independent response scorer is
`scripts/validate_model_grading_outputs.py`. It snapshots active immutable ledgers,
uses independently implemented extraction and Fraction arithmetic, and records
paired four-cell counts. Partial snapshots are explicitly labeled; they do not
replace the final 200-question denominators. Initial recorded API replies return
the intended SiliconFlow provider and DeepSeek model identifier. The local runtime
metadata match the declared cached revision, float16, MPS and greedy settings.

Actual early responses show substantial format noncompliance: missing final units
and literal `<unit>` placeholders occur even beside correct-looking calculations.
The original strict parser and results must remain primary. A separate timestamped
numeric-final-line sensitivity may diagnose this confound, but it is exploratory
after observing early failures; it must not search reasoning text, normalize rate
fractions or silently overwrite strict decisions. Recovered unitless values support
numeric correctness under the requested-unit assumption, not verified unit compliance.
The strict endpoint enforces its frozen final-line grammar and source-question
numeric contract. It does not enforce every system instruction, including the
minimum four decimal places or the reasoning sentence limit. Describe those
dimensions separately from complete instruction-following compliance.

The original 600-response panel now passes independent comparisons of every
value, error, unit state, decision and aggregate under both endpoints. The actual
24-answer anonymous packet is prepared with a separate key; human review remains
pending. Detailed results and checkpoint hashes are in
`docs/MODEL_GRADING_INDEPENDENT_RESULTS.md`. Exploratory 4B, combined 800-record
and 1,600 convention-endpoint comparisons also pass independently.

The completed DeepSeek subset independently yields 137 strict parsed answers and
136 valid answers under the declared oracle. Source-label absolute 0.005 scoring
credits 81 and denies credit to 55 valid answers. The exploratory numeric endpoint
parses all 200 and validates 199; the same source policy credits 102 and denies 97
valid numeric answers. Full original three-model comparisons pass independently.

The remaining DeepSeek answer requires care: row
`cosimo_CFA_Level_I_231729_be0ed4387b76d0b9` uses continuous compounding and gives
3.06. The declared one-period gross `1+rf` gives `64/21 ≈ 3.047619`; using `exp(rf)`
gives approximately 3.063280, within 0.005 of the model answer. The question does
not explicitly state the compounding convention. Preserve the frozen oracle and
report this as a convention mismatch under its declared specification, rather
than an unqualified arithmetic failure. Source gold 12.95 remains a different
financial quantity under either convention. Human financial adjudication remains
pending.

The source-based selection check is reproducible with
`scripts/validate_model_grading_selection.py`, which reads the pinned parquet,
deduplicates independently and checks all 200 IDs, questions, exact fractions and
targets. Its SHA256 is
`9a9355b8afeca690d97b4194e9c672925c71140205d23bc9ddda2ce0d800f53a`.

The supplementary unit correction retains the original parser and driver under
`outputs/model-grading-v1/sensitivity-original/`. Independent validation checks
their original frozen hashes, the unchanged original freeze and all corrected
version-2 hashes. It separately rejects explicit currency/percent contradictions.
Final real-response contradiction accounting remains pending the complete panel.

The completed binomial text census so far finds exponential-compounding markers
in all 50 Qwen3 responses and one of 50 DeepSeek responses. None of the Qwen3
parsed finals is valid under either convention within 0.005; their errors cannot
be attributed solely to compounding. The DeepSeek case above is valid under the
continuous convention. Coder has nine markers in its 50 completed binomial answers
and gains no valid numerical answers under the alternative. Raw text, marker contexts,
declared and alternative formulas are preserved in
`outputs/model-grading-review/model-case-notes.json`; this descriptive census does
not replace the frozen oracle or prove consistent implementation from a marker.
The completed 4B census has 39 markers in 50 binomial answers and no additional
compatible parsed finals; the complete convention comparison confirms this.

## Exploratory matched-checkpoint extension

The Qwen3 4B extension was frozen at `2026-09-29T18:50:42.038841+00:00`,
after 188 Qwen3 1.7B and all 200 DeepSeek answers but before any 4B financial
answer. It uses the original panel and the same Qwen3 nonthinking mode, FP16 MPS,
greedy decoding, token limit and prompts. This supports a matched comparison of
released Qwen3 checkpoints; differing training remains a possible explanation,
so the comparison cannot identify a causal parameter-count effect. Cross-family
comparison additionally mixes architectures, training, specialization, serving
runtime and quantization. Keep the original 600-response analysis separate from
the extension and combined 800-response results. The independent extension scorer
`scripts/validate_model_grading_extension.py` checks extension freeze/runtime
metadata and compares all strict and supplementary values, decisions, failures,
unit states and aggregates, then checks the combined outputs and constituent hashes.

The compounding sensitivity keeps the declared oracle unchanged and separately
accepts compatibility with either `1+rf` or `exp(rf)`. Independent 100-digit
mpmath replication confirms that the same 975 of 1,000 source labels fail both;
the remaining 25 all have zero gold and zero call value. This does not certify
the generator's financing-debt formula. The first sensitivity freeze recorded
64 Coder answers, including 14 binomial answers; its claim to precede those
answers was incorrect. The original freeze/driver are retained and a separate
timestamped correction fixes the claim. Both freezes precede all 4B answers.
Full result comparison is reported separately in the independent results report.
