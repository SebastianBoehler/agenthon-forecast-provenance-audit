"""Executive summary: plot individual pilot models, preserving the baseline comparison."""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import tueplots

from style import paper_style


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads(args.results.read_text())
    colors = {"one_direction": "#B44334", "balanced_cycles": "#276C91",
              "unrestricted_signed": "#3C8060"}
    args.output_dir.mkdir(parents=True, exist_ok=False)
    with paper_style(6.8, 2.9, font_size=8), plt.rc_context({"font.family": "DejaVu Sans"}):
        fig, axes = plt.subplots(1, 2, layout="constrained")
        for coverage, color in colors.items():
            rows = [m for name, m in result["models"].items() if name.startswith(coverage + "/mlp")]
            axes[0].scatter([r["same_coverage_validation_rmse"] for r in rows],
                            [r["common_validation_rmse"] for r in rows], color=color,
                            label=coverage.replace("_", " "), s=25)
            axes[1].scatter([r["common_validation_rmse"] for r in rows],
                            [r["minimum_expected_cycle_cost"] for r in rows], color=color, s=25)
        baselines = [m for name, m in result["models"].items() if "/mlp" not in name]
        axes[0].scatter([r["same_coverage_validation_rmse"] for r in baselines],
                        [r["common_validation_rmse"] for r in baselines], marker="s", color="black",
                        label="linear / exponential fits", s=22)
        axes[1].scatter([r["common_validation_rmse"] for r in baselines],
                        [r["minimum_expected_cycle_cost"] for r in baselines], marker="s", color="black", s=22)
        axes[0].plot([0, 0.15], [0, 0.15], color="gray", linestyle=":", linewidth=0.6)
        axes[0].set(xlabel="Own-coverage response RMSE", ylabel="Common-bank response RMSE",
                    title="Validation depends on action coverage")
        axes[0].legend(fontsize=6, loc="lower right")
        axes[1].axhline(-result["config"]["effect_threshold"], color="gray", linestyle="--", linewidth=0.7)
        axes[1].set(xlabel="Common-bank response RMSE", ylabel="Minimum expected cycle cost",
                    title="Neural seeds can differ in cycle behavior")
        fig.savefig(args.output_dir / "coverage_pilot.pdf")
        fig.savefig(args.output_dir / "coverage_pilot.png", dpi=300)
        plt.close(fig)
    metadata = {"results_sha256": hashlib.sha256(args.results.read_bytes()).hexdigest(),
                "plot_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "style_source_sha256": hashlib.sha256(Path(__file__).with_name("style.py").read_bytes()).hexdigest(),
                "matplotlib": matplotlib.__version__, "tueplots": tueplots.__version__,
                "font": "DejaVu Sans", "size_inches": [6.8, 2.9],
                "status": "development_analysis_figure_not_final_paper_layout"}
    (args.output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")


if __name__ == "__main__":
    main()
