"""Executive summary: reproducible CPU development pilot, not paper confirmation."""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import time

import numpy as np
import scipy
import torch

from .learner import fit_structural, predict_mlp, train_mlp
from .learning_audit import audit_schedules
from .learning_data import dataset, evaluation_schedules
from .reference import Parameters


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    raw = args.config.read_bytes()
    config = json.loads(raw)
    params = Parameters(**config["parameters"])
    if config["horizon"] != 16 or config["sequences"] < 1:
        raise ValueError("This pilot fixes the 16-step horizon and positive data budget")
    args.output_dir.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    start = time.monotonic()
    models = {}
    schedules = evaluation_schedules()
    (args.output_dir / "evaluation_schedules.json").write_text(json.dumps(schedules, indent=2))
    common_x = np.concatenate([
        dataset(c, config["validation_sequences"], config["horizon"],
                config["validation_seed"], params.decay)[1]
        for c in config["coverages"]
    ])
    common_y = common_x @ (params.decay ** np.arange(1, config["horizon"] + 1))
    for coverage in config["coverages"]:
        actions, x, y = dataset(coverage, config["sequences"], config["horizon"],
                                config["data_seed"], params.decay)
        np.savez_compressed(args.output_dir / f"{coverage}_data.npz", actions=actions, x=x, y=y)
        _, vx, vy = dataset(coverage, config["validation_sequences"], config["horizon"],
                            config["validation_seed"], params.decay)
        linear, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
        structure = fit_structural(x, y)
        weights = structure["decay"] ** np.arange(1, config["horizon"] + 1)
        predictors = [("linear_ls", lambda inputs, w=linear: inputs @ w),
                      ("admissible_exponential", lambda inputs, w=weights: inputs @ w)]
        artifact = {"linear_weights": linear.tolist(), "linear_rank": int(rank),
                    "structural_fit": structure,
                    "mean_abs_action": float(np.abs(actions).mean()),
                    "mean_abs_terminal_inventory": float(np.abs(actions.sum(axis=1)).mean()),
                    "mean_sign_reversals": float(np.mean(np.sum(actions[:, 1:] * actions[:, :-1] < 0, axis=1)))}
        (args.output_dir / f"{coverage}_comparators.json").write_text(json.dumps(artifact, indent=2))
        for seed in config["model_seeds"]:
            model, losses = train_mlp(x, y, config["training"], seed)
            name = f"mlp_seed_{seed}"
            torch.save(model.state_dict(), args.output_dir / f"{coverage}_{name}.pt")
            (args.output_dir / f"{coverage}_{name}_losses.json").write_text(json.dumps(losses))
            predictors.append((name, lambda inputs, model=model: predict_mlp(model, inputs)))
        for name, predict in predictors:
            audit = audit_schedules(predict, schedules, params, config["horizon"])
            scale = params.impact_per_unit * params.max_trade_units
            models[f"{coverage}/{name}"] = {
                "training_rmse": float(np.sqrt(np.mean((predict(x) - y) ** 2))) * scale,
                "same_coverage_validation_rmse": float(np.sqrt(np.mean((predict(vx) - vy) ** 2))) * scale,
                "common_validation_rmse": float(np.sqrt(np.mean((predict(common_x) - common_y) ** 2))) * scale,
                "minimum_expected_cycle_cost": min(row["learned_expected_cost"] for row in audit.values()),
                "negative_cost_cycles_beyond_threshold": sum(row["learned_expected_cost"] < -config["effect_threshold"] for row in audit.values()),
                "cycles": audit,
            }
            print(coverage, name, "min cost", round(models[f"{coverage}/{name}"]["minimum_expected_cycle_cost"], 6), flush=True)
    result = {"status": "development_pilot_not_confirmatory", "config": config,
              "config_sha256": hashlib.sha256(raw).hexdigest(), "models": models,
              "elapsed_seconds": time.monotonic() - start,
              "runtime": {"python": platform.python_version(), "torch": torch.__version__,
                          "numpy": np.__version__, "scipy": scipy.__version__, "device": "cpu"},
              "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in sorted(Path(__file__).parent.glob("*.py"))}}
    (args.output_dir / "results.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in args.output_dir.iterdir() if p.is_file()}
    (args.output_dir / "artifact_hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")


if __name__ == "__main__":
    main()
