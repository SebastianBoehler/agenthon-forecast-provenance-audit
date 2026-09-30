"""Executive summary: adversarial controls for exact excerpt provenance and citation coverage."""

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from citation_assets import digest, extract
from citation_draft import inventory
from citation_evidence import bind_evidence, check_run
from citation_excerpt_integrity import check_excerpt, locate_excerpt


class ExcerptIntegrityTests(unittest.TestCase):
    def test_whitespace_mapping_keeps_exact_raw_text(self):
        raw = "Header\nA naïve model\n  reports 18 of 22.\nFooter"
        record = locate_excerpt(raw, "A naïve model reports 18 of 22.")
        self.assertEqual(record["excerpt"], "A naïve model\n  reports 18 of 22.")
        check_excerpt(raw, record)

    def test_numeric_fabrication_does_not_match(self):
        self.assertEqual(locate_excerpt("Matches: 18 of 22.", "Matches: 19 of 22.")["integrity"], "unlocated")

    def test_disjoint_passages_do_not_become_a_quote(self):
        self.assertEqual(locate_excerpt("A is true. B is uncertain. C is false.", "A is true. C is false.")["integrity"], "unlocated")

    def test_duplicate_excerpt_is_disclosed(self):
        self.assertEqual(locate_excerpt("Same text. Same text.", "Same text.")["match_count"], 2)

    def test_shifted_offset_is_rejected(self):
        record = locate_excerpt("Header. Exact evidence.", "Exact evidence.")
        record["start_char"] += 1
        with self.assertRaises(ValueError):
            check_excerpt("Header. Exact evidence.", record)

    def test_modified_quote_and_forged_digest_are_rejected(self):
        record = locate_excerpt("Evidence says 18.", "Evidence says 18.")
        record["excerpt"] = "Evidence says 19."
        record["excerpt_sha256"] = digest(record["excerpt"].encode())
        with self.assertRaises(ValueError):
            check_excerpt("Evidence says 18.", record)

    def test_empty_candidate_is_unlocated(self):
        self.assertEqual(locate_excerpt("Some text.", "  ")["integrity"], "unlocated")


class SourceAndDraftTests(unittest.TestCase):
    def test_blank_pdf_page_is_preserved(self):
        class Page:
            def __init__(self, text): self.text = text
            def extract_text(self): return self.text
        class Reader:
            pages = [Page("Page one."), Page(""), Page("Page three.")]
        with patch("pypdf.PdfReader", return_value=Reader()):
            self.assertEqual(extract(Path("authored-control.pdf"), "pdf"), ["Page one.", "", "Page three."])

    def test_wrong_source_key_is_rejected(self):
        with self.assertRaises(ValueError):
            bind_evidence({"source_id": "a:0", "citation_key": "b", "text": "Quote."},
                          {"a:0": ({"key": "a"}, {}, ["Quote."])})

    def test_table_multiline_and_appendix_citations_are_inventoried(self):
        text = r"""\documentclass{article}
\begin{document}
\section{Introduction}
Dataset A has a reasoning program~\cite{a}
and explicit units.

% A commented citation must not count: \cite{false}
\begin{table}
\begin{tabular}{ll}
Dataset B uses tables~\cite{b}. & Our contribution.\\
\end{tabular}
\end{table}

\begin{thebibliography}{9}
\bibitem{a} A.
\end{thebibliography}

\section{Appendix}
Method C executes code~\cite{c}.
\end{document}
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "authored-control.tex"
            path.write_text(text)
            claims, occurrences = inventory(path)
        self.assertEqual({k for o in occurrences for k in o["citation_keys"]}, {"a", "b", "c"})
        self.assertTrue(all(o["parser_covers_keys"] for o in occurrences))
        self.assertEqual(len(claims), 3)

    def test_draft_changes_invalidate_saved_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "paper.tex").write_text("Changed draft")
            (root / "receipt.json").write_text(json.dumps({
                "draft": "paper.tex", "draft_sha256": digest(b"Original draft")}))
            with self.assertRaisesRegex(ValueError, "Draft changed"):
                check_run(root, root)


if __name__ == "__main__":
    unittest.main()
