"""Executive summary: calculate finance answers from visible operands, without generator code."""
import re
from decimal import Decimal as D

NUM = r'(-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)'


def operands(pattern: str, prompt: str) -> list[D]:
    match = re.search(pattern, prompt)
    if match is None:
        raise ValueError(f'Unparsed visible question: {prompt}')
    return [D(value.replace(',', '')) for value in match.groups()]


def numeric_answer(answer: str) -> D:
    values = re.findall(r'-?\d[\d,]*(?:\.\d+)?', answer)
    if len(values) != 1:
        raise ValueError(f'Expected one numeric answer: {answer}')
    return D(values[0].replace(',', ''))


def gordon(prompt: str):
    dividend, growth, rate = operands(
        rf'D0 = \${NUM}, growth g = {NUM}%, required return r = {NUM}%', prompt)
    if rate <= growth:
        raise ValueError('Gordon requires rate > growth')
    denominator = (rate - growth) / 100
    return dividend * (1 + growth / 100) / denominator, dividend / denominator, None


def annuity(prompt: str):
    payment, annual, periods = operands(
        rf'deposits \${NUM} at the END of each month into an account paying {NUM}% compounded monthly. Compute the future value after {NUM} months', prompt)
    rate = annual / 1200
    value = payment * ((1 + rate) ** int(periods) - 1) / rate
    independent = sum(payment * (1 + rate) ** k for k in range(int(periods)))
    return value, value * (1 + rate), independent


def wacc(prompt: str):
    equity, debt, re_, rd, tax = operands(
        rf'market equity {NUM}, market debt {NUM}, cost of equity {NUM}%, cost of debt {NUM}%, and a marginal tax rate {NUM}%', prompt)
    value = (equity * re_ + debt * rd * (1 - tax / 100)) / (equity + debt)
    wrong = (equity * re_ + debt * rd) / (equity + debt)
    return value, wrong, None


def capm(prompt: str):
    risk_free, market, beta = operands(rf'rf = {NUM}%, E\(Rm\) = {NUM}%, β = {NUM}', prompt)
    return risk_free + beta * (market - risk_free), risk_free + beta * market, None


def present_value(prompt: str):
    cash, years, annual = operands(
        rf'amount of \${NUM} is received in {NUM} years. The discount rate is {NUM}% per year', prompt)
    rate = annual / 100
    value = cash / (1 + rate) ** int(years)
    independent = cash
    for _ in range(int(years)):
        independent /= 1 + rate
    return value, cash / (1 + rate * years), independent


def effective_rate(prompt: str):
    annual, periods = operands(rf'annual rate of {NUM}% is compounded {NUM} times per year', prompt)
    return ((1 + annual / (100 * periods)) ** int(periods) - 1) * 100, annual, None


def binomial(prompt: str):
    spot, up, down, strike, annual = operands(
        rf'S0={NUM}, u={NUM}, d={NUM}, K={NUM}, rf={NUM}%', prompt)
    gross = 1 + annual / 100
    if not down < gross < up:
        raise ValueError('Binomial no-arbitrage condition violated')
    cu, cd = max(spot * up - strike, D(0)), max(spot * down - strike, D(0))
    probability = (gross - down) / (up - down)
    value = (probability * cu + (1 - probability) * cd) / gross
    hedge = (cu - cd) / (spot * (up - down))
    bond_debt = (hedge * spot * up - cu) / gross
    replication = hedge * spot - bond_debt
    if not max(spot - strike / gross, D(0)) - D('1e-20') <= value <= spot:
        raise ValueError('Call price violates no-arbitrage bounds')
    return value, bond_debt, replication


FORMULAS = {'cr_eq_gordon': gordon, 'eq_gordon': gordon,
            'deriv_binomial_call': binomial, 'tvm_annuity_fv': annuity,
            'v_tvm_annuity_fv': annuity, 'corp_wacc': wacc, 'm_corp_wacc': wacc,
            'port_capm': capm, 'tvm_pv_lump': present_value, 'tvm_eay': effective_rate}
