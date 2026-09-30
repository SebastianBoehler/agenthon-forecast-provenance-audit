"""Executive summary: verify actual packet isolation, grouping and prospective timing."""
from __future__ import annotations

import json
from datetime import datetime

from common import CONFIG, FREEZE, OUT, ROOT, digest, read_json, require_freeze, timestamp, write_json


def rows(name: str) -> list[dict]:
    return [json.loads(line) for line in (OUT / name).read_text().splitlines()]


def no_target_fields(value: object) -> None:
    forbidden = {"answer", "exe_ans", "program", "program_re", "gold_inds",
                 "derivation", "scale", "facts", "mapping", "mappings", "answer_type", "answer_from"}
    if isinstance(value, dict):
        assert not forbidden.intersection(value), "Source annotation leaked into reviewer context"
        for item in value.values():
            no_target_fields(item)
    elif isinstance(value, list):
        for item in value:
            no_target_fields(item)


def main() -> None:
    freeze = require_freeze()
    ingestion = read_json(OUT / "ingestion_manifest.json")
    manifest = read_json(OUT / "selection_manifest.json")
    config = read_json(CONFIG)
    selected = rows("selection_metadata.jsonl")
    ids = [r["source"] + ":" + r["native_id"] for r in selected]
    assert len(ids) == len(set(ids))
    assert len({r["context_sha256"] for r in selected}) == len(selected)
    for source in config["sources"]:
        source_rows = [r for r in selected if r["source"] == source]
        assert len({r["group_id"] for r in source_rows}) == len(source_rows)
        assert len(source_rows) == manifest["sampling"][source]["selected"]
        assert len(source_rows) <= config["target_per_source"]
    frozen_at = datetime.fromisoformat(ingestion["freeze_utc"])
    for artifact in ingestion["artifacts"]:
        assert frozen_at < datetime.fromisoformat(artifact["downloaded_utc"])
        assert digest((ROOT / artifact["path"]).read_bytes()) == artifact["sha256"]
    assert digest(FREEZE.read_bytes()) == manifest["protocol_freeze_sha256"]
    for name, expected in manifest["artifacts_sha256"].items():
        assert digest((OUT / name).read_bytes()) == expected
    sheets = {}
    for reviewer in ("a", "b"):
        sheet = rows(f"reviewer_{reviewer}.jsonl")
        assert [r["case_id"] for r in sheet] == ids
        for row in sheet:
            assert set(row) == {"case_id", "reviewer", "question", "original_context", "rubric", "review_status"}
            assert row["reviewer"] == reviewer and row["review_status"] == "blank_not_reviewed"
            assert row["rubric"] == {field: "" for field in config["blank_rubric_fields"]}
            no_target_fields(row["original_context"])
        sheets[reviewer] = sheet
    for a, b in zip(sheets["a"], sheets["b"]):
        assert {k: v for k, v in a.items() if k != "reviewer"} == {
            k: v for k, v in b.items() if k != "reviewer"}
    targets = rows("source_targets.jsonl")
    assert [r["case_id"] for r in targets] == ids
    for packet, target in zip(sheets["a"], targets):
        assert packet["question"] == target["original_annotation"]["question"]
    write_json(OUT / "preparation_checks.json", {
        "executive_summary": "Actual prepared artifacts pass timing, identity, grouping and gold-isolation checks; no financial answer evaluated.",
        "checked_utc": timestamp(), "status": "PASS", "selected_cases": len(selected),
        "blank_independent_reviewer_sheets": 2, "human_reviews_completed": 0,
        "financial_answers_recomputed": 0, "models_called": 0,
        "protocol_freeze_sha256": digest(FREEZE.read_bytes()),
        "selection_manifest_sha256": digest((OUT / "selection_manifest.json").read_bytes())
    })


if __name__ == "__main__":
    main()
