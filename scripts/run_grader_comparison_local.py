"""Executive summary: run one frozen local model arm, without retries or paid requests."""

import argparse
from grader_comparison.local import collect

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", choices=("gemma", "qwen"))
    collect(parser.parse_args().model)
