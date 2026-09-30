"""Executive summary: record explicit review-unit conversions without consulting native labels."""
from __future__ import annotations

import re
from decimal import Decimal


def signature(unit: str, monetary_scale: str | None = None) -> dict:
    text = unit.lower().strip().replace("_", " ")
    if "percent or percentage" in text or "percent or percentage" in text.replace("-", " "):
        return {"dimension": "ambiguous", "factor": None, "currency": None}
    if "percentage point" in text:
        dimension, factor = "percentage_points", Decimal(1)
    elif "percent" in text or text == "%":
        dimension, factor = "proportion", Decimal("0.01")
    elif any(word in text for word in ["ratio", "proportion", "portion", "dimensionless"]):
        dimension, factor = "proportion", Decimal(1)
    elif any(word in text for word in ["usd", "dollar", "eur", "gbp", "rmb", "yuan",
                                      "currency", "monetary", "cent", "$", "£", "€"]):
        dimension, factor = "monetary", Decimal(1)
        if "cent" in text:
            factor = Decimal("0.01")
    elif any(word in text for word in ["shares", "years", "year", "count"]):
        dimension, factor = "count", Decimal(1)
    elif "boolean" in text:
        dimension, factor = "boolean", None
    else:
        return {"dimension": "unresolved", "factor": None, "currency": None}
    if dimension in {"monetary", "count"}:
        scale = monetary_scale if monetary_scale is not None else text
        if "billion" in scale:
            factor *= Decimal("1e9")
        elif "million" in scale:
            factor *= Decimal("1e6")
        elif "thousand" in scale:
            factor *= Decimal("1e3")
    elif monetary_scale not in {None, "none"}:
        return {"dimension": "incompatible_scale", "factor": None, "currency": None}
    currency = next((code for code in ["USD", "EUR", "GBP", "RMB"]
                     if re.search(rf"\b{code.lower()}\b", text)), None)
    if "yuan" in text:
        currency = "RMB"
    unspecified_scale = any(phrase in text for phrase in [
        "scale unspecified", "scale not specified", "scale absent",
        "currency and scale unspecified", "currency and scale not specified",
    ])
    return {"dimension": dimension, "factor": str(factor) if factor is not None else None,
            "currency": currency, "scale_unspecified": unspecified_scale,
            "original_unit": unit, "explicit_model_scale": monetary_scale}


def canonical_values(values: list[str], unit: dict) -> list[Decimal]:
    if unit["factor"] is None:
        return []
    return [Decimal(value) * Decimal(unit["factor"]) for value in values]


def compatible_units(first: dict, second: dict) -> bool:
    if first["dimension"] != second["dimension"] or first["factor"] is None or second["factor"] is None:
        return False
    return not (first.get("currency") and second.get("currency")
                and first["currency"] != second["currency"])
