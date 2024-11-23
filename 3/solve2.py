#!/usr/bin/env python3

import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    return np.array(list(map(lambda line: list(line.strip()), lines)))


def solve(board):
    tree_counts = 1

    for slope in [
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1),
    ]:
        tree_counts *= count_trees(board, *slope)

    return tree_counts


def count_trees(board, dy, dx):
    n_trees = 0
    y, x = 0, 0

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
    main("test.txt", 336)
    main("input.txt", 2138320800)
