## Executive summary (read this first)

The frozen384-attempt collection returned383 actual API records. Seven record
transport failures; one additional DeepSeek reminder attempt never returned.
At2026-09-30 01:27:23 UTC the local collector was terminated after more than eight
minutes without that final result. No request was retried, provider changed,
prompt repaired or answer inferred. Its remote completion/cost remain unknown.

`responses.jsonl` preserves all383 actual records unchanged. A separate derived
`effective_attempts.jsonl` retains them verbatim and adds an explicitly identified
censored-attempt event: no raw response, empty text, unknown elapsed time/cost and
collector error. Its metadata is reconstructed from the frozen planned request;
it is not a fabricated API response. The pending case is TAT-QA
`b5310b6e-25a0-4d4e-9c6b-62291a6be033`, DeepSeek quantity reminder. Its reference
is conditional, outside the original 62-case numerical subset.

The original frozen analyzer requires a complete384-record raw response ledger
and a normal completion receipt; it cannot replay this interrupted collector.
Retain it unchanged. `close_finance_document_collection.py` and the saved-artifact
replay script explicitly handle the recorded closure. They reuse the unchanged
frozen parser, comparator and native adapter; the censored attempt is a failure,
never a denominator exclusion. Record both raw-ledger and derived-ledger hashes.

The later closure does not turn a prospective model protocol into preregistered
failure handling. Report the intervention and unknown cost. Summed provider-
reported cost excludes missing usage, rather than treating it as zero. The pinned
conservative request bound still covers every originally attempted request.
