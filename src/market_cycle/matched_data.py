"""Executive summary: alter temporal ordering while preserving each signed multiset."""

import numpy as np

from .learning_data import histories


def matched_banks(sequences: int, seed: int, decay: float) -> dict:
    rng = np.random.default_rng(seed)
    magnitudes = rng.integers(1, 21, size=(sequences, 8)) / 20.0
    orientation = rng.choice([-1, 1], size=(sequences, 1))
    blocked = np.concatenate([magnitudes, -magnitudes], axis=1) * orientation
    shuffled = np.stack([rng.permutation(sequence) for sequence in blocked])
    if not np.array_equal(np.sort(blocked, axis=1), np.sort(shuffled, axis=1)):
        raise ValueError("Matched signed multisets differ")
    banks = {}
    weights = decay ** np.arange(1, 17)
    for name, actions in (("blocked", blocked), ("shuffled", shuffled)):
        x = histories(actions, 16)
        banks[name] = (actions, x, x @ weights)
    return banks


def heldout_schedules() -> dict:
    """Predeclared finite bank; no claim of disjoint semantic family support."""
    base = {
        "ramp_flat_exit": [2, 4, 6, 8, 10, 12, 14, 16] + [-9] * 8,
        "unequal_pulses": [18, -6, 0, -6, 0, -6, 0, 12, -4, 0, -4, 0, -4],
        "nested_exit": [12, 4, 4, 0, -5, -5, 0, -10],
        "delayed_alternation": [16, -16, 0, 0, 8, -8, 0, 0, 12, -12, 0, 0, 4, -4],
    }
    return {name + reverse + sign_name: [sign * q for q in sequence]
            for name, quantities in base.items()
            for reverse, sequence in (("", quantities), ("_reversed", quantities[::-1]))
            for sign_name, sign in (("_buy", 1), ("_sell", -1))}
