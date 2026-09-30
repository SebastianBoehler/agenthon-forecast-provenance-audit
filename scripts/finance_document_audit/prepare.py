"""Executive summary: freeze first, fetch pinned local sources, then select blank packets."""
from __future__ import annotations

import argparse
import hashlib
import platform
import urllib.request
from pathlib import Path

from admission import (finqa_identity, overlap_inventory, reviewer_packets,
                       schema_inventory, source_targets, tatqa_identity)
from common import (CONFIG, FREEZE, OUT, ROOT, digest, freeze_amendment, freeze_protocol, read_json,
                    require_freeze, timestamp, write_json, write_jsonl)
from sampling import finqa_candidates, select, tatqa_candidates


def fetch() -> None:
    freeze = require_freeze()
    config = read_json(CONFIG)
    records = []
    for source, spec in config["sources"].items():
        for name, artifact in spec["artifacts"].items():
            destination = OUT / "raw" / source / artifact["path"]
            if destination.exists():
                raise ValueError("Existing source artifact; refusing replacement")
            url = f'https://raw.githubusercontent.com/{spec["repository"]}/{spec["revision"]}/{artifact["path"]}'
            with urllib.request.urlopen(url, timeout=90) as response:
                data = response.read()
            git_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            if git_blob != artifact["git_blob"]:
                raise ValueError(f"Pinned source blob mismatch: {source}/{name}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as stream:
                stream.write(data)
            records.append({"source": source, "artifact": name, "url": url,
                            "path": str(destination.relative_to(ROOT)), "bytes": len(data),
                            "git_blob": git_blob, "sha256": digest(data), "downloaded_utc": timestamp()})
    write_json(OUT / "ingestion_manifest.json", {
        "executive_summary": "Full corpus and notices downloaded locally only after the prospective protocol freeze.",
        "freeze_utc": freeze["created_utc"], "freeze_sha256": digest(FREEZE.read_bytes()),
        "finished_utc": timestamp(), "artifacts": records, "status": "downloaded_not_selected"
    })


def load_sources() -> tuple[dict, dict]:
    require_freeze()
    config = read_json(CONFIG)
    manifest = read_json(OUT / "ingestion_manifest.json")
    for artifact in manifest["artifacts"]:
        if digest((ROOT / artifact["path"]).read_bytes()) != artifact["sha256"]:
            raise ValueError("Local source artifact changed after ingestion")
    files = {}
    for source, spec in config["sources"].items():
        files[source] = {name: read_json(OUT / "raw" / source / artifact["path"])
                         for name, artifact in spec["artifacts"].items() if artifact["path"].endswith(".json")}
    return config, files


def inspect() -> None:
    _, files = load_sources()
    inventories = [schema_inventory(rows, source + ":" + name)
                   for source, artifacts in files.items() for name, rows in artifacts.items()]
    write_json(OUT / "schema_inventory_v1a.json", {
        "executive_summary": "Root schema inspected after freeze; no cases selected and no gold correctness examined.",
        "created_utc": timestamp(), "inventories": inventories,
        "finqa_identity": finqa_identity(files["finqa"]["public_test"], files["finqa"]["evaluator_test"]),
        "tatqa_identity": tatqa_identity(files["tatqa"]["public_test"], files["tatqa"]["public_test_gold"])
    })


def prepare() -> None:
    config, files = load_sources()
    if not (OUT / "schema_inventory_v1a.json").exists():
        raise ValueError("Inspect and review source identities before selecting")
    salt = config["selection_salt"]
    fq, fq_meta = finqa_candidates(files["finqa"]["public_test"], salt)
    tq, tq_meta = tatqa_candidates(files["tatqa"]["public_test"], files["tatqa"]["public_test_gold"],
                                    salt, config["sources"]["tatqa"]["eligible_answer_types"])
    contexts, questions, selected, sampling = set(), set(), [], {}
    for source, candidates in (("finqa", fq), ("tatqa", tq)):
        chosen, result = select(candidates, config["target_per_source"], contexts, questions)
        selected.extend(chosen)
        sampling[source] = result
    write_jsonl(OUT / "admitted_pool_metadata.jsonl", [r.metadata() for r in fq + tq])
    write_jsonl(OUT / "selection_metadata.jsonl", [r.metadata() for r in selected])
    for reviewer in ("a", "b"):
        write_jsonl(OUT / f"reviewer_{reviewer}.jsonl", reviewer_packets(selected, config["blank_rubric_fields"], reviewer))
    write_jsonl(OUT / "source_targets.jsonl", source_targets(selected, files["finqa"]["public_test"],
                                                            files["tatqa"]["public_test"],
                                                            files["tatqa"]["public_test_gold"]))
    created = [p for p in OUT.glob("*.json*") if p.name != "selection_manifest.json"]
    write_json(OUT / "selection_manifest.json", {
        "executive_summary": "Blind metadata/hash selection complete; reviewer fields blank; no answer correctness calculated.",
        "created_utc": timestamp(), "status": "selected_unreviewed_no_defect_labels",
        "protocol_freeze_sha256": digest(FREEZE.read_bytes()),
        "initial_download_freeze_sha256": read_json(OUT / "ingestion_manifest.json")["freeze_sha256"],
        "code_and_protocol_hashes": require_freeze()["files_sha256"],
        "runtime": {"python": platform.python_version(), "implementation": platform.python_implementation()},
        "selection_salt": salt, "source_order": ["finqa", "tatqa"],
        "sampling": sampling, "admission_metadata": {"finqa": fq_meta, "tatqa": tq_meta},
        "overlap": overlap_inventory(fq + tq, selected),
        "artifacts_sha256": {p.name: digest(p.read_bytes()) for p in sorted(created)},
        "notice_status": {s: spec["notice_status"] for s, spec in config["sources"].items()},
        "original_gold_used_for_selection": False, "human_reviews_completed": 0,
        "models_called": 0, "answers_recomputed": 0,
        "corpus_and_targets_release_status": "local ignored/excluded; no redistribution admission"
    })


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["freeze", "amend", "fetch", "inspect", "select"])
    args = parser.parse_args()
    {"freeze": freeze_protocol, "amend": freeze_amendment, "fetch": fetch,
     "inspect": inspect, "select": prepare}[args.action]()


if __name__ == "__main__":
    main()
