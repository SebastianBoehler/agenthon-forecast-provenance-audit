## Executive summary (read this first)

The positive artifact contribution is a concrete, replayable record of this financial
supervision audit: pinned inputs, independently checked calculations, saved model
answers, endpoint amendments, unsuccessful research branches and an interrupted
adaptation attempt. Agent-Native Research Artifacts (ARA) supplies the design precedent.
Neither ARA nor preserving failed experiments is our invention. The current package
does not establish formal ARA compliance, a Seal certificate, or a benefit from using
this format. Its value is that readers can inspect and rerun the evidence supporting
the bounded financial findings, including evidence that prevented stronger claims.

## Verified primary source and version

[The Last Human-Written Paper: Agent-Native Research Artifacts](https://arxiv.org/abs/2604.24658v3)
is an arXiv preprint, submitted 27 April 2026, with current version **v3, 19 May 2026**
on the record checked 30 September 2026. No peer-reviewed publication is established
by that record. Its example manifest says `venue: NeurIPS 2026` and `status: draft`
(Appendix A.3.1, p. 26); that is not an acceptance announcement.

Current arXiv author metadata lists Jiachen Liu, Jiaxin Pei, Jintao Huang, Chenglei Si,
Ao Qu, Xiangru Tang, Runyu Lu, Lichang Chen, Xiaoyan Bai, Haizhong Zheng, Carl Chen,
Zhiyang Chen, Haojie Ye, Yujuan Fu, Zexue He, Zijian Jin, Zhenyu Zhang, Shangquan Sun,
Maestro Harmon, John Dianzhuo Wang, Jianqiao Zeng, Jiachen Sun, Mingyuan Wu, Baoyu Zhou,
Chenyu You, Shijian Lu, Yiming Qiu, Fan Lai, Yuan Yuan, Yao Li, Junyuan Hong, Ruihao Zhu,
Beidi Chen, Alex Pentland, Ang Chen, Mosharaf Chowdhury and Zechen Zhang.
The cached PDF author block additionally contains Qian-ze Zhu and uses Dianzhuo Wang;
do not silently equate that block with the 37-author metadata list. `J. Liu et al.`
avoids inventing a reconciled list; cite the exact arXiv version.

The accessible 46-page v3 PDF is already cached locally; this review inspected its
protocol, verification and schema sections, rather than relying on the abstract:
[PDF](https://arxiv.org/pdf/2604.24658v3),
locally cached extracted text (not distributed in the research bundle).
Cached PDF SHA-256: `c6418d4d62f49ce3fc267df62afd30f002007e2d0b1ed87e45ec6d4853895a4b`.
The paper-linked repository now redirects to
[ARA-Labs/Agent-Native-Research-Artifact](https://github.com/ARA-Labs/Agent-Native-Research-Artifact).
Its live compiler specification reports version 1.2.1; that evolving implementation
is distinct from the fixed paper v3. It was read as a source, not installed or run.

## Concrete requirements and their meaning

The paper specifies four interconnected layers (§2.2, pp. 4–5):

| Layer | Concrete expectation | Meaning for this study |
|---|---|---|
| Scientific logic | Root `PAPER.md`; problem, solution, claims, experiments and typed related-work dependencies | Every bounded finding should point to a declared test and its limitations. |
| Executable implementation | Code in kernel or repository mode; annotated configurations and pinned environment, hardware and seeds | Replaying saved-answer grading must be distinguishable from fresh inference. |
| Exploration graph | Typed question, decision, experiment, dead-end and pivot nodes; explicit dependencies | Preserve rejected hypotheses, failure modes and lessons without manufacturing chronology. |
| Evidence | Raw metrics and logs; claim → experiment → evidence links | Rounded narrative values and diagrams must trace to exact data and code. |

Claims carry statement, status, falsification criteria and proof; heuristics carry
rationale, sensitivity and bounds (§5.2, pp. 9–10). Appendix A.3 supplies examples
with provenance labels distinguishing user decisions, AI suggestions and execution.
Completeness is capability-relative: the proposed sufficiency criterion is zero-shot
reproduction without human intervention or external context beyond the artifact
(§2.2, p. 5). A directory layout alone does not demonstrate that criterion.

The proposed Seal levels test different properties (§5.2): Level 1 checks schema and
reference integrity; Level 2 audits argumentative rigor; Level 3 performs sandboxed,
scaled directional execution checks while withholding reported evidence from the
verification agent. Hash agreement is not a financial correctness certificate.
These are requirements of the authors' proposed ARA review system, not automatically
requirements of NeurIPS or our workshop. Novelty and significance remain judgments.

The [current compiler specification](https://github.com/ARA-Labs/Agent-Native-Research-Artifact/blob/main/skills/compiler/SKILL.md)
also requires a claim's conditions, explicit/inferred support labels, an environment
manifest, and an evidence inventory covering every numbered table and figure.
Retrospective reconstruction is permitted if identified as such; invented history is
not. An optional agent deliberation field requires grounded verbatim source material,
so the artifact should store concise observed decisions rather than synthesized
claims about what an earlier agent privately thought.

## What the local record actually supports

| Existing evidence | Positive artifact property | Scope limit |
|---|---|---|
| [Audit manifest](../outputs/answer-contract-v1/manifest.json) and [reproduction guide](../docs/ANSWER_CONTRACT_REPRODUCE.md) | Public source, code/protocol and result hashes; executable numerical replay | Pinned bytes establish identity, not correct semantics. |
| [Clean reproduction receipt](../outputs/answer-contract-v1/clean-reproduction.json) | Five scientific output files reproduced byte for byte after fresh downloads | Existing recorded Python runtime; identified earlier bundle, not a new isolated environment or complete current-package replay. All five recorded hashes still match current files. |
| [Evolution record](../docs/ANSWER_CONTRACT_EVOLUTION.md) and [saved amendment snapshot](../outputs/answer-contract-v1/snapshots/before-beta-only-amendment/manifest.json) | Prior CAPM implementation and rows/results remain inspectable | A documented subset of history, not proof every attempted idea was captured. |
| [Model replay guide](../docs/MODEL_GRADING_REPRODUCE.md) and [timing correction](../docs/MODEL_GRADING_CONVENTION_TIMING_CORRECTION.md) | Strict primary endpoint and post hoc sensitivity/correction remain separate | No retroactive preregistration; API identifiers do not guarantee immutable weights. |
| [V1 execution failure](../outputs/finance-adaptation-v1/execution_failure.json), [V2 execution amendment](../docs/FINANCE_ADAPTATION_EXECUTION_AMENDMENT.md) and [V2 results](../outputs/finance-adaptation-v2/results.json) | Interrupted attempt, separate execution freeze, unchanged scientific rules and completed unsuccessful pilot are retained | Operational rerun followed observed development outputs; no measured optimization harm or repair benefit. |
| [Document preparation reproduction](../docs/FINANCE_DOCUMENT_AUDIT_REPRODUCTION_REVIEW.md) | Fresh-copy selection and blank gold-free review packets match recorded bytes | Preparation only; no financial defect labels, expert adjudication or new environment. Full packets remain local. |

The research branches are real documented ideas, not multiple Git branches: the
checked local refs are `main` and `origin/main`. Failed directions are supported by
the [looped forecasting result](../docs/LOOPED_FORECAST_PILOT_RESULT_V1.md),
[matched market-cycle follow-up](../docs/MARKET_CYCLE_MATCHED_RESULTS_V2.md)
and [MarS finite-cycle audit](../docs/MARS_CYCLE_RESULTS_V3.md).
Each fails its proposed positive contribution gate; none establishes that the whole
research direction is impossible. Numerous research files are currently untracked,
so hashes/snapshots carry much of the revision identity. Do not claim a complete
commit-level research history.

A later [clean extracted-package replay](FINAL_ARTIFACT_REPLAY_2026-09-30.md)
covers the audit, saved-answer analyses, adaptation checks and new grading exports.
It reuses the recorded runtime and discloses timestamp/relocation metadata differences;
it does not test a newly isolated environment or rerun historical training branches.

## Bounded contribution wording

Suggested present-tense wording for the current local record; final packaging must
include the indices and validation receipt:

> We construct an ARA-inspired evidence package for the financial supervision audit,
> linking pinned inputs, protocols and amendments, executable analyses and saved
> outputs. The package preserves unsuccessful research branches and the interrupted
> adaptation attempt alongside the completed study, so readers can inspect both the
> reported findings and the evidence that limited stronger claims.

Add the verified scope if useful: numerical audit outputs reproduced with fresh
downloads using the recorded runtime; model and adaptation measurements replay from
saved answers without paid inference. Describe this as a study-specific research
resource and reproducibility practice. Claiming a new artifact protocol, guaranteed
independence, reduced research cost, improved agent performance, or a complete ARA
would require additional evidence. Failure preservation alone is already prior art.

## Missing pieces and bounded next steps

The new [root review index](../PAPER.md)
provides a portable front door to the canonical manuscript, protocols, endpoints,
results, failure records and no-inference replay commands. It uses our own schema.

1. The [retrospective graph](../experiments/research_exploration_graph_v1.json)
   and [claim/evidence map](../experiments/research_claim_evidence_v1.json)
   are now complete for their declared scope. A read-only run of the custom validator
   passes: 117 linked files, nine nodes, four documented edges, 13 claims and 58
   recorded-value checks, matching the [saved receipt](../outputs/research-artifact-v1/validation.json).
   Unknown historical authorship and chronology remain unreconstructed. This checks
   the linked inventory, not every nested dependency or complete research history;
   recorded-value agreement is not semantic validity or an official ARA Seal.
2. Bind every current claim and figure to exact result fields, endpoint, denominator,
   experiment, code/configuration and validation receipt. Include the negative GEPA
   finding and successful cheap controls as evidence limiting the argument.
3. Recheck the final packaged artifact, including new graph/figures and exclusions.
   An earlier clean replay does not validate files added afterward. Preserve source
   licensing/access status; keep private course material and unresolved document
   packets out of the bundle. Nothing here authorizes publication.
4. Formal ARA adoption would additionally need its root manifest and layer/schema
   mapping, consistent provenance and typed literature dependencies, environment and
   evidence inventories, and recorded checks against a pinned official specification.
   The custom root `PAPER.md` now exists; official `logic/`,
   `trace/exploration_tree.yaml`, `src/environment.md` and `evidence/` layer files
   remain absent. An index and equivalent scattered content support inspiration,
   not official schema conformance.
5. ARA-style evidence-withheld verification has not been demonstrated for this
   entire package. AI-assisted independent arithmetic/replay is valuable but read
   primary implementation/output context; it is not blind human expert review or
   an official Level 3 certificate. Human semantic adjudication remains separate.

For the paper figures, show exact finite-study evidence first; an optional small
artifact flow can expose source → freeze → saved answers → policies → results.
The new [figure metadata](../figures/generated/paper-evidence-v1/metadata.json)
binds saved strict and exploratory counts to the rendering code. The embedded
TikZ check is `scripts/render_answer_contract_figures.py --check`; it complements
the generated table check. A process diagram explains provenance; it does not add an experiment or
establish a measured benefit of ARA. This review creates no figure, PDF or editor tab.
