import ast
import operator
from datetime import datetime

from langchain_core.tools import tool
import requests


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


@tool
def placeholder_todo() -> str:
    """Fetch todo item 1 from the JSONPlaceholder demo API."""
    try:
        response = requests.get(
            "https://jsonplaceholder.typicode.com/todos/1",
            timeout=10,
        )
        response.raise_for_status()
        todo = response.json()
        return (
            f"Todo {todo['id']}: {todo['title']} "
            f"(completed: {todo['completed']})"
        )
    except (requests.RequestException, ValueError, KeyError) as error:
        return f"Could not fetch the todo item: {error}"


TOOLS = [calculator, current_date_time, placeholder_todo]