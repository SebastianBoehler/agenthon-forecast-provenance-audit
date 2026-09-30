"""Executive summary: exercise economic-unit invariance and unresolved-case boundaries."""
from finance_document_review.comparison import locked_match
from finance_document_review.reporting import reference_projection
from finance_document_review.units import signature


def reference(value, unit, status='agreed_determinate_numeric'):
    return {'joint_status': status, 'unit_a': signature(unit), 'reference_values': [str(value)],
            'source': 'tatqa'}


def candidate(value, unit, scale='none'):
    return {'status': 'answer', 'value': str(value), 'unit': unit, 'scale': scale}


def test_economic_amount_is_invariant_to_declared_rescaling():
    target = reference('2.5', 'million USD')
    assert locked_match(target, candidate('2500', 'USD', 'thousand'))['matches']
    assert locked_match(target, candidate('2500000', 'USD'))['matches']
    assert not locked_match(target, candidate('2.5', 'USD', 'thousand'))['matches']
    assert not locked_match(target, candidate('2.5', 'EUR', 'million'))['matches']


def test_cents_and_dollars_are_equivalent_but_percentage_point_difference_is_distinct():
    assert locked_match(reference('44', 'cents per share'), candidate('.44', 'USD per share'))['matches']
    target = reference('25', 'percent relative change')
    assert locked_match(target, candidate('.25', 'ratio'))['matches']
    assert not locked_match(target, candidate('25', 'percentage_points'))['matches']


def test_native_rounded_answer_does_not_automatically_satisfy_unrounded_endpoint():
    target = reference('14.12037037037037', 'percent')
    assert locked_match(target, candidate('14.12037037', 'percent'))['matches']
    assert not locked_match(target, candidate('14.12', 'percent'))['matches']
    # The latter can still be an economically sensible rounded answer. This is an endpoint check.


def test_uncertain_reading_does_not_supply_a_primary_reference():
    for status in ['agreed_numeric_conditional', 'disputed_numeric_or_units',
                   'agreed_numeric_scale_unspecified', 'agreed_insufficient_information']:
        result = locked_match(reference('2.5', 'USD', status), candidate('2.5', 'USD'))
        assert result['eligible'] is False and result['matches'] is None
    assert locked_match(reference('2.5', 'USD'), None)['matches'] is False


def test_later_reference_projection_preserves_counts_and_handles_native_percent_fraction():
    target = reference('14.12037037037037', 'percent')
    assert reference_projection(target, candidate('14.12', 'percent'))['additional_rounded_match']
    assert not reference_projection(target, candidate('14.13', 'percent'))['matches']
    assert not reference_projection(reference('3', 'years'), candidate('3.004', 'count'))['matches']
    target['source'] = 'finqa'
    result = reference_projection(target, candidate('14.12', 'percent'))
    assert result['quantum_in_reference_unit'] == '0.001'
    assert result['matches'] is True
    assert reference_projection(target, candidate('14.120', 'percent'))['matches'] is True
    assert reference_projection(target, candidate('14.121', 'percent'))['matches'] is False
    assert reference_projection(target, candidate('14.12037037', 'percent'))['matches']
