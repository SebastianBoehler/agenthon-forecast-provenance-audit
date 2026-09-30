"""Executive summary: test valuation identities, output projection and ambiguous half ties."""
from decimal import Decimal as D, localcontext

from answer_contract.formulas import binomial, capm
from answer_contract.types import Case


def test_call_replication_prices_option_not_bond():
    value, bond, replication = binomial('S0=58, u=1.15, d=0.85, K=48, rf=6.0%')
    assert abs(value - (D(58)-D(48)/D('1.06'))) < D('1e-20')
    assert abs(value-replication) < D('1e-20')
    assert abs(value-bond) > 30


def test_out_of_money_call_is_zero():
    value, _, replication = binomial('S0=40, u=1.15, d=0.85, K=60, rf=6.0%')
    assert value == replication == 0


def test_integer_projection_rejects_raw_and_keeps_half_ties():
    case = Case('test', 'gordon', '1', '', D('30.94'), D('30.941176'), D(1), True, D('29.4'))
    assert case.accepts(D(31))
    assert not case.accepts(D('30.94'))
    assert not case.accepts(D(31), rounding=False)
    tie = Case('test', 'gordon', '2', '', D('30.5'), D('30.5'), D(1), True, D(29))
    assert tie.accepts(D(30)) and tie.accepts(D(31))
    assert not tie.accepts(D('30.5'))


def test_capm_parser_does_not_consume_sentence_period():
    value, wrong, _ = capm('CAPM: rf = 3.3%, E(Rm) = 8.4%, β = 1.56. Compute the required return.')
    assert value == D('11.256') and wrong == D('16.404')


def test_decimal_context_does_not_change_binomial_identity():
    with localcontext() as context:
        context.prec = 50
        value, _, replication = binomial('S0=47, u=1.15, d=0.80, K=53, rf=5.0%')
        assert abs(value-replication) < D('1e-45')
