"""Executive summary: reject false completion, unexpected model output and invalid native budgets."""

import copy

import pytest

from model_grading_lmstudio import INSTANCE, MAX_TOKENS, normalized


def reply():
    return {
        "model_instance_id": INSTANCE,
        "output": [{"type": "message", "content": "FINAL: 21 currency"}],
        "stats": {
            "input_tokens": 150,
            "total_output_tokens": 8,
            "reasoning_output_tokens": 0,
        },
    }


def test_normal_return_does_not_invent_native_eos():
    result = normalized(reply())
    assert result["text"] == "FINAL: 21 currency"
    assert result["finish_reason"] == "stop"
    assert result["native_finish_reason"] is None


def test_at_cap_is_conservative_failure_even_with_parseable_final():
    raw = reply()
    raw["stats"]["total_output_tokens"] = MAX_TOKENS
    assert normalized(raw)["finish_reason"] == "length"


@pytest.mark.parametrize(
    "mutation",
    [
        {"model_instance_id": "another_model"},
        {
            "stats": {
                "input_tokens": 0,
                "total_output_tokens": 8,
                "reasoning_output_tokens": 0,
            }
        },
        {
            "stats": {
                "input_tokens": 150,
                "total_output_tokens": 0,
                "reasoning_output_tokens": 0,
            }
        },
        {"output": [{"type": "reasoning", "content": "FINAL: 21 currency"}]},
        {
            "stats": {
                "input_tokens": 150,
                "total_output_tokens": 8,
                "reasoning_output_tokens": 1,
            }
        },
        {
            "stats": {
                "input_tokens": 150,
                "total_output_tokens": True,
                "reasoning_output_tokens": 0,
            }
        },
        {
            "stats": {
                "input_tokens": 4000,
                "total_output_tokens": 8,
                "reasoning_output_tokens": 0,
            }
        },
    ],
)
def test_invalid_native_accounting_is_rejected(mutation):
    raw = copy.deepcopy(reply())
    raw.update(mutation)
    with pytest.raises(ValueError):
        normalized(raw)
