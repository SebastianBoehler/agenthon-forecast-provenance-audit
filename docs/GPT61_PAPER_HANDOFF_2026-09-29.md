## Executive summary (read this first)

The user explicitly requested a **new GPT-6.1 chat** to reassess the best Agenthon
2026 paper idea, finally select a direction, and produce its experiments, data,
figures, and manuscript. This file transfers the current evidence without requiring
the new chat to inherit the entire long conversation. The current answer-contract
audit is a conditional lead, not a user-finalized topic or a proven novelty claim.
Use fresh scientific judgment and continue concrete work after the decision.

## User objective and working style

- Present an accepted poster at the Agenthon workshop at NeurIPS 2026 during the
  user's master's. The scientific opportunity, networking, and CV signal matter.
- Aim for a useful, distinguishable contribution with enough empirical evidence
  for a credible workshop submission. The user believes the workshop threshold is
  realistic and does not require inventing a new foundation model.
- Review actual accepted workshop papers when judging scale. Avoid presenting
  acceptance probabilities without evidence or promising a guaranteed acceptance.
- The user works quickly: a bachelor's thesis and experiments took two weeks and
  its paper extension took one week. Conservative duration estimates should not
  preemptively reduce an interesting idea to a trivial contribution.
- Avoid repeated brainstorming loops, superficial novelty searches, and stopping
  after another proposal. Choose a direction on evidence, then execute it.
- Follow standard academic practice: research question, motivation, cited gap
  comparison, research design distinct from techniques, fair controls, ablations,
  meaningful metrics, limitations, independent review, and a response to review.
- Explain mechanisms concretely, preferably with geometric intuition.
- Preserve source-linked claims, failed attempts, code evolution, and executable
  reproduction artifacts. The user wants the agent-native artifact principle from
  *The Last Human-Written Paper: Agent-Native Research Artifacts* referenced and
  applied; it is a reproducibility practice rather than our novelty by itself.
- Use figures4papers and tueplots for publication figures, as previously requested:
  https://github.com/ChenLiu-1996/figures4papers and
  https://github.com/pnkraemer/tueplots.
- Public papers and the user's authorized IU EBSCO library may be searched. Download
  relevant legally accessible full texts into ignored local storage. Distinguish
  full-text reading from abstract-only access. Do not bypass access controls.

## Locations and boundaries

- Dedicated paper repository: `/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit`.
  It has `.venv`, `src/`, `scripts/`, `docs/`, `literature/`, `figures/`, and ignored
  local `data/`, `outputs/`, and `literature/pdfs/`.
- The saved Agenthon project starts in
  `/Users/sebastianboehler/Documents/GitHub/agenthon-2026-t2-forecasting`.
  Work on independent paper artifacts in the dedicated paper repository.
- Sibling competition repositories are `agenthon-2026-t1-coding`,
  `agenthon-2026-t3-simulation`, and `agenthon-2026-t4-analysis` under the same GitHub directory.
- Respect their AGENTS.md instructions and competition public/private firewall.
  Never disclose sealed tasks, answers, realized outcomes, credentials, or private
  competition artifacts. Public independently obtained research data belong in
  the paper repository, not the T2 public repo.
- The user often has unrelated concurrent edits. Preserve them. Keep files small
  (300 lines is the soft limit) and changes surgical.
- Apple `git` commands currently fail on the unaccepted Xcode license. Do not
  accept a legal agreement on behalf of the user. No commit/push was requested
  for the latest research pass.
- For standalone LaTeX, use the native source editor and compiler. Inspect existing
  manuscript structure before deciding whether a standalone file is appropriate.

## Venue and deadline

The official call was checked on September 29, 2026:
https://www.agenthon.net/#call-for-papers.
It invites AI and quantitative finance papers, explicitly including evaluation,
verification, benchmarks, reinforcement learning, forecasting, simulation, and
autonomous agents. It also welcomes strong general ML/AI work.

- Deadline: **September 30, 2026, 23:59 AoE**, equivalent to **October 1, 13:59 CEST**
  in Europe/Berlin (11:59 UTC). Recheck the live call before finalizing submission.
- Full or short papers, any format and length, one PDF. Non-archival; competing in
  Agenthon is not required. Accepted papers are posters; no oral route was confirmed.
- Decisions announced by October 2 at 23:59 AoE. At least one author must present
  in person in Atlanta on December 12. The form asks for the presenting author's
  NeurIPS-account email and a Google sign-in for upload.
- Writing and preparation are authorized; do not submit a form or email organizers
  without the human's explicit authorization for that action.

## Highest-value reading order

1. `docs/ANSWER_CONTRACT_NOVELTY_PAGE_2026-09-29.md`: latest conditional idea,
   measured evidence, nearest-work comparisons, methodology, falsifiers, outline.
2. `docs/FRESH_NOVELTY_LANDSCAPE_2026-09-29.md`: alternative candidates and collisions.
3. `docs/WORKSHOP_ACCEPTED_PAPER_COMPARISON_2026-09-29.md`: six primary-source accepted
   examples, five cached full PDFs. Includes negative studies, datasets, and systems.
4. `docs/FINANCE_BENCHMARK_CANDIDATE_REVIEW_2026-09-29.md` and
   `docs/FINANCE_RL_CANDIDATE_REVIEW_2026-09-29.md`: previous candidate screens.
5. `docs/LOOPED_FORECAST_PILOT_RESULT_V1.md` and `docs/MARS_CYCLE_RESULTS_V3.md`:
   completed negative pilots; do not repeat their positive framing.
6. `docs/PROCESS_RESET_2026-09-28.md`, `docs/LITERATURE_AUDIT_2026-09-28.md`, and
   `literature/README.md`: source/access records and academic workflow.

`docs/PROPOSAL.md` is an older provenance proposal, not the current chosen topic.
Some earlier decision documents also predate the newer experiments. Use the actual
dated reports and outputs to determine the latest status.

## Current conditional lead: visible-question answer contracts

Working title: **What Does Execution Verification Verify? Answer Contracts in
Financial Reasoning Data**. Question: do code-verified finance training labels
agree with the numeric information and requested precision visible to the model;
which grading/preference decisions change; can a validated repair fix the problem?

Two independent public releases now show distinct mechanisms. Counts are within
two selected templates/families, not prevalence across the financial AI field.

### Financial RLVR 10k Enterprise

- Dataset: https://huggingface.co/datasets/coslinedev/financial-rlvr-10k-enterprise.
  Revision `6cfa9a71e777026ba7242fbbb96c11c7dece5011`.
- Source: `literature/pdfs/financial-rlvr-10k-6cfa9a71.jsonl`, SHA256
  `86968a146a09e2ba1b19aac3a5ca2bec7e878358341a7972fddeb4b8cd7754af`.
- `scripts/audit_rlvr_dcf.py` independently recomputes with Decimal. Run it from
  the paper repo using `.venv/bin/python scripts/audit_rlvr_dcf.py`.
- Of 2,655 nonedge DCF cases, 2,385 displayed-input calculations differ from stored
  gold beyond the card's stated absolute 1e-4 numerical tolerance; 2,220 differ by
  over 0.1% and 128 by over 1%.
- **Crucial correction:** all 2,655 golds lie inside the interval implied by rounding
  both displayed rates to 0.1 percentage point. Median relative interval width is
  2.22%. This supports underdetermination from visible inputs, not intrinsically
  wrong finance golds. If rates are exact, use the displayed-input result; if rounded,
  multiple outcomes are consistent and the exact hidden target is not identifiable.
- The advertised tolerance was applied analytically. Actual released reward code
  was not located/reproduced and no real model reward loss was observed.
- Output: ignored `outputs/reward-contract/rlvr-dcf-audit.json`.

### Cosimo CFA/FRM 71k

- Dataset: https://huggingface.co/datasets/btech-software/cosimo-cfa-frm-71k.
  MIT license; revision `42244d29c6b9912683213a08d1a9c5b0373b381b`.
- Source: `literature/pdfs/cosimo-cfa-level-i.parquet`, SHA256
  `afa7e9241e0f06df090916e289a8e39d7fc9c4245c3b21c0c0f1188edafb0abb`.
- `scripts/audit_cosimo_gordon.py` independently recomputes its `cr_eq_gordon`
  template. Run `.venv/bin/python scripts/audit_cosimo_gordon.py`.
- All 1,000 questions explicitly request the nearest whole unit; all 1,000 raw
  formula values agree with cent-level labels. In 946 rows, the stored label differs
  from the requested whole-unit value. Example: prompt-consistent 31, label 30.94.
- Among 337 preference pairs in that template, 312 `chosen` answers also differ
  from the requested whole-unit answer. All 1,000 rows are marked verified.
- This is a prompt/output-format conflict with preference supervision, not proof
  of degraded trained-model behavior or arithmetic failure. Only one template checked.
- Output: ignored `outputs/reward-contract/cosimo-gordon-audit.json`.

### Nearest work and unresolved novelty

- FinVerBench full text https://arxiv.org/html/2605.29586v1 already studies hidden
  versus observable fields, answer validity and rounded financial statements.
- FinanceReasoning https://aclanthology.org/2025.acl-long.766/ corrects financial QA
  labels and provides executable solutions. Label correction alone is not new.
- FinChain https://aclanthology.org/2026.acl-long.662/ has expert-reviewed executable
  finance templates; candidate independent audit or clean negative-control source.
- Arcifa and Carra, *Fair and cheap*, official abstract:
  https://montanaresearch.org/publications/mrf-2026-04/.
  It already frames answer determinacy from model-visible information. Its open-data
  README was inspected; full manuscript remained behind a reader form. The Zenodo
  record supplied data ZIP only. Full-text overlap remains unresolved.
- Do not claim to invent determinacy or finance verification. A substantial paper
  needs cross-source mechanisms, consequential comparator/preference results,
  independently adjudicated examples, and a correction with false-accept controls.

## Other completed routes and their limits

- Looped FOMC forecasting: 216 official statement cases, chronological train/val/test
  split 160/34/22; three seeds. Tied three-pass text model test Gaussian CRPS 4.557bp
  versus 4.504bp without text and 4.494bp untied equal-attention text control. Gate failed.
  Small sample and unverified FRED vintage; do not market a positive looped-text effect.
- Learned market cycles: official pinned MarS checkpoint/exchange exercised through
  experimental CPU client. 60 attempts, 52 completed cycles, eight initialization
  failures, one profitable completed cycle. No causal defect or robust arbitrage
  demonstrated. Earlier synthetic effect disappeared after more optimization.
- Existing fast Track 3 Rust simulator: plausible systems asset, but generic speedup
  or documenting the track is insufficient. Paper-grade controlled comparison and
  distinct mechanism were not established. Do not use leaderboard throughput as
  a controlled baseline speedup or Final result.
- Generic financial harnesses, text ablations, faithfulness audits, finance tuning,
  and reward mismatch have many predecessors. Need exact mechanism and fair controls.
- `orca_clmm_agent` was a casual example of the user's experience, not a required
  research direction. Their prior user-turn LoRA paper is already accepted; they
  want a substantive new opportunity, not automatic repackaging of that paper.

## Requested execution in the new chat

Reassess the evidence and strongest alternative without anchoring on the latest
candidate. Bound the novelty review by a decisive comparison, choose one scientific
claim, state the reasons, and then carry out the necessary experiments and writing.
The user has already authorized continuing research and implementation; no routine
plan-approval pause is needed. Ask only about missing constraints that materially
change execution, while doing independent work.

Produce a source-linked novelty matrix, frozen experimental specification, real
data manifest, relevant baselines and ablations, results with uncertainty and
limitations, publication figures, readable manuscript and reviewer response.
Use falsification checks to improve the selected study. A failed feasibility pilot
must change the claim rather than be hidden. Report honestly if the deadline cannot
support a defensible submission. Treat posters as the confirmed presentation path.
