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
        expression = expression.replace("*", "@")
        expression = expression.replace("+", "*")
        expression = expression.replace("@", "+")
        expression = expression.split()
        expressions.append(expression)

    return expressions


class BackwardsInt:
    """
    This is probably not the intended method but it's interesting.

    The function of * and + are swapped, then the +/* are swapped in the
    expression, finally eval takes care of the precedence using an eval.
    """

    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return BackwardsInt(self.value * other.value)

    def __mul__(self, other):
        return BackwardsInt(self.value + other.value)

    def __repr__(self):
        return f"{self.value}"

    def __eq__(self, other):
        return self.value == other.value


def solve(expressions):
    res = BackwardsInt(0)

    for expression in expressions:
        res *= evaluate(expression)

    return res


def evaluate(expression):

    str_expression = ""

    for token in expression:

        try:
            str_expression += f" BackwardsInt({int(token)}) "
        except:
            str_expression += f" {token} "

    return eval(str_expression)


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    assert solve(parse(["2 * 3 + (4 * 5)"])) == BackwardsInt(46)
    assert solve(parse(["5 + (8 * 3 + 9 + 3 * 4 * 3)"])) == BackwardsInt(1445)
    assert solve(parse(["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"])) == BackwardsInt(
        669060
    )
    assert solve(
        parse(["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"])
    ) == BackwardsInt(23340)
    main("input.txt")
