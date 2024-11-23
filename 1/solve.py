#!/usr/bin/env python3

from itertools import combinations
from math import prod


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    return list(map(int, lines))


def solve(entries, n_entries):
    for combination in combinations(entries, n_entries):
        if sum(combination) == 2020:
            return prod(combination)


def main(filename, n_entries, expected=None):
    result = solve(parse(read_file(filename)), n_entries)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 2, 514579)
    main("test.txt", 3, 241861950)
    main("input.txt", 2, 964875)
    main("input.txt", 3)
