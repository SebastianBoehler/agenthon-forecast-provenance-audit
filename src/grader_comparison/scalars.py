"""Executive summary: exact equality on a declared rational grammar; unsupported is not wrong."""

from decimal import Decimal, localcontext
from fractions import Fraction
import re

ATOM = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)"


def scalar(text):
    text = text.strip()
    if text.startswith("$") and text.endswith("$"):
        text = text[1:-1].strip()
    # One whole-answer box, not arbitrary nested expression simplification.
    if text.startswith(r"\boxed{") and text.endswith("}"):
        text = text[7:-1].strip()
    if re.fullmatch(ATOM, text):
        return Fraction(text)
    match = re.fullmatch(rf"({ATOM})\s*/\s*({ATOM})", text)
    if match:
        denominator = Fraction(match[2])
        return Fraction(match[1]) / denominator if denominator else None
    match = re.fullmatch(r"([+-]?)\\(?:dfrac|tfrac|frac)\{([+-]?\d+)\}\{([+-]?\d+)\}", text)
    if match and int(match[3]):
        sign = -1 if match[1] == "-" else 1
        return Fraction(sign * int(match[2]), int(match[3]))
    return None


def final_scalar(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None
    match = re.fullmatch(r"Final Answer:\s*(.+)", lines[-1], re.I)
    return match[1] if match and scalar(match[1]) is not None else None


def canonical(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def decimal(value):
    denominator = value.denominator
    for prime in (2, 5):
        while denominator % prime == 0:
            denominator //= prime
    if denominator != 1:
        return None
    with localcontext() as ctx:
        ctx.prec = len(str(abs(value.numerator))) + value.denominator.bit_length() + 10
        return format(Decimal(value.numerator) / Decimal(value.denominator), "f")


def controls(reference):
    value = scalar(reference)
    if value is None:
        raise ValueError("Controls require an admitted rational reference")
    pairs = [("identity", reference), ("canonical", canonical(value)),
             ("unreduced", f"{4 * value.numerator}/{4 * value.denominator}"),
             ("shift_tenth", canonical(value + Fraction(1, 10))),
             ("shift_integer", canonical(value + 1))]
    if value:
        pairs.append(("sign_flip", canonical(-value)))
    exact_decimal = decimal(value)
    if exact_decimal is not None:
        pairs.append(("terminating_decimal", exact_decimal))
    return [(name, text, scalar(text) == value) for name, text in pairs]
