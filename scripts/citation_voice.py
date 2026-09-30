"""Executive summary: reuse CiteProof's revision-bound audit for the author-led voice draft."""

import audit_paper_citations as audit

audit.DRAFT = "paper/answer_contract_voice_draft.tex"
audit.CATALOG = "literature/citations/voice_source_catalog.json"

if __name__ == "__main__":
    audit.main()
