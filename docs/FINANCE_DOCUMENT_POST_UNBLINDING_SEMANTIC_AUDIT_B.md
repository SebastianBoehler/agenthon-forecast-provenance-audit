## Executive summary (read this first)

This new, explicitly **post-unblinding** AI-assisted technical audit covers all 96 FinQA/TAT-QA cases. It preserves both locked reviews and the original 62-case primary set. Agreement on arithmetic and units does not certify the requested financial meaning. Four of those 62 cases have clear FinQA requested-quantity contradictions; three other scalar mismatches admit defensible conventions. No definite TAT-QA contradiction is established in this packet. A separate FinQA Boolean answer contradicts the visible comparison.

The full classification is 32 compatible, 39 rounding/representation, 11 defensible alternatives, 4 insufficient-information, 5 unresolved, and 5 definite contradictions. These are bounded technical judgments about this selected packet, **not a population error estimate, new benchmark score, human adjudication, or first-discovery claim**. Prior published repairs and derivative lineage must accompany any paper claim about these cases.

### Stage, inputs and preservation

- The [pre-target lock](../outputs/finance-document-review-v1/pre_target_lock.json) was created at `2026-09-30T00:54:55.648456+00:00`; [native-target access](../outputs/finance-document-review-v1/source_target_unblinding.json) followed at `2026-09-30T00:55:28.817673+00:00`.
- Inputs were the original [review A](../outputs/finance-document-review-v1/review_a.jsonl), [review B](../outputs/finance-document-review-v1/review_b.jsonl), [combined record](../outputs/finance-document-review-v1/pre_target_combined.jsonl), both blank packets, and the native `source_targets.jsonl`. All 96 IDs, question strings and visible contexts match between the blank packets.
- All 96 visible-context cases and native answer/program/derivation channels were inspected. Calculations in the supplement use numeric-only arithmetic with exact `Fraction` operands and 50-digit `Decimal` display. Corpus programs were read as data; no arbitrary corpus text was executed. Pinned native evaluator code was inspected separately to establish representation conventions.
- The three locked review/combined hashes were checked against the lock before and after writing. The source-target hash matches the unblinding record. No original review, protocol, freeze, source target, scoring implementation, manuscript or model output was changed or generated.
- The new [96-record supplement](../outputs/finance-document-review-v1/semantic_source_audit_post_unblinding_b.jsonl) completed at `2026-09-30T01:26:50.216794+00:00`; SHA256 `15af8623e7e9e340179247bfced7cd0b22b410c2d79792a7b1ba0403c04472c4`. Raw packets and targets remain local excluded artifacts.

### Classification scope

The main FinQA numeric endpoint is `exe_ans`; the textual answer and executable program are inspected as separate channels. The Boolean case is classified against its textual answer. TAT-QA uses answer plus declared scale. Each record retains the locked joint status and explicit interpretation conditions. “Compatible” includes compatibility under a stated contextual reading; it does not certify an unrounded economic quantity or uniquely correct interpretation.

| Classification | FinQA (48) | TAT-QA (48) | Total | Within locked 62 |
|---|---:|---:|---:|---:|
| Compatible | 10 | 22 | 32 | 23 |
| Rounding/representation | 23 | 16 | 39 | 32 |
| Defensible alternative | 4 | 7 | 11 | 3 |
| Insufficient information | 4 | 0 | 4 | 0 |
| Unresolved | 2 | 3 | 5 | 0 |
| Definite contradiction | 5 | 0 | 5 | 4 |

The 62 remain the frozen arithmetic/unit agreement set. The table is a new semantic supplement, not a replacement endpoint. Cases excluded from that set retain their original status.

### Four clear numerical contradictions within the 62

Evidence indices below refer to the blank packet's visible table/text, using zero-based indices. Native programs corroborate the diagnosed computation; they do not prove how the original annotations were produced.

| FinQA ID | Requested quantity and visible evidence | Native computation | Judgment |
|---|---|---|---|
| `JPM/2018/page_90.pdf-6` | 2017 CIB income as part of managed income: `table[2][2]=4630`, `table[1][2]=51410`; `4630/51410*100 = 9.006029955...%`. | `4630/46780`, with `46780` the **excluding-CIB** total at `table[3][2]`; exe `.09897`, text `9.9%`. | Wrong denominator for the requested whole. |
| `SLG/2011/page_91.pdf-6` | Percentage change in year-end balance: beginning `2728290`, ending `2912456`, `table[1][1]`, `table[4][1]` and prior-year ending `table[4][2]`; growth `6.7502355...%`. | `2728290/2912456`; exe `.93677`, text `93.7%`. | Beginning/end **level ratio**, not percentage change. Start/end change-baseline choices do not explain this level ratio. |
| `PPG/2012/page_29.pdf-4` | Difference from 2011 to 2012: `post_text[9]` gives `56` then `122` USD million; requested difference magnitude `66`. | `56-34=22`, using 2010 and 2011. | Wrong year interval; choosing signed versus unsigned difference cannot produce `22`. |
| `ETFC/2011/page_144.pdf-2` | Explicit December 2010 ratio: `post_text[0]` collateral `19.3`, `post_text[1]` borrowing `.5` USD million; ratio `38.6`. | `2.3/.5=4.6`, using December 2011 collateral. | Wrong-year numerator. |

These are source-channel contradictions under the visible question, not claims of previously unknown defects. The overlapping reviewed/corrected FinanceReasoning/CodeFinQA lineage needs case-level attribution before publication. This audit does not independently establish correction priority or exact original generation history.

### Three other scalar residuals are not definite errors

- `UA/2011/page_69.pdf-1` asks a “percentage decrease” from `5.3%` to `3.5%`. Both reviews chose positive decrease magnitude `33.962264...%`; native uses signed relative change `-.33962`, textual `-34%`. A negative signed change is defensible. The new reconciliation arose after unblinding; it does not amend the frozen primary reading.
- TAT-QA `1bdabc6c-198d-4999-80aa-7c54b1f86513` asks percentage change in a compensation-growth rate, `2.7%` to `3.3%`. Relative growth is `22.222...%`; the absolute rate increase is `.6` **percentage points**. Review B recorded the latter alternative before unblinding. Native answer `.6` with scale `percent` follows that rate-gap reading. Native scale alone cannot distinguish percent from percentage points.
- TAT-QA `83b8b0ea-3cfe-4191-8acb-fecaced1f680` asks change between Q4 costs `10800` and `9241` RMB million. Signed change is `-1559`; the native answer `1559` is decrease magnitude, consistent with visible decrease prose. The unsigned reconciliation is new after unblinding and is not a new frozen answer.

Both AI reviewers overstated uniqueness by marking their primary numerical readings determinate in these cases. This is a technical-review limitation even when their chosen formulas are reasonable.

### Two false unit disputes are a post-lock implementation error

For `HWM/2018/page_96.pdf-1` and `GPN/2014/page_92.pdf-1`, reviewer A used monetary units containing “consideration”; reviewer B used “proceeds.” Both computed the same conditional USD-million exercise-price amount: `241.11` and `31.32382085` respectively.

The locked [`units.py`](../src/finance_document_review/units.py) checks unanchored `ratio` substrings before currency. `consideration` contains `ratio`, so A's units were wrongly classified as dimensionless proportion, while B's were monetary with multiplier `10^6`. The resulting disagreements were produced **after the reviews were locked**; they were not reviewer disputes or source faults.

A separate correction would change joint conditional agreements from 20 to 22 and disputed numeric/unit cases from 5 to 3. The original 62 determinate cases remain unchanged. If “64” is reported for corrected numeric agreement coverage, it means **62 original determinate plus 2 conditional agreements**, not 64 determinate or semantically certified questions. Any scoring sensitivity requires separate explicit versioning; none is performed here.

### Native channels and normalization must stay distinct

FinQA's pinned [number parser](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/code/evaluate/evaluate.py#L27) divides percent-marked operands by 100; ordinary division programs also yield fractional ratios. The [evaluator](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/code/evaluate/evaluate.py#L188) rounds numeric program outputs to five decimals and compares them with `exe_ans`. Thus textual `74.4%`, executable `.74371`, and an independently computed `74.37067... percent` are related representations, not automatically contradictory labels. A literal scalar adaptation and a declared-unit conversion are different evaluation policies; neither is the original program-accuracy task.

- `ABMD/2012/page_79.pdf-1`: native program/exe sum `1.6+2.7+2.2=6.5` USD million, while textual answer is `6.6`. This is an internal annotation-channel inconsistency. The inputs explicitly say approximately; the underlying unrounded rent total is not known, so `6.6` is not ruled out as an economic value.
- `DG/2007/page_67.pdf-2`: textual answer is empty while executable/program target is `10.2`. Do not treat this as a missing numeric executable target. Period scope includes predecessor 2007.
- `PPG/2018/page_85.pdf-1`: visible environmental reserves `291` exceed approximately `180` USD million asbestos reserves, so Boolean **yes**. Native text **no** contradicts that comparison. Native program `add(180,291)` and exe `471` compute an unrelated sum. Review B's positive margin `111` explains yes; it must not be scored as a monetary answer to the Boolean question. This contradiction is outside the 62 scalar cases.

TAT-QA's pinned [number conversion](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/tatqa_utils.py#L89) first rounds converted numbers to four decimal places. Its [answer normalization](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/tatqa_metric.py#L145) uses further two-decimal floating-point rounding and scale multiplication for ordinary numeric answers; [scale accuracy](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/tatqa_metric.py#L244) is recorded separately. This is not a universal economic precision requirement or arbitrary Decimal half-up policy. For `aee0871a-63d4-493e-985e-e2c40650c9de`, `20.7749609...%` can normalize through `20.775` to `20.77` using that floating-point route; the native `20.77` is not a new label-error discovery.

### Ambiguity, insufficient information and reviewer scope

- Literal requested information is absent in FinQA `DISCA/2011/page_49.pdf-3` (five years versus a September-2008-to-December-2011 graph), `UNP/2011/page_24.pdf-4` (2001 base year absent), and `UPS/2007/page_49.pdf-2` (2018 amount absent from a 2008-2012-plus-later schedule). Native shorter/wrong-year computations do not repair the literal question.
- FinQA `LMT/2014/page_91.pdf-2` asks employee contributions, but the visible amounts are company contributions. An employer-contribution reading yields the native mean; literal employee contributions are insufficiently specified.
- FinQA `ALXN/2016/page_153.pdf-1` has an ambiguous `$2014` token; dash/zero versus literal-number readings differ. The native and prose total corroborate one reading but do not replace an original-document formatting check.
- FinQA `AAL/2013/page_18.pdf-3` does not clearly specify the percentage baseline for a hedge effect. The reduction relative to `104` is `16.346...%`; native divides the `17` gap by `87`, giving `19.5402...%`. Do not assert a definite denominator error from this malformed wording alone.
- TAT-QA `99159896-6e6f-4479-afe6-b1d766a59b8b` has a table/anti-dilution-footnote conflict; the target matches the table mean but does not resolve the conflict or questionable thousand-share scale. `78eee0a5-7b9e-4370-9160-dd2890502705` never defines “deferred value.” `55f1de35-99c0-44a9-a96f-6706921539fe` has Kapuria salary `450000` in the table versus `440000` in prose, giving totals `3140000` versus `3130000`. These remain unresolved.
- Other target-compatible readings depend on the local note: unrecognized-tax liabilities rather than whole-company liabilities; deferred-compensation **tax assets** rather than compensation paid; performance-share **expense** rather than share count; gross listed fixed assets rather than all corporate assets. Three TAT cases lack monetary scale; native empty scale is compatible in reported units and does not authorize guessing a currency or multiplier.

### Consequence for claims

Report a selected, source-aware technical audit with preserved uncertainty. The strongest bounded statement is: **four numerical targets contradict explicit quantities in the visible FinQA questions, while three other disagreements reflect defensible conventions; native representation and post-lock comparison errors explain additional apparent failures.** Add the separately scoped Boolean and textual-channel findings only with their correct endpoints.

This supplement does not establish causal training damage, population prevalence, human expertise, first discovery, error independence between AI reviewers, or original production provenance. Post-unblinding interpretations are hypotheses for a separately versioned sensitivity or further adjudication, never retroactive primary truths. Published prior repairs and derivative-case overlap should narrow the novelty claim to the new locked-review/measurement evidence that is actually added.
