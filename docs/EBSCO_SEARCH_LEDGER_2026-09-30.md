## Executive summary (read this first)

The user's IU EBSCO Discovery session was used for seven targeted searches, not
only web search or arXiv. Journal and IEEE conference leads narrow broad financial
evaluation novelty claims. Primary verification and reading limits are recorded
in the linked reviews. Hit counts are discovery metadata, not papers read or quality.

Checked September 30, 2026, Europe/Berlin; the search occurred September 29 UTC.
The existing Google Chrome institutional session was used. No account, saved
project, publisher agreement or sharing action was changed. Licensed full text,
article PDFs, author emails and browser session tokens are excluded from the bundle.

## Search settings and coverage

Peer-Reviewed was on; Available in Library Collection and Fulltext limiters were
off. All dates were eligible, relevance ordering was used, and AI search was off.
Q1 initially included full-text and subject-concept expansion. These expanders
were removed for Q2 onward. Returning from an article detail page reset expansion
for the first Q5 attempt (2,011 hits); it was removed before the 226-hit Q5 screening
reported below. These changes matter for reproducibility.

| Query | Exact entered text | Reported hits | Records screened |
|---|---|---:|---:|
| Q1 | `("label noise" OR "annotation errors") AND (benchmark* OR "model evaluation")` | 10,747 | First 10 |
| Q2 | `"reward hacking" OR "reward misspecification"` | 121 | First 10 |
| Q3 | `(financ* OR numerical) AND ("question answering" OR benchmark*) AND (validity OR verification OR "data quality")` | 6,881 | First 10 |
| Q4 | `"financial question answering" OR FinQA OR "TAT-QA"` | 91 | First 10 |
| Q5 | `"Confident Learning" OR "Pervasive Label Errors" OR "Classification in the Presence of Label Noise"` | 226 | First 10 |
| Q6 | `TI ("Confident Learning" OR "Pervasive Label Errors" OR "Classification in the Presence of Label Noise")` | 79 | First 10 |
| Q7 | `TI "Classification in the Presence of Label Noise"` | 9 before deduplication | All 3 displayed unique records |

`TI` restricts the phrase to titles. Q7's header reported nine results, but its
footer reported three unique records and displayed three. Screened records overlap
across queries; do not sum them as unique papers. There was no exhaustive pagination,
formal recall assessment, date-restricted systematic review or duplicate screening.
A peer-review filter can miss useful records or proceedings; original conference
and journal sources were also checked outside EBSCO. Absence from the first page
is not absence from the literature. Counts may change as the index updates.

The metadata-only machine-readable log is
`outputs/literature-search-20260930/ebsco_query_metadata.json`.
It contains exact queries and settings, not copied abstracts or institutional
session URLs. Primary DOI/proceedings links are used for citations.

## Leads actually followed

| Lead | EBSCO evidence and subsequent verification | Relevance |
|---|---|---|
| Measurement Risk in LLM-Based Financial NLP, IEEE CIFEr 2026 | Q3 record; IEEE-deposited DOI metadata and author preprint checked. Final/preprint title difference retained. | Financial rubric/metric/ranking sensitivity and pinned-artifact metadata drift already exist. |
| RewardHackingAgents, IEEE ICDEW 2026 | Q2 record; IEEE-deposited DOI metadata and selected author-preprint sections checked. | Reported versus protected-reference evaluation integrity is established. |
| Backtest Lie Detector, IEEE CIFEr 2026 | Q3 detail `edseee.11692419`, DOI and author abstract read in Chrome; full IEEE text unread. | Its abstract describes 141 point-in-time workflow cases and false-valid/false-invalid tradeoffs. Broad financial-auditor novelty is untenable. |
| Quality Control for Crowd Workers and for Language Models, Information Systems Research 2026 issue | Q3 detail; DOI/all five authors verified; EBSCO HTML full text available. Selected publisher sections reviewed separately. First online September 2025. | Aggregated free-text evaluation without observed gold is established; correlated errors remain a limitation. |
| Frénay and Verleysen's label-noise survey, IEEE TNNLS 2014 | Q7 detail `edseee.6685834`, journal/pages/DOI and author abstract verified. Author manuscript inspected separately. | Feature-dependent noise and insufficient labeling information are historical context, not our new contribution. |

Q4 also surfaced program-assisted small-model financial QA. The review therefore
checked original Program-of-Thoughts and PAL publications, rather than citing a
recent derivative as the origin of program-assisted reasoning.

Broad medical/vision noise papers, speaker-verification papers, generic RAG
architectures and surveys without a direct mechanism link were screened out of
the current manuscript. A later issue date is not proof of availability today;
unverified future-dated items were not adopted. Bibliography size and venue names
do not substitute for reading relevant methods and limitations.

## How this changes the submission

See [EBSCO discovery triage](EBSCO_DISCOVERY_TRIAGE_2026-09-30.md) for exact identities,
access levels and collisions, and [extended primary-source review](EXTENDED_LITERATURE_REVIEW_2026-09-30.md)
for twelve additional candidates, including original FinQA/TAT-QA and PoT/PAL.
These are overlapping research sets, not sixteen EBSCO full texts.

The present contribution is bounded source-traced evidence about released numeric
and preference supervision. Label audits, ranking sensitivity, financial auditing,
program execution and independent checks are established ideas. A main-track
extension must add a falsifiable predictive or consequential result on independently
adjudicated, held-out sources/tasks. These discoveries do not establish defects in
the blank 96-case document packets or rescue the inconclusive GEPA pilot.
