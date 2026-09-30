"""Executive summary: append only explicit source-pointer formats to the unchanged V1 judge."""

from finance_quantity_transfer.protocol import JUDGE, OUT as V1_OUT

OUT = V1_OUT.parent / "finance-quantity-judge-v2"
PHASE = "judge_v2"
FORMAT = (
    " Evidence location FORMAT: use exact original_context-relative pointers, "
    "with zero-based integer indices. For FinQA or an authored top-level table, "
    "use table[r][c], for example table[1][1]. For FinQA prose, use pre_text[i] "
    "or post_text[i], for example pre_text[0] or post_text[1]. For TAT-QA nested "
    "tables, use table.table[r][c], for example table.table[2][1]. For TAT-QA "
    "paragraph text, use paragraphs[i].text, for example paragraphs[0].text. "
    "Replace indices with locations that actually exist in the supplied context. "
    "The evidence list must contain only these pointer strings, without prose, "
    "colon descriptions, JSONPath prefixes, or an original_context prefix. "
    "Each pointer must identify a whole table cell or paragraph string, not a "
    "character within a string; do not append character indices or extra indices. "
    "Use the same pointer format for source locations in operand_checks."
)
SYSTEM = JUDGE + FORMAT
