"""Executive summary: reserve each call and persist observed billing before another call."""

import fcntl
import json
import os
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path

from .client import now
from .protocol import FOLLOWUP_CAP, MAX_TOKENS, OUTPUT_PRICE, PROMPT_PRICE, STUDY_CAP

CONTEXT_LENGTH = 163840  # Fixed SiliconFlow catalogue snapshot, not a tokenizer proof.


class BudgetStop(RuntimeError):
    """A missing cost, unsettled call or exhausted bound requires stopping."""


def reservation_usd(request_body):
    """UTF-8 bytes bound ordinary tokenization; include framing and full output."""
    prompt_bound = len(json.dumps(request_body, ensure_ascii=False).encode()) + 256
    output_bound = request_body.get("max_tokens", MAX_TOKENS)
    if output_bound != MAX_TOKENS or prompt_bound + output_bound > CONTEXT_LENGTH:
        raise BudgetStop("Full byte/framing/output bound exceeds the fixed context limit")
    return PROMPT_PRICE * prompt_bound + OUTPUT_PRICE * output_bound


def observed_cost(record):
    usage = record.get("usage")
    if not isinstance(usage, dict) or "cost" not in usage:
        raw = record.get("raw_response", {})
        usage = raw.get("usage", {}) if isinstance(raw, dict) else {}
    value = usage.get("cost") if isinstance(usage, dict) else None
    if value is None or isinstance(value, bool):
        raise BudgetStop("Missing usage.cost; no further calls are permitted")
    try:
        cost = Decimal(str(value))
    except (ValueError, ArithmeticError):
        raise BudgetStop("Invalid usage.cost; no further calls are permitted") from None
    if not cost.is_finite() or cost < 0:
        raise BudgetStop("Nonfinite/negative usage.cost; no further calls are permitted")
    return cost


class Budget:
    def __init__(self, path, study_id, study_cap=STUDY_CAP, total_cap=FOLLOWUP_CAP):
        self.path = Path(path)
        self.study_id = study_id
        self.study_cap, self.total_cap = Decimal(study_cap), Decimal(total_cap)
        if self.study_cap != STUDY_CAP or self.total_cap != FOLLOWUP_CAP:
            raise ValueError("Use the fixed $2 study and $10 aggregate caps")
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def locked(self):
        with self.path.open("a+", encoding="utf-8") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            try:
                stream.seek(0)
                try:
                    events = [json.loads(line) for line in stream if line.strip()]
                except ValueError:
                    raise BudgetStop("Malformed spend ledger; cannot resume") from None
                yield stream, events
            finally:
                fcntl.flock(stream, fcntl.LOCK_UN)

    @staticmethod
    def append(stream, event):
        stream.seek(0, os.SEEK_END)
        stream.write(json.dumps(event, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())

    def state(self, events):
        reservations, settlements = {}, {}
        for event in events:
            key = event["call_id"]
            target = reservations if event["event"] == "reserved" else settlements
            if key in target or event["event"] not in {"reserved", "settled"}:
                raise BudgetStop("Invalid or duplicate spend-ledger event")
            target[key] = event
        if set(settlements) - set(reservations):
            raise BudgetStop("Spend ledger contains an unreserved settlement")
        if any(x["cost_usd"] is None for x in settlements.values()):
            raise BudgetStop("Ledger contains unknown billing; cannot resume calls")
        costs = {}
        for key, event in settlements.items():
            cost = observed_cost({"usage": {"cost": event["cost_usd"]}})
            reservation = reservations[key]
            if event["study_id"] != reservation["study_id"] or cost > Decimal(reservation["reserve_usd"]):
                raise BudgetStop("Ledger contains a billing/reservation violation; cannot resume")
            costs[key] = cost
        total = sum(costs.values(), Decimal(0))
        study = sum((costs[key] for key, event in settlements.items()
                     if event["study_id"] == self.study_id), Decimal(0))
        study_totals = {}
        for key, event in settlements.items():
            sid = event["study_id"]
            study_totals[sid] = study_totals.get(sid, Decimal(0)) + costs[key]
        if total > self.total_cap or any(x > self.study_cap for x in study_totals.values()):
            raise BudgetStop("Ledger contains an exceeded fixed cap; cannot resume")
        pending = set(reservations) - set(settlements)
        return reservations, settlements, total, study, pending

    def reserve(self, call_id, request_body, identity):
        allowed = {"case_id", "arm", "phase", "target_model", "target_provider",
                   "request_sha256"}
        if set(identity) - allowed:
            raise ValueError("Unexpected reservation identity fields")
        reserve = reservation_usd(request_body)
        with self.locked() as (stream, events):
            reservations, _, total, study, pending = self.state(events)
            if call_id in reservations:
                raise BudgetStop("Call identity already reserved; never retry")
            if pending:
                raise BudgetStop("An unsettled call must be reconciled before proceeding")
            if total + reserve > self.total_cap or study + reserve > self.study_cap:
                raise BudgetStop("Conservative reservation exceeds the fixed spend cap")
            self.append(stream, {"event": "reserved", "call_id": call_id,
                                 "study_id": self.study_id, "utc": now(),
                                 "reserve_usd": str(reserve), **identity})
        return reserve

    def settle(self, call_id, record):
        error = None
        try:
            cost = observed_cost(record)
        except BudgetStop as failure:
            cost, error = None, str(failure)
        with self.locked() as (stream, events):
            reservations, settlements, total, study, _ = self.state(events)
            if call_id not in reservations or call_id in settlements:
                raise BudgetStop("Cannot settle an absent/already settled reservation")
            reserved = reservations[call_id]
            self.append(stream, {"event": "settled", "call_id": call_id,
                                 "study_id": reserved["study_id"], "utc": now(),
                                 "cost_usd": None if cost is None else str(cost),
                                 "cost_error": error,
                                 "request_sha256": record.get("request_sha256"),
                                 "returned_model": record.get("returned_model"),
                                 "returned_provider": record.get("provider"),
                                 "finish_reason": record.get("finish_reason"),
                                 "error": record.get("error")})
            if error:
                raise BudgetStop(error)
            if cost > Decimal(reserved["reserve_usd"]):
                raise BudgetStop("Observed billing exceeded the reserved bound")
            if total + cost > self.total_cap or study + cost > self.study_cap:
                raise BudgetStop("Observed billing exceeded a fixed cap")
        return cost

    def totals(self):
        with self.locked() as (_, events):
            _, _, total, study, pending = self.state(events)
            return {"aggregate_usd": str(total), "study_usd": str(study),
                    "pending": len(pending), "initial_actual_usd": "0"}
