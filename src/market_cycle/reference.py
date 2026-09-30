"""Executive summary: linear transient-impact reference with explicit fill accounting."""

from dataclasses import asdict, dataclass
from math import exp, fsum, isfinite


@dataclass(frozen=True)
class Parameters:
    initial_price: float
    impact_per_unit: float
    decay_per_second: float
    step_seconds: float
    half_spread: float
    fee_per_unit: float
    volatility_per_sqrt_second: float
    max_trade_units: float

    def __post_init__(self) -> None:
        for name, value in asdict(self).items():
            if isinstance(value, bool) or not isinstance(value, (float, int)):
                raise ValueError(f"{name} must be numeric")
            if not isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and nonnegative")
        for name in ("initial_price", "step_seconds", "max_trade_units"):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")

    @property
    def decay(self) -> float:
        return exp(-self.decay_per_second * self.step_seconds)


@dataclass(frozen=True)
class Fill:
    step: int
    signed_quantity: float
    unaffected_price: float
    impact_before: float
    execution_price: float
    fee: float
    cash_after: float
    inventory_after: float


def validate_cycle(quantities: tuple[float, ...], params: Parameters) -> None:
    if len(quantities) < 2:
        raise ValueError("A cycle requires at least two steps")
    for quantity in quantities:
        if isinstance(quantity, bool) or not isinstance(quantity, (int, float)):
            raise ValueError("Every quantity must be numeric")
        if not isfinite(quantity) or abs(quantity) > params.max_trade_units:
            raise ValueError("Quantity is nonfinite or exceeds the declared limit")
    if not any(quantities) or fsum(quantities) != 0:
        raise ValueError("A nonempty cycle must close exactly; no implicit liquidation")


def execute(
    quantities: tuple[float, ...],
    increments: tuple[float, ...],
    params: Parameters,
    *,
    omit_self_impact: bool = False,
    pretrade_impacts: tuple[float, ...] | None = None,
) -> tuple[Fill, ...]:
    """Fill each fixed-grid trade; increments arrive after the current fill.

    omit_self_impact is solely a deliberately invalid detector control.
    Each trade fills fully; spread is in execution price, fee in cash.
    pretrade_impacts substitutes only the response, keeping execution math fixed.
    """
    validate_cycle(quantities, params)
    if len(increments) != len(quantities) - 1 or not all(map(isfinite, increments)):
        raise ValueError("Supply one finite price increment between adjacent steps")
    if pretrade_impacts is not None and (
        len(pretrade_impacts) != len(quantities) or not all(map(isfinite, pretrade_impacts))
    ):
        raise ValueError("Supply one finite pre-trade impact per step")
    price, impact, cash = params.initial_price, 0.0, 0.0
    fills = []
    for step, quantity in enumerate(quantities):
        if pretrade_impacts is not None:
            impact = pretrade_impacts[step]
        sign = (quantity > 0) - (quantity < 0)
        self_impact = 0.0 if omit_self_impact else params.impact_per_unit * quantity / 2
        execution_price = price + impact + self_impact + sign * params.half_spread
        fee = abs(quantity) * params.fee_per_unit
        cash = fsum((cash, -quantity * execution_price, -fee))
        inventory = fsum(quantities[: step + 1])
        fill = Fill(step, quantity, price, impact, execution_price, fee, cash, inventory)
        if not all(isfinite(v) for v in asdict(fill).values()):
            raise ValueError("Nonfinite reference ledger")
        fills.append(fill)
        impact = params.decay * (impact + params.impact_per_unit * quantity)
        if step < len(increments):
            price += increments[step]
    return tuple(fills)


def expected_cost(
    quantities: tuple[float, ...], params: Parameters, *, omit_self_impact: bool = False
) -> float:
    """Analytical expected cost for a deterministic closed schedule, currency units."""
    validate_cycle(quantities, params)
    terms = [
        params.impact_per_unit * quantities[t] * quantities[s] * params.decay ** (t - s)
        for t in range(len(quantities)) for s in range(t)
    ]
    if not omit_self_impact:
        terms.extend(params.impact_per_unit * q * q / 2 for q in quantities)
    terms.extend(abs(q) * (params.half_spread + params.fee_per_unit) for q in quantities)
    return fsum(terms)


def cost_variance(quantities: tuple[float, ...], params: Parameters) -> float:
    """Variance under independent Gaussian martingale increments on the fixed grid."""
    validate_cycle(quantities, params)
    exposures = [fsum(quantities[: t + 1]) for t in range(len(quantities) - 1)]
    return (
        params.volatility_per_sqrt_second ** 2 * params.step_seconds
        * fsum(inventory ** 2 for inventory in exposures)
    )
