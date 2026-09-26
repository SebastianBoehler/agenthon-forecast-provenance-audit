## Executive summary (read this first)

Paper figures will use `figures4papers` for publication-oriented design patterns and `tueplots` for Matplotlib figure dimensions and typography. We will fit dimensions to the actual LaTeX template and keep source scripts plus PDF outputs with the paper artifact.

## References

- [Chen Liu's figures4papers](https://github.com/ChenLiu-1996/figures4papers/tree/f0bb7559abe90f5e1828797126d4d133c1bd47d7) — use its `scientific-figure-making` skill and selected `figure_*` examples as design references. Its README describes project-specific figure scripts and outputs; the skill emphasizes publication figures and vector/PDF export. We will adapt relevant ideas rather than copy entire scripts.
- [tueplots](https://github.com/pnkraemer/tueplots/tree/ba2616bfa4ba538d5d27d494ee61f5f1242199e2) — use the pinned `v0.2.4` release for Matplotlib figure-size, font, and line-style configuration. Its API returns dictionaries usable with `plt.rc_context()` or `rcParams`.

## Figure rules for this study

1. Read the actual LaTeX template's `\columnwidth` and font settings before choosing figure sizes. Agenthon accepts papers in any format and length, so do not assume a NeurIPS conference bundle is the workshop requirement.
2. Use `tueplots` sizing and typography helpers where they match the template; use a scoped `plt.rc_context(...)` so plotting configuration does not leak between figures.
3. Adapt the `figures4papers` guidance on clear hierarchy, restrained colors, uncluttered axes, and vector export. Do not copy its oversized slide-style fonts or extremely wide canvases into a compact paper figure.
4. Prefer PDF vector output for the LaTeX paper and a 300-dpi PNG preview. Keep the plotting script, input summary, package versions, and generated PDF together under `figures/`.
5. Show uncertainty and individual-case variation. Avoid bar charts that hide the small sample or imply precision the study does not have. Choose encodings only after the analysis table and uncertainty method are fixed.

## Current dependency

Install plotting tools separately from the packet-builder runtime:

```bash
python -m pip install -e '.[figures]'
```

The `figures` extra pins `tueplots` to `0.2.4`. Record the resolved Matplotlib and font environment in the final ARA-style run metadata.
