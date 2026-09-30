"""Executive summary: keep source supervision and independently derived targets separate."""
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Case:
    source: str
    family: str
    case_id: str
    prompt: str
    gold: Decimal
    formula: Decimal
    quantum: Decimal
    requested_rounding: bool
    mutation: Decimal
    chosen: Decimal | None = None
    rejected: Decimal | None = None
    interval: tuple[Decimal, Decimal] | None = None
    hidden_formula: Decimal | None = None
    independent_formula: Decimal | None = None

    @property
    def target(self) -> Decimal:
        from decimal import ROUND_HALF_UP
        if self.requested_rounding:
            return self.formula.quantize(self.quantum, rounding=ROUND_HALF_UP)
        return self.formula

    def accepts(self, answer: Decimal, rounding: bool = True) -> bool:
        if self.requested_rounding and rounding:
            if abs(self.formula - self.target) == Decimal('.5'):
                return answer in (self.target, self.target - 1)
            return answer == self.target
        tolerance = Decimal('.005') if self.requested_rounding else self.quantum / 2
        return abs(answer - self.formula) <= tolerance + Decimal('1e-20')
