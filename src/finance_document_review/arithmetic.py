"""Executive summary: compute declared numeric expressions without executing annotation code."""
from __future__ import annotations

import ast
from decimal import Decimal, localcontext


def calculate(expression: str) -> Decimal:
    """Accept finite numeric literals and elementary arithmetic only."""
    if not isinstance(expression, str) or not expression.strip() or len(expression) > 2048:
        raise ValueError("Expected a nonempty arithmetic expression of at most 2048 characters")
    tree = ast.parse(expression, mode="eval")
    if sum(1 for _ in ast.walk(tree)) > 256:
        raise ValueError("Arithmetic expression is too large")

    def visit(node: ast.AST) -> Decimal:
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            literal = ast.get_source_segment(expression, node)
            value = Decimal(literal.replace("_", ""))
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            operand = visit(node.operand)
            value = operand if isinstance(node.op, ast.UAdd) else -operand
        elif isinstance(node, ast.BinOp):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                value = left + right
            elif isinstance(node.op, ast.Sub):
                value = left - right
            elif isinstance(node.op, ast.Mult):
                value = left * right
            elif isinstance(node.op, ast.Div):
                value = left / right
            elif isinstance(node.op, ast.Pow):
                if right != right.to_integral_value() or abs(right) > 32:
                    raise ValueError("Only integer powers between -32 and 32 are admitted")
                value = left ** int(right)
            else:
                raise ValueError("Unsupported arithmetic operator")
        else:
            raise ValueError("Only numeric literals, signs and elementary arithmetic are admitted")
        if not value.is_finite() or abs(value) > Decimal("1e100"):
            raise ValueError("Nonfinite or excessively large arithmetic value")
        return value

    with localcontext() as context:
        context.prec = 60
        return visit(tree.body)
