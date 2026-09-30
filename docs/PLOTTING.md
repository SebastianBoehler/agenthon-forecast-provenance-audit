## Executive summary (read this first)

Paper figures use `figures4papers` for publication-oriented design patterns and `tueplots` for Matplotlib figure dimensions and typography. Dimensions fit the actual LaTeX template; source scripts and figure exports accompany the paper artifact.

## References

- [Chen Liu's figures4papers](https://github.com/ChenLiu-1996/figures4papers/tree/f0bb7559abe90f5e1828797126d4d133c1bd47d7) — use its `scientific-figure-making` skill and selected `figure_*` examples as design references. Its README describes project-specific figure scripts and outputs; the skill emphasizes publication figures and vector/PDF export. We will adapt relevant ideas rather than copy entire scripts.
- [tueplots](https://github.com/pnkraemer/tueplots/tree/ba2616bfa4ba538d5d27d494ee61f5f1242199e2) — use the pinned `v0.2.4` release for Matplotlib figure-size, font, and line-style configuration. Its API returns dictionaries usable with `plt.rc_context()` or `rcParams`.

## Figure rules for this study

1. Read the actual LaTeX template's `\columnwidth` and font settings before choosing figure sizes. Agenthon accepts papers in any format and length, so do not assume a NeurIPS conference bundle is the workshop requirement.
2. Use `tueplots` sizing and typography helpers where they match the template; use a scoped `plt.rc_context(...)` so plotting configuration does not leak between figures.
3. Adapt the `figures4papers` guidance on clear hierarchy, restrained colors, uncluttered axes, and vector export. Do not copy its oversized slide-style fonts or extremely wide canvases into a compact paper figure.
4. Export vector PDF/SVG and a 300-dpi PNG preview for figures. The current native editor compiles one standalone source, so the paper embeds generated TikZ rather than requiring external project files. Keep scripts, exact counts, package versions and vector exports under `figures/`.
5. Show uncertainty and individual-case variation. Avoid bar charts that hide the small sample or imply precision the study does not have. Choose encodings only after the analysis table and uncertainty method are fixed.

## Current dependency

In the full repository checkout, install plotting tools separately from the packet-builder runtime:

```bash
python -m pip install -e '.[figures]'
```

The extracted research bundle omits the repository's editable-package metadata.
Its equivalent pinned plotting dependencies are installed with
`python -m pip install -r experiments/answer_contract_requirements.txt`.

The `figures` extra pins `tueplots` to `0.2.4`. Shared style context lives in `figures/style.py`; every figure should use it and record the resolved Matplotlib and font environment in the final ARA-style run metadata.

The new `figures/paper_evidence.py` uses tueplots figure sizing and font helpers,
adjusted to the manuscript's actual 6.8-inch text width. It adapts figures4papers'
blue/red/neutral palette, direct annotations and uncluttered axes. Its strict
counts and exploratory ordering use distinct panels with explicit denominators.
`scripts/render_answer_contract_figures.py --check` verifies that the embedded
TikZ agrees with saved result fields. No source-question or model answer is rerun
to improve a plot. Metadata binds data, plotting source, style and every export.
