#!/usr/bin/env python3

import re


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    expressions = []

    for expression in lines:
        expression = expression.replace("(", "( ")
        expression = expression.replace(")", " )")
        expression = expression.split()
        expressions.append(expression)

    return expressions


def solve(expressions):
    res = 0

    for expression in expressions:
        res += evaluate(expression)

    return res


def evaluate(expression):
    left, right, operator = (None,) * 3

    while len(expression) > 0:
        token = expression.pop(0)

        if token == "(":
            expression.insert(0, evaluate(expression))

        elif token == ")":
            return left

        elif token in ("+", "*"):
            operator = token

        else:
            if left is None:
                left = int(token)
            else:
                right = int(token)

        if right is not None:
            expression.insert(0, do_math(left, right, operator))
            left, right, operator = (None,) * 3

    return left


def do_math(left, right, operator):
    if operator == "+":
        return left + right
    return left * right


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    assert solve(parse(["2 * 3 + (4 * 5)"])) == 26
    assert solve(parse(["5 + (8 * 3 + 9 + 3 * 4 * 3)"])) == 437
    assert solve(parse(["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"])) == 12240
    assert solve(parse(["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"])) == 13632
    main("input.txt")
