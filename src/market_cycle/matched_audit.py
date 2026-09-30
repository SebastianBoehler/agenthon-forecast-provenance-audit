"""Executive summary: fixed diagnostic ablations, not new consistency repairs."""

import numpy as np

from .learning_audit import audit_schedules


def audit_variants(predict, schedules, params):
    zero = float(predict(np.zeros((1, 16)))[0])
    variants = {"raw": predict, "centered": lambda x: predict(x) - zero,
                "odd": lambda x: (predict(x) - predict(-x)) / 2}
    results = {}
    for name, variant in variants.items():
        audit = audit_schedules(variant, schedules, params, 16)
        results[name] = {"minimum_expected_cost": min(r["learned_expected_cost"] for r in audit.values()),
                         "cycles": audit}
    results["zero_history_prediction_currency_per_unit"] = zero * params.impact_per_unit * params.max_trade_units
    # Centering cannot change a closed cycle: constant offset times sum(q) is zero.
    residual = max(abs(results["raw"]["cycles"][n]["learned_expected_cost"] -
                       results["centered"]["cycles"][n]["learned_expected_cost"]) for n in schedules)
    results["centering_cost_identity_max_residual"] = residual
    mirror_residual = []
    for name in schedules:
        if not name.endswith("_buy"):
            continue
        mirror = name[:-4] + "_sell"
        average = (results["raw"]["cycles"][name]["learned_expected_cost"] +
                   results["raw"]["cycles"][mirror]["learned_expected_cost"]) / 2
        mirror_residual.append(abs(average - results["odd"]["cycles"][name]["learned_expected_cost"]))
    results["odd_mirror_average_identity_max_residual"] = max(mirror_residual)
    return results
