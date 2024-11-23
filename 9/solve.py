#!/usr/bin/env python3

from itertools import combinations


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    return list(map(int, lines))


def solve(numbers, window):
    for idx, number in enumerate(numbers[window:]):
        candidates = numbers[idx : idx + window]

        if not valid(number, candidates):
            return number


def valid(number, candidates):
    for combination in combinations(candidates, 2):
        if sum(combination) == number:
            return True
    return False


def main(filename, window, expected=None):
    result = solve(parse(read_file(filename)), window)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 5, 127)
    main("input.txt", 25)
