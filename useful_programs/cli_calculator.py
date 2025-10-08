#!/usr/bin/env python3
"""Simple CLI calculator: supports + - * / and parentheses via eval with safety."""
import ast
import operator as op
import sys

ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def eval_expr(expr: str):
    """Safely evaluate a math expression using AST."""
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    parsed = ast.parse(expr, mode="eval")
    return _eval(parsed.body)


def main():
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
    else:
        expr = input("Enter expression: ")
    try:
        result = eval_expr(expr)
        print(result)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
