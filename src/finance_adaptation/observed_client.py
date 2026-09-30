"""Executive summary: observe bounded egress slots without changing API or scoring rules.

The inherited client retains request bodies, reservations and error handling.
Slot intervals bound actual request overlap; they are not exact HTTP wire times.
"""
import threading
from datetime import datetime, timezone

from finance_adaptation.client import BudgetClient
from model_grading.protocol import append_record


class ObservedGate:
    def __init__(self, client):
        self.client = client
        self.semaphore = threading.BoundedSemaphore(4)
        self.lock = threading.Lock()

    def __enter__(self):
        self.semaphore.acquire()
        self.client.local.entered = datetime.now(timezone.utc).isoformat()

    def __exit__(self, *_):
        left = datetime.now(timezone.utc).isoformat()
        try:
            with self.lock:
                append_record(self.client.timings, {
                    'tag': self.client.local.tag,
                    'entered_egress_slot_utc': self.client.local.entered,
                    'left_egress_slot_utc': left})
        finally:
            self.semaphore.release()


class ObservedBudgetClient(BudgetClient):
    def __init__(self, directory, catalogue, limit):
        super().__init__(directory, catalogue, limit)
        self.local = threading.local()
        self.timings = directory / 'egress_slots.jsonl'
        if self.timings.exists():
            raise ValueError('A new run cannot overwrite existing egress timing records')
        self.gate = ObservedGate(self)

    def call(self, messages, *, tag, max_tokens=512, temperature=0):
        self.local.tag = tag
        return super().call(messages, tag=tag, max_tokens=max_tokens,
                            temperature=temperature)
