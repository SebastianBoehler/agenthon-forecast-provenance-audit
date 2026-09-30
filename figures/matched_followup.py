"""Executive summary: show negative controls honestly beside the first apparent failures."""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import tueplots

from style import paper_style


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matched", type=Path, required=True)
    parser.add_argument("--duration", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    matched = json.loads(args.matched.read_text())
    duration = json.loads(args.duration.read_text())
    args.output_dir.mkdir(parents=True, exist_ok=False)
    with paper_style(6.8, 2.9, 8), plt.rc_context({"font.family": "DejaVu Sans"}):
        fig, axes = plt.subplots(1, 2, layout="constrained")
        for seed, row in duration["results"].items():
            epochs = sorted(map(int, row["checkpoints"]))
            costs = [row["checkpoints"][str(e)]["audit"]["raw"]["minimum_expected_cost"] for e in epochs]
            axes[0].plot(epochs, costs, marker="o", markersize=3, linewidth=0.8, label=f"init {seed}")
        axes[0].axhline(-0.1, linestyle="--", linewidth=0.6, color="gray")
        axes[0].set(xlabel="Optimization updates, original V1 data", ylabel="Minimum expected cycle cost",
                    title="Original finite-bank failures disappear")
        axes[0].legend(fontsize=6)
        for coverage, color in (("blocked", "#B44334"), ("shuffled", "#276C91")):
            names = [n for n in matched["audits"] if coverage in n and n.endswith("fixed_budget")]
            errors = []
            costs = []
            for name in names:
                trajectory = name.removesuffix("_fixed_budget")
                errors.append(matched["validation_trajectories"][trajectory][-1]["common_rmse"])
                costs.append(matched["audits"][name]["new_bank"]["raw"]["minimum_expected_cost"])
            axes[1].scatter(errors, costs, color=color, s=22, label=coverage)
        baseline_names = [n for n in matched["audits"] if n.endswith("linear_ls")]
        axes[1].scatter([0]*len(baseline_names),
                        [matched["audits"][n]["new_bank"]["raw"]["minimum_expected_cost"] for n in baseline_names],
                        marker="s", color="black", s=20, label="linear fits")
        axes[1].axhline(-0.1, linestyle="--", linewidth=0.6, color="gray")
        axes[1].set(xlabel="Common-bank response RMSE", ylabel="Minimum expected cycle cost",
                    title="Matched trades: no detected violations")
        axes[1].legend(fontsize=6)
        fig.savefig(args.output_dir / "followup.pdf")
        fig.savefig(args.output_dir / "followup.png", dpi=300)
        plt.close(fig)
    metadata = {"inputs_sha256": {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in [args.matched, args.duration]},
                "plot_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "style_source_sha256": hashlib.sha256(Path(__file__).with_name("style.py").read_bytes()).hexdigest(),
                "matplotlib": matplotlib.__version__, "tueplots": tueplots.__version__,
                "font": "DejaVu Sans", "status": "development_figures_not_final_paper_layout"}
    (args.output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")


if __name__ == "__main__":
    main()
