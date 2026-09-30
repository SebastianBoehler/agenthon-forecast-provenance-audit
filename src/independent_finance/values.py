"""Executive summary: derive exact values and explicit intermediate-rounding interpretations from questions."""

from fractions import Fraction as F
from itertools import product
import re

NUMBER = r"([\d]+(?:\.[\d]+)?)"


def extract(pattern, text):
    match = re.search(pattern, text)
    if match is None:
        raise ValueError("Unsupported frozen native question grammar")
    return [F(value) for value in match.groups()]


def nearest(value, quantum):
    units = value / quantum
    floor = units.numerator // units.denominator
    remainder = units - floor
    if remainder == F(1, 2):
        return {floor * quantum, (floor + 1) * quantum}
    return {(floor + int(remainder > F(1, 2))) * quantum}


def expected(family, question):
    evidence = {}
    if family == "binomial_call":
        spot, strike, up, down, rate = extract(
            rf"S0=\${NUMBER}, K=\${NUMBER}, u={NUMBER}, d={NUMBER}, r={NUMBER} %", question)
        gross = 1 + rate / 100
        if not down < gross < up:
            raise ValueError("No-arbitrage assumption failed")
        cu, cd = max(spot * up - strike, 0), max(spot * down - strike, 0)
        probability = (gross - down) / (up - down)
        value = (probability * cu + (1 - probability) * cd) / gross
        delta = (cu - cd) / (spot * (up - down))
        debt = (delta * spot * up - cu) / gross
        if delta * spot - debt != value:
            raise ValueError("Independent replication identity failed")
        alternatives = [(probability * max(su - strike, 0) + (1 - probability) * max(sd - strike, 0)) / gross
                        for su, sd in product(nearest(spot * up, F(1, 100)), nearest(spot * down, F(1, 100)))]
        evidence = {"debt": str(debt), "call_debt_numeric_collision": abs(value - debt) <= F(1, 200),
                    "replication_identity": True, "bounds": [str(max(spot - strike / gross, 0)), str(spot)],
                    "mutation_value": str(debt)}
    elif family == "wacc":
        equity, debt, re_, rd, tax = extract(
            rf"Equity value = \${NUMBER} (?:million|billion).*?Debt value\s*= \${NUMBER} (?:million|billion).*?"
            rf"Cost of equity = {NUMBER}%.*?Cost of debt\s*= {NUMBER}%.*?Tax rate\s*= {NUMBER}%", question.replace("\n", " "))
        value = (equity * re_ + debt * rd * (1 - tax / 100)) / (equity + debt)
        # A separately written weighted-cash-cost identity checks the same exact target.
        if value != re_ + debt / (equity + debt) * (rd * (1 - tax / 100) - re_):
            raise ValueError("WACC identity failed")
        alternatives = [we * re_ + wd * rd * (1 - tax / 100)
                        for we, wd in product(nearest(equity / (equity + debt), F(1, 10000)),
                                              nearest(debt / (equity + debt), F(1, 10000)))]
        evidence = {"mutation_value": str((equity * re_ + debt * rd) / (equity + debt))}
    elif family == "compound_interest":
        principal, rate, years = extract(
            rf"invested \${NUMBER}.*?annual interest rate of {NUMBER}% compounded annually over {NUMBER} years", question)
        if years.denominator != 1:
            raise ValueError("Noninteger compounding horizon")
        amount = principal * (1 + rate / 100) ** int(years)
        repeated = principal
        for _ in range(int(years)):
            repeated *= 1 + rate / 100
        if repeated != amount:
            raise ValueError("Compound amount identity failed")
        value = amount - principal
        alternatives = [rounded - principal for rounded in nearest(amount, F(1, 100))]
        evidence = {"mutation_value": str(amount)}
    else:
        raise ValueError("Unexpected frozen family")
    return value, alternatives, evidence


def native_final(family, solution):
    line = [part.strip() for part in solution.splitlines() if part.strip()][-1]
    marker = rf"= \$\s*{NUMBER}$" if family != "wacc" else rf"= {NUMBER}%$"
    values = extract(marker, line)
    return values[0]


def accepted(value, reference):
    return abs(value - reference) <= F(1, 200)
