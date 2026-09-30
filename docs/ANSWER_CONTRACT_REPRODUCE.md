## Executive summary (read this first)

Reproduce the selected financial supervision audit with pinned public input downloads,
an independent Fraction implementation, and publication figures. The PDF source is
standalone and editable in Codex's native LaTeX editor. The numerical patches are an
audit artifact, not a certified training corpus. No sealed competition data are used.

## Runtime and commands

Use Python 3.13, with the versions in `experiments/answer_contract_requirements.txt`.
The original run used Python 3.13.2. From the repository or extracted artifact root:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r experiments/answer_contract_requirements.txt
PYTHONPATH=src .venv/bin/python scripts/stage_answer_contract.py
PYTHONPATH=src .venv/bin/python scripts/run_answer_contract.py
.venv/bin/python scripts/independent_contract_validation.py
.venv/bin/python figures/answer_contract.py
```

Staging accesses only pinned public Hugging Face files and GitHub source text.
It verifies every SHA256 hash before using a cached or downloaded file. It does not
execute upstream generators or solution code. Any missing file, unexpected parser
case, altered hash or valuation disagreement stops the run.

The focused implementation checks require pytest 9.1.1:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=src .venv/bin/python -m pytest tests/test_answer_contract.py -q
```

The independent script needs the staged Cosimo source manifest and the primary row
artifact. It creates exact fractions for 5,935 rows and validates their patch records.
Figure reproduction uses the shared `figures/style.py`; exports are PDF, PNG and SVG.

## Paper export

Open `paper/answer_contract_audit.tex` in the built-in editor and use the native
compiler. No companion TeX file or image dependency is needed. A standard TeX Live
installation can export the same source with two pdflatex passes:

```bash
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=outputs/answer-contract-v1 paper/answer_contract_audit.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=outputs/answer-contract-v1 paper/answer_contract_audit.tex
```

The current model-study revision stays in the same native editor and its PDF preview.
The latest research bundle contains that `.tex` source; no separate paper PDF was
compiled or exported after the user requested keeping the current document open.
Earlier local PDF exports precede this revision. The draft names Sebastian Böhler;
coauthors/affiliation remain to confirm. A successful compile does not establish
scientific validity or venue acceptance.

## Output map and checks

| Artifact | Role |
|---|---|
| `outputs/answer-contract-v1/results.json` | Complete selected-family counts, comparator sensitivity and ablations |
| `outputs/answer-contract-v1/rows.jsonl` | Source IDs, prompt hashes, formula values and admissibility decisions |
| `outputs/answer-contract-v1/numerical-patches.jsonl` | Explicit exact-input convention and repaired numerical labels |
| `outputs/answer-contract-v1/manifest.json` | Input, protocol, implementation and result hashes |
| `outputs/answer-contract-independent/summary.json` | Rational validation, sampled/census scope and source inspection |
| `outputs/answer-contract-independent/review_sample.jsonl` | 440 executable review examples; no human annotation claimed |
| `figures/generated/answer-contract-v1/metadata.json` | Figure code/style/input hashes and export versions |
| `docs/ANSWER_CONTRACT_REVIEW_RESPONSE.md` | Reviewer objections, revisions and remaining limitations |

Rows and aggregate results should reproduce byte-for-byte with the recorded versions.
This was verified for five primary/independent scientific output files using fresh
downloads in a separate directory. The reproduction record is included in
`outputs/answer-contract-v1/clean-reproduction.json`; its archive hash identifies
the pre-report bundle tested before adding that verification record to the final bundle.
Manifest paths and PDF creation metadata may change by machine/run. Compare numerical
results and document source hashes, rather than treating PDF timestamp differences as
scientific disagreement. Original third-party full papers are intentionally excluded
from the bundle; their access ledger and links are in the novelty reassessment.
