#!/usr/bin/env python3

import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    return np.array(list(map(lambda line: list(line.strip()), lines)))


def solve(board):
    n_trees = 0
    y, x = 0, 0
    dy, dx = 1, 3

    while y < board.shape[0]:
        if board[y, x] == "#":
            n_trees += 1
        y += dy
        x += dx
        x %= board.shape[1]

    return n_trees


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 7)
    main("input.txt", 220)
