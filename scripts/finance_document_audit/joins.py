"""Executive summary: reconcile changed native IDs by exact original input identity."""
from __future__ import annotations

from common import canonical, digest


def context_hash(context: dict) -> str:
    return digest(canonical({"table": context["table"]["table"],
                             "paragraphs": [p["text"] for p in context["paragraphs"]]}))


def question_key(context: dict, question: dict) -> str:
    return digest(canonical([context_hash(context), question["question"]]))


def exact_question_context_join(raw: list[dict], gold: list[dict]) -> tuple[dict, dict]:
    mapping, gold_ids, raw_ids, native_id_matches = {}, set(), set(), 0
    gold_by_key = {}
    for context in gold:
        for question in context["questions"]:
            uid = question["uid"]
            if uid in gold_ids:
                raise ValueError("Duplicate TAT-QA gold question UID")
            gold_ids.add(uid)
            key = question_key(context, question)
            if key in gold_by_key:
                raise ValueError("Ambiguous duplicate TAT-QA gold question/context identity")
            gold_by_key[key] = question
    seen_keys, joined_gold_ids, missing_raw = set(), set(), []
    for context in raw:
        for question in context["questions"]:
            uid = question["uid"]
            if uid in raw_ids:
                raise ValueError("Duplicate TAT-QA raw question UID")
            raw_ids.add(uid)
            key = question_key(context, question)
            if key in seen_keys:
                raise ValueError("Ambiguous duplicate TAT-QA raw question/context identity")
            seen_keys.add(key)
            if key not in gold_by_key:
                missing_raw.append(uid)
                continue
            annotation = gold_by_key[key]
            mapping[uid] = annotation
            joined_gold_ids.add(annotation["uid"])
            native_id_matches += int(uid == annotation["uid"])
    return mapping, {
        "strategy": "unique exact original table/ordered text plus question SHA-256",
        "raw_questions": len(raw_ids), "gold_questions": len(gold_ids),
        "joined_questions": len(mapping), "joined_native_uid_equal": native_id_matches,
        "native_question_uid_overlap": len(raw_ids & gold_ids),
        "unmatched_raw_question_uids": sorted(missing_raw),
        "unmatched_gold_question_uids": sorted(gold_ids - joined_gold_ids),
        "original_answer_values_used_for_join": False,
        "context_identity": "Exact input strings/cells/order; no fuzzy matching or semantic repair"
    }
