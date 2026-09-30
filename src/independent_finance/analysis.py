"""Executive summary: keep every scheduled source case and separate exact, rounded and quantity endpoints."""

from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib

from .source import generate, FUNCTIONS
from .values import accepted, expected, native_final


def assess(family, question, solution):
    value, alternatives, evidence = expected(family, question)
    answer = native_final(family, solution)
    mutation = F(evidence["mutation_value"])
    row = {"exact_reference": str(value), "source_convention_references": sorted(map(str, set(alternatives))),
           "native_value": str(answer), "distance_from_exact": str(abs(answer - value)),
           "exact_compatible": accepted(answer, value),
           "source_convention_compatible": any(accepted(answer, v) for v in alternatives),
           "mutation_compatible": accepted(mutation, value), "evidence": evidence}
    if family == "binomial_call":
        lower, upper = map(F, evidence["bounds"])
        if not lower <= value <= upper:
            raise ValueError("Independent exact call fails no-arbitrage bounds")
        row["native_bounds_compatible"] = lower - F(1, 200) <= answer <= upper + F(1, 200)
    return row


def collect():
    rows = []
    for family in FUNCTIONS:
        for seed in range(100):
            row = {"id": f"{family}/{seed}", "family": family, "seed": seed}
            try:
                question, solution = generate(family, seed)
                row.update(question=question, solution=solution,
                           question_sha256=hashlib.sha256(question.encode()).hexdigest(),
                           solution_sha256=hashlib.sha256(solution.encode()).hexdigest())
                row.update(assess(family, question, solution), status="assessed")
            except Exception as exc:
                row.update(status="nondecision", error_type=type(exc).__name__, error=str(exc))
            rows.append(row)
    return rows


def summarize(rows):
    counters, seen, questions = defaultdict(Counter), set(), defaultdict(set)
    for row in rows:
        identity = (row["family"], row["seed"])
        if identity in seen or row["id"] != f"{identity[0]}/{identity[1]}":
            raise ValueError("Duplicate or changed case identity")
        seen.add(identity)
        counter = counters[row["family"]]
        counter["attempted"] += 1
        if "question" in row:
            questions[row["family"]].add(row["question_sha256"])
        if row["status"] != "assessed":
            counter["nondecisions"] += 1
            continue
        counter["assessed"] += 1
        for key in ("exact_compatible", "source_convention_compatible", "mutation_compatible"):
            counter[key] += int(row[key])
        counter["outside_exact_inside_source_convention"] += int(
            not row["exact_compatible"] and row["source_convention_compatible"])
        counter["outside_both_conventions"] += int(
            not row["exact_compatible"] and not row["source_convention_compatible"])
        if "native_bounds_compatible" in row:
            counter["native_bounds_compatible"] += int(row["native_bounds_compatible"])
    scheduled = {(family, seed) for family in FUNCTIONS for seed in range(100)}
    if seen != scheduled:
        raise ValueError("Attempt membership changed")
    for family, counter in counters.items():
        counter.update(scheduled=100, unique_questions=len(questions[family]))
    return {"scheduled": 300, "counts": {k: dict(v) for k, v in counters.items()},
            "scope": "New seeded native template instances; final scalar compatibility under declared conventions"}
