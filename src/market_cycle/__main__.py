"""Executive summary: explicit-config CLI for the controlled reference pilot."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from .pilot import run_pilot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        raw = args.config.read_bytes()
        result = run_pilot(json.loads(raw))
        result["config_sha256"] = hashlib.sha256(raw).hexdigest()
        package = Path(__file__).parent
        result["source_sha256"] = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(package.glob("*.py"))
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x") as stream:
            json.dump(result, stream, indent=2, allow_nan=False)
            stream.write("\n")
        print(f"Reference controls saved: {args.output}")
        for name, models in result["results"].items():
            print(name, {key: round(value["sample_mean_cost"], 6) for key, value in models.items()})
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"market-cycle: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
