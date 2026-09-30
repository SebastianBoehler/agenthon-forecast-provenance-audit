"""Executive summary: matched neural learners and established structural comparators."""

import numpy as np
from scipy.optimize import minimize_scalar
import torch
from torch import nn


def make_model(history: int, hidden: int, seed: int):
    torch.manual_seed(seed)
    return nn.Sequential(nn.Linear(history, hidden), nn.Tanh(),
                         nn.Linear(hidden, hidden), nn.Tanh(), nn.Linear(hidden, 1)).double()


def train_mlp(x: np.ndarray, y: np.ndarray, config: dict, seed: int):
    model = make_model(x.shape[1], config["hidden"], seed)
    optimizer = torch.optim.Adam(model.parameters(), lr=config["learning_rate"])
    inputs = torch.from_numpy(x)
    targets = torch.from_numpy(y).unsqueeze(1)
    losses = []
    for _ in range(config["epochs"]):
        optimizer.zero_grad()
        loss = ((model(inputs) - targets) ** 2).mean()
        if not torch.isfinite(loss):
            raise ValueError("Nonfinite training loss")
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
    model.eval()
    return model, losses


def predict_mlp(model, x: np.ndarray) -> np.ndarray:
    with torch.no_grad():
        return model(torch.from_numpy(x)).squeeze(1).numpy()


def fit_structural(x: np.ndarray, y: np.ndarray) -> dict:
    """Fit admissible exponential decay; scale equals the known shared self-impact."""
    lags = np.arange(1, x.shape[1] + 1)

    def fit_at(decay):
        response = x @ (decay ** lags)
        return float(np.mean((response - y) ** 2))

    solution = minimize_scalar(fit_at, bounds=(0.001, 1.0), method="bounded",
                               options={"xatol": 1e-12})
    if not solution.success:
        raise ValueError(f"Structural fit failed: {solution.message}")
    return {"decay": float(solution.x), "scale": 1.0, "training_mse": fit_at(solution.x)}
