"""Executive summary: check a completed blind technical review without opening native labels."""
import argparse
import json
from pathlib import Path

from finance_document_review.review_validation import validate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reviewer", choices=["a", "b"])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = validate(args.reviewer)
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps({key: result[key] for key in [
        "status", "cases", "reviewer", "statuses", "arithmetic_errors",
        "reported_output_projection_checks", "native_targets_accessed"
    ]}, indent=2))
    if result["arithmetic_errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
