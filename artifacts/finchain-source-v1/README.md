## Executive summary (read this first)

These are verbatim files from MBZUAI NLP's FinChain repository, pinned to
`9bd2942b85d992844b77094a8b822aa16832703c`. They enable the new finite source-code
comparison; they do not recover the historical ACL paper's 2,900 instances.

The [source manifest](source_manifest.json) records original paths, complete-file
SHA-256 hashes and contiguous fragment intervals. Reassembly preserves all original
bytes. Splitting long files keeps source fragments below 180 lines; no source body
is edited. `independent_finance.source.sources()` verifies fragments and complete
files before loading the selected functions.

The current author's Apache-2.0 license and README notices are retained verbatim in
`LICENSE_001_180.txt`, `LICENSE_181_202.txt` and `readme_*`. The historical paper's
MIT statement and separately pinned demo are different artifact/version scopes.
This directory preserves the current code's license, attribution and notices.

Only three inspected function definitions and their original literal entity pools
are executed. Imports, main scripts, file-writing paths and other functions are
excluded. WACC uses the original `misc.py` company pool. Randomness comes from one
`random.Random(seed)` per original function invocation, with the declared Python
runtime. Upstream source: [FinChain pinned tree](https://github.com/mbzuai-nlp/finchain/tree/9bd2942b85d992844b77094a8b822aa16832703c).

The linked [protocol](../../docs/INDEPENDENT_FINCHAIN_CODE_PROTOCOL_V1.md) and
[results](../../docs/INDEPENDENT_FINCHAIN_CODE_RESULTS_V1.md) distinguish exact
question-visible arithmetic, source intermediate rounding and wrong-quantity
controls. These checks do not run native ChainEval or evaluate reasoning traces.
