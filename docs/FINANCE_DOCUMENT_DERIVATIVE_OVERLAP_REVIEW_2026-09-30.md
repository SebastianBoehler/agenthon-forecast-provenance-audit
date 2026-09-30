## Executive summary (read this first)

37/48 selected FinQA cases have unique matching question wording in released
BizBench CodeFinQA test data and linked FinanceReasoning examples. All 48 have
their native paragraph sequences in CodeFinQA test text contexts. These are
content joins, not direct native-ID joins: BizBench does not retain those IDs.
Two specifically inspected candidate corrections, PPG 2012 and ETFC 2011, are
already present in FinanceReasoning. They must not be described as new discoveries.

No TAT-QA case identity was verified. None of the 48 selected questions matches
released CodeTAT-QA test wording; one generic wording matches two train rows and
remains unresolved. Neither a no-match nor a context-only match establishes
novelty, report disjointness, correction status or model-training contamination.

### Primary provenance and pinned availability

[BizBench, ACL 2024](https://aclanthology.org/2024.acl-long.452.pdf), §3.1 and
Appendix A, derives CodeFinQA from FinQA and CodeTAT-QA from table-answerable
TAT-QA questions. It changes program/context representations and filters examples.
Its paper counts differ from the currently released files; this check uses the
pinned actual release, not paper counts. [The publisher's dataset card](https://huggingface.co/datasets/kensho/bizbench/blob/0a793f2f886156902c72b4a22cab82bb9dceaecf/README.md)
links the public data and a separate curated leaderboard. The latter was not accessed.

[FinanceReasoning, ACL 2025](https://aclanthology.org/2025.acl-long.766.pdf), §2.1,
Table 1 and Appendix C, reviews CodeFinQA/CodeTAT-QA and distinguishes corrections,
disambiguations and program elaborations. The release retains a `source` field
such as `CodeFinQA-test-742`; its own `question_id` is independently renumbered.
It releases no per-case update-action flag. [Official repository](https://github.com/BUPT-Reasoning-Lab/FinanceReasoning/tree/b0fe6455396f831955e4eb988472b4a563403bc5).

- FinanceReasoning Git revision: `b0fe6455396f831955e4eb988472b4a563403bc5`.
  Public easy/medium/hard JSON files contain 1,000/1,000/238 examples.
- BizBench dataset revision: `0a793f2f886156902c72b4a22cab82bb9dceaecf`.
  Actual CodeFinQA counts are train 4,668/test 795; CodeTAT-QA train 2,856/test 288.
- FinanceReasoning `source` positions cover all 795/288 released derivative test
  positions exactly once. Its contexts equal BizBench contexts byte-for-byte for
  795/795 CodeFinQA and 284/288 CodeTAT-QA examples. Four TAT contexts differ;
  they are not treated as exact context matches.
- Native inputs remain the audit's pinned FinQA `0f16e2867befa6840783e58be38c9efb9229d742`
  and TAT-QA `870accc41953dcde885aabeb963d94aabdc0fbc3` public test releases.

### Join procedure and exact matched identifiers

`outputs/finance-document-derivative-overlap-v1/check_overlap.py` verifies all
seven downloaded-file hashes and reconstructs the frozen question/context hashes
for all 96 selected IDs. It projects question/text/table fields from native inputs,
not answer annotations. BizBench metadata comparison reads only task, question,
context. Question comparison changes only case and whitespace; FinQA context
comparison requires every native paragraph in order. Complete transformed-table
equivalence is not established by paragraph overlap.

The following 37 unique FinQA wording joins also share ordered native paragraphs.
Positions are zero-based after filtering the pinned BizBench test rows to CodeFinQA.
FinanceReasoning `source` is `CodeFinQA-test-` followed by that position.

| Selected native FinQA ID | BizBench position | FinanceReasoning question_id |
|---|---:|---|
| HWM/2018/page_96.pdf-1 | 699 | test-403 |
| CB/2008/page_229.pdf-1 | 591 | test-1540 |
| JPM/2010/page_281.pdf-2 | 372 | test-662 |
| V/2014/page_126.pdf-1 | 54 | test-282 |
| GPN/2014/page_92.pdf-1 | 241 | test-623 |
| ABMD/2006/page_43.pdf-2 | 652 | test-394 |
| DVN/2015/page_79.pdf-2 | 585 | test-1539 |
| PM/2017/page_32.pdf-1 | 177 | test-849 |
| STT/2011/page_69.pdf-4 | 594 | test-718 |
| SNA/2013/page_34.pdf-1 | 553 | test-369 |
| UPS/2010/page_52.pdf-4 | 384 | test-1351 |
| FIS/2017/page_64.pdf-4 | 45 | test-281 |
| HOLX/2009/page_127.pdf-1 | 59 | test-201 |
| MRO/2017/page_96.pdf-4 | 536 | test-937 |
| AAL/2014/page_15.pdf-1 | 503 | test-696 |
| JPM/2003/page_106.pdf-3 | 458 | test-349 |
| TMUS/2017/page_29.pdf-4 | 439 | test-346 |
| BKNG/2016/page_33.pdf-3 | 704 | test-1939 |
| DISCA/2011/page_49.pdf-3 | 35 | test-1299 |
| GS/2013/page_72.pdf-1 | 734 | test-77 |
| ALXN/2016/page_153.pdf-1 | 487 | test-1536 |
| PKG/2005/page_74.pdf-4 | 550 | test-232 |
| LMT/2014/page_91.pdf-2 | 184 | test-850 |
| AMT/2008/page_94.pdf-2 | 393 | test-43 |
| MSI/2014/page_76.pdf-2 | 491 | test-1725 |
| UA/2007/page_70.pdf-1 | 296 | test-640 |
| CMCSA/2015/page_67.pdf-3 | 688 | test-744 |
| AWK/2017/page_148.pdf-2 | 110 | test-1314 |
| AWK/2012/page_117.pdf-4 | 8 | test-593 |
| UA/2011/page_69.pdf-1 | 341 | test-855 |
| PPG/2012/page_29.pdf-4 | 742 | test-408 |
| UAA/2016/page_42.pdf-2 | 222 | test-931 |
| NWS/2019/page_116.pdf-2 | 455 | test-228 |
| ETFC/2011/page_144.pdf-2 | 243 | test-306 |
| GS/2014/page_165.pdf-2 | 336 | test-220 |
| AAL/2013/page_18.pdf-3 | 77 | test-1638 |
| UPS/2007/page_49.pdf-2 | 100 | test-1622 |

The remaining 11 FinQA cases have text-context overlap only. Their IDs and all
neighbor positions are retained in `overlap_receipt.json`; none has a released
CodeFinQA train wording match. For TAT-QA, raw UID
`f96d1e32-3e9a-44dd-baf4-57de98ad9d11` matches generic wording at CodeTAT-QA
train positions 1084/1791. The different table representations and missing native
IDs leave that join unresolved. TAT report-level overlap is also unresolved.

### Separately authorized post-unblinding corroboration

After the metadata check, the parent explicitly authorized derivative answer and
program inspection for six named source-audit candidates. Nine context-neighbor
derivative rows were inspected. This is later corroboration, not blinded review;
the original review sheets, frozen sampling and native metric adapter were not changed.

| Native case / parent-supplied candidate | Matching derivative evidence | Verdict |
|---|---|---|
| PPG/2012/page_29.pdf-4; shifted years | BizBench 742 → FR test-408. Same base question; FR adds integer precision. BizBench `answer=22`, program `56−34`; FR `ground_truth=66`, program `122−56=66`. FR/BizBench contexts are identical. | The specific correction already exists in FinanceReasoning. |
| ETFC/2011/page_144.pdf-2; wrong collateral quantity | BizBench 243 → FR test-306. Same base question; FR adds three-decimal precision. BizBench `answer≈4.6`, program `2.3/0.5`; FR `ground_truth=38.6`, program `19.3/0.5=38.6`. Contexts are identical. | The specific correction already exists in FinanceReasoning. |
| JPM/2018/page_90.pdf-6; denominator 46,780 versus total 51,410 | Same-text neighbors 17 → FR test-507 and 159 → test-512 ask yield changes, with results 11/14 basis points. Neither asks the selected CIB share question. Parent supplies candidate `4630/51410`, versus `4630/46780`. | No matched correction/program for this selected question was verified. |
| SLG/2011/page_91.pdf-6; change versus level ratio | Neighbor 338 → FR test-35 asks capitalized compensation, `3.4+2.2=5.6`, not balance change. Parent supplies change 6.7502% versus level ratio 0.93677. | Context-only; candidate mathematics not corroborated here. |
| PPG/2018/page_85.pdf-1; boolean comparison | Neighbors 535/647/650 → FR test-1726/test-731/test-732 ask reserve percentages. None asks whether environmental reserves exceed asbestos reserves. Parent supplies `291>180`, versus text `no`/execution 471. | No matching boolean derivative annotation verified. |
| ABMD/2012/page_79.pdf-1; rent sum / annotation mismatch | Neighbor 648 → FR test-865 asks a facility base-rent percentage increase, `((64350−40000)/40000)×100=60.875`, not total rent expense. Parent supplies text 6.6 versus execution 6.5. | Different-question neighbor; selected mismatch not corroborated here. |

Only the first two mathematical corrections are corroborated by matching released
programs in the [pinned easy.json release](https://github.com/BUPT-Reasoning-Lab/FinanceReasoning/blob/b0fe6455396f831955e4eb988472b4a563403bc5/data/FinanceReasoning/easy.json).
Neighbor presence does not validate the other four audit conclusions.
These six were supplied because of candidate faults; they are not a random
subsample for estimating the fraction of previously known corrections. Public
annotations do not establish individual annotator identity or expert endorsement.

### Reproduction, hashes and inference boundary

Run `.venv/bin/python outputs/finance-document-derivative-overlap-v1/check_overlap.py`
against the pinned locally retained files. It performs no program execution,
grading, inference or network call. `overlap_receipt.json` binds script, selection
metadata and acquisition-manifest hashes and records all 96 joins and nine later
candidates. Raw derivative JSON/parquet/README files remain under ignored `outputs/`;
no redistribution or Git action was performed. No reviewer packet or
`source_targets.jsonl` was opened for this check.

| Pinned downloaded file | SHA256 |
|---|---|
| FinanceReasoning easy.json | `53890ee130f33759cf53cc71943248671e27e6035e75e4234373587784e56dd9` |
| FinanceReasoning medium.json | `98098f9b54c0a8c6192b3f3f8b7afe514b0fef2b0972ff0fe63ff43202c20e22` |
| FinanceReasoning hard.json | `ca8c055ef104176131da2e0f533897350cde3b93c4754575b09c7c7fbd046d9f` |
| FinanceReasoning README.md | `e28710c714bc056cce8bf6291e1b730a73f18a11eec6c7d0da2da0e6797e565c` |
| BizBench released test parquet | `a3b5bec29e12df3e58869526a19e96701541c5831b62dab9f9d7e37ab75f397c` |
| BizBench released train parquet | `d0af1868ac46b082f153981b813b97b78707153b7a5cd872b30490bec47b3cc1` |
| BizBench README.md | `5afcdfea0c404ed81a08fda8bf870ae6d997482c5abcac080639b3e84a4f76bb` |

The contribution can concern blinded reconstruction and separation of native
annotation, representation and scoring layers. Additional defects in familiar
sources, especially these two already repaired cases, do not establish firstness.
Do not treat BizBench and FinanceReasoning as extra independent source producers.
