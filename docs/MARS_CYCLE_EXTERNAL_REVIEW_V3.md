## Executive summary (read this first)

The pinned official MarS example supports initialization by a noise agent, followed
by a learned background agent inside the official exchange. This provides a valid
experimental starting path. A validation feature array is not an exchange reset
state. The external audit must use actual executions, cancel resting leftovers,
and attempt to close actual inventory before the exchange closes.

The proposed direct CPU client is an experimental adapter. The official server
uses CUDA and optionally half precision. Positive cash profit in this experiment
would establish profitable simulated execution under the stated initialization,
policy, and fee assumptions. It would not establish real market manipulation,
universal arbitrage, or a neural simulator defect against known counterfactual truth.

Review scope: static inspection of source text inside the cached official ZIP.
No imports of MarS, models, inference, tests, or execution were performed.

## Primary source inspected

Repository pin: `microsoft/MarS`, commit
`f04dd87a4d56342a6a2fc271cdb158fbacd83674`.
Archive: `data/external-baselines/mars-2m-pinned-v1/official-source.zip`.
Line numbers below refer to source at this exact pin.
[Official source](https://github.com/microsoft/MarS/tree/f04dd87a4d56342a6a2fc271cdb158fbacd83674).

## Initialization and state contracts

1. `market_simulation/examples/market_impact.py:32–60,99–163` constructs
   `NoiseAgent(init_price=100000, interval_seconds=1, seed=seed)` until
   `init_end_time`. It constructs `BackgroundAgent(..., init_agent=init_agent)`
   starting at that boundary. It registers both with the same `Env` and registers
   `OrderState(num_max_orders=C.order_model.seq_len, ... converter=converter)` and
   `TradeInfoState` on the exchange. Reuse this actual sequence of APIs.
2. `BackgroundAgent` copies initialization agent base information on its first
   active action. `BaseAgent.init_base_info`, lines 49–60, shares dictionary objects
   for state, resting orders, and holdings; it copies scalar cash. This is not a
   general independent snapshot/restore API. Register agents in the official
   example's order and do not clone just the features as a substitute.
3. `OrderState.to_vector`, lines 319–328, concatenates available tokens without
   padding. Before first learned inference require exactly
   `seq_len * token_dim` int32 elements and a valid latest book snapshot.
   A fixed warmup duration alone does not guarantee enough tokens: consecutive
   cancels may merge. Log insufficient history as initialization failure.
4. `ModelClient.test_model_client` uses validation feature arrays to test prediction.
   These do not contain exchange order ownership, outstanding orders, agent cash,
   or inventory. They must not be called historical exchange reset states.
5. Noise initialization is officially demonstrated. Its distribution need not
   equal the model's real training distribution. Report this external validity
   limitation separately from adapter correctness.

## Sampling contract and CPU adapter

- Official `OrderModelServing`, lines 23–46, loads `OrderModel.from_pretrained`,
  moves to CUDA, calls `eval`, optionally uses half precision, reshapes features
  to `(batch, seq_len, token_dim)`, and calls `model.sample(features, temperature)`.
- `OrderModel.sample`, lines 158–165, takes final-token logits, divides by
  temperature, applies softmax, and calls `torch.multinomial(...,1,replacement=True)`.
  Greedy `top` is a different policy and must not replace sampling silently.
- A direct client must return the same interface as `ModelClient.get_prediction`:
  one integer class in a flattened array. Decoding belongs to
  `OrderState.get_pred_order_info`, followed by the official converter sampling.
- `BinConverter.sample`, lines 77–85, uses global NumPy randomness. Torch seed
  alone is insufficient. Noise initialization uses its own Python random seed;
  cancellation tie handling can use global Python randomness. Record all seeds,
  temperature, dtype, model/converter pins, and CPU device.
- `BackgroundAgent` first samples a planned action, then executes it at the
  sampled later time. Its concrete price uses the sampling-time mid price.
  Preserve both phases. Recomputing price from arrival-time mid changes the model.
- CPU float32 can differ numerically and in random draws from official CUDA or
  half precision. Describe architectural/API reuse and these runtime differences;
  do not claim bitwise equivalence or official default CPU support.

## Actual fills and terminal inventory

`Transaction` contains time, symbol, price, volume, buy/sell order IDs, and
optional `order_matched_volume`. `BaseAgent.on_order_executed`, lines 141–184,
changes cash and holdings from actual matched quantities. Cancels release
reserved quantities without a cash trade. The exchange/engine assigns order IDs
and maps them to agent ownership (`Engine:111–133,291–311`).

Recommended ledger:

- Identify the auditing agent by its registered ID, not a hardcoded example ID.
- Maintain buy and sell fill quantities and cash changes from its execution
  notifications. If replaying transactions independently, map each order ID to
  owner and use per-order matched volume when present. Exclude `C` transactions
  from traded cash and volume. Avoid counting a fill once per notification twice.
- Reconcile independent signed-fill inventory and cash with the agent's actual
  `holdings[symbol]` and `cash` after all result events have been processed.
- Fees are absent from these base cash updates. Apply explicitly declared fees
  once to actual executed notional. Price units are integer ticks; use documented
  normalization and do not label raw `100000` as a currency amount without scale.

An aggressive limit order is not an immediate-or-cancel market order.
`Orderbook:250–311` matches at resting level prices and puts unmatched remainder
on the book. Therefore cancel remaining entry orders and process cancellations
before reversing. Otherwise entry orders can execute during exit, and opposite
own resting orders can interact: `Level:59–78` has no owner-based self-trade
prevention. Such execution is an accounting/control confound.

Exit size must follow filled holdings, not submitted entry quantity. A terminal
close attempt must submit against available liquidity before market close, leave
time for notifications/cancels, and record unsuccessful residual inventory.
`BaseAgent.on_market_close` is a no-op; it does not liquidate holdings.
Orders outside the trading period are ignored by `Engine:257–277`.

## Failure denominator and claims

Record separately: warmup/history failure, inference error, empty book, partial
entry, partial exit, nonzero terminal inventory, and successful flat round trip.
The audit denominator is every attempted run, with counts and reasons. Closed-cycle
cash profit requires zero final inventory and no resting audit orders. Report
conditional profit on successful flat cycles alongside completion rates; incomplete
positions are not flat-cycle profits. Do not silently assign them zero profit.

Pair buy-first and sell-first policies with declared initialization seeds. A
passive baseline helps diagnose drift. Identical RNG seeds do not imply identical
future event paths after intervention because states and event schedules diverge.
Report any selected profitable schedule on fresh confirmation seeds, without
selecting confirmation seeds by success or profitability.

Even a profitable flat cycle can reflect directional drift, initialization,
stochastic sampling, or a policy exploiting the simulated environment. Separate
these explanations from evidence of action-dependent impact composition defects.
The admissible synthetic reference proof does not transfer to MarS's learned
order distribution. A finite unprofitable bank likewise proves no universal
no-manipulation property.

## Review verdict

Proceed with the bounded external runtime/audit under these contracts. The largest
implementation risks are insufficient warmup history, stale base-state copying,
resting entry leftovers, counting requested quantities as fills, and treating
market close as liquidation. This review establishes source-level API readiness;
runtime success and statistical evidence remain to be established by actual runs.
