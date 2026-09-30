"""Executive summary: bind the submission's census and figure counts to saved analyses."""
from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def check():
    text = (ROOT / 'paper/answer_contract_voice_draft.tex').read_text()
    census = json.loads((ROOT / 'artifacts/financial-audit-summary-v1/results.json').read_text())['families']
    assert sum(r['rows'] for r in census.values()) == 12655
    assert sum(r['unique_questions'] for r in census.values()) == 10476
    for label, key in [('Binomial call', 'cosimo/deriv_binomial_call'),
                       ('Whole-unit Gordon', 'cosimo/cr_eq_gordon'), ('CAPM', 'cosimo/port_capm')]:
        row = census[key]
        expected = f"{label} & {row['rows']:,} & {row['unique_questions']:,} & {row['gold_invalid_exact_contract']:,}"
        assert expected in text, expected
    analysis = json.loads((ROOT / 'artifacts/grader-comparison-v1/analysis.json').read_text())
    counts = {}
    for model, y, top in [('gemma', '-.6', '-.25'), ('qwen', '-2.6', '-2.25')]:
        rows = [r for k, r in analysis['counts'].items() if k.startswith(model + '/') and k.endswith('/finance')]
        counts[model] = {k: sum(r[k] for r in rows) for k in
                         ['attempted', 'released_label_cent_accept', 'complete_contract_accept', 'valid_denied_by_label']}
        assert counts[model]['attempted'] == 24
        assert counts[model]['released_label_cent_accept'] == 6
        number = counts[model]['complete_contract_accept']
        assert f'(0,{y}) rectangle ({number},{top})' in text
    assert sum(r['valid_denied_by_label'] for r in counts.values()) == 16
    extension = json.loads((ROOT / 'artifacts/final-model-extensions-v1/analysis.json').read_text())
    assert extension['counts']['glm/finance']['complete_contract'] == 17
    assert extension['counts']['llama/math']['unequal_credit'] == 2
    assert 'seven released-label credits versus 17 question-contract credits' in text
    assert 'The two unequal credits are repeated answers of zero' in text
    cited = {k.strip() for g in re.findall(r'\\cite\{([^}]+)\}', text) for k in g.split(',')}
    bib = re.findall(r'\\bibitem\{([^}]+)\}', text)
    assert len(bib) == len(set(bib)) and set(bib) == cited
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    assert len(labels) == len(set(labels))
    assert set(re.findall(r'\\ref\{([^}]+)\}', text)) <= set(labels)
    environments = Counter(re.findall(r'\\begin\{([^}]+)\}', text))
    assert environments == Counter(re.findall(r'\\end\{([^}]+)\}', text))
    assert '\\FloatBarrier\n\\Needspace{23\\baselineskip}\n\\begin{samepage}' in text
    return {'status': 'PASS', 'cited_sources': len(cited), 'local_financial_counts': counts,
            'scope': 'Saved census/figure counts, references and source structure; not PDF layout or semantic certification'}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
