"""Executive summary: run one pinned MarS noise-init exchange cycle and preserve the fill ledger."""
import json
import time
from pathlib import Path

import pandas as pd
from mars_cycle.cycle_agent import CycleAgent
from mars_cycle.runtime import DirectClient
from market_simulation.agents.background_agent import BackgroundAgent
from market_simulation.agents.noise_agent import NoiseAgent
from market_simulation.states.order_state import Converter, OrderState
from market_simulation.states.trade_info_state import TradeInfoState
from mlib.core.env import Env
from mlib.core.event import create_exchange_events
from mlib.core.exchange import Exchange
from mlib.core.exchange_config import create_exchange_config_without_call_auction

ROOT = Path("data/external-baselines/mars-2m-pinned-v1")
OUT = Path("outputs/market-cycle/mars-external-v3")


def run_one(index: int, direction: str):
    OUT.mkdir(parents=True, exist_ok=True)
    symbol = "AUDIT"
    start = pd.Timestamp("2026-01-05 09:30:00")
    switch = start + pd.Timedelta(minutes=25)
    end = switch + pd.Timedelta(seconds=20)
    config = create_exchange_config_without_call_auction(start, end, [symbol])
    exchange = Exchange(config)
    converter = Converter(ROOT / "assets/converters")
    client = DirectClient(ROOT, 7000 + index)
    noise = NoiseAgent(symbol, 100000, 1, start, switch, 7100 + index)
    background = BackgroundAgent(symbol, converter, switch, end, client, noise)
    cycle = CycleAgent(symbol, switch + pd.Timedelta(seconds=2), direction=direction)
    state = OrderState(1024, converter.price_level.num_bins, converter.pred_order_volume.num_bins,
                       converter.order_interval.num_bins, converter)
    exchange.register_state(state)
    exchange.register_state(TradeInfoState())
    env = Env(exchange, description="MarS direct-CPU closed-cycle diagnostic")
    for agent in (noise, background, cycle):
        env.register_agent(agent)
    env.push_events(create_exchange_events(config))
    start_wall = time.perf_counter()
    observed_actions = 0
    status = "completed"
    error = None
    try:
        for observation in env.env():
            observed_actions += 1
            env.step(observation.agent.get_action(observation))
    except Exception as exc:
        status = "failed"
        error = repr(exc)
    cash_change = cycle.cash - 100_000_000
    result = {"status": status, "error": error, "source_revision": "f04dd87a4d56342a6a2fc271cdb158fbacd83674",
              "model_revision": "b8f8c818c2a270844961b975f311457628bf2972",
              "asset_revision": "de761abefc1e3c0a8106a03b4fed6fc73cf702d3",
              "noise_seed": 7100 + index, "torch_numpy_seed": 7000 + index, "direction": direction, "warmup_seconds": 1500,
              "transport": "experimental direct CPU fp32", "observed_actions": observed_actions,
              "warmup_orders": len(state.recent_orders), "model_calls": client.calls,
              "model_seconds": client.seconds, "wall_seconds": time.perf_counter() - start_wall,
              "actions": cycle.actions, "fills": cycle.fills, "terminal_inventory": cycle.holdings.get(symbol),
              "cash_change": cash_change, "cycle_cost": -cash_change if cycle.holdings.get(symbol) == 0 and len(cycle.fills) >= 2 and not cycle.lob_orders.get(symbol) else None,
              "open_orders": len(cycle.lob_orders.get(symbol, {})),
              "interpretation": "One noise-initialized simulation diagnostic; a negative cost alone does not establish real-market arbitrage or learned-model defect."}
    (OUT / f"seed-{index:02d}-{direction}.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"{index:02d} {direction} {status} fills={len(cycle.fills)} cost={result['cycle_cost']}", flush=True)
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", action="store_true")
    args = parser.parse_args()
    if args.bank:
        results = [run_one(index, direction) for index in range(1, 31) for direction in ("B", "S")]
        (OUT / "bank.json").write_text(json.dumps(results, indent=2) + "\n")
    else:
        run_one(1, "B")
