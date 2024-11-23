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

            if board[y, x] == ".":
                continue

            count = 0

            for idx in [
                get_indices(board, y, x, "ul"),
                get_indices(board, y, x, "ur"),
                get_indices(board, y, x, "dr"),
                get_indices(board, y, x, "dl"),
                get_indices(board, y, x, "_l"),
                get_indices(board, y, x, "_r"),
                get_indices(board, y, x, "u_"),
                get_indices(board, y, x, "d_"),
            ]:
                board_slice = board[idx]
                if first_seat_occupied(board_slice):
                    count += 1

            if board[y, x] == "#" and count >= 5:
                next_board[y, x] = "L"

            elif board[y, x] == "L" and count == 0:
                next_board[y, x] = "#"

    return next_board


def first_seat_occupied(board_slice):
    for element in board_slice:

        if element == "#":
            return True

        elif element == "L":
            return False

    return False


def get_indices(board, y, x, direction):
    y_dir, x_dir = direction
    idx_y = np.arange(1, max(board.shape))
    idx_x = np.arange(1, max(board.shape))

    match y_dir:

        case "d":
            idx_y = y + idx_y

        case "u":
            idx_y = y - idx_y

        case "_":
            idx_y = np.full_like(idx_y, y)

    match x_dir:

        case "r":
            idx_x = x + idx_x

        case "l":
            idx_x = x - idx_x

        case "_":
            idx_x = np.full_like(idx_x, x)

    # get mask of in-bound indices
    valid_y = (idx_y >= 0) & (idx_y < board.shape[0])
    valid_x = (idx_x >= 0) & (idx_x < board.shape[1])
    valid = valid_x & valid_y

    return idx_y[valid], idx_x[valid]


def board_str(board):
    return "\n".join("".join(row) for row in board)


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 26)
    main("input.txt")
