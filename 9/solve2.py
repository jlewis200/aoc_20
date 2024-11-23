#!/usr/bin/env python3

from itertools import combinations


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    return list(map(int, lines))


def solve(numbers, window):
    invalid_number = get_invalid_number(numbers, window)
    return find_sequence(numbers, invalid_number)


def find_sequence(numbers, invalid_number):
    """
    If the sequence is smaller, move right edge right.
    If the sequence is larger, move left edge right.
    """
    idx_0 = 0
    idx_1 = 1

    while sum(numbers[idx_0:idx_1]) != invalid_number:

        if sum(numbers[idx_0:idx_1]) < invalid_number:
            idx_1 += 1
        else:
            idx_0 += 1

    return min(numbers[idx_0:idx_1]) + max(numbers[idx_0:idx_1])


def get_invalid_number(numbers, window):
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
    main("test.txt", 5, 62)
    main("input.txt", 25)
