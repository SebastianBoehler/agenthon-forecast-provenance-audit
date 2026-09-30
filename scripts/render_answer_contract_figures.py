"""Executive summary: embed measured TikZ into the existing standalone manuscript.

The native editor compiles a single source file. Keep coordinates and count
generation reproducible while embedding the result rather than external includes.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'figures'))
from paper_evidence import evidence, tikz

PAPER = ROOT / 'paper/answer_contract_audit.tex'
BEGIN = '% BEGIN GENERATED GRADING_FIGURE'
END = '% END GENERATED GRADING_FIGURE'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text = PAPER.read_text()
    assert text.count(BEGIN) == text.count(END) == 1
    before, remainder = text.split(BEGIN)
    _, after = remainder.split(END)
    expected = before + BEGIN + '\n' + tikz(evidence()) + END + after
    if args.check:
        assert text == expected, 'Embedded figure differs from saved-result rendering'
        print('PASS: embedded TikZ agrees with saved grading results')
    else:
        PAPER.write_text(expected)


if __name__ == '__main__':
    main()
