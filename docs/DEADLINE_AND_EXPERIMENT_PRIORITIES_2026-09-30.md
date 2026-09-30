## Executive summary (read this first)

**The workshop paper deadline is October 1 at 13:59 Berlin time.** It is dated
September 30 in Anywhere on Earth time. At verification, roughly 29.5 hours remain.
The highest-value additional model run is one representation-matched comparison
after a native-tokenizer preflight. The highest-value saved-output ablation tests
whether the reported numerical discrepancies survive stricter quantity/unit
attribution. More model families alone do not resolve novelty or semantic validity.

Live verification: **2026-09-30 06:24 UTC / 08:24 Europe/Berlin**, with the
conversion independently calculated using Python datetime and zoneinfo.
This is an internal assessment, not actual organizer/professor feedback, an
acceptance prediction or a claim that an experiment has been run. No login,
submission, contact, inference, expenditure or frozen-artifact edit occurred.

### Venue requirements: verified versus unavailable

| Item | Live primary-source finding |
|---|---|
| Deadline | September 30, 2026, 23:59 AoE; the form closes then. |
| Local conversion | October 1, 11:59 UTC / 13:59 CEST, Europe/Berlin. AoE is UTC−12; Berlin is UTC+2 on that date. |
| Format / pages | One PDF; full or short paper; any format and length. No page cap is stated. |
| Anonymity | No anonymity requirement is stated in the inspected public CFP. Form-specific requirements are unverified. |
| Archival status | Non-archival; already published or simultaneously reviewed work is welcome. |
| Attendance | At least one author presents in person in Atlanta on December 12, 2026. |
| Submission | Google-account sign-in for PDF upload and presenting author's NeurIPS-account email. |
| Competition entry | Optional for paper submission. |
| Decisions | October 2, 23:59 AoE. |
| Review criteria | No detailed public rubric or acceptance rate was found. |

Source: [current official CFP](https://www.agenthon.net/#call-for-papers).
Its paper deadline is distinct from the competition's October 12 deadline.
The [official rules](https://www.agenthon.net/rules/) identify AoE as UTC−12
and make registration, admission and venue requirements the attendee's
responsibility; acceptance does not itself establish travel or badge eligibility.

The CFP's [submission link](https://forms.gle/oBs6nVyvyZG2Ky2P7) redirects to
[this Google form](https://docs.google.com/forms/d/e/1FAIpQLSfSCLrUNQ4zewF9JJjTpaVnyjd8YXnONzQ9iQQCw-H7kMcNJQ/viewform?usp=send_form).
The read-only fetch could not access its contents. The link is verified from the
official site; upload limits, additional form fields and current upload acceptance
were not independently checked. No claim about anonymity beyond the public CFP
is justified. Presenter availability and account details remain user-specific.

### Main scientific risk

The defensible contribution is a pinned empirical supervision/answer-contract
audit with transparent negative attempts and fixed-answer grading evidence.
Its largest scientific risk is that familiar annotation repairs, representation
choices and broad-unit proxies are mistaken for a new general verification
mechanism or financial correctness. Extra architectures do not fix that problem.

The current document extension explicitly distinguishes 96 selected questions,
62 locked numerical readings, 384 attempted model events and AI-assisted technical
review. Two of the corroborated FinQA numerical repairs already appear in
FinanceReasoning; exact source lineage and disputed interpretations remain
important. [Final independent validation](FINANCE_DOCUMENT_FINAL_INDEPENDENT_VALIDATION_V1.md),
[derivative overlap](FINANCE_DOCUMENT_DERIVATIVE_OVERLAP_REVIEW_2026-09-30.md).
These selected cases do not support population prevalence or independent-report
claims. Public benchmark pretraining exposure remains unknown.

### Priority 1: representation-matched local comparison

Use one cached checkpoint, preferably a genuinely different available instruction
model family. The parent task owns runtime/model feasibility. Before opening
evaluation outputs, freeze its exact model/tokenizer revisions, files, dtype or
quantization, backend, context/output limits, decoding and stopping conditions.
Run a source-free authored format preflight and stop on failure; do not rescue
selected-case outputs with retries or choose prompts using their success.

First verify the tokenizer produces identical IDs through native chat-template
tokenization and rendered-template tokenization with additional special tokens
disabled. Check assistant generation boundaries, EOS handling, thinking settings,
truncation and intact financial text. Preserve prompt bytes and token-ID hashes.
[Transformers' official guidance](https://huggingface.co/docs/transformers/main/en/chat_templating)
explains model-specific role tokens and warns that re-tokenizing rendered chats
with extra special tokens can duplicate them. The old local runner renders a
template then tokenizes without explicitly disabling special tokens; this is a
reason to check actual IDs, **not proof of an observed tokenizer defect**.

Then run baseline versus a label-free quantity reminder with the **same output
fields and executable-calculation grammar in both arms**. Keep assumption prose
outside calculation if a separate, identically specified field is introduced;
that requires its own schema/parser freeze. Keep field/unit/scale rules identical.
Retain all failures and the separate Boolean/abstention channels. Do not modify
the previous protocol or recast this run as a correction of its results.

Prefer all 96 current questions (192 new attempts for one checkpoint). If local
throughput requires a smaller panel, predeclare a metadata-only salted-hash subset,
balanced by source, before answers; report its reduced scope. Current cases are
already observed discovery cases, not an unseen semantic-transfer benchmark.
Match/interleave conditions and preserve each model's native tokenizer rather
than forcing identical token IDs across unrelated models.

Primary endpoints: strict response availability and paired locked value/broad-unit
matches, with identical failure denominators and explicit native/adapted score
channels. Separate changed numerical values, unit strings, transport and schema
effects. Executable coverage is secondary. A formatting gain alone is a formatting
result. A null or negative result still tests the measurement explanation.

This directly addresses the original reminder's conflict: its instruction allows
assumption prose in calculation while the baseline requests a numeric expression.
The saved 72→39 DeepSeek and 56→12 Qwen executable counts cannot establish worse
arithmetic. Qwen's zero strict numeric responses also cannot establish zero latent
financial ability. [Diagnostic independent validation](FINANCE_DOCUMENT_DIAGNOSTIC_INDEPENDENT_VALIDATION_V1.md).

### Priority 2: saved-output attribution falsification

Audit **all 131** supported-expression/locked-reference attempts, including
passing and failing transitions, rather than inspecting only the 47 apparent
reported-mismatch→executed-match transitions. No new inference is required.
Use original question/context and saved operand provenance to distinguish the
requested quantity and compatible units from numerical proximity. Explicitly
test duration versus count, per-share versus total and rate difference versus
relative change where those distinctions are actually supported by context.

Freeze a new posthoc attribution rubric and preserve original scores. Record
precision-only disagreement, unchanged correct quantity, wrong/unsupported
quantity, incompatible units and unresolved interpretation separately. No unit,
operand or answer may be guessed to make an output pass. Technical author/AI
inspection is not independent human financial-expert adjudication.

Decisive endpoint: how many of the 47 transitions remain supported after this
stricter attribution, with reasons and passing controls. If many disappear, narrow
the current conclusion to numeric/representation consistency. If supported
quantities remain, show faithful native scoring and both acceptance directions
on the unchanged outputs; do not call every rounding-cell credit a false financial
acceptance or an official evaluator bug. FinQA's scalar adaptation is still not
full native program equivalence. Keep source-label validity separate.

This ablation attacks the most consequential remaining interpretation weakness.
It is post-unblinding diagnostic evidence, not a new benchmark or first correction
claim. Native identity/precision controls already exist; do not duplicate them
without a specific unresolved condition. [Comparison protocol](FINANCE_DOCUMENT_COMPARISON_PROTOCOL_V1.md),
[closest-work review](MAIN_TRACK_DOCUMENT_EXTENSION_REVIEW_2026-09-30.md).

### What to finish before adding more families

Secure a compiled, checked, upload-ready PDF and concrete attendance/account
readiness first. Keep enough deadline buffer for packaging and upload failure.
Do not replace an eligible empirical audit with an unfinished expanded-method
claim. Tokenizer correctness is instrumentation; more checkpoints establish
bounded robustness only. A same-family size sweep does not resolve independent
source breadth, benchmark leakage, semantic expertise or novelty.

No experiment count yields acceptance certainty. The public CFP supplies topic
fit and eligibility, not evidence of a particular review outcome. Prioritize the
two measurement questions above and retain their failures rather than searching
across configurations until a positive result appears.
