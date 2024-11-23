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
            "(?P<idx_0>\d+)-(?P<idx_1>\d+) (?P<char>.): (?P<password>.+)", line
        )
        database.append(
            {
                "idx_0": int(match.group("idx_0")) - 1,
                "idx_1": int(match.group("idx_1")) - 1,
                "char": match.group("char"),
                "password": match.group("password"),
            }
        )
    return database


def solve(database):
    n_valid = 0

    for entry in database:
        idx_0 = entry["idx_0"]
        idx_1 = entry["idx_1"]
        char = entry["char"]
        password = entry["password"]

        if (password[idx_0] == char and password[idx_1] != char) or (
            password[idx_0] != char and password[idx_1] == char
        ):
            n_valid += 1

    return n_valid


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 1)
    main("input.txt")
