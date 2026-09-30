"""Executive summary: run the frozen matched-multiset and fidelity comparison."""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import time

import numpy as np
import scipy
import torch

from .learner import fit_structural, make_model, predict_mlp
from .learning_data import dataset, evaluation_schedules
from .matched_audit import audit_variants
from .matched_data import heldout_schedules, matched_banks
from .matched_train import choose_match, fit_checkpoints
from .reference import Parameters


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    raw = args.config.read_bytes()
    cfg = json.loads(raw)
    params = Parameters(**cfg["parameters"])
    if params.max_trade_units != 20:
        raise ValueError("Matched pilot fixes the 20-unit action scale")
    root = args.output_dir
    root.mkdir(parents=True, exist_ok=False)
    snapshot = root / "source_snapshot"
    snapshot.mkdir()
    for source in Path(__file__).parent.glob("*.py"):
        shutil.copy2(source, snapshot / source.name)
    save(root / "config.json", cfg)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    started = time.monotonic()
    validation = matched_banks(cfg["validation_sequences"], cfg["validation_seed"], params.decay)
    iid = dataset("unrestricted_signed", cfg["validation_sequences"], 16, cfg["validation_seed"], params.decay)
    vx = np.concatenate([bank[1] for bank in validation.values()] + [iid[1]])
    vy = vx @ (params.decay ** np.arange(1, 17))
    np.savez_compressed(root / "common_validation.npz", x=vx, y=vy)
    scale = params.impact_per_unit * params.max_trade_units
    trajectories, selections, baseline_parameters, coverage_diagnostics = {}, {}, {}, {}
    for data_seed in cfg["data_seeds"]:
        banks = matched_banks(cfg["sequences"], data_seed, params.decay)
        for coverage, (actions, x, y) in banks.items():
            stem = f"data_{data_seed}_{coverage}"
            np.savez_compressed(root / (stem + ".npz"), actions=actions, x=x, y=y)
            linear, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
            baseline_parameters[stem] = {"linear": linear.tolist(), "rank": int(rank),
                                         "structural": fit_structural(x, y)}
            coverage_diagnostics[stem] = {"mean_abs_action_normalized": float(np.abs(actions).mean()),
                                          "mean_sign_reversals": float(np.mean(np.sum(actions[:, 1:] * actions[:, :-1] < 0, axis=1)))}
            for seed in cfg["model_seeds"]:
                name = stem + f"_init_{seed}"
                destination = root / name
                destination.mkdir()
                checkpoints, losses = fit_checkpoints(x, y, vx, vy, cfg["training"], seed,
                                                      destination, scale)
                save(destination / "losses.json", losses)
                trajectories[name] = checkpoints
                print(name, [(c["epoch"], round(c["common_rmse"], 6)) for c in checkpoints], flush=True)
        for seed in cfg["model_seeds"]:
            pair = f"data_{data_seed}_init_{seed}"
            left = trajectories[f"data_{data_seed}_blocked_init_{seed}"]
            right = trajectories[f"data_{data_seed}_shuffled_init_{seed}"]
            selections[pair] = choose_match(left, right, cfg["matching"])
    # Freeze validation-only selections before reading any audit outcomes.
    save(root / "selection.json", selections)
    save(root / "validation_trajectories.json", trajectories)
    save(root / "baseline_parameters.json", baseline_parameters)
    save(root / "coverage_diagnostics.json", coverage_diagnostics)
    schedules = {"new_bank": heldout_schedules(), "v1_development": evaluation_schedules()}
    save(root / "schedules.json", schedules)
    audits = {}
    for data_seed in cfg["data_seeds"]:
        for coverage in ("blocked", "shuffled"):
            stem = f"data_{data_seed}_{coverage}"
            fitted = baseline_parameters[stem]
            weights = np.asarray(fitted["linear"])
            structural = fitted["structural"]["decay"] ** np.arange(1, 17)
            for name, w in (("linear_ls", weights), ("admissible_exponential", structural)):
                predict = lambda x, w=w: x @ w
                audits[stem + "_" + name] = {bank: audit_variants(predict, q, params)
                                             for bank, q in schedules.items()}
            for seed in cfg["model_seeds"]:
                pair = f"data_{data_seed}_init_{seed}"
                choices = {"fixed_budget": max(cfg["training"]["checkpoints"])}
                if selections[pair] is not None:
                    choices["fidelity_matched"] = selections[pair][coverage]["epoch"]
                for comparison, epoch in choices.items():
                    directory = root / (stem + f"_init_{seed}")
                    model = make_model(16, cfg["training"]["hidden"], seed)
                    model.load_state_dict(torch.load(directory / f"epoch_{epoch}.pt", weights_only=True))
                    predict = lambda x, m=model: predict_mlp(m, x)
                    name = stem + f"_init_{seed}_{comparison}"
                    audits[name] = {bank: audit_variants(predict, q, params) for bank, q in schedules.items()}
    result = {"status": "prespecified_followup_not_novelty_certificate", "config": cfg,
              "config_sha256": hashlib.sha256(raw).hexdigest(), "selections": selections,
              "validation_trajectories": trajectories, "audits": audits,
              "elapsed_seconds": time.monotonic() - started,
              "runtime": {"python": platform.python_version(), "torch": torch.__version__,
                          "numpy": np.__version__, "scipy": scipy.__version__, "device": "cpu"}}
    save(root / "results.json", result)
    hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in root.rglob("*") if p.is_file()}
    save(root / "artifact_hashes.json", hashes)
    print("Completed", sum(s is not None for s in selections.values()), "of", len(selections), "matched pairs", flush=True)


if __name__ == "__main__":
    main()
