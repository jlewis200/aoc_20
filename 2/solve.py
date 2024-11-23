#!/usr/bin/env python3

import re
import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    database = []
    for line in lines:
        match = re.search(
            "(?P<min_count>\d+)-(?P<max_count>\d+) (?P<char>.): (?P<password>.+)", line
        )
        min_count = int(match.group("min_count"))
        max_count = int(match.group("max_count"))
        database.append(
            {
                "count_range": range(min_count, max_count + 1),
                "char": match.group("char"),
                "password": match.group("password"),
            }
        )
    return database


def solve(database):
    n_valid = 0

    for entry in database:
        counts = dict(
            zip(
                *np.unique(
                    list(entry["password"]),
                    return_counts=True,
                )
            )
        )

        if entry["char"] not in counts:
            continue

        if counts[entry["char"]] in entry["count_range"]:
            n_valid += 1

    return n_valid


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 2)
    main("input.txt")
