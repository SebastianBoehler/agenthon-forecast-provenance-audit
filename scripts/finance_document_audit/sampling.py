"""Executive summary: choose questions using only source identity, type and context."""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass

from common import canonical, digest, require_table, require_text
from joins import exact_question_context_join


@dataclass(frozen=True)
class Candidate:
    source: str
    native_id: str
    native_context_id: str
    native_report_id: str | None
    group_id: str
    question: str
    table: list
    paragraphs: list[str]
    original_context: dict
    native_answer_type: str | None
    context_sha256: str
    question_sha256: str
    order_sha256: str

    def metadata(self) -> dict:
        row = asdict(self)
        for key in ("question", "table", "paragraphs", "original_context"):
            del row[key]
        return row


def candidate(source: str, native_id: str, context_id: str, report_id: str | None,
              question: str, table: list, paragraphs: list[str], kind: str | None,
              salt: str, original_context: dict) -> Candidate:
    context_hash = digest(canonical({"table": table, "paragraphs": paragraphs}))
    question_hash = digest(canonical({"question": question, "context": context_hash}))
    order_hash = digest(canonical([salt, source, native_id, question_hash]))
    return Candidate(source, native_id, context_id, report_id, report_id or context_id,
                     question, table, paragraphs, original_context, kind, context_hash, question_hash,
                     order_hash)


def finqa_candidates(rows: list[dict], salt: str) -> tuple[list[Candidate], dict]:
    candidates = []
    for row in rows:
        native_id = require_text(row["id"], "FinQA ID")
        match = re.fullmatch(r"([^/]+)/([0-9]{4})/(.+\.pdf)-([0-9]+)", native_id)
        if not match:
            raise ValueError(f"Unrecognized native FinQA report/page ID: {native_id}")
        report_id = "/".join(match.group(1, 2))
        context_id = report_id + "/" + match.group(3)
        table = require_table(row["table"], "FinQA table")
        paragraphs = row["pre_text"] + row["post_text"]
        if not isinstance(paragraphs, list) or any(not isinstance(p, str) for p in paragraphs):
            raise ValueError("FinQA text must be a string list")
        question = require_text(row["qa"]["question"], "FinQA question")
        candidates.append(candidate("finqa", native_id, context_id, report_id,
                                    question, table, paragraphs, None, salt,
                                    {"pre_text": row["pre_text"], "table": table,
                                     "post_text": row["post_text"]}))
    return candidates, {"native_rows": len(rows), "eligible_rows": len(candidates),
                        "report_identity": "company/year parsed from native report/page ID"}


def tatqa_candidates(raw: list[dict], gold: list[dict], salt: str,
                     allowed_types: list[str]) -> tuple[list[Candidate], dict]:
    gold_questions, join_metadata = exact_question_context_join(raw, gold)
    candidates, types, seen = [], Counter(), set()
    context_ids = set()
    for context in raw:
        context_id = require_text(context["table"]["uid"], "TAT-QA context/table UID")
        if context_id in context_ids:
            raise ValueError("Duplicate TAT-QA native context/table UID")
        context_ids.add(context_id)
        table = require_table(context["table"]["table"], "TAT-QA table")
        paragraphs = [require_text(p["text"], "TAT-QA paragraph") for p in context["paragraphs"]]
        original_context = {"table": {k: context["table"][k] for k in ("uid", "table")},
                            "paragraphs": [{k: p[k] for k in ("uid", "order", "text")}
                                           for p in context["paragraphs"]]}
        for question in context["questions"]:
            uid = require_text(question["uid"], "TAT-QA question UID")
            if uid in seen:
                raise ValueError("Duplicate TAT-QA raw question UID")
            seen.add(uid)
            text = require_text(question["question"], "TAT-QA question")
            if uid not in gold_questions:
                continue
            annotation = gold_questions[uid]
            if text != annotation["question"]:
                raise ValueError("TAT-QA raw/gold question identity mismatch")
            kind = require_text(annotation["answer_type"], "native TAT-QA answer type")
            types[kind] += 1
            if kind in allowed_types:
                candidates.append(candidate("tatqa", uid, context_id, None, text,
                                            table, paragraphs, kind, salt, original_context))
    return candidates, {"native_rows": len(seen), "native_contexts": len(raw),
                        "eligible_rows": len(candidates), "answer_type_counts": dict(types),
                        "excluded_noneligible_native_types": len(gold_questions) - len(candidates),
                        "excluded_missing_annotation_identity": len(seen) - len(gold_questions),
                        "identity_join": join_metadata,
                        "report_identity": "unknown; grouping uses native context/table UID"}


def select(candidates: list[Candidate], count: int,
           occupied_contexts: set[str], occupied_questions: set[str]) -> tuple[list[Candidate], dict]:
    selected, groups, skipped = [], set(), Counter()
    for row in sorted(candidates, key=lambda c: (c.order_sha256, c.native_id)):
        if len(selected) == count:
            break
        reason = None
        if row.group_id in groups:
            reason = "native_group_already_selected"
        elif row.context_sha256 in occupied_contexts:
            reason = "exact_context_already_selected"
        elif row.question_sha256 in occupied_questions:
            reason = "exact_question_context_already_selected"
        if reason:
            skipped[reason] += 1
            continue
        selected.append(row)
        groups.add(row.group_id)
        occupied_contexts.add(row.context_sha256)
        occupied_questions.add(row.question_sha256)
    return selected, {"target": count, "selected": len(selected),
                      "shortfall": count - len(selected), "skipped_until_stop": dict(skipped)}
