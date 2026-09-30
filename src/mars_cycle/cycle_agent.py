"""Executive summary: audit an actual buy then sell cycle with exchange fills."""
from pandas import Timedelta
from mlib.core.action import Action
from mlib.core.base_agent import BaseAgent
from mlib.core.limit_order import LimitOrder
from market_simulation.states.trade_info_state import TradeInfoState


class CycleAgent(BaseAgent):
    """One bounded long-only probe with explicit cancellation and flattening."""

    def __init__(self, symbol, start_time, direction="B", volume=100):
        super().__init__(init_cash=100_000_000)
        self.symbol = symbol
        self.start_time = start_time
        self.volume = volume
        self.direction = direction
        self.stage = 0
        self.fills = []
        self.actions = []

    def on_order_executed(self, time, transaction, trans_order_id_to_notify):
        before = self.holdings[self.symbol]
        removed = super().on_order_executed(time, transaction, trans_order_id_to_notify)
        delta = self.holdings[self.symbol] - before
        if delta:
            self.fills.append({"time": time.isoformat(), "side": "B" if delta > 0 else "S",
                               "quantity": abs(delta), "price": transaction.price, "cash_after": self.cash,
                               "inventory_after": self.holdings[self.symbol]})
        return removed

    def get_action(self, observation):
        time = observation.time
        if time < self.start_time:
            return Action(agent_id=self.agent_id, orders=[], time=time, next_wakeup_time=self.start_time)
        if self.stage >= 6:
            return Action(agent_id=self.agent_id, orders=[], time=time, next_wakeup_time=None)
        state = self.symbol_states[self.symbol][TradeInfoState.__name__]
        lob = state.trade_infos[-1].lob_snapshot
        orders = []
        if self.stage in (0, 2, 4):
            side = self.direction if self.stage == 0 else ("S" if self.direction == "B" else "B")
            quantity = self.volume if self.stage == 0 else abs(self.holdings[self.symbol])
            if quantity:
                if side == "B" and not lob.ask_prices:
                    raise RuntimeError("No ask liquidity for entry")
                if side == "S" and not lob.bid_prices:
                    raise RuntimeError("No bid liquidity for exit")
                price = (lob.ask_prices[0] + 1000) if side == "B" else max(100, lob.bid_prices[0] - 1000)
                orders = self.construct_valid_orders(time, self.symbol, side, price, quantity)
        else:
            for resting in list(self.lob_orders[self.symbol].values()):
                orders.append(LimitOrder(time=time, type="C", price=resting.price,
                                         volume=resting.volume, symbol=self.symbol, agent_id=self.agent_id,
                                         order_id=-1, cancel_type=resting.type, cancel_id=resting.order_id, tag=""))
        self.actions.append({"time": time.isoformat(), "stage": self.stage, "orders": len(orders),
                             "inventory_before": self.holdings[self.symbol], "cash_before": self.cash})
        self.stage += 1
        return Action(agent_id=self.agent_id, orders=orders, time=time,
                      next_wakeup_time=time + Timedelta(seconds=1) if self.stage < 6 else None)
