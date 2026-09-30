"""Executive summary: render the saved document panel with explicit endpoint denominators."""
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tueplots import fontsizes

from style import paper_style

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'figures/generated/document-evidence-v1'
RESULT = ROOT / 'outputs/finance-document-replay-v1/results.json'
ORDER = [('deepseek-v3.2', 'DeepSeek'), ('qwen3.5-9b', 'Qwen9B')]


def evidence():
    result = json.loads(RESULT.read_text())
    rows = []
    for model, label in ORDER:
        for arm in ['baseline', 'quantity_reminder']:
            r = result['models'][model][arm]
            a, f, t = r['aggregate'], r['sources']['finqa'], r['sources']['tatqa']
            unrounded = a['locked_matches_all_attempts']
            rounded = sum(s['later_precision_diagnostic']['matches'] for s in [f, t])
            assert a['attempts'] == 96 and a['locked_reference_cases'] == 62
            assert 0 <= unrounded <= rounded <= 62
            rows.append({'model': model, 'label': label, 'arm': arm,
                         'numeric': a['response_states'].get('answer', 0),
                         'unrounded': unrounded, 'rounded': rounded,
                         'finqa_fraction_credits': f['percent_fraction_sensitivity']['native_credits_all_attempts'],
                         'tatqa_em': int(t['native_channels']['tatqa_answer_em_sum']),
                         'tatqa_scale': t['native_channels']['tatqa_scale_correct'],
                         'composition': [unrounded, rounded - unrounded, 62 - rounded]})
    return {'executive_summary': 'Locked numerical/broad-unit agreement is a proxy; later rounding diagnostic is exploratory.',
            'source_sha256': hashlib.sha256(RESULT.read_bytes()).hexdigest(),
            'locked_subset': 62, 'attempts_per_arm': 96, 'source_attempts_per_arm': 48, 'rows': rows}


def table(data):
    lines = []
    for r in data['rows']:
        arm = 'Base' if r['arm'] == 'baseline' else 'Reminder'
        cells = [r['label'], arm, f"{r['numeric']}/96", f"{r['unrounded']}/62",
                 f"{r['rounded']}/62", f"{r['finqa_fraction_credits']}/48",
                 f"{r['tatqa_em']}/48", f"{r['tatqa_scale']}/48"]
        lines.append(' & '.join(cells) + r'\\')
    return '\n'.join(lines)


def tikz(data):
    colors = ['auditblue', 'auditblue!30', 'black!10']
    lines = [r'\begin{tikzpicture}[x=.29cm,y=.05cm,font=\scriptsize]']
    for y in [0, 20, 40, 62]:
        lines += [rf'\draw[black!12] (0,{y}) -- (48,{y});',
                  rf'\node[anchor=east] at (-1,{y}) {{{y}}};']
    for i, r in enumerate(data['rows']):
        x, bottom = i * 12 + 2, 0
        for count, color in zip(r['composition'], colors):
            top = bottom + count
            if count:
                lines.append(rf'\fill[{color}] ({x},{bottom}) rectangle ({x+7},{top});')
            bottom = top
        arm = 'Base' if r['arm'] == 'baseline' else 'Reminder'
        lines.append(rf'\node[align=center,anchor=north] at ({x+3.5},-2) {{{r["label"]}\\{arm}}};')
        lines.append(rf'\node[anchor=south] at ({x+3.5},63) {{{r["unrounded"]}/{r["rounded"]}}};')
    lines.append(r'\node[rotate=90] at (-6,31) {Cases in fixed numerical subset (62)};')
    for x, text, color in [(0, 'Unrounded match', colors[0]), (18, 'Rounded reference only', colors[1]),
                            (41, 'Other', colors[2])]:
        lines.append(rf'\fill[{color}] ({x},-19) rectangle ({x+1.5},-16);')
        lines.append(rf'\node[anchor=west] at ({x+2},-17.5) {{{text}}};')
    return '\n'.join(lines + [r'\end{tikzpicture}'])


def render(data):
    OUT.mkdir(parents=True, exist_ok=True)
    colors = ['#0F4D92', '#ADC4DD', '#E5E5E5']
    with paper_style(6.8, 2.8, 8), plt.rc_context({**fontsizes.tmlr2023(default_smaller=2),
            'svg.hashsalt': 'finance-document-evidence-v1', 'font.family': 'DejaVu Sans'}):
        fig, ax = plt.subplots()
        for i, row in enumerate(data['rows']):
            bottom = 0
            for count, color in zip(row['composition'], colors):
                ax.bar(i, count, bottom=bottom, color=color, width=.65, edgecolor='white', linewidth=.4)
                bottom += count
            ax.text(i, 63, f"{row['unrounded']}/{row['rounded']}", ha='center', fontsize=8)
        ax.set(ylim=(0, 69), yticks=[0, 20, 40, 62], ylabel='Cases (fixed subset n=62)',
               xticks=range(4), xticklabels=[r['label'] + '\n' + ('Base' if r['arm']=='baseline' else 'Reminder') for r in data['rows']])
        handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in colors]
        ax.legend(handles, ['Unrounded match', 'Rounded reference only (exploratory)', 'Other'],
                  ncol=3, loc='upper center', bbox_to_anchor=(.5, -.2), fontsize=7)
        fig.subplots_adjust(bottom=.28)
        for suffix in ['png', 'pdf', 'svg']:
            metadata = {'CreationDate': None, 'ModDate': None} if suffix=='pdf' else (
                {'Date': None} if suffix=='svg' else {'Software': 'document_evidence.py'})
            fig.savefig(OUT / f'document_panel.{suffix}', dpi=300, bbox_inches='tight', metadata=metadata)
        plt.close(fig)
    (OUT / 'metadata.json').write_text(json.dumps(data, indent=2) + '\n')
    (OUT / 'model_table.tikz').write_text(table(data) + '\n')
    (OUT / 'document_panel.tikz').write_text(tikz(data) + '\n')


if __name__ == '__main__':
    render(evidence())
