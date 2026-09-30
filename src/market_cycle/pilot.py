"""Executive summary: run paired reference controls and preserve every fill ledger."""

from dataclasses import asdict
from math import fsum, sqrt
from random import Random
from statistics import NormalDist

from .reference import Parameters, cost_variance, execute, expected_cost


def run_pilot(config: dict) -> dict:
    required = {"parameters", "schedules", "episodes", "seed", "alpha"}
    if set(config) != required:
        raise ValueError(f"Configuration requires exactly {sorted(required)}")
    params = Parameters(**config["parameters"])
    episodes, seed, alpha = config["episodes"], config["seed"], config["alpha"]
    if type(episodes) is not int or not 2 <= episodes <= 10000:
        raise ValueError("episodes must be an integer from 2 to 10000")
    if type(seed) is not int:
        raise ValueError("seed must be an integer")
    if isinstance(alpha, bool) or not isinstance(alpha, (int, float)) or not 0 < alpha < 1:
        raise ValueError("alpha must lie strictly between zero and one")
    schedules = config["schedules"]
    if not isinstance(schedules, dict) or not schedules:
        raise ValueError("schedules must be a nonempty mapping")
    if any(not isinstance(v, list) or len(v) > 500 for v in schedules.values()):
        raise ValueError("Each schedule must be a list of at most 500 quantities")
    horizon = max(map(len, schedules.values()))
    rng = Random(seed)
    scale = params.volatility_per_sqrt_second * sqrt(params.step_seconds)
    # Fixed grid gives each episode/step the same exogenous draw in both controls.
    shocks = [tuple(rng.gauss(0, scale) for _ in range(horizon - 1)) for _ in range(episodes)]
    results = {}
    quantile = NormalDist().inv_cdf(1 - alpha / (4 * len(schedules)))
    for name, values in schedules.items():
        quantities = tuple(values)
        models = {}
        for model, malformed in (("admissible_reference", False), ("invalid_self_impact_control", True)):
            ledgers = [execute(quantities, row[: len(values) - 1], params, omit_self_impact=malformed)
                       for row in shocks]
            costs = [-ledger[-1].cash_after for ledger in ledgers]
            mean = fsum(costs) / episodes
            standard_error = sqrt(cost_variance(quantities, params) / episodes)
            models[model] = {
                "analytical_expected_cost": expected_cost(quantities, params, omit_self_impact=malformed),
                "sample_mean_cost": mean,
                "known_variance_standard_error": standard_error,
                "simultaneous_gaussian_interval": [mean - quantile * standard_error,
                                                   mean + quantile * standard_error],
                "fills_by_episode": [[asdict(fill) for fill in ledger] for ledger in ledgers],
            }
        results[name] = models
    return {"status": "reference_controls_only_not_learned_model_evidence",
            "config": config, "results": results}
