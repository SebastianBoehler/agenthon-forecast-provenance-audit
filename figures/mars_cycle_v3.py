"""Executive summary: show each completed MarS cycle cost and censored seed."""
import json
from pathlib import Path
import matplotlib.pyplot as plt
from style import paper_style

ROOT = Path("outputs/market-cycle/mars-external-v3")
OUT = Path("figures/generated/mars-external-v3")


def main():
    rows = json.loads((ROOT / "bank.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    with paper_style(5.8, 2.6):
        fig, ax = plt.subplots()
        colors = {"B": "#1d6a8a", "S": "#ba672e"}
        for direction, shift, label in (("B", -0.12, "Buy then sell"), ("S", 0.12, "Sell then buy")):
            completed = [r for r in rows if r["direction"] == direction and r["cycle_cost"] is not None]
            ax.scatter([r["noise_seed"] - 7100 + shift for r in completed],
                       [r["cycle_cost"] / 10000 for r in completed],
                       s=17, alpha=0.85, color=colors[direction], label=label, zorder=3)
        ax.axhline(0, linewidth=0.8, color="#555555")
        for seed in (2, 7, 27, 28):
            ax.axvspan(seed - 0.37, seed + 0.37, color="#777777", alpha=0.12, linewidth=0)
        ax.set(xlim=(0, 31), ylim=(-2, 10), xticks=(1, 5, 10, 15, 20, 25, 30),
               xlabel="Initialization seed index", ylabel="Completed-cycle cost (10,000 units)")
        ax.text(1.0, 9.2, "Shaded: initialization failed in both directions", fontsize=7)
        ax.legend(loc="upper right")
        fig.tight_layout()
        fig.savefig(OUT / "cycle_costs.pdf")
        fig.savefig(OUT / "cycle_costs.png", dpi=300)
        plt.close(fig)


if __name__ == "__main__":
    main()
