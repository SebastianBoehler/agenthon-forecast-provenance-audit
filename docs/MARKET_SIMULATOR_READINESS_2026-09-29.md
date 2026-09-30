## Executive summary (read this first)

Read-only inspection confirms released MarS weights and shared simulation assets.
TRADES supplies an official checkpoint link, but those files were not fetched or
validated. Neither runtime was installed or executed. Available source code is
not proof of experiment readiness. The causal core requires separately specified
known-reference training data; pretrained generators support external diagnostics.

Inspection date: 29 September 2026. Small source snapshots and API metadata are
cached locally under ignored `literature/pdfs/market-cycle-source-inspection/`.
No competition-private inputs are involved.

## MarS: first external diagnostic target

| Item | Verified observation |
| --- | --- |
| Source revision | `f04dd87a4d56342a6a2fc271cdb158fbacd83674` from GitHub main commit API |
| Published sizes | Official README lists released 2M, 5M, 10M; larger models are not released |
| 2M checkpoint revision | `b8f8c818c2a270844961b975f311457628bf2972` |
| Checkpoint access | HF API reports public, ungated; model.safetensors is 10,101,496 bytes |
| Model license metadata | MIT; retain actual model and data license files on download |
| Assets revision | `de761abefc1e3c0a8106a03b4fed6fc73cf702d3` |
| Shared assets | Converters, a validation-sample archive and a stylized-facts archive are publicly listed |
| Runtime | Official Dockerfile uses CUDA 12.4.1, Ubuntu 22.04 and Python 3.12; README says direct installation unsupported |
| Serving | Ray model server plus client, exchange and background-agent code |
| Existing intervention | market_impact.py creates a buy-direction TWAP agent and compares rollout groups |
| Initialization | That example uses a noise agent before learned background generation |

Primary sources:
[repository](https://github.com/microsoft/MarS),
[pinned impact example](https://github.com/microsoft/MarS/blob/f04dd87a4d56342a6a2fc271cdb158fbacd83674/market_simulation/examples/market_impact.py),
[2M model](https://huggingface.co/Don-Don/mars-order-2m),
[shared dataset assets](https://huggingface.co/datasets/Don-Don/mars-order-assets).
The assets are a dataset repository, not a model repository. A failed model-API
lookup was corrected with the dataset endpoint; it was not an access barrier.

### Required adapter work before measurement

- Implement a cycle agent with actual fill-level cash and inventory records.
  Existing one-direction TWAP evaluation is not a closed-cycle ledger.
- Verify terminal closure and costs under the exchange's actual transaction rules.
- Record generated order histories and response-conditioning state.
- Inspect and control model sampling randomness separately from initialization.
- Record failures explicitly: the impact example can return an empty list on
  rollout exceptions, which must not silently disappear from study accounting.
- Determine whether released validation states support interactive resets and
  whether their usage rights permit an artifact release. File existence alone
  does not answer either question.

No CPU compatibility, GPU memory requirement, rollout speed, complete state-reset
support or valid counterfactual coupling is established yet. The 2M file's small
size is evidence about download size, not measured runtime cost.

## TRADES / DeepMarket: second external diagnostic target

| Item | Verified observation |
| --- | --- |
| Source revision | `8f1f89b7285c79a73f528b88b60f74ce58faadc4` |
| Framework | Official TRADES repository extends ABIDES with a learned WorldAgent |
| License | Root LICENSE is MIT; bundled ABIDES has a separate license file |
| TRADES weights | README links a Google Drive folder; access and payload not validated |
| Checked-in checkpoint paths | API tree includes TSLA and INTC CGAN checkpoints; these are not TRADES weights |
| Data path | README offers public LOBSTER sample data, explicitly outside model training support |
| Paper reproduction | README requires the corresponding 2015 TSLA/INTC historical data |
| Training data | README says new training requires LOBSTER data |
| Dependencies | Unpinned requirements include Lightning, torch/torchvision CUDA 11.8, pandas, scipy and gdown |
| Interactive source | ABIDES/agent/WorldAgent.py and config/world_agent_sim.py exist |

Primary source: [official repository](https://github.com/LeonardoBerti00/DeepMarket).
Checkpoint folder:
[author-linked Drive](https://drive.google.com/drive/folders/1fg5G9KzmzC6E4FUYSCjObJ7sCEdjo43W).
Do not equate public synthetic TRADES-LOB exports with the historical training
states or an interactive simulator. Static rows alone cannot establish action
responses. Do not infer that IU library access includes LOBSTER market data.

## Controlled-reference readiness

No reference implementation or new surrogate training run exists yet. Before
implementing, fix discrete order timing, execution prices, admissible schedules,
impact kernel, affected versus unaffected prices, cost terms and random processes.
Check the resulting cost quadratic form on the permitted zero-inventory subspace.
Include a deliberately incompatible response as a declared detector control.

Known-reference synthetic data would be an authorized research benchmark with
explicit provenance, not invented measurements standing in for real experiments.
Keep the controlled tier's claims separate from real-data generator diagnostics.

## Next readiness check

1. Finish economic/full-text review before selecting the reference equations.
2. Validate checkpoint/data access and reset/ledger interfaces without treating
   either pretrained model as ground truth.
3. Establish a reproducible runtime and measure one rollout's compute cost.
4. Freeze the controlled experiment specification and training budget before
   adaptive search or repair training.

The present result is source and artifact discovery. No simulator defect,
correction benefit, empirical novelty or acceptance probability is established.
