"""Executive summary: export measured comparator trade-offs and input uncertainty geometry."""
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import tueplots

from style import paper_style

RESULT = Path('outputs/answer-contract-v1/results.json')
DESTINATION = Path('figures/generated/answer-contract-v1')
BLUE, RED, GRAY = '#0F4D92', '#B64342', '#767676'


def export(fig, name):
    for extension in ['pdf', 'png', 'svg']:
        fig.savefig(DESTINATION/f'{name}.{extension}', dpi=300)
    plt.close(fig)


def main():
    results = json.loads(RESULT.read_text())
    DESTINATION.mkdir(parents=True, exist_ok=True)
    with paper_style(6.8, 3.0, 8), plt.rc_context({'font.family': 'DejaVu Sans', 'pdf.fonttype': 42}):
        fig, axes = plt.subplots(1, 2)
        fig.subplots_adjust(top=.79, bottom=.18, left=.08, right=.99, wspace=.28)
        names = ['cosimo/cr_eq_gordon', 'cosimo/deriv_binomial_call']
        labels = ['Whole-unit Gordon', 'Binomial call']
        for axis, name, label in zip(axes, names, labels):
            base = results['comparators'][name]
            rows = [base[2], base[3], base[7], results['repairs'][name][0], results['repairs'][name][1]]
            tick_labels = ['±0.005','±0.5','5%','Formula\nonly','Full\ncontract']
            if name == 'cosimo/cr_eq_gordon':
                rows.insert(4, results['simple_integer_baseline'])
                tick_labels.insert(4, 'Integer +\n±0.5')
            x = np.arange(len(rows))
            fr = [r['valid_answer_rejected']/r['valid_answer_count']*100 for r in rows]
            fa = [r.get('source_invalid_rejected_accepted',0)/r.get('source_rejected_invalid',1)*100 for r in rows]
            axis.bar(x-.18, fr, .36, color=RED, edgecolor='black', linewidth=.4, label='Valid answers rejected')
            axis.bar(x+.18, fa, .36, color=BLUE, hatch='///', edgecolor='black', linewidth=.4, label='Source errors accepted')
            for i,(a,b) in enumerate(zip(fr,fa)):
                for dx,y in [(-.18,a),(.18,b)]:
                    if y>0: axis.text(i+dx,y+2,f'{y:.1f}',ha='center',fontsize=6)
            axis.set(xticks=x, xticklabels=tick_labels,
                     ylim=(0,112), yticks=[0,25,50,75,100], ylabel='Answers (%)', title=label)
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper center', ncol=2, fontsize=7)
        export(fig,'comparator_tradeoffs')
    with paper_style(6.8, 2.5, 8), plt.rc_context({'font.family': 'DejaVu Sans', 'pdf.fonttype': 42}):
        fig, axes = plt.subplots(1, 2, layout='constrained')
        spread = np.linspace(6.4,6.6,200)
        axes[0].plot(spread,74000/spread,color=BLUE)
        axes[0].scatter([6.5,6.49],[74000/6.5,74000/6.49],color=[GRAY,RED],s=22,zorder=4)
        axes[0].axvspan(6.4,6.6,color=BLUE,alpha=.10)
        axes[0].annotate('Visible inputs',xy=(6.5,74000/6.5),xytext=(6.51,11480),fontsize=7,
                         arrowprops={'arrowstyle':'-','color':GRAY})
        axes[0].annotate('Hidden target',xy=(6.49,74000/6.49),xytext=(6.41,11300),fontsize=7,
                         arrowprops={'arrowstyle':'-','color':RED})
        axes[0].set(xlabel='Discount rate − growth (percentage points)',ylabel='Terminal value ($)',
                    title='Rounded inputs permit a range of answers')
        x=np.array([30.5,30.94,31,31.49])
        axes[1].plot([30.5,31.5],[31,31],color=BLUE,linewidth=3)
        axes[1].scatter([30.94],[31],color=BLUE,s=25,label='Requested rounded answer')
        axes[1].scatter([30.94],[30.94],color=RED,s=25,label='Stored raw answer')
        axes[1].plot([30.94,30.94],[30.94,31],color=GRAY,linestyle=':')
        axes[1].set(xlim=(30.5,31.5),ylim=(30.85,31.06),xlabel='Raw formula value ($)',
                    ylabel='Final answer ($)',title='Output rounding projects onto an integer')
        axes[1].legend(loc='lower right',fontsize=6)
        export(fig,'contract_geometry')
    metadata={'results_sha256':hashlib.sha256(RESULT.read_bytes()).hexdigest(),
              'plot_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'style_sha256':hashlib.sha256(Path(__file__).with_name('style.py').read_bytes()).hexdigest(),
              'matplotlib':matplotlib.__version__,'tueplots':tueplots.__version__,
              'design_reference':'https://github.com/ChenLiu-1996/figures4papers',
              'palette':[BLUE,RED,GRAY],'font':'DejaVu Sans','exports':['pdf','png','svg'],
              'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(DESTINATION.glob('*'))
                       if p.suffix in ['.pdf','.png','.svg']}}
    (DESTINATION/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')


if __name__=='__main__':
    main()
