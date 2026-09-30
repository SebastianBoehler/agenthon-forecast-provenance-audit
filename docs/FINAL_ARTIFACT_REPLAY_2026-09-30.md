## Executive summary (read this first)

The clean extracted candidate passes the requested saved-evidence replay. All
681 manifest hashes and the exact 682-file inventory agree before and after the
checks. Of 44 selected regenerated outputs, 37 match the packaged bytes exactly.
The other seven have the disclosed metadata differences below; no scientific
value changed. All 15 focused tests pass. No missing bundled dependency was found.

At replay time the candidate was `outputs/answer-contract-research-20260929.zip`, SHA256
`11f2a4b6d818e0035c2d7c69cce1e601f759821f1aa091c1bce98c2d7d10f2c4`.
The repository retains those exact 8,549,181 bytes as
[the tested candidate ZIP](../outputs/answer-contract-research-20260929-tested-11f2a4b6.zip).
This receipt concerns those bytes, not the forthcoming documentation-only repack.
It is AI-assisted technical validation, without human annotations or ARA certification.

## Runtime, extraction and ordering

The existing repository runtime was used explicitly:
`/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/.venv/bin/python`.
Its Python version is 3.13.2; installed packages are NumPy 2.4.3, pandas 2.3.1,
PyArrow 21.0.0, Matplotlib 3.10.3, tueplots 0.2.4, mpmath 1.3.0, pytest 9.1.1
and GEPA 0.1.1. No new or isolated environment was installed or tested.

Extraction rejected absolute paths and `..` components. The temporary parent was
`/var/folders/n4/d1s6w7jn7jg1x7dnv_c53jd40000gn/T/answer-contract-replay-20260930-opkujwa5`.
Its `evidence` directory remained unchanged. Copies named `audit`, `model`,
`adaptation`, `checks` and `finance-reference` held regenerated outputs.

Graph integrity was checked before recomputation on a pristine copy. This order
matters: independent validators rewrite timestamped receipts, and the audit runner
rewrites its path/inventory manifest. A graph hash check on a recomputation copy
can therefore reject metadata despite identical scientific values. The unchanged
`evidence` copy passed the complete bundle manifest check again after replay.

Only public source staging used network access. The two full release inputs were
absent from the extraction and downloaded at the pinned revisions. Their hashes
match the declared Cosimo parquet and financial-RLVR JSONL hashes. All six pinned
Cosimo source/license files were hash-checked; missing source files were staged.
Upstream financial solution code was inspected rather than executed.

## Executed checks and consequences

| Check | Observed result |
|---|---|
| Audit census | 12,655 rows; results, row ledger and numerical patches reproduce exactly |
| Independent audit | 5,935 exact Fraction calculations; independent rows, sample and summary reproduce exactly |
| Model selection | All 200 prompts, 50 per family, and formulas reproduced directly from public parquet |
| Original model panel | 600 saved answers independently rescored under strict and supplementary numeric parsing |
| Roster extension | 200 added answers; combined 800 strict/numeric results and ledgers reproduce exactly |
| Compounding sensitivity | 1,000 source cases and 1,600 independent response endpoints agree using 100-digit mpmath |
| Adaptation references | 152 cases rebuilt; split/operand exclusions pass; boundary checks reproduce |
| Adaptation postflight | 989 saved occurrences, including 541 optimizer rows and 432 heldouts, independently rescored |
| Frozen execution evidence | Original 34 files, V2 65 files, installed GEPA 81 source files, interrupted ledgers and unchanged references pass |
| Research graph/map | 117 linked files, 9 nodes, 4 edges, 13 claims and 58 recorded-value checks pass |
| Manuscript data bindings | Table check and embedded TikZ check pass |
| New grading exports | PNG, PDF, SVG, TikZ and metadata all reproduce byte-for-byte |
| Focused tests | 15 pass with `PYTHONPATH=src:scripts` |

The substantive audit results remain 946 whole-unit Gordon and 975 binomial
source-label violations. CAPM and DCF precision findings remain conditional on
displayed-input interpretation. The compounding sensitivity still rescues one
DeepSeek answer and no source labels; 975 source binomial labels fail both conventions.
Strict parsing failures remain an output-format measurement, not latent incapacity.

The GEPA occurrence supplement preserves six repeated training tags rather than
deduplicating them. It matches 878 actor API occurrences and retains 111 overlong
placeholders. The frozen tag-uniqueness assumption remains the disclosed reason
the original unsupplemented checker fails. No parser, numerical rule, feedback,
selection rule or raw response was changed for this replay.

The interrupted V1 retains 459 attempts and $0.089236560. V2 retains 942 attempts
and $0.162813161; cumulative accounted cost is $0.252049721 under the $0.90 cap.
Recorded egress slots peak at four and precede the original request cutoff,
`2026-09-29T23:33:58.526883+00:00`; slots bound requests, not exact wire times.
All four optimizer arms retain the seed strategy, including the first-maximum tie.
Both consequence and repair gates are false for both seeds. Variation between
holdout calls using the same seed prompt is not an optimization effect.

## Exact output comparison and metadata differences

All 16 primary model scoring/summary files, all regenerated independent row
ledgers, the audit scientific outputs, the GEPA results, and all five new figure
files are among the 37 exact matches. Full saved and replayed SHA256 pairs for
all 44 outputs are recorded in
[the machine-readable receipt](../outputs/final-artifact-replay-results.json).

Six receipts differ only in UTC timestamps: original model summary, extension
summary, convention summary, descriptive model-case notes, GEPA occurrence
receipt, and adaptation prereview benchmark receipt. The graph receipt separately
differs only in `checked_utc`; its remaining JSON fields agree exactly.

The seventh selected difference is `outputs/answer-contract-v1/manifest.json`.
The runner records its own absolute path, which changes after extraction. It also
includes the already-present later `clean-reproduction.json` in the output inventory
on rerun. Existing scientific output hashes agree. This manifest is consequently
not byte-portable across this relocation, although its scientific values are.

Representative exact result hashes are:

| Output | SHA256 |
|---|---|
| Audit `results.json` | `fd7c78e021124b6409054bfeb4ed310f0da56d2622da66b1e0c3d05973fd0d69` |
| Combined strict results | `46e9bcb2980330238f556bc94d536c909302c4b2f5b1ea5f30ce54d20fbeac90` |
| Combined numeric results | `2c85587f7874bf37930208c91d73678187f94e2565373aeed0366bc961e60375` |
| Compounding results | `36f89979b260a51ab88dc9feaf30879ba80129bf2987f6c82acc9eb1d7a58260` |
| GEPA V2 results | `a597add5b288a9d376e15c9f3fd883895edf573abffbff59c8f498b1e44d5fee` |

## Commands and boundaries

The commands below used the absolute existing interpreter as `REPLAY_PY` and the
indicated extracted-copy working directory. Source staging occurred once in
`audit`; its verified input bytes were copied to `model` and `finance-reference`.

```bash
REPLAY_PY=/Users/sebastianboehler/Documents/GitHub/agenthon-forecast-provenance-audit/.venv/bin/python
# pristine checks copy
"$REPLAY_PY" scripts/validate_research_artifact.py --output ../graph-replay.json
"$REPLAY_PY" scripts/render_answer_contract_tables.py --check
"$REPLAY_PY" scripts/render_answer_contract_figures.py --check
"$REPLAY_PY" figures/paper_evidence.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=src:scripts "$REPLAY_PY" -m pytest tests/test_answer_contract.py tests/test_model_grading.py tests/test_model_grading_sensitivity.py tests/test_finance_adaptation.py tests/test_finance_adaptation_logging.py -q
# audit copy
PYTHONPATH=src "$REPLAY_PY" scripts/stage_answer_contract.py
PYTHONPATH=src "$REPLAY_PY" scripts/run_answer_contract.py
"$REPLAY_PY" scripts/independent_contract_validation.py
# model copy, in dependency order
PYTHONPATH=src "$REPLAY_PY" scripts/evaluate_model_grading.py
PYTHONPATH=src "$REPLAY_PY" scripts/evaluate_model_grading_sensitivity.py
PYTHONPATH=src "$REPLAY_PY" scripts/evaluate_model_grading_extension.py
PYTHONPATH=src "$REPLAY_PY" scripts/analyze_model_grading_conventions.py
"$REPLAY_PY" scripts/validate_model_grading_selection.py
"$REPLAY_PY" scripts/validate_model_grading_outputs.py
"$REPLAY_PY" scripts/validate_model_grading_extension.py
"$REPLAY_PY" scripts/validate_model_grading_conventions.py
"$REPLAY_PY" scripts/census_model_grading_conventions.py
# adaptation copy
PYTHONPATH=src "$REPLAY_PY" scripts/report_finance_adaptation_v2.py
"$REPLAY_PY" scripts/validate_finance_adaptation_occurrences.py
# separate finance-reference copy: preserve original frozen receipts elsewhere
"$REPLAY_PY" scripts/finance_adaptation/independent_validation.py
"$REPLAY_PY" scripts/finance_adaptation/check_oracle_boundaries.py
```

The initial combined test command used `PYTHONPATH=src` and failed collection
because the logging test imports the bundled runner from `scripts`. Adding that
directory resolved it; no missing file, code change or dependency install was needed.

This replay did not run model inference, fresh training, paper compilation,
credential/firewall scans, historical checkpoint tensor replay or a new FinQA/TAT-TQA
download. Prior unchanged-script document staging reproduction is separate evidence.
Numerical and structural agreement does not supply expert semantic adjudication,
causal adaptation evidence, a representative prevalence estimate or official ARA
compliance. The documentation-only final repack requires its own archive/inventory
hash check; this receipt must not be described as testing those future ZIP bytes.
