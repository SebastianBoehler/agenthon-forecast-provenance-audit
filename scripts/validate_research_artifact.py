"""Executive summary: check the custom historical graph, evidence hashes and claims.

This offline check establishes file/reference integrity and recorded-value agreement.
It does not establish financial correctness, causal validity, replayability or ARA Seal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

GRAPH_PATH = "experiments/research_exploration_graph_v1.json"
CLAIMS_PATH = "experiments/research_claim_evidence_v1.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def local_file(root: Path, relative: str) -> Path:
    path = Path(relative)
    require(not path.is_absolute() and ".." not in path.parts, f"Unsafe path: {relative}")
    resolved = (root / path).resolve()
    require(resolved.is_relative_to(root.resolve()), f"Escaping path: {relative}")
    require(resolved.is_file(), f"Missing evidence: {relative}")
    return resolved


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def unique_records(records: list[dict], label: str) -> dict:
    indexed = {record["id"]: record for record in records}
    require(len(indexed) == len(records), f"Duplicate {label} IDs")
    require(all(indexed), f"Empty {label} ID")
    return indexed


def references(ids: list[str], available: dict, label: str) -> None:
    require(bool(ids), f"Empty {label} references")
    require(len(ids) == len(set(ids)), f"Duplicate {label} reference")
    require(all(item in available for item in ids), f"Unknown {label} reference: {ids}")


def pointer(document, location: str):
    require(location == "" or location.startswith("/"), f"Invalid JSON pointer: {location}")
    value = document
    for token in location.split("/")[1:]:
        key = token.replace("~1", "/").replace("~0", "~")
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def check_graph(graph: dict, root: Path) -> tuple[dict, dict]:
    require(graph["schema_version"] == 1, "Unsupported graph version")
    require(graph["record_status"] == "retrospective_reporting_only", "Wrong graph status")
    evidence = unique_records(graph["evidence"], "evidence")
    nodes = unique_records(graph["nodes"], "node")
    for item in evidence.values():
        path = local_file(root, item["path"])
        require(sha256(path) == item["sha256"], f"SHA256 mismatch: {item['path']}")
        require(path.stat().st_size == item["bytes"], f"Byte-size mismatch: {item['path']}")
    for node in nodes.values():
        require(node["support_level"] == "explicit_documented", f"Unsupported node: {node['id']}")
        for key in ["question", "outcome", "failure_mode", "lesson", "limitations"]:
            require(bool(node[key]), f"Missing node {key}: {node['id']}")
        references(node["evidence"], evidence, "node evidence")
        references(node["raw_evidence"], evidence, "raw evidence")
        require(set(node["raw_evidence"]) <= set(node["evidence"]), "Raw evidence outside node")
        for ids in node["bindings"].values():
            references(ids, evidence, "binding evidence")
            require(set(ids) <= set(node["evidence"]), "Binding outside node evidence")
    adjacency = {node_id: [] for node_id in nodes}
    seen = set()
    for edge in graph["edges"]:
        start, end = edge["from"], edge["to"]
        require(start in nodes and end in nodes and start != end, "Invalid graph edge endpoint")
        key = (start, end, edge["relation"])
        require(key not in seen, "Duplicate graph edge")
        seen.add(key)
        support = edge["support"]
        require(support["evidence"] in evidence, "Unknown edge evidence")
        text = local_file(root, evidence[support["evidence"]]["path"]).read_text()
        require(support["contains"] in text, f"Edge support text missing: {key}")
        adjacency[start].append(end)
    active, complete = set(), set()

    def visit(node_id: str) -> None:
        require(node_id not in active, f"Cyclic graph at {node_id}")
        if node_id in complete:
            return
        active.add(node_id)
        for child in adjacency[node_id]:
            visit(child)
        active.remove(node_id)
        complete.add(node_id)

    for node_id in nodes:
        visit(node_id)
    return evidence, nodes


def check_observation(observation: dict, evidence: dict, root: Path, cache: dict) -> None:
    item = evidence[observation["evidence"]]
    path = local_file(root, item["path"])
    operation = observation.get("operation", "json_pointer")
    if operation == "jsonl_record_count":
        with path.open() as handle:
            actual = sum(1 for line in handle if line.strip())
    else:
        if item["id"] not in cache:
            cache[item["id"]] = json.loads(path.read_text())
        actual = pointer(cache[item["id"]], observation["pointer"])
        if operation == "sum_field":
            actual = sum(value[observation["field"]] for value in actual.values())
        elif operation == "list_length":
            actual = len(actual)
        elif operation in {"count_records", "mean_metric"}:
            records = actual.items() if isinstance(actual, dict) else enumerate(actual)
            selected = []
            for key, value in records:
                if not str(key).endswith(observation.get("key_suffix", "")):
                    continue
                if any(pointer(value, field) != expected for field, expected in observation.get("where", {}).items()):
                    continue
                cutoff = observation.get("less_than")
                if cutoff and not pointer(value, cutoff["pointer"]) < cutoff["value"]:
                    continue
                selected.append(value)
            actual = len(selected)
            if operation == "mean_metric":
                require(bool(selected), "Empty metric selection")
                actual = round(sum(pointer(value, observation["metric"]) for value in selected) / len(selected), observation["round_digits"])
        else:
            require(operation == "json_pointer", f"Unknown observation operation: {operation}")
    require(actual == observation["equals"], f"Recorded-value mismatch: {observation}")


def check_claims(claim_map: dict, graph: dict, evidence: dict, nodes: dict, root: Path) -> int:
    require(claim_map["schema_version"] == 1, "Unsupported claim-map version")
    graph_link = claim_map["graph"]
    require(graph_link["path"] == GRAPH_PATH, "Unexpected graph path")
    require(sha256(local_file(root, GRAPH_PATH)) == graph_link["sha256"], "Graph hash mismatch")
    claims = unique_records(claim_map["claims"], "claim")
    cache, checks = {}, 0
    for claim in claims.values():
        require(claim["experiment"] in nodes, f"Unknown claim experiment: {claim['id']}")
        for key in ["statement", "status", "conditions", "falsification_criteria", "inference_limits"]:
            require(bool(claim[key]), f"Missing claim {key}: {claim['id']}")
        proof = claim["proof"]
        references(proof["evidence"], evidence, "claim evidence")
        references(proof["raw_evidence"], evidence, "claim raw evidence")
        require(set(proof["raw_evidence"]) <= set(proof["evidence"]), "Raw proof outside evidence")
        require(set(proof["evidence"]) <= set(nodes[claim["experiment"]]["evidence"]), "Proof outside experiment")
        for observation in proof.get("recorded_value_checks", []):
            require(observation["evidence"] in proof["evidence"], "Observation outside proof")
            check_observation(observation, evidence, root, cache)
            checks += 1
        for location in proof.get("source_locations", []):
            require(location["evidence"] in proof["evidence"], "Source location outside proof")
            lines = local_file(root, evidence[location["evidence"]]["path"]).read_text().splitlines()
            require(1 <= location["start"] <= location["end"] <= len(lines), "Invalid source line location")
    return checks


def validate(root: Path) -> dict:
    graph = json.loads(local_file(root, GRAPH_PATH).read_text())
    claim_map = json.loads(local_file(root, CLAIMS_PATH).read_text())
    evidence, nodes = check_graph(graph, root)
    checks = check_claims(claim_map, graph, evidence, nodes, root)
    return {
        "executive_summary": "Custom retrospective references, file hashes, DAG and recorded values agree; no scientific or ARA certification.",
        "status": "PASS_STRUCTURAL_AND_RECORDED_VALUE_CHECKS",
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "evidence_files": len(evidence), "nodes": len(nodes), "edges": len(graph["edges"]),
        "claims": len(claim_map["claims"]), "recorded_value_checks": checks,
        "sha256": {GRAPH_PATH: sha256(root / GRAPH_PATH), CLAIMS_PATH: sha256(root / CLAIMS_PATH),
                   "validator": sha256(Path(__file__))},
        "limits": graph["validation_limits"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = validate(args.root.resolve())
    except (ValueError, KeyError, TypeError, IndexError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Research artifact validation failed: {exc}\n")
    serialized = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
