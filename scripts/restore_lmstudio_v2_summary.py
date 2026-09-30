"""Executive summary: preserve and copy a misrouted V2 summary without changing results."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "outputs/model-grading-lmstudio-v1/results.json"
TARGET = ROOT / "outputs/model-grading-lmstudio-v2/results.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    data = SOURCE.read_bytes()
    result = json.loads(data)
    freeze = TARGET.parent / "freeze.json"
    if result["freeze_sha256"] != sha(freeze):
        raise ValueError("Misrouted summary does not identify the V2 freeze")
    if not result["complete"] or result["attempts"] != 200:
        raise ValueError("Expected the completed 200-question V2 summary")
    with TARGET.open("xb") as stream:
        stream.write(data)
    receipt = {
        "executive_summary": (
            "Reporting-only correction: the frozen analyzer's imported writer "
            "retained its V1 output directory; identical V2 summary bytes are copied."
        ),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(SOURCE.relative_to(ROOT)),
        "target": str(TARGET.relative_to(ROOT)),
        "source_sha256": sha(SOURCE),
        "target_sha256": sha(TARGET),
        "correction_script_sha256": sha(Path(__file__)),
        "original_preserved": True,
        "inference_repeated": False,
        "scoring_changed": False,
        "frozen_code_changed": False,
    }
    with (TARGET.parent / "summary_path_correction.json").open("x") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
