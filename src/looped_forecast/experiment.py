"""Executive summary: fit frozen probabilistic baselines and neural contrasts."""
import json
import time
from pathlib import Path

import numpy as np
import torch
from scipy.stats import norm
from sklearn.linear_model import Ridge

from .data import load_cases, make_features
from .model import GaussianTransformer


def gaussian_crps(actual, mean, scale):
    z = (actual - mean) / scale
    return scale * (z * (2 * norm.cdf(z) - 1) + 2 * norm.pdf(z) - 1 / np.sqrt(np.pi))


def metrics(actual, mean, scale):
    return {"crps_bp": float(np.mean(gaussian_crps(actual, mean, scale))),
            "mae_bp": float(np.mean(np.abs(actual - mean))),
            "coverage_90": float(np.mean(np.abs(actual - mean) <= norm.ppf(0.95) * scale)),
            "mean_scale_bp": float(np.mean(scale))}


def baseline_predictions(features):
    x, y, split = features["x"], features["raw_y"], features["split"]
    train, val = split == "train", split == "val"
    candidates = []
    for name in ("climatology", "numeric_ridge"):
        for alpha in ([0] if name == "climatology" else [0.1, 1, 10, 100]):
            if name == "climatology":
                mean = np.full(len(y), np.mean(y[train]))
            else:
                model = Ridge(alpha=alpha).fit(x[train], y[train])
                mean = model.predict(x)
            residual_sd = max(float(np.std(y[train] - mean[train], ddof=1)), 0.1)
            for multiplier in (0.75, 1.0, 1.25, 1.5):
                scale = np.full(len(y), residual_sd * multiplier)
                score = metrics(y[val], mean[val], scale[val])["crps_bp"]
                candidates.append((name, score, alpha, multiplier, mean, scale))
    results = []
    for name in ("climatology", "numeric_ridge"):
        best = min((c for c in candidates if c[0] == name), key=lambda c: c[1])
        _, _, alpha, multiplier, mean, scale = best
        results.append({"model": name, "alpha": alpha, "scale_multiplier": multiplier,
                        "validation": metrics(y[val], mean[val], scale[val]),
                        "test": metrics(y[split == "test"], mean[split == "test"], scale[split == "test"]),
                        "test_predictions": mean[split == "test"].tolist(),
                        "test_scales": scale[split == "test"].tolist()})
    return results


def train_neural(features, depth, tied, use_text, seed, max_epochs=200):
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    x = torch.tensor(features["x"])
    text = torch.tensor(features["text"])
    y = torch.tensor(features["y"])
    split = features["split"]
    train, val = np.flatnonzero(split == "train"), np.flatnonzero(split == "val")
    model = GaussianTransformer(text.shape[1], depth, tied, use_text)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
    best_score, best_state, best_epoch, stale = float("inf"), None, 0, 0
    t0 = time.perf_counter()
    for epoch in range(max_epochs):
        model.train()
        optimizer.zero_grad()
        mean, scale = model(x[train], text[train])
        loss = torch.mean(0.5 * ((y[train] - mean) / scale) ** 2 + torch.log(scale))
        if not torch.isfinite(loss):
            raise ValueError(f"Nonfinite training loss: epoch={epoch}")
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        model.eval()
        with torch.no_grad():
            mu, sd = model(x[val], text[val])
        score = float(np.mean(gaussian_crps(y[val].numpy(), mu.numpy(), sd.numpy())))
        if score < best_score - 1e-5:
            best_score = score
            best_state = {key: value.detach().clone() for key, value in model.state_dict().items()}
            best_epoch, stale = epoch + 1, 0
        else:
            stale += 1
        if stale >= 30:
            break
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        start = time.perf_counter()
        mu, sd = model(x, text)
        latency_ms = (time.perf_counter() - start) * 1000 / len(x)
    mean = mu.numpy() * features["target_scale"] + features["target_center"]
    scale = sd.numpy() * features["target_scale"]
    raw_y = features["raw_y"]
    test = split == "test"
    return {"model": f"{'tied' if tied else 'untied'}_{depth}_{'text' if use_text else 'blind'}", "seed": seed,
            "best_epoch": best_epoch, "epochs_run": epoch + 1, "training_seconds": time.perf_counter() - t0,
            "parameters": sum(p.numel() for p in model.parameters()), "latency_ms_per_case": latency_ms,
            "validation": metrics(raw_y[val], mean[val], scale[val]), "test": metrics(raw_y[test], mean[test], scale[test]),
            "test_predictions": mean[test].tolist(), "test_scales": scale[test].tolist()}


def run(data_root: Path, output_root: Path):
    cases, exclusions = load_cases(data_root)
    features = make_features(cases)
    output_root.mkdir(parents=True, exist_ok=True)
    case_meta = [{key: case[key] for key in ("date", "url", "text_sha256", "target_bp")} |
                 {"split": str(features["split"][i])} for i, case in enumerate(cases)]
    (output_root / "cases.json").write_text(json.dumps(case_meta, indent=2) + "\n")
    results = baseline_predictions(features)
    for depth, tied, use_text in ((1, True, False), (1, True, True), (3, True, False),
                                  (3, True, True), (3, False, False), (3, False, True)):
        for seed in (7, 17, 37):
            result = train_neural(features, depth, tied, use_text, seed)
            results.append(result)
            print(result["model"], seed, result["best_epoch"], result["validation"]["crps_bp"], result["test"]["crps_bp"], flush=True)
            (output_root / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    summary = {"source_manifest": json.loads((data_root / "manifest.json").read_text()),
               "exclusions": exclusions, "split_counts": {name: int(sum(features["split"] == name)) for name in ("train", "val", "test")},
               "text_vocabulary": features["vocab_size"], "text_dimensions": features["text_dimensions"]}
    (output_root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return results, summary
