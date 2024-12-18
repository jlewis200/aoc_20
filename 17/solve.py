#!/usr/bin/env python3

from itertools import product
import numpy as np

offsets = list(product([-1, 0, 1], repeat=3))
offsets.remove((0, 0, 0))
offsets = np.array(offsets)


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    return np.array([list(line.strip()) for line in lines])


def solve(board):
    cubes = np.argwhere(board == "#").tolist()
    cubes = {tuple(cube) + (0,) for cube in cubes}

    for _ in range(6):
        cubes = step(cubes)

    return len(cubes)


def step(cubes):
    """
    Copy the cubes, perform activation and deactivation.
    """
    new_cubes = cubes.copy()
    deactivate(cubes, new_cubes)
    activate(cubes, new_cubes)
    return new_cubes


def activate(cubes, new_cubes):
    """
    Check the 26 adjacent empty locations.  If those have exactly 3
    adjacencies, activate the location.
    """
    for cube in cubes:
        for next_cube in adjacency_generator(cube):
            if next_cube not in cubes and count_adjacent(next_cube, cubes) == 3:
                new_cubes.add(next_cube)


def deactivate(cubes, new_cubes):
    """
    Deactivate a cube if number of adjacent isnt 2 or 3.
    """
    for cube in cubes:
        if count_adjacent(cube, cubes) not in (2, 3):
            new_cubes.remove(cube)


def count_adjacent(cube, cubes):
    """
    Count the number of active cubes adjacent to a cube.
    """
    n_adjacent = 0

    for next_cube in adjacency_generator(cube):
        if next_cube in cubes:
            n_adjacent += 1

    return n_adjacent


def adjacency_generator(cube):
    for offset in offsets:
        yield tuple(cube + offset)


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 112)
    main("input.txt")
