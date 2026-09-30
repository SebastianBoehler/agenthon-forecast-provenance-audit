## Executive summary (read this first)

The first public-data feasibility pilot **does not support the proposed looped-text forecasting paper**. On 22 held-out 2023–2025 Federal Open Market Committee (FOMC) statements, the three-pass weight-tied transformer averaged 4.557 basis points (bp) Gaussian continuous ranked probability score (CRPS) with statement text versus 4.504 bp without it. Lower is better. It was also worse than the equal-attention-compute, three-block untied text model (4.494 bp) and a one-pass blind model (4.521 bp). The differences are small relative to the sample, so this is a failure to find a promising effect, not a proof that text or recurrence cannot help finance forecasting.

## Research question and decision rule

Could dated financial text make extra latent computation more useful for a probabilistic forecast, beyond a one-pass text model and an equal-compute deeper model? The frozen [pilot specification](LOOPED_FORECAST_PILOT_SPEC_V1.md) required a held-out gain over both those controls without worse calibration. That gate failed. This pilot has fixed one or three passes; it does not implement or assess evidence-adaptive stopping.

## Data and provenance

- Source: official [Federal Reserve FOMC statement archives](https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm) and [meeting calendar](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm). The calendar also links minutes and projections, so the harvester admits only the monetary-statement HTML URL pattern; minutes are excluded. Statement HTML/text SHA256 and URL are in the ignored local data manifest.
- Target: next *observed trading-day* change in the [DGS10 ten-year Treasury constant-maturity yield](https://fred.stlouisfed.org/series/DGS10), in basis points. The prediction time is the evening of the statement, after that day's yield is known. This is not an intraday policy-reaction forecast.
- Frozen source cutoff: 2025-09-29. Harvest: 218 statement pages, zero download failures; the Sunday statements of 2010-05-09 and 2020-03-15 lack same-day DGS10 and are excluded. No duplicate dates survive. The final 216 cases split chronologically into 160 train (2000–2018), 34 validation (2019–2022), and 22 test (2023–2025).
- Input: statement text, current DGS10, and 20 prior observed daily changes. The next-day change is excluded from inputs. TF-IDF, 16-dimensional text singular-value decomposition, and input/target normalization are fit on training dates only. This follows a date cutoff, but the downloadable DGS10 series may include later revisions; vintage exactness is unverified.

## Method

Each neural model uses 32-dimensional tokens, four attention heads, a two-layer feed-forward block, and a Gaussian mean/scale head. We compared one transformer pass, three repetitions of one shared block, and three distinct blocks, each with text enabled or zeroed. Three seeds (7, 17, 37) were run per neural condition. Gaussian negative log likelihood trained the models; validation Gaussian CRPS selected the checkpoint. A train-only Gaussian climatology and validation-selected ridge/scale baseline were included. The three-pass conditions have approximately equal attention work, though the untied model has more parameters. Per-case latency, parameter count, checkpoint epoch, coverage, and predictions are recorded in the ignored local results.

## Results

Mean held-out Gaussian CRPS across three seeds, in bp; lower is better. Parentheses give the seed-to-seed standard deviation, **not** a confidence interval over statement dates.

| Model | Validation CRPS | Test CRPS | Test 90% coverage |
|---|---:|---:|---:|
| Train Gaussian climatology | 3.761 | 4.597 | 0.909 |
| Numeric ridge with selected scale | 3.480 | 5.009 | 0.773 |
| One pass, no text | 3.666 | 4.521 (0.034) | 0.924 |
| One pass, text | 3.674 | 4.597 (0.136) | 0.864 |
| Three tied passes, no text | 3.639 | 4.504 (0.019) | 0.924 |
| Three tied passes, text | 3.653 | 4.557 (0.046) | 0.818 |
| Three untied passes, no text | 3.632 | 4.470 (0.042) | 0.909 |
| Three untied passes, text | 3.640 | 4.494 (0.017) | 0.879 |

The tied three-pass text model loses to its no-text version by 0.053 bp on average and has lower nominal 90% coverage (0.818 versus 0.924). It wins only 10 of the 22 held-out cases against the no-text version. Its paired CRPS difference varies by year: +0.208 bp in 2023, +0.032 in 2024, and −0.126 in 2025. This instability and the small sample do not justify a positive interaction claim. The best aggregate neural score is the untied no-text model, which is not the proposed method.

The one-pass and tied three-pass models each have 9,954 trainable parameters; the untied three-pass model has 27,042. Mean CPU inference latency was about 0.019 ms per case for one pass, 0.052 ms for three tied passes, and 0.054 ms for three untied passes. These are small local-batch measurements, not deployment throughput benchmarks.

## Limits and decision

The 216 events are correlated policy dates, with only 22 held-out cases. The task is univariate and Gaussian; it does not test Agenthon Track 2's joint dependence or tail scoring. The current FRED series is not a vintage-exact reconstruction. Old HTML pages include small amounts of page chrome. We did not run semantic text shuffles after the main text-benefit gate failed; such controls would be mandatory before any text-faithfulness claim. We also did not tune or compare recent time-series foundation models in this kill test.

**Decision:** do not write a submission claiming that fixed looped transformers exploit FOMC text better than equal-compute alternatives. The [nearest-work review](LOOPED_FORECAST_LITERATURE_REVIEW_V1.md) already shows that looped time-series modeling, text fusion, and iterative finance refinement exist. A separate, substantive mechanism and independently replicated positive results would be needed for a competitive Agenthon poster paper.

## Reproduction and research record

From the repository root, with the existing Python environment and network access, run `PYTHONPATH=src .venv/bin/python scripts/build_fomc_dataset.py` and then `PYTHONPATH=src .venv/bin/python scripts/run_looped_forecast_pilot.py`. Outputs are under ignored `data/fomc-looped-pilot-v1/` and `outputs/looped-forecast-pilot-v1/`. The harvest records source hashes; a later rerun may differ if the official pages or FRED history change. The scripts, specification, literature critique, and this negative-result report retain the code evolution and why this idea was stopped.
