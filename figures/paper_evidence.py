"""Executive summary: render saved grading counts with tueplots and inline TikZ.

The strict four-model endpoint and exploratory two-model ordering stay separate.
No inference, confidence intervals or causal model-size claims are introduced.
"""
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import tueplots
from tueplots import figsizes, fontsizes

from style import paper_style

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'figures/generated/paper-evidence-v1'
MODELS = {'qwen3-1.7b': 'Qwen3 1.7B', 'qwen3-4b': 'Qwen3 4B',
          'qwen2.5-coder-3b': 'Qwen2.5-Coder 3B', 'deepseek-v3.2': 'DeepSeek V3.2'}
COLORS = ['#0F4D92', '#B64342', '#767676', '#E5E5E5']
KINDS = ['Valid, source credited', 'Valid, source denied',
         'Parsed, contract mismatch', 'Final line unparsed']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence():
    paths = [ROOT / 'outputs/model-grading-v1' / name for name in
             ('combined_results.json', 'combined_numeric_sensitivity.json')]
    strict, numeric = [json.loads(p.read_text()) for p in paths]
    rows = []
    for key, label in MODELS.items():
        a = strict['models'][key]['aggregate']
        denied = a['policies']['source_abs_0.005']['valid_rejected']
        counts = [a['visible_valid'] - denied, denied,
                  a['parsed_completed'] - a['visible_valid'],
                  a['attempts'] - a['parsed_completed']]
        assert min(counts) >= 0 and sum(counts) == a['attempts'] == 200
        rows.append({'model': key, 'label': label, 'counts': counts})
    ordering = []
    for key in ('qwen3-1.7b', 'deepseek-v3.2'):
        a = numeric['models'][key]['families']['cr_eq_gordon']
        assert a['attempts'] == 50
        ordering.append({'model': key, 'label': MODELS[key],
                         'source_credit': a['policies']['source_abs_0.005']['accepted'],
                         'integer_valid': a['visible_valid'], 'attempts': a['attempts']})
    return {'executive_summary': 'Finite saved-response counts; strict and posthoc endpoints separated.',
            'source_sha256': {str(p.relative_to(ROOT)): digest(p) for p in paths},
            'strict_composition': rows, 'exploratory_gordon_ordering': ordering,
            'kinds': KINDS, 'strict_denominator_per_model': 200,
            'exploratory_denominator_per_model': 50}


def plot(data):
    size = figsizes.tmlr2023(rel_width=6.8 / 6.5, ncols=2,
                            height_to_width_ratio=.94)
    with paper_style(6.8, 3.2, 8), plt.rc_context({
            **size, **fontsizes.tmlr2023(default_smaller=2),
            'font.family': 'DejaVu Sans', 'pdf.fonttype': 42,
            'svg.hashsalt': 'answer-contract-paper-evidence-v1'}):
        fig, axes = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1.42, 1]})
        left = np.zeros(4)
        y = np.arange(4)
        for col, (kind, color) in enumerate(zip(KINDS, COLORS)):
            values = np.array([r['counts'][col] for r in data['strict_composition']])
            axes[0].barh(y, values, left=left, height=.58, label=kind,
                         color=color, edgecolor='white', linewidth=.5,
                         hatch='///' if col == 1 else None)
            for pos, start, value in zip(y, left, values):
                if value >= 12:
                    axes[0].text(start + value / 2, pos, str(value),
                                 va='center', ha='center', fontsize=7,
                                 color='black' if col == 3 else 'white')
            left += values
        axes[0].set(yticks=y, yticklabels=list(MODELS.values()), xlim=(0, 200),
                    xticks=[0, 50, 100, 150, 200], xlabel='Saved responses (200 per model)',
                    title='(a) Strict final-line endpoint')
        axes[0].invert_yaxis()
        axes[0].legend(loc='upper center', bbox_to_anchor=(.4, -.3),
                       ncol=2, fontsize=6.5, handlelength=1.4)
        for r, color, marker in zip(data['exploratory_gordon_ordering'],
                                    COLORS[:2], ['o', 's']):
            values = [r['source_credit'], r['integer_valid']]
            axes[1].plot([0, 1], values, color=color, marker=marker,
                         linewidth=1.4, label=r['label'])
            for x, value in enumerate(values):
                axes[1].annotate(str(value), (x, value), xytext=(5, 4),
                                 textcoords='offset points', fontsize=7, color=color)
        axes[1].set(xlim=(-.16, 1.25), ylim=(0, 58), yticks=[0, 10, 20, 30, 40, 50],
                    xticks=[0, 1], xticklabels=['Source credit', 'Integer valid'],
                    ylabel='Answers (same 50 per model)',
                    title='(b) Exploratory whole-unit Gordon')
        axes[1].legend(loc='lower right', fontsize=7)
        for suffix in ('pdf', 'png', 'svg'):
            metadata = {'CreationDate': None, 'ModDate': None} if suffix == 'pdf' else (
                {'Date': None} if suffix == 'svg' else {'Software': 'paper_evidence.py'})
            fig.savefig(OUT / f'grading_evidence.{suffix}', dpi=300, metadata=metadata)
        plt.close(fig)


def tikz(data):
    lines = [r'\begin{figure}[!ht]', r'\centering',
             r'\begin{tikzpicture}[font=\scriptsize]',
             r'\node[anchor=west,font=\small] at (-2.1,3.45) {(a) Strict final-line endpoint};']
    colors = ['auditblue', 'auditred', 'black!55', 'black!9']
    for i, row in enumerate(data['strict_composition']):
        y, start = 2.8 - i * .68, 0
        lines.append(rf'\node[anchor=east] at (-.12,{y + .18:.3f}) {{{row["label"]}}};')
        for j, count in enumerate(row['counts']):
            if count:
                a, b = start * .026, (start + count) * .026
                lines.append(rf'\filldraw[fill={colors[j]},draw=white,line width=.3pt] '
                             rf'({a:.3f},{y:.3f}) rectangle ({b:.3f},{y + .36:.3f});')
                if count >= 12:
                    text_color = 'black' if j == 3 else 'white'
                    lines.append(rf'\node[text={text_color}] at ({(a+b)/2:.3f},{y+.18:.3f}) {{{count}}};')
                start += count
    lines.append(r'\draw[black!55] (0,.57) -- (5.2,.57);')
    for count in (0, 50, 100, 150, 200):
        x = count * .026
        lines.append(rf'\draw[black!55] ({x:.3f},.57) -- ({x:.3f},.51); '
                     rf'\node[anchor=north] at ({x:.3f},.49) {{{count}}};')
    lines.append(r'\node at (2.6,.03) {Saved responses (200 per model)};')
    for i, (kind, color) in enumerate(zip(KINDS, colors)):
        x, y = (i % 2) * 3.05 - 1.7, -.48 - (i // 2) * .35
        lines.append(rf'\fill[{color}] ({x:.3f},{y:.3f}) rectangle ({x+.16:.3f},{y+.14:.3f}); '
                     rf'\node[anchor=west] at ({x+.22:.3f},{y+.07:.3f}) {{{kind}}};')
    lines += [r'\begin{scope}[xshift=7.45cm]',
              r'\node[anchor=west,font=\small,align=left] at (-.25,3.45) {(b) Exploratory whole-unit Gordon};',
              r'\draw[black!55] (0,0) -- (0,3.1);',
              r'\draw[black!55] (0,0) -- (3.1,0);']
    for n in (0, 20, 40, 50):
        lines.append(rf'\node[anchor=east] at (-.08,{n*.06:.3f}) {{{n}}};')
    for row, color, shape in zip(data['exploratory_gordon_ordering'],
                                  colors[:2], ['circle', 'rectangle']):
        a, b = row['source_credit'] * .06, row['integer_valid'] * .06
        lines.append(rf'\draw[{color},line width=.9pt] (0,{a:.3f}) -- (3,{b:.3f});')
        for x, y, count in [(0, a, row['source_credit']), (3, b, row['integer_valid'])]:
            lines.append(rf'\node[{shape},fill={color},inner sep=1.5pt] at ({x},{y:.3f}) {{}}; '
                         rf'\node[anchor=south west,text={color}] at ({x+.08},{y+.03:.3f}) {{{count}}};')
        lines.append(rf'\node[anchor=west,text={color}] at (.7,{b-.35:.3f}) {{{row["label"]}}};')
    lines += [r'\node[align=center,anchor=north] at (0,-.18) {Source credit\\$\pm0.005$};',
              r'\node[align=center,anchor=north] at (3,-.18) {Integer\\validity};',
              r'\node at (1.5,-.85) {Same 50 answers per model};', r'\end{scope}',
              r'\end{tikzpicture}',
              r'\caption{Grading saved answers without changing inference. (a) Counts partition all 200 responses per model; the reconstructed original-label comparator denies credit to 55 of 136 valid strict-format DeepSeek answers. Gray separates contract mismatch from final-line parsing failure; validity uses the declared $1+r$ convention, and DeepSeek\textquotesingle s one mismatch is compatible with continuous compounding. (b) Separately recorded post hoc extraction reverses the ordering of two models on the 50-question whole-unit Gordon family. This is not a general model ranking or a training effect. Zero-width categories are omitted visually; Table~\ref{tab:models} reports exact counts.}',
              r'\label{fig:grading-evidence}', r'\end{figure}']
    return '\n'.join(lines) + '\n'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    data = evidence()
    plot(data)
    (OUT / 'grading_evidence.tikz').write_text(tikz(data))
    data.update({'plot_source_sha256': digest(Path(__file__)),
                 'style_sha256': digest(Path(__file__).with_name('style.py')),
                 'matplotlib': matplotlib.__version__, 'tueplots': tueplots.__version__,
                 'sizing': 'tueplots TMLR base adjusted to actual 6.8-inch manuscript text width',
                 'design_reference': 'figures4papers/f0bb7559abe90f5e1828797126d4d133c1bd47d7',
                 'files': {p.name: digest(p) for p in sorted(OUT.iterdir())
                           if p.suffix in ('.png', '.pdf', '.svg', '.tikz')}})
    (OUT / 'metadata.json').write_text(json.dumps(data, indent=2) + '\n')


if __name__ == '__main__':
    main()
