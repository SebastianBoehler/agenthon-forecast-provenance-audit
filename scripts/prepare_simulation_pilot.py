"""Executive summary: freeze public inputs and a schedule; launch no simulations."""

import argparse
import hashlib
import json
import random
import uuid
from pathlib import Path

UPSTREAM = "f9cbe51342b7dedd9587e4e069040d68a5c6477f"
NATIVE_SHA = "f1f0ff871568407e1d8bfe9b68fa39a35e2b505362d8e0da5583c145cc79f577"
SOURCES = (
    "s012_partial_fill_cancel_race.json",
    "mr_deep_book_state_size.json",
    "ra05_shock_momentum_heavy.json",
)
PATCHES = (
    "order_size_model.pomegranate-free.patch",
    "kernel_message_ledger.patch",
    "exchange_protocol_stp.patch",
    "oracle_scheduled_jump.patch",
)
SEEDS = (2026092801, 2026092802)
SCHEDULE_SEED = 20260928


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--track", required=True, type=Path)
    parser.add_argument("--native", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    track, native, out = args.track.resolve(), args.native.resolve(), args.out.resolve()
    if out.exists():
        raise FileExistsError(f"Preserve existing campaign: {out}")
    research = Path(__file__).resolve().parents[1]
    if not out.is_relative_to(research / "data"):
        raise ValueError("Campaign must live inside this research repo's ignored data directory")
    if digest(native) != NATIVE_SHA:
        raise ValueError("Native executable does not match retained r4")
    baseline = track / "baselines"
    required = [baseline / "Dockerfile", baseline / "simulate", baseline / "simulate-batch"]
    required += [baseline / "patches" / name for name in PATCHES]
    required += sorted((baseline / "abides_fork").rglob("*.py"))
    if not required[-1].is_file():
        raise FileNotFoundError("Baseline adapter missing")
    files = {str(p.relative_to(track)): digest(p) for p in required}
    cases = []
    configs = []
    for filename in SOURCES:
        source = track / "regression_suite/scenarios" / filename
        original = json.loads(source.read_text())
        files[str(source.relative_to(track))] = digest(source)
        for scale in (1, 2):
            for seed in SEEDS:
                case_id = f"{source.stem}-h{scale}-s{seed}"
                config = json.loads(json.dumps(original))
                config["seed"] = seed
                config["horizon_ns"] = original["horizon_ns"] * scale
                config["scenario_id"] = str(uuid.uuid5(uuid.NAMESPACE_URL, case_id))
                configs.append((case_id, config))
                cases.append(dict(case_id=case_id, source=str(source.relative_to(track)),
                                  horizon_multiplier=scale, seed=seed,
                                  config=f"inputs/{case_id}/scenario.json"))
    out.mkdir(parents=True)
    for case_id, config in configs:
        folder = out / "inputs" / case_id
        folder.mkdir(parents=True)
        write_json(folder / "scenario.json", config)
    for case in cases:
        case["sha256"] = digest(out / case["config"])
    rng = random.Random(SCHEDULE_SEED)
    schedule = []
    positions = {case["case_id"]: index for index, case in enumerate(cases)}
    for block in range(4):
        order = list(cases)
        rng.shuffle(order)
        for case in order:
            first = (block + positions[case["case_id"]]) % 2 == 0
            arms = ("python", "native") if first else ("native", "python")
            schedule.append(dict(block=block, case_id=case["case_id"], arms=list(arms)))
    aa_schedule = []
    for block in range(4):
        for family in range(3):
            case = cases[family * 4]
            arms = ["native-A", "native-B"] if block % 2 == 0 else ["native-B", "native-A"]
            aa_schedule.append(dict(block=block, case_id=case["case_id"], arms=arms))
    write_json(out / "manifest.json", dict(
        executive_summary="Public input and proposed schedule freeze; baseline runtime unresolved; no results.",
        status="inputs_frozen_runtime_not_ready", upstream_commit=UPSTREAM,
        baseline_source_sha256=files, native=dict(path=str(native), sha256=NATIVE_SHA),
        generator_sha256=digest(Path(__file__)), cases=cases,
        observations=dict(
            trace=["t_ns", "agent_id", "msg_type", "side", "price", "size", "order_id"],
            message_trace=["seq", "t_recv_ns", "t_send_ns", "latency_ns", "src_id",
                           "dst_id", "message_id", "msg_type", "order_id", "causal_parent"],
            equality="Exact ordered decoded column types and values, including nulls",
            blind_spots=["Unexposed final agent state", "Unobserved internal kernel state"]),
        resource_caps=dict(cpus=4, memory_bytes=17179869184, swap_bytes=0, network="none"),
        budget=dict(preflight_launches=24, timing_launches=96, aa_launches=24,
                    timeout_per_launch_seconds=120,
                    total_execution_seconds=1800), schedule_seed=SCHEDULE_SEED,
        unresolved=["Verified cached Python baseline image", "Successful paired semantic preflight",
                    "Exclusive bench reservation", "External timing launcher identities",
                    "Mechanism ablation artifacts"]))
    write_json(out / "schedule.json", schedule)
    write_json(out / "aa-schedule.json", aa_schedule)
    print(json.dumps(dict(campaign=str(out), cases=len(cases), timing_launches=96,
                          manifest_sha256=digest(out / "manifest.json"))))


if __name__ == "__main__":
    main()
