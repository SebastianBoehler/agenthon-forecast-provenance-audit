"""Executive summary: save fixed-budget checkpoints and select solely on response error."""

import numpy as np
import torch

from .learner import make_model, predict_mlp


def fit_checkpoints(x, y, vx, vy, config, seed, destination, scale):
    model = make_model(x.shape[1], config["hidden"], seed)
    optimizer = torch.optim.Adam(model.parameters(), lr=config["learning_rate"])
    inputs, targets = torch.from_numpy(x), torch.from_numpy(y).unsqueeze(1)
    checkpoints, losses = [], []
    for epoch in range(1, max(config["checkpoints"]) + 1):
        optimizer.zero_grad()
        loss = ((model(inputs) - targets) ** 2).mean()
        if not torch.isfinite(loss):
            raise ValueError("Nonfinite training loss")
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
        if epoch in config["checkpoints"]:
            name = f"epoch_{epoch}.pt"
            torch.save(model.state_dict(), destination / name)
            prediction = predict_mlp(model, vx)
            checkpoints.append({"epoch": epoch, "file": name,
                                "common_rmse": float(np.sqrt(np.mean((prediction - vy) ** 2))) * scale})
    return checkpoints, losses


def choose_match(left, right, tolerance):
    pairs = []
    for a in left:
        for b in right:
            high = max(a["common_rmse"], b["common_rmse"])
            difference = abs(a["common_rmse"] - b["common_rmse"])
            relative = difference / high if high else 0.0
            if difference <= tolerance["absolute"] and relative <= tolerance["relative"]:
                pairs.append((high, difference, a["epoch"], b["epoch"], a, b))
    if not pairs:
        return None
    selected = min(pairs, key=lambda item: item[:4])
    return {"blocked": selected[4], "shuffled": selected[5]}
