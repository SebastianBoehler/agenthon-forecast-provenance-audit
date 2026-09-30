"""Executive summary: reuse frozen V1 scoring for the disclosed execution repeat."""
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


if __name__ == '__main__':
    report = runpy.run_path(str(ROOT / 'scripts/report_finance_adaptation.py'))
    report['main'].__globals__['OUT'] = ROOT / 'outputs/finance-adaptation-v2'
    report['main']()
    document = ROOT / 'docs/FINANCE_ADAPTATION_RESULTS_V1.md'
    note = ('\nExecution note: these are V2 results after a disclosed logging repair. '
            'The incomplete V1 attempt remains intact with459 calls and no holdouts. '
            'The repeat uses unchanged scientific rules and a separate prospective '
            'execution freeze; it is a feasibility rerun after observed development outputs. '
            'See FINANCE_ADAPTATION_EXECUTION_AMENDMENT.md.\n')
    document.write_text(document.read_text() + note)
