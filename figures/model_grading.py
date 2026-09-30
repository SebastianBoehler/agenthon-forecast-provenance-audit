"""Executive summary: plot format compliance and exploratory grader disagreements from saved answers."""
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from style import paper_style

SOURCE = Path('outputs/model-grading-v1')
DESTINATION = Path('figures/generated/model-grading-v1')
MODELS = {'qwen3-1.7b': 'Qwen3 1.7B', 'qwen3-4b': 'Qwen3 4B',
          'qwen2.5-coder-3b': 'Qwen2.5-Coder 3B',
          'deepseek-v3.2': 'DeepSeek V3.2'}
FAMILIES = {'cr_eq_gordon': 'Whole-unit Gordon', 'deriv_binomial_call': 'Binomial call',
            'eq_gordon': 'Ordinary Gordon', 'corp_wacc': 'WACC'}
POLICIES = {'source_abs_0.005': 'Original ±0.005', 'source_abs_0.5': 'Original ±0.5',
            'source_relative_5pct': 'Original 5%'}


def export(figure, name):
    for suffix in ['pdf', 'png', 'svg']:
        figure.savefig(DESTINATION / f'{name}.{suffix}', dpi=300)
    plt.close(figure)


def main():
    strict = json.loads((SOURCE / 'combined_results.json').read_text())
    numeric = json.loads((SOURCE / 'combined_numeric_sensitivity.json').read_text())
    DESTINATION.mkdir(parents=True, exist_ok=True)
    with paper_style(6.8, 2.9), plt.rc_context({'font.family': 'DejaVu Sans', 'pdf.fonttype': 42}):
        figure, axis = plt.subplots(layout='constrained')
        x = np.arange(len(MODELS))
        for offset, results, label, color in [
            (-.19, strict, 'Strict final-line compliance', '#0F4D92'),
            (.19, numeric, 'Exploratory numeric extraction', '#B64342'),
        ]:
            values = [results['models'][key]['aggregate']['parsed_completed'] for key in MODELS]
            axis.bar(x + offset, values, .38, color=color, label=label)
            for position, value in zip(x + offset, values):
                axis.text(position, value + 3, str(value), ha='center', fontsize=7)
        axis.set(xticks=x, xticklabels=list(MODELS.values()), ylim=(0,225),
                 yticks=[0,50,100,150,200], ylabel='Completed final answers (of 200)',
                 title='Output format is an additional measurement constraint')
        axis.legend(loc='upper left', fontsize=7)
        export(figure, 'format_compliance')
    labels = [f'{model}: {family}' for model in MODELS.values() for family in FAMILIES.values()]
    with paper_style(6.8, 5.8), plt.rc_context({'font.family': 'DejaVu Sans', 'pdf.fonttype': 42}):
        figure, axes = plt.subplots(1, 2, sharey=True)
        figure.subplots_adjust(left=.39, right=.88, bottom=.12, top=.85, wspace=.25)
        for axis, field, title in zip(axes, ['valid_rejected', 'numeric_invalid_accepted'],
                                     ['Numerically valid rejected', 'Numerically invalid accepted']):
            values = np.array([[numeric['models'][m]['families'][f]['policies'][p][field]
                                for p in POLICIES] for m in MODELS for f in FAMILIES])
            plot = axis.imshow(values, vmin=0, vmax=50, cmap='Blues', aspect='auto')
            for (i, j), count in np.ndenumerate(values):
                axis.text(j, i, str(count), ha='center', va='center', fontsize=7,
                          color='white' if count > 25 else 'black')
            axis.set(xticks=np.arange(3), xticklabels=['±0.005', '±0.5', '5%'],
                     yticks=np.arange(len(labels)), yticklabels=labels, title=title)
            axis.tick_params(axis='both', length=0)
        figure.colorbar(plot, ax=axes, fraction=.035, pad=.04,
                        label='Disagreements (of 50 questions per row)')
        figure.suptitle('Exploratory numeric-only grading of unchanged model answers', fontsize=9)
        export(figure, 'numeric_grader_disagreements')
    tracked = [SOURCE / name for name in ['combined_results.json', 'combined_numeric_sensitivity.json']]
    tracked += [Path(__file__), Path(__file__).with_name('style.py')]
    metadata = {'executive_summary': 'Strict endpoint and posthoc numeric sensitivity shown separately.',
                'input_and_source_hashes': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked},
                'denominators': {'aggregate_per_model': 200, 'per_family_per_model': 50},
                'matplotlib': matplotlib.__version__,
                'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(DESTINATION.glob('*')) if p.suffix in ['.pdf', '.png', '.svg']}}
    (DESTINATION / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')


if __name__ == '__main__':
    main()
