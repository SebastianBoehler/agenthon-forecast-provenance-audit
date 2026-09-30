## Executive summary (read this first)

This is a finite external diagnostic of the pinned public MarS 2m model, not a claim of real-market arbitrage. The primary question is whether the actual exchange can complete short-horizon buy–sell and sell–buy cycles with negative cash cost under noise initialization. We count every attempted episode, including no fills, failed runs, open orders, and nonzero terminal inventory.

## Frozen before the multi-seed run

- Official source `f04dd87a4d56342a6a2fc271cdb158fbacd83674`; model `b8f8c818c2a270844961b975f311457628bf2972`; assets `de761abefc1e3c0a8106a03b4fed6fc73cf702d3`.
- The experimental transport calls the unchanged pinned `OrderModel.sample` with temperature 1, CPU fp32 and one torch thread. The official Ray/HTTP/CUDA/fp16 serving path is not being replicated.
- One symbol; official `NoiseAgent` starts at 09:30, one-second interval, price 100000. Warmup lasts 1500 seconds. The official `BackgroundAgent` then samples until 09:55:20. The `OrderState` uses 1024 orders and all 13 released converters.
- Seeds: 30 initialization seeds 7101 through 7130. Corresponding model/NumPy/Python-global seeds 7001 through 7030. Each seed is run separately in buy–sell and sell–buy directions with the same model seed and noise seed. Both directions begin at 09:55:02.
- The probe submits one marketable 100-unit limit order, cancels any remainder after one second, reverses its **actual** inventory two seconds later, cancels any remainder after a further second, tries to flatten actual residual inventory at four seconds, and cancels again at five seconds. The market stays open 20 seconds after background begins.
- Cash starts at 100,000,000 simulator units. Short selling is permitted by this exchange; no borrowing fee or finance constraint exists in this pilot. Record direction explicitly.
- A completed cycle requires terminal inventory zero, at least one entry fill and one opposite exit fill, and no open orders. Its cost is negative final cash change. A failed or censored run stays in the denominator but has no completed-cycle cost.
- Report 60/60 outcome statuses, completion, profitable/negative-cost rate among completed and attempted, cost distribution by direction, runtime, and model call counts. These are descriptive finite-bank numbers. No p-value or causal claim from common seeds alone.
- A price-cycle profit here would show simulator trading opportunity under this protocol. It would not establish a wrong learned response without a valid reference market or correction and fidelity checks.

## Reproducibility correction before final bank

An initial 60-episode run did not seed Python global randomness, which the official cancellation tie handler may consume. Its outputs are preserved as exploratory under `outputs/market-cycle/mars-external-v3-unseeded-python-pilot/`. The final run below seeds Torch, NumPy, and Python global RNG with the corresponding model seed. No interpretation or selection changed after seeing the exploratory bank.

## Pilot before the freeze

One buy–sell episode with initialization seed 7101 and model seed 7001 completed: buy 100 at 99700, sell 100 at 99600, final cash change −10000, inventory 0. It was used only for runtime/interface readiness and is included as a prespecified seed in the finite bank; do not represent it as independent confirmation.
