"""Executive summary: execute the frozen census, comparators and correction ablations."""
import hashlib
import json
import platform
from collections import defaultdict
from decimal import localcontext
from pathlib import Path

import pandas
import pyarrow

from answer_contract.experiment import comparator_rows, integer_filter_baseline, repairs, rounded_error_controls, row_record, summarize
from answer_contract.sources import SOURCES, cosimo_cases, rlvr_cases
from answer_contract.repair import repair_record


def main():
    destination = Path('outputs/answer-contract-v1')
    destination.mkdir(parents=True, exist_ok=True)
    with localcontext() as context:
        context.prec = 50
        cases = cosimo_cases() + rlvr_cases()
        families = defaultdict(list)
        for case in cases:
            families[f'{case.source}/{case.family}'].append(case)
        results = {'status': 'executed_selected_family_audit_not_training_effect',
                   'families': {name: summarize(rows) for name, rows in sorted(families.items())},
                   'comparators': {name: comparator_rows(rows) for name, rows in sorted(families.items())},
                   'repairs': {name: repairs(rows) for name, rows in sorted(families.items())},
                   'rounded_error_controls': rounded_error_controls(cases),
                   'simple_integer_baseline': integer_filter_baseline(cases)}
        records = [row_record(case) for case in cases]
        patches = [repair_record(case) for case in cases]
    (destination/'rows.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in records))
    (destination/'results.json').write_text(json.dumps(results, indent=2)+'\n')
    (destination/'numerical-patches.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in patches))
    code_paths = sorted(Path('src/answer_contract').glob('*.py')) + [Path(__file__)]
    protocol = Path('docs/ANSWER_CONTRACT_PROTOCOL_V1.md')
    amendment = Path('docs/ANSWER_CONTRACT_PROTOCOL_AMENDMENTS.md')
    hashes = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in code_paths+[protocol, amendment]}
    manifest = {'sources': SOURCES, 'code_and_protocol_sha256': hashes,
                'command': '.venv/bin/python scripts/run_answer_contract.py',
                'python': platform.python_version(), 'pandas': pandas.__version__,
                'pyarrow': pyarrow.__version__, 'decimal_precision': 50,
                'output_sha256': {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                  for path in sorted(destination.glob('*.json*')) if path.name!='manifest.json'}}
    (destination/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(results['families'], indent=2))


if __name__ == '__main__':
    main()
