"""Executive summary: bind the standalone manuscript's document displays to saved results."""
import argparse
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    path = ROOT / 'figures/document_evidence.py'
    import sys
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location('document_evidence', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data = module.evidence()
    replacements = {'DOCUMENT_MODEL_TABLE': module.table(data),
                    'DOCUMENT_MODEL_FIGURE': module.tikz(data)}
    manuscript = ROOT / 'paper/answer_contract_audit.tex'
    original = text = manuscript.read_text()
    for name, value in replacements.items():
        start, end = f'% BEGIN GENERATED {name}\n', f'\n% END GENERATED {name}'
        a, b = text.index(start) + len(start), text.index(end)
        if args.check and text[a:b] != value:
            raise AssertionError(f'Saved-result display drift: {name}')
        text = text[:a] + value + text[b:]
    if not args.check:
        module.render(data)
        if text != original:
            manuscript.write_text(text)
    print('PASS: document displays match saved endpoint counts' if args.check else 'Rendered document table/TikZ and publication figure')


if __name__ == '__main__':
    main()
