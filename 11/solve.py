#!/usr/bin/env python3

import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    board = np.array([list(line.strip()) for line in lines])
    return np.pad(board, 1, constant_values=".")


def solve(next_board):
    board = np.zeros_like(next_board)

    while (next_board != board).any():
        board = next_board
        next_board = step(board)

    return (board == "#").sum()


def step(board):
    next_board = board.copy()

    for y in range(1, board.shape[0]):
        for x in range(1, board.shape[1]):
            board_slice = board[y - 1 : y + 2, x - 1 : x + 2]

            if board[y, x] == "L" and "#" not in board_slice:
                next_board[y, x] = "#"

            elif board[y, x] == "#" and ("#" == board_slice).sum() >= 5:
                # 5 to account for self
                next_board[y, x] = "L"

    return next_board


def board_str(board):
    return "\n".join("".join(row) for row in board)


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 37)
    main("input.txt")
