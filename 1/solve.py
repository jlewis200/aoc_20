#!/usr/bin/env python3

from itertools import combinations


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    return list(map(int, lines))


def solve(entries):
    for entry_0, entry_1 in combinations(entries, 2):
        if entry_0 + entry_1 == 2020:
            return entry_0 * entry_1


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 514579)
    main("input.txt")
