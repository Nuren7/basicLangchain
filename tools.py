import ast
import operator
from datetime import datetime

from langchain_core.tools import tool


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _calculate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_calculate(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](
            _calculate(node.left), _calculate(node.right)
        )
    raise ValueError("Only basic arithmetic is supported.")


@tool
def calculator(expression: str) -> str:
    """Calculate a basic arithmetic expression such as 12 * (3 + 4)."""
    try:
        result = _calculate(ast.parse(expression, mode="eval").body)
        return str(result)
    except (SyntaxError, TypeError, ValueError, ZeroDivisionError) as error:
        return f"Could not calculate that expression: {error}"


@tool
def current_date_time() -> str:
    """Return the computer's current local date and time."""
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


TOOLS = [calculator, current_date_time]