## Executive summary (read this first)

Before complete-panel scoring, correct the supplementary parser to reject a
contradictory currency prefix with a percent suffix. Preserve the strict primary
protocol, every response, the first supplementary freeze and its implementation
snapshot. This is a documented implementation correction, not a new extraction rule.

## Evidence and correction

Two independent technical reviewers reproduced the synthetic edge case
`FINAL: $7.25 percent`: the supplementary parser incorrectly let the percent
suffix override the currency prefix. The original amendment already requires
rejecting explicitly inconsistent units. The correction implements that rule.
No such case was seen in the incomplete live ledger checked by the reviewers.
The complete-panel census will report whether any real response is affected.

The strict parser is unchanged. Supplementary scoring checks the version-two
freeze hashes and records that freeze hash. The original supplementary parser
and driver are saved under `outputs/model-grading-v1/sensitivity-original/`;
`numeric_sensitivity_freeze.json` remains intact. No answer is regenerated.
