"""Executive summary: reconcile source identities without computing answer correctness."""
from __future__ import annotations

from collections import Counter

from common import canonical, digest
from joins import exact_question_context_join
from sampling import Candidate


def schema_inventory(rows: list[dict], source: str) -> dict:
    keys = lambda values: dict(Counter(",".join(sorted(row)) for row in values))
    inventory = {"source": source, "record_count": len(rows), "root_key_sets": keys(rows)}
    if source.startswith("finqa"):
        inventory["qa_key_sets"] = keys([row["qa"] for row in rows])
    else:
        inventory["table_key_sets"] = keys([row["table"] for row in rows])
        inventory["paragraph_key_sets"] = keys([p for row in rows for p in row["paragraphs"]])
        inventory["question_key_sets"] = keys([q for row in rows for q in row["questions"]])
    return inventory


def finqa_identity(public: list[dict], evaluator: list[dict]) -> dict:
    maps = []
    for rows in (public, evaluator):
        mapping = {row["id"]: row for row in rows}
        if len(mapping) != len(rows):
            raise ValueError("Duplicate FinQA ID in pinned source")
        maps.append(mapping)
    left, right = maps
    shared = sorted(left.keys() & right.keys())
    mismatches = Counter()
    for uid in shared:
        for field in ("table", "pre_text", "post_text"):
            if left[uid][field] != right[uid][field]:
                mismatches[field] += 1
        if left[uid]["qa"]["question"] != right[uid]["qa"]["question"]:
            mismatches["question"] += 1
    return {"public_count": len(public), "evaluator_count": len(evaluator),
            "shared_ids": len(shared), "public_only_ids": sorted(left.keys() - right.keys()),
            "evaluator_only_ids": sorted(right.keys() - left.keys()),
            "shared_input_field_mismatch_counts": dict(mismatches),
            "canonical_selection_source": "dataset/test.json regardless of evaluator input differences",
            "original_answer_values_compared": False,
            "different_complete_file_bytes_are_not_a_defect_label": True}


def tatqa_identity(raw: list[dict], gold: list[dict]) -> dict:
    def contexts(rows: list[dict]) -> dict:
        return {row["table"]["uid"]: row for row in rows}
    left, right = contexts(raw), contexts(gold)
    shared = sorted(left.keys() & right.keys())
    different = []
    for uid in shared:
        if left[uid]["table"]["table"] != right[uid]["table"]["table"] or (
            left[uid]["paragraphs"] != right[uid]["paragraphs"]
        ):
            different.append(uid)
    return {"raw_contexts": len(raw), "gold_contexts": len(gold),
            "shared_context_uids": len(shared), "input_context_mismatch_uids": different,
            "raw_only_context_uids": sorted(left.keys() - right.keys()),
            "gold_only_context_uids": sorted(right.keys() - left.keys()),
            "question_identity_join": exact_question_context_join(raw, gold)[1],
            "native_answer_type_used_for_eligibility": True,
            "original_answer_values_compared": False}


def overlap_inventory(candidates: list[Candidate], selected: list[Candidate]) -> dict:
    def count_dupes(rows: list[Candidate], field: str) -> dict:
        groups = {}
        for row in rows:
            key = getattr(row, field)
            if key is not None:
                groups.setdefault(key, []).append(row)
        duplicate_groups = [group for group in groups.values() if len(group) > 1]
        cross = [group for group in duplicate_groups if len({r.source for r in group}) > 1]
        return {"duplicate_groups": len(duplicate_groups), "cross_source_groups": len(cross),
                "cross_source_native_ids": [[r.source + ":" + r.native_id for r in group] for group in cross]}
    return {"eligible_pool": {field: count_dupes(candidates, field) for field in
                             ("context_sha256", "question_sha256", "native_report_id")},
            "selected": {field: count_dupes(selected, field) for field in
                         ("context_sha256", "question_sha256", "native_report_id")},
            "unknown_report_identity_counts": dict(Counter(
                row.source for row in candidates if row.native_report_id is None)),
            "comparison_boundary": "Exact original string/cell context only; no semantic near-duplicate or PDF/company matching.",
            "report_cross_source_overlap": "Unknown when TAT-QA lacks report identity; zero exact contexts cannot establish document disjointness."}


def source_targets(selected: list[Candidate], finqa: list[dict], raw_tatqa: list[dict], tatqa: list[dict]) -> list[dict]:
    annotations = {("finqa", row["id"]): row["qa"] for row in finqa}
    for uid, annotation in exact_question_context_join(raw_tatqa, tatqa)[0].items():
        annotations[("tatqa", uid)] = annotation
    return [{"case_id": row.source + ":" + row.native_id, "source": row.source,
             "native_id": row.native_id, "original_annotation": annotations[(row.source, row.native_id)],
             "status": "unreviewed_source_annotation_no_recomputation"} for row in selected]


def reviewer_packets(selected: list[Candidate], fields: list[str], reviewer: str) -> list[dict]:
    return [{"case_id": row.source + ":" + row.native_id, "reviewer": reviewer,
             "question": row.question, "original_context": row.original_context,
             "rubric": {field: "" for field in fields}, "review_status": "blank_not_reviewed"}
            for row in selected]
