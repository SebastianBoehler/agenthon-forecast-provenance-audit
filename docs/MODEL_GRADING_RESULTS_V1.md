## Executive summary (read this first)

Executed 800 responses to the same 200 distinct public questions: four models, 50 questions per family. The original three-model 600-response panel is preserved separately from the later 4B extension. This measures grading of saved model answers, not training effects. Strict final-line parsing, post hoc numeric extraction and post hoc compounding sensitivity are distinct endpoints.

Reported API usage cost: $0.027243020; the additional local run uses cached weights.

## Completion and declared numerical validity

Every cell has the same 200-question denominator. Strict is the declared final-line endpoint, not complete compliance with all system instructions. Numeric recovery may lack an explicit unit. The last column broadens only binomial validity to either simple or continuous compounding.

| Model | Strict parsed | Strict valid | Numeric parsed | Numeric valid (1+r) | Numeric valid (either convention) |
| --- | --- | --- | --- | --- | --- |
| Qwen3 1.7B | 0 | 0 | 189 | 41 | 41 |
| Qwen3 4B | 34 | 3 | 90 | 46 | 46 |
| Qwen2.5-Coder 3B | 0 | 0 | 192 | 39 | 39 |
| DeepSeek V3.2 | 137 | 136 | 200 | 199 | 200 |

## Grading unchanged recovered numbers

All cells are counts among the same 50 questions per model/family, including failures in the denominator. “Denied” counts declared-contract-valid numbers rejected by an original-label comparator; “credited” counts parsed numbers outside that contract accepted by it. They are paired numerical decisions, not separate generations. Here the binomial reference remains 1+r.

Constructed-Gordon source-cent credits are 10/50 for Qwen3 1.7B versus 2/50 for DeepSeek; visible integer-contract validity is 22/50 versus 50/50. Changing only the grader reverses their ordering on this family under the exploratory numeric endpoint. This is not a general model ranking.

| Model | Family | Cent denied | Cent credited | Half denied | Half credited | 5% denied | 5% credited |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3 1.7B | Whole-unit Gordon | 20 | 8 | 0 | 20 | 0 | 27 |
| Qwen3 4B | Whole-unit Gordon | 36 | 0 | 0 | 0 | 0 | 0 |
| Qwen2.5-Coder 3B | Whole-unit Gordon | 27 | 1 | 0 | 3 | 0 | 16 |
| DeepSeek V3.2 | Whole-unit Gordon | 48 | 0 | 0 | 0 | 0 | 0 |
| Qwen3 1.7B | Binomial call | 0 | 0 | 0 | 0 | 0 | 0 |
| Qwen3 4B | Binomial call | 0 | 0 | 0 | 0 | 0 | 0 |
| Qwen2.5-Coder 3B | Binomial call | 0 | 0 | 0 | 0 | 0 | 0 |
| DeepSeek V3.2 | Binomial call | 49 | 0 | 49 | 0 | 49 | 0 |
| Qwen3 1.7B | Ordinary Gordon | 0 | 0 | 0 | 28 | 0 | 29 |
| Qwen3 4B | Ordinary Gordon | 0 | 0 | 0 | 0 | 0 | 0 |
| Qwen2.5-Coder 3B | Ordinary Gordon | 0 | 0 | 0 | 33 | 0 | 39 |
| DeepSeek V3.2 | Ordinary Gordon | 0 | 0 | 0 | 0 | 0 | 0 |
| Qwen3 1.7B | WACC | 0 | 0 | 0 | 35 | 0 | 35 |
| Qwen3 4B | WACC | 2 | 0 | 0 | 22 | 0 | 21 |
| Qwen2.5-Coder 3B | WACC | 0 | 0 | 0 | 12 | 0 | 11 |
| DeepSeek V3.2 | WACC | 0 | 0 | 0 | 0 | 0 | 0 |

## Cheap rounding baseline

Only constructed Gordon has a meaningful integer-plus-original-half-unit baseline. Other-family mechanical JSON values are not interpreted.

| Model | Valid recovered | Half: invalid credited | Integer+half: invalid credited | Integer+half: valid denied |
| --- | --- | --- | --- | --- |
| Qwen3 1.7B | 22 | 20 | 0 | 0 |
| Qwen3 4B | 37 | 0 | 0 | 0 |
| Qwen2.5-Coder 3B | 28 | 3 | 0 | 0 |
| DeepSeek V3.2 | 50 | 0 | 0 | 0 |

## Paired Qwen3 checkpoint comparison

Counts use all 200 shared question IDs. This controls prompt, model generation, precision, runtime and decoding; it does not identify a causal parameter-count effect because checkpoints/training differ.

| Endpoint | Both valid | 1.7B only valid | 4B only valid | Neither valid |
| --- | --- | --- | --- | --- |
| Strict | 0 | 0 | 3 | 197 |
| Numeric | 21 | 20 | 25 | 134 |
| Numeric, either convention | 21 | 20 | 25 | 134 |

## Convention robustness and limits

Among all 1,000 source binomial labels, 975 remain invalid under both checked conventions. The source generator computes financing debt; coincident numerical values do not certify that formula. The convention sensitivity is a union of two cent neighborhoods, not the interval between their prices. Literal reasoning keywords are not a gate for this test.

The original compounding-sensitivity timing claim was corrected in a separate note: its first freeze followed 14 Coder binomial responses and preceded all 4B responses. The endpoint remains explicitly post hoc. Neither the size extension nor numerical recovery is retrospectively preregistered.

Family selection is purposive; repeated templates prevent treating the census as independent population samples. No fine-tuning, executable upstream reward, general-validator accuracy, human expert review or causal model ranking is claimed. Final-answer compatibility does not certify a reasoning trace. A 12-item anonymous human-review packet is prepared but its sheet remains blank.

## Input analysis hashes

- `results.json`: `27149487d4709c646f0da807c5305c6890858658beb71436523cec9c93f94355`
- `numeric_sensitivity.json`: `0a91a0f9f4e2de1db5bd6fd6ce6bb564694bcdf719728896aac55d3e467925f9`
- `extension_results.json`: `cac08fdcf3bc7574ef3016af9c05ece7386b0ebbd859b3cbd7bd956e4084f1be`
- `combined_results.json`: `46e9bcb2980330238f556bc94d536c909302c4b2f5b1ea5f30ce54d20fbeac90`
- `combined_numeric_sensitivity.json`: `2c85587f7874bf37930208c91d73678187f94e2565373aeed0366bc961e60375`
- `convention_sensitivity.json`: `36f89979b260a51ab88dc9feaf30879ba80129bf2987f6c82acc9eb1d7a58260`
