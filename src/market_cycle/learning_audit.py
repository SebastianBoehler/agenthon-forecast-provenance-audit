"""Executive summary: audit learned responses under the unchanged reference fill rule."""

from dataclasses import asdict

import numpy as np

from .learning_data import histories
from .reference import Parameters, execute, expected_cost


def audit_schedules(predict, schedules: dict, params: Parameters, history: int) -> dict:
    results = {}
    for name, quantities in schedules.items():
        if len(quantities) > history:
            raise ValueError("Pilot excludes omitted-history extrapolation")
        actions = np.asarray([quantities], dtype=np.float64) / params.max_trade_units
        features = histories(actions, history)
        impact = np.asarray(predict(features)) * params.impact_per_unit * params.max_trade_units
        reference = features @ (params.decay ** np.arange(1, history + 1))
        reference *= params.impact_per_unit * params.max_trade_units
        # Unaffected noise has zero expectation and response excludes prices/shocks.
        fills = execute(tuple(quantities), (0.0,) * (len(quantities) - 1), params,
                        pretrade_impacts=tuple(impact))
        learned_cost = -fills[-1].cash_after
        true_cost = expected_cost(tuple(quantities), params)
        results[name] = {
            "reference_expected_cost": true_cost,
            "learned_expected_cost": learned_cost,
            "reference_minus_learned_cost": true_cost - learned_cost,
            "response_rmse_currency_per_unit": float(np.sqrt(np.mean((impact - reference) ** 2))),
            "fills": [asdict(fill) for fill in fills],
        }
    return results
