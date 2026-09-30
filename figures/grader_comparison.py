"""Executive summary: render the fixed control tradeoff with tueplots and an embedded TikZ companion."""

import hashlib
import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from style import paper_style

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/grader-comparison-v1/analysis.json"
LABELS = [("native", "Native"), ("without_intpart", "No integer part"),
          ("without_digits", "No digits-only"), ("without_both", "Neither"),
          ("exact", "Exact rational")]


def main():
    report = json.loads(SOURCE.read_text())
    controls = report["controls"]
    output = ROOT / "figures/generated"
    output.mkdir(parents=True, exist_ok=True)
    with paper_style(6.3, 2.6, 8):
        fig, axes = plt.subplots(1, 2, sharey=True, constrained_layout=True)
        for ax, endpoint, title, total, color in zip(
            axes, ("false_accepts", "false_rejects"),
            ("Unequal value credited", "Equivalent value rejected"),
            (1097, 1451), ("#C34D4D", "#386C9B"), strict=True):
            values = [controls[key][endpoint] for key, _ in LABELS]
            ax.barh(range(5), values, color=color, height=0.58)
            ax.set_xlim(0, 510)
            ax.set_yticks(range(5), [label for _, label in LABELS])
            ax.set_xlabel(f"Count; {total:,} authored controls")
            ax.set_title(title, loc="left")
            for y, value in enumerate(values):
                ax.text(value + 7, y, str(value), va="center", fontsize=7)
        axes[0].invert_yaxis()
        for extension in ("pdf", "svg"):
            fig.savefig(output / f"grader-comparison.{extension}", bbox_inches="tight")
        plt.close(fig)
    lines = [r"% Executive summary: fixed authored-control counts; generated from the scalar artifact.",
             r"\begin{tikzpicture}[x=.006cm,y=.5cm,font=\scriptsize]",
             r"\node[anchor=west,font=\small] at (0,1) {Unequal credit};",
             r"\node[anchor=west,font=\small] at (610,1) {Equivalent rejection};"]
    for i, (key, label) in enumerate(LABELS):
        y = -i
        lines.append(r"\node[anchor=east] at (-10," + str(y) + ") {" + label + "};")
        for offset, endpoint, color in ((0, "false_accepts", "auditred"), (610, "false_rejects", "auditblue")):
            value = controls[key][endpoint]
            lines.append(f"\\fill[{color}!75] ({offset},{y-.2}) rectangle ({offset+value},{y+.2});")
            lines.append(f"\\node[anchor=west] at ({offset+value+6},{y}) {{{value}}};")
    lines.extend([r"\end{tikzpicture}", ""])
    generated = ROOT / "paper/generated/grader_comparison.tikz"
    generated.write_text("\n".join(lines))
    metadata = {"source": str(SOURCE.relative_to(ROOT)), "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                "renderer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "tikz_sha256": hashlib.sha256(generated.read_bytes()).hexdigest(),
                "denominators": {"equal": 1451, "unequal": 1097},
                "scope": "authored grouped controls; not model accuracy or prevalence"}
    (ROOT / "paper/generated/grader_comparison_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    paper = ROOT / "paper/answer_contract_audit.tex"
    text = paper.read_text()
    start, end = "% BEGIN GENERATED GRADER FIGURE", "% END GENERATED GRADER FIGURE"
    figure = start + "\n" + generated.read_text() + end
    if start in text:
        before, rest = text.split(start, 1)
        _, after = rest.split(end, 1)
        text = before + figure + after
    else:
        text = text.replace(r"\section{Final scalar comparison protocol}", r"""\begin{figure}[!ht]
\centering
""" + figure + r"""
\caption{Authored-control loss under each comparison rule. Denominators are 1,097 unequal and 1,451 equivalent pairs. Zero exact-rational losses establish consistency on the admitted grammar; grouped controls do not estimate benchmark error prevalence.}
\label{fig:grader-comparison}
\end{figure}

\section{Final scalar comparison protocol}""", 1)
    paper.write_text(text)
    print(json.dumps(metadata))


if __name__ == "__main__":
    main()
