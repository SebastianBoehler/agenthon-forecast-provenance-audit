"""Executive summary: validate source pointers and immutable structured review records."""

import hashlib
import json
import re
from pathlib import Path

from finance_document_review.arithmetic import calculate


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rows(path):
    def unique(pairs):
        if len(dict(pairs)) != len(pairs):
            raise ValueError("Duplicate review JSON field")
        return dict(pairs)
    return [json.loads(line, object_pairs_hook=unique)
            for line in Path(path).read_text().splitlines()]


def resolve(context, pointer):
    if not isinstance(pointer, str) or not pointer:
        raise ValueError("Empty or nonstring evidence pointer")
    parts = re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*(?:(?:\.[A-Za-z_][A-Za-z_0-9]*)|(?:\[[0-9]+\]))*", pointer)
    if not parts:
        raise ValueError("Unsupported source pointer: " + pointer)
    current = context
    for token in re.findall(r"[A-Za-z_][A-Za-z_0-9]*|\[[0-9]+\]", pointer):
        if token.startswith("["):
            if not isinstance(current, list):
                raise ValueError("Indexing a nonlist source value")
            current = current[int(token[1:-1])]
        else:
            if not isinstance(current, dict):
                raise ValueError("Accessing a nonobject source value")
            current = current[token]
    return current


def review_record(record, packet, fields, statuses, id_field):
    if set(record) != fields or record[id_field] != packet[id_field]:
        raise ValueError("Review schema/identity mismatch")
    if record["status"] not in statuses:
        raise ValueError("Unknown review status")
    for field in ("requested_quantity", "entity", "time_scope", "rationale"):
        if not isinstance(record[field], str) or not record[field].strip():
            raise ValueError("Missing review explanation: " + field)
    if not isinstance(record["assumptions"], list) or any(not isinstance(x, str) for x in record["assumptions"]):
        raise ValueError("Invalid assumptions")
    if not isinstance(record["operand_bindings"], list):
        raise ValueError("Invalid operand bindings")
    pointers = list(record["evidence_paths"])
    if not isinstance(record["evidence_paths"], list):
        raise ValueError("Invalid evidence paths")
    for binding in record["operand_bindings"]:
        if set(binding) != {"literal", "role", "evidence_paths"}:
            raise ValueError("Invalid operand binding schema")
        if not isinstance(binding["role"], str) or not binding["role"].strip():
            raise ValueError("Missing operand role")
        if not isinstance(binding["literal"], str) or not isinstance(binding["evidence_paths"], list):
            raise ValueError("Invalid operand literal/pointers")
        pointers.extend(binding["evidence_paths"])
    for pointer in pointers:
        resolve(packet["original_context"], pointer)
    expression_field = "reference_expression" if id_field == "review_id" else "expression"
    expression = record[expression_field]
    if expression is not None:
        calculate(expression)
    return {"source_pointers_checked": len(pointers), "arithmetic_checked": expression is not None}
