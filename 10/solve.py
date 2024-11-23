#!/usr/bin/env python3

import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    return list(map(int, lines))


def solve(numbers):
    """
    The joltage adapters only accept lower, so the only possible arragement is
    ascending.
    """
    numbers.append(0)
    numbers.append(max(numbers) + 3)
    numbers = sorted(numbers)
    numbers = np.array(numbers)

    differences = dict(
        zip(
            *np.unique(
                numbers[1:] - numbers[:-1],
                return_counts=True,
            )
        )
    )

    return differences[1] * differences[3]


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 7 * 5)
    main("test2.txt", 22 * 10)
    main("input.txt")
