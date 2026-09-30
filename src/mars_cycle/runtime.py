"""Executive summary: run the pinned MarS order model directly on CPU, in fp32."""
import inspect
import json
import random
import time
from pathlib import Path

import numpy as np
import torch
from safetensors.torch import load_file
from market_simulation.models.order_model import OrderModel


class DirectClient:
    """Experimental local transport; keep official forward and multinomial sampling."""

    def __init__(self, root: Path, seed: int):
        torch.set_num_threads(1)
        torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)
        config = json.loads((root / "model/config.json").read_text())
        allowed = set(inspect.signature(OrderModel).parameters)
        self.metadata = {k: v for k, v in config.items() if k not in allowed}
        self.model = OrderModel(**{k: v for k, v in config.items() if k in allowed})
        self.model.load_state_dict(load_file(root / "model/model.safetensors"), strict=True)
        self.model.eval()
        self.calls = 0
        self.seconds = 0.0

    def get_prediction(self, state):
        if state.size != 1024 * 15:
            raise ValueError(f"Incomplete official context: {state.size}")
        start = time.perf_counter()
        with torch.inference_mode():
            value = self.model.sample(torch.from_numpy(state.copy()).long().reshape(1, -1), temperature=1.0)
        self.calls += 1
        self.seconds += time.perf_counter() - start
        return value.numpy().astype(np.int32).reshape(-1)
