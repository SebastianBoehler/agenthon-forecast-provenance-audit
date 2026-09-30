"""Executive summary: isolate training duration on the exact original one-direction data."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

import numpy as np
import torch

from market_cycle.learner import make_model, predict_mlp
from market_cycle.learning_data import dataset, evaluation_schedules
from market_cycle.matched_audit import audit_variants
from market_cycle.matched_train import fit_checkpoints
from market_cycle.reference import Parameters


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    cfg = json.loads(args.config.read_text())
    original = Path(cfg["original_run"])
    first = json.loads((original / "results.json").read_text())
    old = first["config"]
    params = Parameters(**old["parameters"])
    root = args.output_dir
    root.mkdir(parents=True, exist_ok=False)
    snapshot = root / "source_snapshot"
    snapshot.mkdir()
    for source in (Path(__file__).parent.parent / "src/market_cycle").glob("*.py"):
        shutil.copy2(source, snapshot / source.name)
    shutil.copy2(__file__, snapshot / Path(__file__).name)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    saved = np.load(original / "one_direction_data.npz")
    x, y = saved["x"], saved["y"]
    vx = np.concatenate([dataset(c, old["validation_sequences"], old["horizon"],
                                 old["validation_seed"], params.decay)[1] for c in old["coverages"]])
    vy = vx @ (params.decay ** np.arange(1, 17))
    scale = params.impact_per_unit * params.max_trade_units
    results = {}
    for seed in old["model_seeds"]:
        destination = root / f"init_{seed}"
        destination.mkdir()
        training = {"hidden": old["training"]["hidden"],
                    "learning_rate": old["training"]["learning_rate"], "checkpoints": cfg["checkpoints"]}
        checkpoints, losses = fit_checkpoints(x, y, vx, vy, training, seed, destination, scale)
        replay = torch.load(destination / "epoch_200.pt", weights_only=True)
        previous = torch.load(original / f"one_direction_mlp_seed_{seed}.pt", weights_only=True)
        if not all(torch.equal(replay[k], previous[k]) for k in previous):
            raise ValueError("The original 200-step checkpoint did not replay exactly")
        rows = {}
        for row in checkpoints:
            model = make_model(16, old["training"]["hidden"], seed)
            model.load_state_dict(torch.load(destination / row["file"], weights_only=True))
            predict = lambda a, m=model: predict_mlp(m, a)
            rows[str(row["epoch"])] = {"common_rmse": row["common_rmse"],
                "audit": audit_variants(predict, evaluation_schedules(), params)}
        results[str(seed)] = {"original_checkpoint_exact_replay": True, "checkpoints": rows}
        (destination / "losses.json").write_text(json.dumps(losses))
        print(seed, [(e, round(r["audit"]["raw"]["minimum_expected_cost"], 6)) for e,r in rows.items()], flush=True)
    result = {"status": "post_v2_training_duration_diagnostic_not_confirmation", "config": cfg,
              "original_config_sha256": first["config_sha256"], "results": results,
              "original_training_data_sha256": hashlib.sha256((original / "one_direction_data.npz").read_bytes()).hexdigest()}
    (root / "results.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    (root / "artifact_hashes.json").write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*") if p.is_file()}, indent=2) + "\n")


if __name__ == "__main__":
    main()
