## Executive summary (read this first)

This pilot asks whether repeated latent computation and officially dated Federal Reserve statement text improve **probabilistic** next-trading-day 10-year Treasury yield-change forecasts. It is a feasibility gate for a possible Agenthon Track 2 paper, not a submission result. The analysis uses separate public Federal Reserve and FRED data and no Agenthon sealed answers.

## Dataset and information cutoff

- Collect official FOMC statement HTML pages dated 2000-01-01 through the frozen collection cutoff 2025-09-29 from Federal Reserve year archives and meeting calendar. Retain URL, statement date, content SHA256, and plain text. Do not treat meeting minutes as same-day statements.
- Collect daily DGS10 from the Federal Reserve via FRED's public CSV. DGS10 is the 10-year Treasury constant-maturity yield in percentage points.
- At the **evening after a statement**, use that day's DGS10 value and the 20 previous observed trading-day changes, plus the statement published that day. Predict the difference between the next observed DGS10 trading day and the statement-day value. There is no intraday policy-surprise claim.
- Current downloadable historical DGS10 can contain retrospective corrections. This is a point-in-time *date cutoff*, not a verified vintage-exact market feed. Mark this explicitly in results.
- Keep only statements with nonmissing statement-day and next observed trading-day yield. If a statement is on a nontrading day, exclude and count it. Record duplicate statement dates and exclude extras rather than silently multiply cases.
- Use chronological splits: train statement dates 2000–2018, validation 2019–2022, untouched test 2023–2025. Fit TF-IDF/SVD text features and normalization using training dates only. Final model choice uses validation only.

## Minimal model comparison

1. Gaussian climatology from train outcomes, and a regularized linear model on numeric history, as sanity baselines.
2. One-pass transformer on numeric tokens plus one text token, and the same architecture with text ablated.
3. Weight-tied transformer block applied three times; compare text and no-text.
4. Three unshared blocks at approximately the same attention compute. Report parameter count and actual CPU inference time.

The neural models output Gaussian mean and scale, train by Gaussian negative log likelihood, and use analytic Gaussian CRPS for evaluation. Keep model width, optimizer, split, training budget and random seed fixed within this small pilot. If resources permit, run three initialization seeds; report all. Use the same validation selection policy for all neural models. If a text benefit appears, a within-year text-shuffle control can test whether improvement responds to statement identity. With fixed depth this pilot cannot test evidence-adaptive computation.

## Feasibility and interpretation gate

The first gate is data integrity and enough dated cases (>100 train, >20 validation, >20 test). The second is reproducible, finite CRPS for every baseline. The third is looped gain over both the one-pass and equal-compute deeper model on held-out dates without a loss of calibration. A single small pilot cannot establish novelty, causal benefit of text, or assured workshop acceptance. If it fails, report the failure and retain the artifact rather than writing a positive paper claim.
