"""Executive summary: guard requested quantities, exact identities and explicit rounding interpretations."""

from fractions import Fraction as F

import pytest

from independent_finance.values import accepted, expected, native_final, nearest


def test_binomial_requested_call_is_not_financing_debt():
    question = "S0=$58.00, K=$48.00, u=1.15, d=0.85, r=6.00 %"
    value, alternatives, evidence = expected("binomial_call", question)
    assert value == F(674, 53)
    assert alternatives == [value]
    assert evidence["debt"] == str(F(2400, 53))
    assert evidence["replication_identity"]
    assert not accepted(F(evidence["mutation_value"]), value)


def test_rounding_interpretation_is_separate_from_exact_price():
    value, alternatives, _ = expected(
        "binomial_call", "S0=$100.01, K=$105.00, u=1.13, d=0.83, r=5.00 %")
    assert alternatives[0] != value
    assert nearest(F("1.005"), F(".01")) == {F(1), F("1.01")}
    assert accepted(F("1.01"), F("1.005"))
    assert not accepted(F("1.01"), F("1.0049"))


def test_wacc_percent_and_compound_interest_quantities():
    question = ("Equity value = $60 million Debt value = $40 million "
                "Cost of equity = 10% Cost of debt = 5% Tax rate = 25%")
    value, alternatives, evidence = expected("wacc", question)
    assert value == F("7.5") and alternatives == [value]
    assert F(evidence["mutation_value"]) == 8
    value, alternatives, evidence = expected("compound_interest", (
        "Ada invested $1000. annual interest rate of 5% compounded annually over 2 years"))
    assert value == F("102.5") and alternatives == [value]
    assert F(evidence["mutation_value"]) == F("1102.5")


def test_final_extraction_never_recovers_an_intermediate_number():
    assert native_final("compound_interest", "Amount = $ 1102.50\nInterest = $ 102.50") == F("102.5")
    assert native_final("wacc", "Intermediate = 8%\n = 7.5%") == F("7.5")
    with pytest.raises(ValueError):
        native_final("binomial_call", "Price = $12.72\nExplanation without final value")
