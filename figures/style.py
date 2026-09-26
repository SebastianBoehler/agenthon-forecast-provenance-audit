"""Executive summary: provide one template-sized Matplotlib style context for paper figures."""

from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator

import matplotlib.pyplot as plt
from tueplots import axes


@contextmanager
def paper_style(width_inches: float, height_inches: float, font_size: float = 8) -> Iterator[None]:
    """Apply compact publication settings scoped to one figure-generation block.

    Set dimensions from the LaTeX template's actual column or text width. Keep font size
    readable at that final physical size; use this context only for paper figures.
    """
    settings = axes.lines(base_width=0.5)
    settings.update({
        "figure.figsize": (width_inches, height_inches),
        "font.family": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "font.size": font_size,
        "axes.labelsize": font_size,
        "axes.titlesize": font_size,
        "xtick.labelsize": font_size - 1,
        "ytick.labelsize": font_size - 1,
        "legend.fontsize": font_size - 1,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "svg.fonttype": "none",
    })
    with plt.rc_context(settings):
        yield
