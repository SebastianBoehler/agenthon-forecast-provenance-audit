## Executive summary (read this first)

The research target is a future NeurIPS main-track submission. The Agenthon
workshop draft is an early checkpoint; its deadline does not create a main-track
submission route. The current audit has useful external evidence but lacks the
breadth and consequential, non-obvious insight needed for that larger target.
Adding a fashionable architecture would not resolve those gaps.

The strongest current question is: **when does executable verification reward
the wrong financial behavior, and which independent checks prevent that behavior
from transferring to unseen tasks?** Build on the completed audit and the inconclusive
paired-objective GEPA pilot, then earn a larger benchmark and training study
through the gates below. This is a research plan, not a promise of acceptance.

September 30 update: the pilot completed 432 held-out responses, selected the
unchanged seed prompt in every arm and passed neither consequence nor repair gate.
This is inconclusive about optimization effects, not evidence of harmless labels.

## How Hennig's and Lu's standards change the plan

These are interpretations of the user's actual course materials and Lu's recorded
writing guidance, not reviews, quotations, endorsements or grades from either
professor. Private course material remains outside the research release bundle.

| Inferred review question | Current answer | Required improvement |
|---|---|---|
| Hennig: is the question original, interesting and not answered in advance? | Released label defects and changed grades are real, but precision and reward misspecification are established. | Find a financial-semantic consequence or prevention result that survives the closest prior-art comparisons. |
| Hennig: can an alternative explanation account for the result? | Formatting, compounding and tolerance-window centers explain some disagreements. | Freeze task conventions; separate parse failure, numeric error, semantic quantity and grader geometry; retain passing controls. |
| Hennig: are uncertainty and evidence units honest? | Repeated synthetic templates prevent treating thousands of rows as independent evidence. | Test across independent releases, held-out financial families and authored/adjudicated templates; report variation at those levels. |
| Lu: why this method, and what is our own contribution? | The audit is external evidence. GEPA is a cheap objective-intervention tool. | Justify every method by the causal question and identify the exact empirical insight or method improvement beyond prior work. |
| Lu: can someone reproduce and independently validate it? | Saved 800 answers and independent arithmetic checks exist; human adjudication does not. | Complete blind expert review, public provenance, durable splits and independent evaluation code. |
| Both: can the author defend the assumptions and limitations? | Current claims are bounded; no training effect has been measured. | Explain the task, failure mechanism, intervention and falsifiers without relying on optimizer names or acceptance tactics. |

## Stage 1: completed consequence pilot

The prospective [GEPA protocol](FINANCE_ADAPTATION_PROTOCOL_V1.md) uses one fixed
actor, two optimizer seeds per objective, 32 training and 32 development questions,
48 fresh released tests and 24 researcher-authored wording tests. Every new operand
tuple excludes the old 200-question study. Source-objective and repaired-objective
adaptation receive only their assigned feedback. A seed prompt and a simple manual
financial instruction are necessary baselines. No model weights change.

**Success check:** source reward increases while independent financial validity
falls on both test sets in both source-objective seeds; repair improves transfer
without deterioration on the passing families. Parsing and failures remain in the
denominator. If the optimizer fails to improve its objective, this test is
inconclusive. If transfer does not worsen, do not claim adaptation harm.

This stage supplies an assigned-objective-and-feedback intervention within one
configuration: corrected targets and the explicit integer constraint change
together. It does not isolate numeric label replacement alone. Equal call caps
also do not imply equal realized compute; retain actor/reflection/token use per arm.
Reflection receives assigned reference values as well as binary credit. This is
target-visible prompt adaptation, not a test of learning from scalar rewards alone.
It does not establish a new optimizer, a broad benchmark or weight-training harm.
Retain the workshop paper even if this optional experiment is inconclusive.

## Stage 2: build a benchmark that can challenge the explanation

Make the benchmark test mechanisms rather than collect more near-identical rows.
First prepare a source/license/provenance ledger for at least two additional
independently produced releases. A release derived from another benchmark is not
automatically a new independent source. Freeze selection before looking for faults;
include clean and defective cases without conditioning on model success.

Hold out whole financial families and source-generation pipelines, not just operand
values. Keep released questions distinct from researcher-authored counterfactuals.
The latter should change one semantic requirement at a time: call value versus
financing debt, next versus current dividend, integer versus cent output, or
specified versus genuinely missing precision. They test quantity grounding and
instruction transfer, not market prediction. The current pilot's 12 family/template
IDs correspond to nine base wording structures because the Gordon families share
their three descriptions; do not count these as 12 independent language templates.

Review every prospectively selected primary case in blind packets. Keep targeted
ambiguous/passing diagnostic additions separate from that primary sample.
Two reviewers independently label requested quantity, available information and
acceptable answer set, recording their own derivations. Lock that review before
showing source targets or model outputs. Assess supplied traces in a subsequent
explicit stage; a blank question packet contains no model trace to validate.
Resolve disagreements transparently.
Use a qualified human financial reviewer before claiming expert adjudication.
Record that an AI-assisted independent calculator is technical validation, not
human domain review. Keep an untouched final test set inaccessible to optimizers.

**Success check:** independent adjudication supports the mechanism, and its effect
appears in a held-out release or financial task. Publish per-release and per-template
variation, label disagreement and negative cases. If effects exist only in the
already discovered Cosimo templates, keep a case-study claim.

The [document-audit preparation](FINANCE_DOCUMENT_AUDIT_READINESS_V1.md) now supplies
48 FinQA questions from distinct native reports and 48 TAT-QA questions from distinct
contexts, selected before correctness checks. The blank review sheets omit source
answers. An exact context/question join handles changed TAT-QA annotation IDs under
a declared amendment. This is completed provenance and packet preparation; no new
financial answer audit, expert review or verifier-training release is established.

A [fresh-copy reproduction](FINANCE_DOCUMENT_AUDIT_REPRODUCTION_REVIEW.md) now
matches all 96 identities/groups and the four deterministic preparation hashes.
It reuses the existing runtime and freshly downloads the pinned public inputs.
Selection uses native TAT-QA answer-type metadata, but no numeric targets or
correctness judgments. This verifies packet preparation, not financial truth.

Before scaling, define the independent sampling units and the smallest consequence
worth detecting. Compare objectives on the same held-out cases and report paired
differences. Group document cases by report, synthetic cases by authored template,
and optimization replicates by seed; repeated operand rows are not independent
replications of a mechanism. Resolve TAT-QA report identity before claiming report
disjointness or report-level uncertainty. With only a few releases or seeds, show
each stratum rather than manufacture narrow intervals from the pooled row count.
Choose the larger sample and seed budget from development variability before
opening the final test set. The present 96 packets are a preparation pilot, not a
power justification for the main study.

The existing question-first hash selection with one case per group is not a
uniform sample of reports: larger eligible groups have more chances to enter.
Describe outcomes on these selected cases, not unweighted population prevalence.
A subsequent prevalence study needs a prospectively defined sampling population,
group selection probabilities and appropriate weighting or group-first sampling.
Separately identify operative reward verifiers; an annotation-only financial
benchmark adds document breadth but does not establish RLVR-release breadth.

Freeze document-specific answer units, scale, rounding and acceptable-answer sets
from visible information before comparison with native labels. A direct-formula
baseline must obtain operands from the same question/table/text available to the
model. Giving it gold programs or manually extracted operands instead makes it an
oracle-assisted diagnostic, which needs a separate label. Preserve the information
advantage of any manual financial instruction when interpreting optimizer results.

## Stage 3: establish what is new before selecting a larger method

The [expansion triage](RESEARCH_EXPANSION_TRIAGE_2026-09-29.md) identifies direct
collisions. Systematic verifier errors already cause RL plateaus/collapse, and their interactions have already been studied; reflective
optimization with an independent corrective oracle already exists; financial
precision and observability audits already exist. “Wrong rewards hurt learning”
and “GEPA helps” are insufficient main-track claims.

The [IU EBSCO search ledger](EBSCO_SEARCH_LEDGER_2026-09-30.md),
[database-lead triage](EBSCO_DISCOVERY_TRIAGE_2026-09-30.md) and
[extended primary-source review](EXTENDED_LITERATURE_REVIEW_2026-09-30.md) further
narrow financial measurement, provenance and auditor-benchmark claims. Label
audits and ranking reversals also predate this work. Compare those exact settings
before presenting an empirical insight as new.

One candidate distinction is naturally occurring, source-traced financial-semantic
defects with independently tested predictive and transfer consequences: whether correction of rounding alone leaves quantity shortcuts intact,
whether numeric tolerance helps some families while rewarding others' errors,
and whether independently budgeted checks prevent those shortcuts on unseen tasks.
These are hypotheses, not established novel results. The current audit does not
show that several natural defects coexist in the same case; merely combining
injected defects is already covered by the systematic-verifier-error literature.
Partial-versus-joint correction experiments require real cases where both
mechanisms apply. If no such cases exist, drop the natural-interaction hypothesis.

Before implementation, write a claim-to-prior-art table and one falsifiable sentence
for each proposed contribution. A discovery paper can contribute a strong empirical
insight without a new architecture. A method paper must show improvement beyond
simple integer checks, direct formula execution, abstention for missing information,
existing verified finance pipelines and noise-correction baselines at matched cost.

For a predictive claim, define defect categories from source/task information before
examining adaptation outcomes. Fit any prediction rule on development releases and
freeze it before the final held-out release. Compare against total label-error rate,
random corruption at matched error rate, task difficulty and response-format failure.
Evaluate predicted changes in independent financial validity, rather than merely
reclassifying labels already used to define the categories. If the categories add
no predictive value beyond those controls, remove that contribution claim.

**Success check:** an outside reviewer can state precisely what the study teaches
that the closest paper does not, and the corresponding controlled experiment can
disprove it. If that fails, change the question before buying training compute.

## Stage 4: run matched adaptation and weight-training experiments

After the benchmark and novelty gates pass, start with one small open model and
replicate in another model family. A 1–3B model is useful for iteration, not a novelty
claim. Verify the actual training stack and memory needs before scheduling a run;
the working MPS inference setup does not prove that an RL trainer supports MPS.
For size comparisons, use within-family pairs and fixed decoding/objectives, then
replicate across families. Checkpoint training differences still prevent attributing
every gap solely to parameter count; report those differences and formatting rates.

Compare unchanged initialization, clean/repaired supervision, original released
supervision and independently controlled corruption at the same data, updates,
decoding and compute budget. Change one defect class at a time, then test their
interaction. Keep ordinary random label noise as a baseline; structured financial
defects must explain something beyond generic noise. Use multiple training seeds,
hold out families/releases, measure financial validity and response format
separately, and examine saved responses for the proposed shortcut mechanism.

For document QA, compare direct answers, chain-of-thought and one matched
[Program-of-Thoughts](https://openreview.net/forum?id=YfZ4ZPt8zd) condition before
selecting a new architecture. PAL is a complementary established precedent.
Freeze identical semantic grading and extraction across strategies; published
PoT uses TAT-QA dev and a relaxed FinQA CoT tolerance, which must not silently
become our test split or strategy-specific scoring policy. Programs receive the
same visible inputs, with syntax/runtime failures retained in denominators.

Start with the simplest objective capable of testing the hypothesis. GEPA studies
prompt adaptation. Supervised fine-tuning tests learning from targets. RL with
verifiable rewards is appropriate only when the reward-gradient consequence is
the research question. Preference optimization requires repaired chosen responses
and reasoning traces; the numerical patches are not a ready preference corpus.

The main study should answer these ablation questions before claiming a repair:

| Controlled comparison | Explanation it tests |
|---|---|
| Original supervision versus quantity-only correction | Is the wrong economic quantity responsible for the change? |
| Original supervision versus rounding-only correction | Is the effect instead explained by output precision? |
| Partial versus joint correction, where defects naturally coexist | Does a residual defect defeat a partial repair? |
| Structured defects versus random corruption at matched error rate | Does financial structure explain more than generic label noise? |
| Scalar reward only versus explicit assigned-target feedback | Does a mechanism depend on revealing incorrect reference values to the optimizer? |
| Learned intervention versus integer checks, direct formula execution and fixed manual instructions | Does learning add value beyond cheap domain rules? |
| Fixed answer format versus separately scored numerical validity | Is apparent improvement primarily format compliance? |
| New operands versus held-out wording, financial families and producers | What actually transfers beyond familiar templates? |

These are planned comparisons. The current pilot does not implement this complete
matrix, isolate every correction, or hold out whole financial families.
Budget one mechanism-focused experiment, its primary outcome and all required
replications before expanding this menu; the entire matrix is not the next run.

**Success check:** the predicted mechanism appears beyond one checkpoint and seed,
survives matched baselines and independent held-out evaluation, and correction
preserves clean-task performance. A null result is evidence; do not select only
successful architectures or seeds after seeing outcomes.

## Where the suggested architectures belong

| Idea | Use only when | Necessary comparison |
|---|---|---|
| GEPA | Prompt adaptation to a flawed objective is itself under study. | Fixed seed/manual instructions, matched evaluation budgets and both objectives. |
| Looped transformers | Repeated computation addresses a measured reasoning bottleneck with sufficient visible information. | Tied and untied models at equal inference compute, clean versus corrupted objectives, held-out tasks. |
| World models | A genuine sequential task has action-conditioned transitions and independent counterfactual ground truth. | Direct forecasting/control baselines, transition fidelity and decision loss; static answer labels supply none of these. |
| Tiny NN with PufferLib RL | There is a grounded sequential checking/acquisition decision with resource cost and consequential action effects. | Exact planning or value-of-information rules and a contextual-bandit baseline; formula selection alone is a toy. |

The Mac has PufferLib 3.0 installed and its native kernel is discoverable; a complete
training run has not been verified. Current Puffer documentation emphasizes a newer
CUDA training path. Infrastructure choice follows the task and platform, and is
not itself a scientific contribution.

## Main-track readiness gate

Before a main-track submission, require a clear significance argument, resolved
nearest-prior-art overlap, independent ground truth, meaningful held-out breadth,
appropriate baselines/ablations, training or adaptation evidence matching the claim,
seed and template variation, reproducibility and a limitations section that does
not contradict the abstract. Re-review the complete manuscript after those results.

See the [primary-source main-track review](MAIN_TRACK_RESEARCH_REVIEW_2026-09-29.md)
for the official criteria, exact novelty collisions and falsification gates.
The [final plan review](MAIN_TRACK_PLAN_FINAL_REVIEW.md) checks sampling, baseline
information access, document contracts and execution feasibility.

The [2026 main-track deadline](https://neurips.cc/Conferences/2026/CallForPapers)
has already passed. The target is a future main-track
cycle; its dates must be checked when officially announced. The Agenthon workshop
checkpoint remains a separate nonarchival submission. Exact acceptance chances
cannot be inferred from these gates, title length or the professors' teaching.

The manuscript keeps the concise title **When Verified Financial Labels Fail**
because it states the observed problem. A reported association between shorter
titles and citations in [Letchford et al. (2015)](https://doi.org/10.1098/rsos.150266)
does not establish a causal increase in acceptance probability.
Use title/abstract clarity to communicate the contribution; assess quality with the
evidence gates above.
