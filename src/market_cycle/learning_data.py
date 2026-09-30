"""Executive summary: reference-derived training data with explicit action coverage."""

import numpy as np


def histories(actions: np.ndarray, history: int) -> np.ndarray:
    """Past signed quantities, most recent first; no current or future action."""
    rows = np.zeros((actions.size, history), dtype=np.float64)
    for episode, sequence in enumerate(actions):
        for step in range(len(sequence)):
            previous = sequence[max(0, step - history):step][::-1]
            rows[episode * len(sequence) + step, :len(previous)] = previous
    return rows


def dataset(coverage: str, sequences: int, horizon: int, seed: int, decay: float):
    rng = np.random.default_rng(seed)
    if coverage == "one_direction":
        actions = rng.integers(1, 21, size=(sequences, horizon)) / 20.0
        actions *= rng.choice([-1, 1], size=(sequences, 1))
    elif coverage == "balanced_cycles":
        magnitudes = rng.integers(1, 21, size=(sequences, horizon // 2)) / 20.0
        actions = np.concatenate([magnitudes, -magnitudes], axis=1)
        actions = np.stack([rng.permutation(sequence) for sequence in actions])
    elif coverage == "unrestricted_signed":
        actions = rng.integers(-20, 21, size=(sequences, horizon)) / 20.0
    else:
        raise ValueError(f"Unknown coverage {coverage}")
    x = histories(actions, horizon)
    weights = decay ** np.arange(1, horizon + 1)
    return actions, x, x @ weights


def evaluation_schedules() -> dict[str, list[int]]:
    """Fixed development families, not a novelty-confirming or exhaustive search."""
    base = {
        "two_trade": [20, -20],
        "hold": [20] + [0] * 14 + [-20],
        "slow_entry": [5] * 4 + [-20],
        "slow_exit": [20] + [-5] * 4,
        "blocks": [20] * 8 + [-20] * 8,
        "alternating": [20, -20] * 8,
        "double_pulse": [20, 0, -20, 0, 20, 0, -20],
    }
    return {name + suffix: [sign * q for q in values]
            for name, values in base.items() for suffix, sign in (("_buy", 1), ("_sell", -1))}
