## Executive summary (read this first)

This private research repo studies whether reviewers can identify answer-first rationales in probabilistic finance forecasts when the forecast and visible evidence are held fixed. Its first tool randomizes matched cases into reviewer packets and writes the provenance key separately. It evaluates detectable construction-order cues; it does not establish that a rationale caused a model's answer.

## Research question

**Can blinded reviewers distinguish a rationale written before forecast commitment from one written after the same forecast was fixed, when both cases expose the same task context and forecast?**

The primary experimental contrast is rationale provenance. Each reviewer sees at most one member of a matched pair. Across reviewers, assignment to the two provenance conditions is balanced. This hides the pair structure and avoids showing one reviewer the same case twice.

## Paper queue

1. **Current paper:** Controlled audit of answer-first rationale provenance in probabilistic finance forecasting.
2. **Possible next paper:** Causal tests of when timestamped text changes probabilistic finance forecasts, using matched corpus interventions.
3. **Possible later paper:** Whether behavioral fork scores improve the cost of causal localization over matched position, surprisal, and entropy baselines. This is more naturally a separate mechanistic interpretability paper.

The second and third ideas are saved as candidates, not approved projects. Whether multiple submissions are allowed must be checked against the applicable call before submitting more than one paper.

## Repository layout

- `docs/EXPERIMENT.md` — design, outcomes, and limits.
- `docs/PLOTTING.md` — paper-figure conventions using figures4papers and tueplots.
- `PAPERS.md` — prior-art boundary and the parked follow-on ideas.
- `src/provenance_audit/` — standard-library-only packet randomizer.
- `data/`, `packets/`, `restricted/` — ignored paths for local inputs and outputs.

Do not place sealed Agenthon answers, private competition data, or identifiable participant material here without authorization. This GitHub repository is private. Case data and unblinding keys are ignored by Git.

## Case input

Provide one JSON object per line with exactly these fields:

```json
{"case_id":"case-001-forward","pair_id":"case-001","provenance":"derived","context":{"task":"...","evidence":[...]},"forecast":{"summary":"..."},"rationale":"...","generation_record":{"protocol":"v1","model_revision":"...","prompt_hash":"..."}}
```

Each `pair_id` must have exactly two cases: one `derived` and one `answer_first`. Their `context` and `forecast` objects must be exactly equal. The rationale text must differ. `generation_record` is retained in the restricted key for provenance and replication; it is never sent to reviewers. Do not use this abbreviated example as experiment data.

## Build blinded reviewer packets

After installing the package with `python -m pip install -e .`, run:

```bash
provenance-audit blind \
  --input data/cases.jsonl \
  --packet-dir packets/run-001 \
  --key-out restricted/run-001-key.json \
  --reviewers 6 \
  --seed 20260926
```

Each reviewer receives one randomly assigned rationale per pair, in a randomized order. Packet records omit source IDs, pair IDs, and provenance labels. The key contains those fields and the seed; it is written outside the packet directory with owner-only permissions. Keep the key restricted to the study operator until reviews are locked.

## Current status

The repository contains the study design and packet-preparation code. No cases have been added and no study result is claimed. The existing eight-trace pilot motivates the design but is too small to establish reviewer accuracy or an operational audit method.
