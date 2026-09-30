"""Executive summary: render hash-bound TikZ counts without treating AI review as expert truth."""

import json
from pathlib import Path

from financial_review_io import digest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'outputs/finance-expression-review-v1/semantic_results.json'
OUT = ROOT/'paper/generated/finance_semantic_review.tikz'
data = json.loads(SOURCE.read_text())
lines = [r'\begin{figure}[!ht]',r'\centering',r'\begin{tikzpicture}[x=.08cm,y=1cm,font=\scriptsize]']
groups = [('All reviewed expressions',data['all_reviewed'],1.5),
          (r'Reported mismatch $\rightarrow$ expression match',data['numeric_transitions'],0)]
for label,row,y in groups:
    c = row['joint_categories']
    counts = [c.get('supported_both',0),c.get('contradicted_either',0),row['ambiguous_or_unresolved_either']]
    assert sum(counts) == row['expressions']
    lines.append(r'\node[anchor=west] at (0,'+str(y+.8)+') {'+label+f"; $n={row['expressions']}$"+'};')
    start = 0
    for count,color in zip(counts,['auditblue','auditred','black!25']):
        if count:
            lines.append(r'\fill['+color+f'] ({start},{y}) rectangle ({start+count},{y+.45});')
            textcolor = 'black' if color == 'black!25' else 'white'
            lines.append(r'\node[text='+textcolor+f'] at ({start+count/2},{y+.225}) '+'{'+str(count)+'};')
        start += count
for i,(color,label) in enumerate([('auditblue','Both supported under assumptions'),('auditred','Both contradicted'),('black!25','Ambiguous or disagreement')]):
    x=i*48
    lines += [r'\fill['+color+f'] ({x},-.7) rectangle ({x+3},-.5);',r'\node[anchor=west] at ('+str(x+4)+',-.6) {'+label+'};']
lines += [r'\end{tikzpicture}',
    r'\caption{Outcome-masked posthoc AI technical review. Counts are expression instances, not independent questions or expert labels. All 131 instances span 58 questions; 253 of the original 384 attempts are outside this subset. The gray group contains three consensus ambiguities and ten status disagreements. Of 47 numerical grading transitions across 24 questions, 41 across 22 questions receive support from both reviewers; six across two questions retain disagreement. All 14 consensus contradictions were already numerical mismatches under both reported and executed values.}',
    r'\label{fig:expression-semantics}',r'\end{figure}']
OUT.parent.mkdir(exist_ok=True)
OUT.write_text('\n'.join(lines)+'\n')
metadata = dict(source=str(SOURCE.relative_to(ROOT)),source_sha256=digest(SOURCE),
    renderer_sha256=digest(__file__),output_sha256=digest(OUT),
    scope='AI-only, posthoc, outcome masked with prior exposure; full study denominator remains 384.')
(ROOT/'paper/generated/finance_semantic_review_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps(metadata))
