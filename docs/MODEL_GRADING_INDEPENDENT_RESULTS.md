## Executive summary (read this first)

Independent validation passes for all original 600 responses under both endpoints:
every value, error, unit state, grading decision and aggregate agrees with the
published original result files. Independent source sampling reproduces all 200
questions and exact numerical targets. The anonymous 24-answer review packet is
prepared; human review is pending. The exploratory 4B, combined 800-response
and 1,600 convention-endpoint comparisons also pass independently. Original
checkpoint hashes remain unchanged.

This is AI-assisted technical validation. It is not human annotation or a blind
conceptual replication: the validating agent read the primary code. No upstream
financial generator or supplied solution was executed.

## Completed source checks

The panel has 50 distinct prompts in each of four families. There are three
shared Gordon operand sets and one exact half tie. Source golds fail the original
visible-question oracle for 48 CR Gordon and all 50 binomial questions; both
50-question controls pass. Full source pools contain no duplicate-question label
conflicts. Source selection was independently deduplicated and hash-ranked from
the pinned parquet using a separate script.

Continuous-rate prices use `delta*S0 - terminal_debt*exp(-rf)` with one period;
both terminal payoff identities are verified using exact rational arithmetic.
All 1,000 questions permit the alternative under its no-arbitrage inequality.
The same 25 source rows pass the simple-rate and continuous-rate neighborhoods;
all 25 have zero payoff, price and gold. None of the other 975 labels is rescued.

## Original response results

Validation completed at `2026-09-29T19:34:09.641351+00:00`. There are exactly
200 frozen question IDs for each original model, without duplicate responses.
Strict and exploratory numeric outputs each contain 600 matching scored records.
Local runtime settings and remote model/provider/request metadata match the
declared configurations. No actual final answer combines a currency prefix and
percent suffix among these 600 raw responses. No answer was regenerated.

All model totals have 200 attempts. Strict failures are 198 format errors and two
unfinished Qwen3 answers, 200 Coder format errors, and 63 DeepSeek format errors.

| Configuration | Strict parsed / valid | Numeric parsed / valid | Source 0.005 credits | Valid denied / invalid credited |
|---|---:|---:|---:|---:|
| Qwen3 1.7B | 0 / 0 | 189 / 41 | 29 | 20 / 8 |
| Qwen2.5-Coder 3B | 0 / 0 | 192 / 39 | 13 | 27 / 1 |
| DeepSeek V3.2 | 137 / 136 | 200 / 199 | 102 | 97 / 0 |

The last two columns use the exploratory numeric endpoint and original-label
absolute allowance 0.005. Absolute allowance 0.5 credits 124, 87 and 150 answers,
including 83, 48 and zero invalid answers respectively. Relative 5% credits 132,
105 and 150, including 91, 66 and zero invalid answers. DeepSeek loses 49 valid
answers under either of these looser comparators; the two local models lose zero.
These are reconstructed grading policies, not observed upstream rewards.

| Numeric valid answers / 50 | CR Gordon | Binomial | Ordinary Gordon | WACC |
|---|---:|---:|---:|---:|
| Qwen3 1.7B | 22 | 0 | 17 | 2 |
| Qwen2.5-Coder 3B | 28 | 0 | 11 | 0 |
| DeepSeek V3.2 | 50 | 49 | 50 | 50 |

Within CR, source 0.005 credits Qwen3 10 answers and DeepSeek two, whereas the
visible contract credits 22 and 50. This observed ordering reversal is specific
to these 50 questions, policy and post hoc extractor. The integer-plus-half-unit
baseline reproduces all 22, 28 and 50 observed CR-valid answers with no invalid
credits. Its mixed-family aggregate has no scientific interpretation.

DeepSeek's only numerical miss uses continuous
compounding; allowing either convention changes these counts to 137 and 200.
The original source-comparator decisions stay fixed. Qwen3 1.7B has zero strict
parsed answers and 41 valid exploratory numeric answers; the convention union
adds none. Coder also gains none. The descriptive text census finds exponential
markers in 50, nine and one completed binomial responses respectively. A marker
does not establish correct implementation; only the DeepSeek case is rescued.

The first convention-sensitivity freeze follows 14 Coder binomial answers and
precedes all 4B answers. Its erroneous timing claim is retained in the original
record and corrected by a separately frozen note/version. Independent validation
checks the original driver snapshot, original freeze identity and version-2 file
hashes. The original strict and supplementary freezes are also checked.

## Reproduction and evidence

Run from `/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit`:

```bash
.venv/bin/python scripts/validate_model_grading_selection.py
.venv/bin/python scripts/validate_model_grading_outputs.py
.venv/bin/python scripts/validate_model_grading_extension.py
.venv/bin/python scripts/validate_model_grading_conventions.py
.venv/bin/python scripts/census_model_grading_conventions.py
.venv/bin/python scripts/append_model_review_responses.py
```

The response-packet command requires all original 600 responses. Ignored
`outputs/model-grading-review/` contains independent row scores, source prices,
summaries, hashed response snapshots and separate blinded materials/answer keys.
The primary study's original ledgers and frozen source files are not modified.

`response-packet/` contains eight selected questions and 24 anonymous raw answers.
The 33 reviewer-facing Markdown files preserve each raw answer exactly, contain
no explicit source/model identifiers and each have fewer than 300 lines. Separate
`RESPONSE_KEY.json` stores the identities and original response text hashes.
The twelve-question financial packet additionally includes four supplementary
rounded-input questions. No human annotation or reviewer contact has occurred.

## Original checkpoint hashes

SHA256 values describe the completed original checkpoint. Later extension checks
have separate summaries; per-file hashes and four-cell counts are in ignored JSON.

| Artifact | SHA256 |
|---|---|
| Independent original scorer | `b0e3e9df11f41e095a0540f31d8353c63eb9e6139981e7c85b20d8fd4a8eebad` |
| Independent original summary | `51c753e90ce0bff459c88d4580275eb847b1dab5f73ee088ff1696ceafa5712a` |
| Independent strict scores | `f0800fb02c64f3c53f240c793c6a68e68798131c5a9831019e04b75573600c93` |
| Independent numeric scores | `c40d0edda944e723b87effba166125900bec08c6ac1857508b5c90328b55df4b` |
| Original primary results | `27149487d4709c646f0da807c5305c6890858658beb71436523cec9c93f94355` |
| Original numeric results | `0a91a0f9f4e2de1db5bd6fd6ce6bb564694bcdf719728896aac55d3e467925f9` |
| Anonymous response packet manifest | `db4e2452a9817311f8fc7119c1371d5d8ff4d9e82b037407c0596b89fec10838` |
| Separate response key | `d57db379fb841f9f1330c6bb751fd9371993c658d70fea6b4d9df0ee89182b09` |

## Completed exploratory extension and convention checks

At `2026-09-29T20:07:47.667909+00:00`, all 200 extension records and both
combined 800-record endpoints agree on every value, error, unit state, decision
and aggregate. Combined constituent hashes agree. No contradictory explicit
currency/percent final line occurs among all 800 responses.

Qwen3 4B has 34 strict parsed answers and three valid answers; all 34 parsed
answers are WACC. Exploratory numeric extraction parses 90 and validates 46.
Its valid counts per 50 are CR 37, binomial zero, ordinary Gordon six and WACC
three. Source 0.005 credits eight and denies 38 valid values, with zero invalid
credits. Source 0.5 credits 68 including 22 invalid values; relative 5% credits
67 including 21 invalid values. The CR integer-plus-half baseline accepts all
37 observed valid CR values with zero invalid credits.

These endpoint counts cannot identify a causal size effect or overall financial
ability: numerical extraction succeeds on 189 Qwen3 1.7B versus 90 Qwen3 4B
answers, and released checkpoint training may differ. The stricter final-line
failures remain visible rather than being silently repaired.

At `2026-09-29T20:07:48.214867+00:00`, the 100-digit independent convention
calculation agrees with all 1,000 primary source prices/flags and all 800 strict
plus 800 numeric decisions, including compatibility cells and paired aggregates.
Allowing either convention adds exactly the previously identified DeepSeek case.
No other model gains a compatible parsed final. Exponential text markers occur
in 50/50, 9/50, 1/50 and 39/50 completed binomial responses in the four named
configurations; this descriptive marker census is not an acceptance prerequisite.
The 975 invalid source labels and 25 zero-value coincidences remain unchanged.

| Exploratory artifact | SHA256 |
|---|---|
| Independent extension summary | `a7f49e4045981c77ba05c22f39d466d65dfe0db4ec5d18ad674fb741323a9e90` |
| Independent convention summary | `6ff5177125d1240f7694925e3ccf3604411e83cde086d94420f4d2bd83873a4e` |
| Combined strict results | `46e9bcb2980330238f556bc94d536c909302c4b2f5b1ea5f30ce54d20fbeac90` |
| Combined numeric results | `2c85587f7874bf37930208c91d73678187f94e2565373aeed0366bc961e60375` |
| Primary convention results | `36f89979b260a51ab88dc9feaf30879ba80129bf2987f6c82acc9eb1d7a58260` |

Each independent summary records its script/dependency hashes, original response
hashes, frozen-version checks and per-file results. The original three-model
checkpoint and 24-answer review packet are preserved separately.
