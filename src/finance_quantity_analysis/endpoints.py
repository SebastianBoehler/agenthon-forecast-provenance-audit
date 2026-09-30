"""Executive summary: independently parse typed answers and evaluate numeric arithmetic."""

import ast
import json
import re
from decimal import Decimal, localcontext
from fractions import Fraction

UNITS = set('currency currency_per_share currency_per_year percent percentage_points ratio count duration_years duration_months duration_days boolean unknown'.split())
SCALES = dict(none=1, thousand=1000, million=10**6, billion=10**9)
SCALED = set('currency currency_per_share currency_per_year count'.split())
FIELDS = set('status value unit scale calculation evidence'.split())
JUDGE_FIELDS = set('verdict requested_quantity operand_checks unit_check reason evidence'.split())


def unique(pairs):
    if len(dict(pairs)) != len(pairs):
        raise ValueError('duplicate JSON key')
    return dict(pairs)


def decode(text):
    def reject(_):
        raise ValueError('nonfinite JSON constant')
    return json.loads(text, object_pairs_hook=unique, parse_constant=reject)


def number(value):
    if not isinstance(value, str):
        raise ValueError('numeric value is not a decimal string')
    d = Decimal(value)
    if not d.is_finite():
        raise ValueError('nonfinite decimal')
    return Fraction(d)


def native_number(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError('invalid native scalar')
    return number(str(value))


def arithmetic(expression):
    if not isinstance(expression, str) or not expression.strip() or len(expression) > 2048:
        raise ValueError('empty/oversized expression')
    tree = ast.parse(expression, mode='eval')
    if sum(1 for _ in ast.walk(tree)) > 256:
        raise ValueError('oversized expression tree')
    def visit(n):
        if isinstance(n, ast.Constant) and type(n.value) in (int, float):
            value = number(ast.get_source_segment(expression, n).replace('_', ''))
        elif isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
            value = visit(n.operand) * (-1 if isinstance(n.op, ast.USub) else 1)
        elif isinstance(n, ast.BinOp):
            a, b = visit(n.left), visit(n.right)
            if isinstance(n.op, ast.Add): value = a + b
            elif isinstance(n.op, ast.Sub): value = a - b
            elif isinstance(n.op, ast.Mult): value = a * b
            elif isinstance(n.op, ast.Div): value = a / b
            elif isinstance(n.op, ast.Pow) and b.denominator == 1 and abs(b) <= 32:
                value = a ** int(b)
            else: raise ValueError('unsupported operator/power')
        else:
            raise ValueError('non-numeric expression')
        if abs(value) > 10**100:
            raise ValueError('excessive arithmetic magnitude')
        return value
    return visit(tree.body)


def decimal_text(value):
    with localcontext() as c:
        c.prec = 60
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def typed(value, unit, scale):
    if unit not in UNITS - {'boolean', 'unknown'} or scale not in SCALES:
        raise ValueError('unrecognized numerical unit/scale')
    if unit not in SCALED and scale != 'none':
        raise ValueError('rate/ratio/duration carries a scale')
    return (value if isinstance(value, Fraction) else number(value)) * SCALES[scale]


def close(actual, reference):
    return abs(actual-reference) <= max(Fraction(1, 10**8), abs(reference)/10000)


def candidate(text):
    try:
        a = decode(text)
        if not isinstance(a, dict) or set(a) != FIELDS:
            raise ValueError('fields')
        if a['status'] not in {'answer','ambiguous','insufficient_information','non_numeric_answer'}:
            raise ValueError('status')
        if a['unit'] not in UNITS or a['scale'] not in SCALES:
            raise ValueError('unit/scale')
        if not isinstance(a['calculation'], str) or not isinstance(a['evidence'], list):
            raise ValueError('calculation/evidence')
        if not all(isinstance(p, str) for p in a['evidence']):
            raise ValueError('evidence type')
        if a['status'] == 'answer':
            typed(a['value'], a['unit'], a['scale'])
            arithmetic(a['calculation'])
        else:
            if a['calculation'].strip(): raise ValueError('non-numeric calculation')
            if a['status'] == 'non_numeric_answer':
                if a['value'] not in {'yes','no'} or a['unit'] != 'boolean' or a['scale'] != 'none':
                    raise ValueError('Boolean')
            elif a['value'] is not None: raise ValueError('nonempty abstention')
        return a, None
    except (ValueError, TypeError, ArithmeticError, SyntaxError, KeyError) as error:
        return None, type(error).__name__ + ': ' + str(error)


def score(text, reference, native=None):
    a, error = candidate(text)
    result = dict(primary_eligible=reference['eligible'] is True, schema_valid=error is None,
                  schema_error=error, reported_numeric_typed_match=False,
                  expression_numeric_typed_match=False, reported_expression_consistent=False,
                  native_literal_exact=None if native is None else False)
    if a and a['status'] == 'answer':
        actual = typed(a['value'], a['unit'], a['scale'])
        expression = arithmetic(a['calculation'])
        expressed = typed(expression, a['unit'], a['scale'])
        result['expression_value'] = decimal_text(expression)
        result['reported_expression_consistent'] = close(actual, expressed)
        if result['primary_eligible']:
            target = typed(reference['value'], reference['unit'], reference['scale'])
            result['reported_numeric_typed_match'] = a['unit'] == reference['unit'] and close(actual, target)
            result['expression_numeric_typed_match'] = a['unit'] == reference['unit'] and close(expressed, target)
        if native is not None:
            result['native_literal_exact'] = number(a['value']) == native_number(native['value'])
    return result


def location(context, path, strict_types=False):
    if not isinstance(path, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*(?:(?:\.[A-Za-z_][A-Za-z_0-9]*)|(?:\[\d+\]))*', path):
        raise ValueError('pointer syntax')
    value = context
    for key, index in re.findall(r'([A-Za-z_][A-Za-z_0-9]*)|\[(\d+)\]', path):
        if strict_types and not isinstance(value, dict if key else list):
            raise ValueError('pointer container type')
        value = value[key] if key else value[int(index)]
    if not isinstance(value, str): raise ValueError('pointer is not a text/cell')
    return value


def judge(text, context, candidate_error):
    try:
        j = decode(text)
        if not isinstance(j, dict) or set(j) != JUDGE_FIELDS: raise ValueError('fields')
        if j['verdict'] not in {'supported','contradicted','ambiguous','unassessable'}:
            raise ValueError('verdict')
        if not all(isinstance(j[k], str) for k in ['requested_quantity','unit_check','reason']):
            raise ValueError('text fields')
        if not isinstance(j['operand_checks'], list) or not all(isinstance(x, dict) for x in j['operand_checks']):
            raise ValueError('operand checks')
        if not isinstance(j['evidence'], list): raise ValueError('evidence')
        for p in j['evidence']: location(context, p)
        return dict(judgment=j, effective_verdict='unassessable' if candidate_error else j['verdict'],
                    candidate_malformed=candidate_error is not None,
                    protocol_violation=bool(candidate_error and j['verdict'] != 'unassessable')), None
    except (ValueError, TypeError, KeyError, IndexError) as error:
        return dict(judgment=None, effective_verdict='unassessable',
                    candidate_malformed=candidate_error is not None, protocol_violation=True), str(error)


def evidence_invalid(evidence, context):
    invalid = []
    for p in evidence:
        try: location(context, p, strict_types=True)
        except (ValueError, TypeError, KeyError, IndexError): invalid.append(p)
    return invalid


def raw_evidence(text, context):
    try: decoded = decode(text)
    except (ValueError, TypeError): decoded = None
    evidence = decoded.get('evidence') if isinstance(decoded, dict) else None
    paths = evidence if isinstance(evidence, list) and all(isinstance(p, str) for p in evidence) else None
    return dict(invalid_paths=evidence_invalid(paths, context) if paths is not None else [],
                unavailable=paths is None, empty=paths == [])
