## Executive summary (read this first)

The first controlled-reference pilot completed. Its admissible model has an
analytical nonnegative expected cycle cost; the intentionally invalid model is
detected by all four declared schedules. These are infrastructure results for a
specified synthetic market. No neural model was trained or audited, and no paper
novelty or external-simulator defect is established.

## Run record

- Python: 3.13.2; platform: Darwin arm64.
- Run: `PYTHONPATH=src python -m market_cycle --config experiments/reference_controls_v1.json --output outputs/market-cycle/reference-controls-v1.json`
- 512 independent Gaussian market episodes, four fixed schedules, two controls.
- Configuration SHA-256: `0345775591d815c42459ae182f75e5b7fd8ed88ad94fd85235b6a40fd1e6fa7d`.
- Source hashes and all fill ledgers are in the ignored result JSON.
- Models share fixed-grid exogenous noise; no episodes were discarded.

## Measured costs

| Schedule | Model | Exact expected cost | Sample mean | Simultaneous 95% interval |
| --- | --- | ---: | ---: | --- |
| two_trade | admissible_reference | 1.001301 | 0.995522 | [0.753836, 1.237208] |
| two_trade | invalid_self_impact_control | -6.998699 | -7.004478 | [-7.246164, -6.762792] |
| hold_then_close | admissible_reference | 2.877440 | 2.871683 | [2.388310, 3.355055] |
| hold_then_close | invalid_self_impact_control | -5.122560 | -5.128317 | [-5.611690, -4.644945] |
| slow_entry_fast_exit | admissible_reference | 1.516983 | 1.535530 | [1.204587, 1.866473] |
| slow_entry_fast_exit | invalid_self_impact_control | -3.483017 | -3.464470 | [-3.795413, -3.133527] |
| fast_entry_slow_exit | admissible_reference | 1.516983 | 1.491240 | [1.160297, 1.822183] |
| fast_entry_slow_exit | invalid_self_impact_control | -3.483017 | -3.508760 | [-3.839703, -3.177817] |

## Interpretation

- All declared ledgers close: True.
- All four valid analytical expected costs are nonnegative: True.
- Two-trade invalid upper cost bound is below the declared -0.10 threshold: True.
- Each reported interval contains its corresponding analytical expectation.
- No inference rests on every reference episode being unprofitable; random
  profitable episodes are compatible with nonnegative expected cost.
- The mathematical guarantee is inherited from the stipulated kernel and fill
  convention, not established by observing four schedules.

## Remaining scientific work

Freeze the neural learning experiment and equal-budget coverage comparison.
Use a correct common ledger for both learned and reference responses. Do not
treat deliberately omitted self-impact as a learned failure or as novelty.
The independent reference review and proof establish foundation validity; they
do not establish the proposed mechanism or repair.
