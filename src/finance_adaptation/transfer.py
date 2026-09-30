"""Executive summary: author three unseen wordings and six new inputs per finance family."""

INPUTS = {
    'cr_eq_gordon': (
        ('2.37', '3.10', '9.40'), ('1.83', '2.60', '8.80'),
        ('3.41', '4.20', '11.70'), ('0.91', '1.90', '7.30'),
        ('2.68', '2.75', '10.35'), ('4.17', '3.65', '12.15')),
    'eq_gordon': (
        ('1.72', '2.25', '8.65'), ('3.26', '3.45', '10.15'),
        ('2.19', '1.85', '7.75'), ('4.03', '4.15', '12.05'),
        ('0.86', '1.35', '6.95'), ('2.94', '2.95', '9.85')),
    'deriv_binomial_call': (
        ('97', '1.18', '0.86', '102', '3.7'),
        ('143', '1.24', '0.81', '149', '4.2'),
        ('81', '1.16', '0.87', '84', '2.8'),
        ('126', '1.21', '0.83', '131', '5.1'),
        ('109', '1.19', '0.84', '114', '3.3'),
        ('172', '1.23', '0.82', '179', '4.6')),
    'corp_wacc': (
        ('6125000', '3875000', '10.65', '6.35', '27'),
        ('4420000', '2180000', '11.25', '5.95', '24'),
        ('7360000', '3640000', '9.85', '6.75', '31'),
        ('5175000', '1825000', '12.15', '7.05', '26'),
        ('8240000', '4760000', '10.35', '6.25', '28'),
        ('3685000', '2315000', '11.55', '7.45', '23')),
}

GORDON_TEMPLATES = (
    'A common share has just paid an annual dividend of {d} currency. Future '
    'dividends grow forever at {g}% per year, and investors require {r}% per year. '
    'Under the Gordon constant-growth model, what is the share worth immediately '
    'after that payment? {rounding}',
    'Value a perpetual growing dividend stream. The time-zero dividend, already '
    'paid, was {d} currency per share. The next dividend arrives in one year; '
    'annual dividend growth is {g}% and the annual discount rate is {r}%. '
    'Compute the current ex-dividend value. {rounding}',
    'A valuation team uses the Gordon growth model. Its last completed dividend '
    'payment was {d} currency per share. Stable annual growth is {g}%, and the '
    'shareholders\' required annual return is {r}%. Calculate today\'s intrinsic '
    'share price using the next annual dividend. {rounding}',
)
BINOMIAL_TEMPLATES = (
    'A European call expires after one period. The non-dividend-paying share currently costs {s} '
    'currency; its terminal price is either {s} times {u} or {s} times {d}. '
    'The strike is {k} currency. The risk-free return is an effective {r}% for '
    'this single period, with gross factor 1 + {r}/100. Find the no-arbitrage '
    'call value now, to the nearest 0.01 currency.',
    'Use a one-step binomial option model with no dividends. A stock priced '
    'at {s} currency either rises by a gross multiplier of {u} or falls by a '
    'gross multiplier of {d}. A call may be exercised at the step\'s end for '
    '{k} currency. This European call is exercised only at expiry. '
    'The effective risk-free rate for this one step is {r}% '
    '(not a continuously compounded rate). What is the call premium today? '
    'Give the value to the nearest 0.01 currency.',
    'Price a European call, exercised only at expiry, by replicating its two '
    'possible payoffs. At the '
    'start the non-dividend-paying underlying trades for {s} currency. Over '
    'one period its up and down price factors are {u} and {d}; the exercise '
    'price at expiry is {k} currency. Risk-free savings earn exactly {r}% '
    'over that period, so one currency becomes 1 + {r}/100 currency. '
    'Report the call\'s current no-arbitrage price to the nearest 0.01 currency.',
)
WACC_TEMPLATES = (
    'A firm is financed only by common equity worth {e} currency and debt worth '
    '{d} currency, both measured at market value. Equity investors require '
    '{re}% annually; the annual borrowing cost before tax is {rd}%. Interest '
    'is tax deductible at a marginal tax rate of {tax}%. Find its weighted '
    'average cost of capital in percentage points, rounded to 0.01.',
    'Calculate an annual discount rate using market-value financing weights. '
    'The business has {e} currency of equity and {d} currency of debt. The '
    'equity cost is {re}% and the pretax debt cost is {rd}%; deductible '
    'interest faces a {tax}% marginal corporate tax rate. There is no '
    'preferred stock. State WACC in percentage points to the nearest 0.01.',
    'Two sources fund this company: common shares with market value {e} '
    'currency and borrowing with market value {d} currency. Their annual '
    'required rates are {re}% for shares and {rd}% before tax for borrowing. '
    'Apply the interest tax shield at a {tax}% marginal rate. What is the '
    'annual weighted average cost of capital? Give percentage points to 0.01.',
)


def transfer_prompt(family: str, values: tuple[str, ...], index: int) -> str:
    if family in ('cr_eq_gordon', 'eq_gordon'):
        rounding = ('Round to the nearest whole currency unit.'
                    if family == 'cr_eq_gordon' else
                    'Round to the nearest 0.01 currency.')
        return GORDON_TEMPLATES[index].format(
            d=values[0], g=values[1], r=values[2], rounding=rounding)
    if family == 'deriv_binomial_call':
        return BINOMIAL_TEMPLATES[index].format(
            s=values[0], u=values[1], d=values[2], k=values[3], r=values[4])
    if family == 'corp_wacc':
        return WACC_TEMPLATES[index].format(
            e=values[0], d=values[1], re=values[2], rd=values[3], tax=values[4])
    raise ValueError(f'Unsupported transfer family: {family}')
