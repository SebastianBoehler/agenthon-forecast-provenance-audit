## Executive summary (read this first)

A bounded **16 FinQA +16 TAT-QA** unused-group test is feasible from the pinned
original public-test releases. The local 32 cases are entirely inside the earlier
96: exclude their union of **96**, then exclude whole discovery groups and exact
question/context hashes. FinQA has **549 remaining rows in 141 reports and 64
previously unused company prefixes**. TAT-QA has **592 eligible rows in 223 unused
native contexts**. Its report/company identities are unavailable; do not claim
company-disjoint or report-disjoint transfer for that source.

This is a metadata census and independent cohort check, conducted September 30,
2026, 08:55–09:14 UTC. This review created no membership, answer reference, model
output or defect label. The separately prepared 32-case cohort passed the check
below. This note is not a prospective experiment freeze or a new benchmark.
It implements the independent background check requested for the
[submission iteration](AGENTHON_SUBMISSION_ITERATION_2026-09-30.md).

For example, excluding one discovery FinQA question excludes every question with
its company/year report key. The stronger recommended holdout excludes every
remaining year under its company prefix. A TAT-QA table UID supports only the
corresponding context exclusion, because its original report cannot be identified.

## Exact inputs and the available identities

Reuse the [V1a configuration](../experiments/finance_document_audit_sources_v1.json)
and [frozen admission/selection code](../scripts/finance_document_audit/sampling.py).
The [identity join](../scripts/finance_document_audit/joins.py) uses exact original
question, table cells and ordered paragraphs. No fuzzy or answer-based join is used.

| Source | Pinned revision | Metadata actually available |
|---|---|---|
| [FinQA repository](https://github.com/czyssrs/FinQA/tree/0f16e2867befa6840783e58be38c9efb9229d742) | `0f16e2867befa6840783e58be38c9efb9229d742` | `id`, `filename`, original question/table/pre-text/post-text. IDs parse as company-prefix/year/page-PDF/example. Group reports by exact prefix/year. |
| [TAT-QA repository](https://github.com/NExTplusplus/TAT-QA/tree/870accc41953dcde885aabeb963d94aabdc0fbc3) | `870accc41953dcde885aabeb963d94aabdc0fbc3` | Raw table UID/cells, paragraph UID/order/text, question UID/order/text. No report URL, filename, company or report-year field. |

FinQA's [pinned README](https://raw.githubusercontent.com/czyssrs/FinQA/0f16e2867befa6840783e58be38c9efb9229d742/README.md)
describes native IDs; its [paper §4.4](https://aclanthology.org/2021.emnlp-main.300.pdf)
states that original train/dev/test input reports do not overlap. Our new subset
is still public test, and that statement does not establish company disjointness
within it. A company prefix is an exact dataset identifier, not a verified legal
entity: ticker changes, aliases, acquisitions and parent/subsidiary relations
remain unresolved. There are 100 prefixes in the admitted test pool, 36 in the
discovery selection, and 64 absent from it. Do not silently merge guessed aliases.

TAT-QA's [paper §2.3](https://aclanthology.org/2021.acl-long.254.pdf) describes
2,757 contexts from 182 reports and a random split **by context**. It does not
guarantee report-disjoint splits. The pinned raw-test schema confirms absent
report/company fields. Paragraph text may mention a company, but mention extraction
cannot supply a reliable native report identity. No such inference was attempted.

FinQA canonical input remains `dataset/test.json`, not the evaluator's separate
test representation. TAT-QA V1a has 1,626 exact raw/gold question-context joins:
raw/gold UIDs themselves do not match. The 43 unmatched raw questions remain
excluded. Native `arithmetic`/`count` eligibility is inherited from the frozen
metadata, not recalculated from targets. No new gold annotation values were read.
See the [original protocol](FINANCE_DOCUMENT_AUDIT_PROTOCOL_V1.md).

## Independently reconstructed census

The new [metadata-only census](../outputs/finance-unused-group-design-v1/census.py)
checks all eight original acquisition hashes, all seven derivative acquisition
hashes and the three cohort/pool hashes. It reconstructs source group IDs and
original question/context hashes for all **1,870 admitted rows** from permitted
input fields. It does not access answer, program, derivation or correctness fields.
The TAT-QA gold file is hashed as bytes only; answer types come from admitted metadata.

| Census boundary | FinQA rows / groups | TAT-QA rows / groups |
|---|---:|---:|
| Frozen admitted pool | 1,147 /278 reports | 723 /271 contexts |
| Earlier discovery selection | 48 /48 reports | 48 /48 contexts |
| Exclude only selected question IDs | 1,099 | 675 |
| Exclude selected groups and all old exact input hashes | 911 /230 reports | 592 /223 contexts |
| Also exclude all discovery company prefixes | 549 /141 reports /64 prefixes | Unknown; no company key |

The local 32 contribute **16+16 previously used IDs and zero additional IDs/groups**.
All old contexts/questions are nevertheless excluded explicitly. The unused FinQA
pool has 308 page contexts and 902 distinct question-context hashes; the stronger
prefix pool has 189 page contexts and 546 distinct question-context hashes.
TAT-QA's remaining types are 557 arithmetic and 35 count. There are zero exact
cross-source context-hash matches; this cannot prove report or semantic independence.

Sorted remaining-metadata hashes, canonical UTF-8 JSON with sorted keys and compact
separators: FinQA `beacbd2ab9c6b449c6cfa10f8539073ef09fb69242bc05f081be0ee3e3386b6e`;
TAT-QA `34b669dd39f512e60b315dda8938fe662a75c7999b9d783621eaa49d5c901ef6`.

## Derivative overlap: disclosure, not novelty-based selection

[BizBench §3.1/Appendix A](https://aclanthology.org/2024.acl-long.452.pdf) derives
CodeFinQA and CodeTAT-QA from these sources. [FinanceReasoning §2.1/Table 1](https://aclanthology.org/2025.acl-long.766.pdf)
already corrects/disambiguates derivative test questions. Both are downstream
lineages, not additional independent source producers. The existing
[overlap review](FINANCE_DOCUMENT_DERIVATIVE_OVERLAP_REVIEW_2026-09-30.md) documents
37 discovery FinQA wording joins and two already published specific repairs.

Reuse BizBench revision `0a793f2f886156902c72b4a22cab82bb9dceaecf` and FinanceReasoning
revision `b0fe6455396f831955e4eb988472b4a563403bc5`, with all hashes in the local
acquisition manifest. The census reads only BizBench task/question/context columns
and FinanceReasoning source/question-ID/context. Every released derivative test
position is linked: 795 CodeFinQA and 288 CodeTAT-QA; contexts are byte-identical
between the two derivative releases for 795/795 and 284/288 respectively.

| Unused candidate pool | Wording match | Wording plus ordered native paragraphs | Any ordered paragraphs |
|---|---:|---:|---:|
| FinQA 911 rows /230 reports | 631 rows | 630 rows /214 reports | 862 rows /214 reports |
| Stronger FinQA 549 rows /141 reports | 376 rows | 375 rows /130 reports | 518 rows /130 reports |
| TAT-QA 592 rows /223 contexts | 21 rows /19 contexts | Unresolved | Unresolved |

Wording comparison changes only case/whitespace. FinQA paragraph matching requires
all nonempty native paragraphs in order, but does not certify transformed-table
equivalence. Of the 631 FinQA wording matches, 630 have a test match and one a
train match. TAT-QA has two test-matched and 21 train-matched rows; categories
overlap. Generic wording and transformed tables prevent a verified TAT-QA identity
join. Its unmatched wording rows are **unknown**, not established derivative-free.

Only 16/230 unused FinQA reports have no recognized derivative paragraph match;
the stronger prefix pool has 11/141. These are absence-of-match counts, not verified
novel reports. Keep derivative flags as metadata strata, with all candidate groups
eligible regardless of those flags. Do not use original/repaired answers to decide
membership, or interpret occurrence as human endorsement or model contamination.

## Actual frozen selection design: 16+16

The [cohort protocol](FINANCE_QUANTITY_TRANSFER_COHORT_PROTOCOL_V1.md) and
[preparation script](../scripts/prepare_finance_quantity_transfer.py) use salt
**`finance-quantity-transfer-v1-20260930`** and preserve every original question.
Membership froze before reference work. Develop the tested procedure only on
existing discovery material. The actual selector orders **questions**, then caps
groups; it does not sample groups uniformly. Larger groups have more chances to
appear early in the hash order. This differs from the group-first recommendation
in this note's working draft; the code and freeze were not altered to adopt it.

```python
salt = "finance-quantity-transfer-v1-20260930"
old_ids = {(r["source"], r["native_id"]) for r in earlier_96}
old_ids |= {(r["source"], r["case_id"].split(":", 1)[1]) for r in local_32}
old_groups = {(r["source"], r["group_id"]) for r in earlier_96}
old_prefixes = {r["native_report_id"].split("/")[0]
                for r in earlier_96 if r["source"] == "finqa"}
contexts = {r["context_sha256"] for r in earlier_96}
questions = {r["question_sha256"] for r in earlier_96}
# H(x) = SHA256(canonical UTF-8 JSON(x)), as in the existing common.py.
for source in ["finqa", "tatqa"]:
    candidates = []
    for r in admitted_metadata:
        if r["source"] != source or (source, r["native_id"]) in old_ids:
            continue
        if (source, r["group_id"]) in old_groups:
            continue
        if r["context_sha256"] in contexts or r["question_sha256"] in questions:
            continue
        group = r["native_report_id"].split("/")[0] if source == "finqa" else r["group_id"]
        if source == "finqa" and group in old_prefixes:
            continue
        candidates.append(r)
    chosen, groups = [], set()
    rows = sorted(candidates, key=lambda r:
        (H([salt, source, r["native_id"], r["question_sha256"]]), r["native_id"]))
    for r in rows:
        group = r["native_report_id"].split("/")[0] if source == "finqa" else r["group_id"]
        if group in groups or r["context_sha256"] in contexts or r["question_sha256"] in questions:
            continue
        chosen.append(r)
        groups.add(group)
        contexts.add(r["context_sha256"])
        questions.add(r["question_sha256"])
        if len(chosen) == 16:
            break
    # Record actual count/shortfall; never replace after answers or reference review.
```

This pseudocode describes the frozen selector; a separate implementation reproduced
its full ordered metadata exactly. The 64 prefix groups and 223 context groups
supplied 16+16 without shortfall. Source order and deduplication are explicit.
FinQA admits all source question types, including possible yes/no questions; no
gold-program/answer filter was used. Difficulty, faults, model-success predictions
and answer values do not determine membership. Report a fixed selected-cohort
transfer result, not a uniform-company sample or population prevalence estimate.

After the membership freeze, build original-question/context-only technical review
sheets; keep release answers/programs and derivative repairs hidden from that stage.
AI references remain technical candidates. Obtain qualified human adjudication for
disputed semantic targets before claiming validated quantity-aware audit performance.
Keep unresolved cases and coverage in the denominator. Existing native metrics,
strict format checks, execution and simple tolerance are separate controls; none
alone establishes entity/year/denominator correctness. A null result remains useful
falsification of the proposed procedure, rather than grounds to select another cohort.

## Independent validation of the prepared 32 cases

The cohort freeze is timestamped **2026-09-30 09:07:35 UTC**, SHA256
`bb7b7aa95c6f57ff394b870b36ed5e2e2d2b056a627cd29ef4b6193bcb95696a`.
At **09:13:47 UTC**, the new [independent validator](../outputs/finance-unused-group-design-v1/validate_cohort.py)
passed **105 checks** without importing the preparation script or any reference
calculator. It verified nine frozen files, eight original acquisition hashes,
all old exclusion sets, 549/592 eligible counts, exact salted order, 16 distinct
new FinQA prefixes, 16 distinct TAT-QA contexts, and every original packet field
and question/context hash. All 32 context and question/context hashes are distinct.
Packets contain only case ID, source, original question and original context.

The [validation receipt](../outputs/finance-quantity-transfer-v1/cohort_validation.json)
also records derivative metadata: **14/16 FinQA** questions have wording plus
ordered-paragraph matches; **1/16 TAT-QA** has a wording-only match, with table
identity unresolved. No derivative target or program was used. These flags are
reported separately and must not be forwarded as defect hints to blind reviewers.

Validator SHA256: `6bb5ac35b018dadaf5d3b325573343db916afdde90eab2a872b33e3c182cd1e8`.
Receipt SHA256: `0b207aacc45305bb52cc10eb41c38b3fa5b49181d27bca86fe026e5beef75327`.
The validation confirms membership, provenance and representation, not financial
reference correctness or expert judgment. No new reference answers were inspected.

## Reproduction and scope receipt

Run `.venv/bin/python outputs/finance-unused-group-design-v1/census.py` from the
audit repository. The [aggregate receipt](../outputs/finance-unused-group-design-v1/census.json)
contains no selected IDs, questions, answer values or programs. It requires the
previously staged, pinned original/derivative files and existing PyArrow runtime;
it is not a corpus-free artifact replay. Missing files/dependency or hash mismatch
fails explicitly. Full corpora remain ignored and retain their unresolved source
notices; this review does not grant redistribution permission.

Census script SHA256: `c38f04f7f10fe9e3cc9c40fd9eb57d29c4b3f25fb7eca125cddc2ce88f25fb5c`.
Aggregate receipt SHA256: `f2a3a055015cf16eb5654ef7ec06e689d3795b02829d0ff28adf82fd3cff4634`.
These bind a metadata review, not financial correctness, expert truth, population
defect prevalence or train-corpus independence. No source targets/reviewer results
were opened, no models called, and no prior protocol, result or manuscript edited.
