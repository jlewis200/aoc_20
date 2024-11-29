#!/usr/bin/env python3

from re import match
import numpy as np


def extract_coords(instruction):
    """
    Extract the ending coordinates for an instruction set.
    """
    y, x = 0, 0

    for direction in instruction:
        dy, dx = get_delta(direction)
        y += dy
        x += dx

    return y, x


def get_delta(direction):
    """
    Get the y, x deltas for a given direction.
    """
    match direction:
        case "w":
            return 0, -2

        case "e":
            return 0, 2

        case "se":
            return 1, 1

        case "sw":
            return 1, -1

        case "ne":
            return -1, 1

        case "nw":
            return -1, -1


def solve(instructions):
    """
    Treat the hexagonal grid as a 2-d square grid by considering single
    direction instruction to increment by 2 and mixed direction instructions
    as 1, 1.

    single direction:
        w: y += 0, x -= 2
        e: y += 0, x += 2

    mixed direction:
        se: y += 1, x += 1
        sw: y += 1, x -= 1
        ne: y -= 1, x += 1
        nw: y -= 1, x -= 1

    Get the coordinate specified by the instruction.  If it's not in the list
    of black tiles, add it.  If it is in the list of black tiles, remove it.
    """
    tiles = initialize_tiles(instructions)

    for _ in range(100):
        tiles = flip_tiles(tiles)
    return len(tiles)


def flip_tiles(tiles):
    """
    Flip tiles according to black-to-white and white-to-black rules.
    """
    next_tiles = set()

    next_tiles |= black_to_white(tiles)
    next_tiles |= white_to_black(tiles)

    return next_tiles


def black_to_white(tiles):
    """
    A tile is retained if it has 1 or 2 adjacencies.
    """
    next_tiles = set()

    for tile in tiles:
        if count_adjacencies(*tile, tiles) in (1, 2):
            next_tiles.add(tile)

    return next_tiles


def white_to_black(tiles):
    """
    Enumerate white adjacencies of every black tile, flip to black if exactly
    2 black adjacencies.
    """
    next_tiles = set()

    for tile in white_tile_adjacency_generator(tiles):
        if count_adjacencies(*tile, tiles) == 2:
            next_tiles.add(tile)

    return next_tiles


def white_tile_adjacency_generator(tiles):
    """
    Get adjacencies of every black tile, remove black adjacencies.
    """
    adjacencies = set()

    for tile in tiles:
        adjacencies |= set(adjacency_generator(*tile))

    adjacencies -= tiles
    return adjacencies


def count_adjacencies(y, x, tiles):
    """
    Count black tile adjacencies.
    """
    n_adjacencies = 0

    for y_1, x_1 in adjacency_generator(y, x):
        if (y_1, x_1) in tiles:
            n_adjacencies += 1

    return n_adjacencies


def adjacency_generator(y, x):
    """
    Generate coords for all tiles adjacent to (y, x).
    """
    for direction in ("e", "se", "sw", "w", "nw", "ne"):
        dy, dx = get_delta(direction)
        yield y + dy, x + dx


def initialize_tiles(instructions):
    coords = set()

    for instruction in instructions:
        coord = extract_coords(instruction)

        if coord in coords:
            coords.remove(coord)

        else:
            coords.add(coord)

    return coords


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


def parse(lines):
    instructions = []

    for line in lines:
        line.strip()
        instruction = []

        while len(line) > 0:
            match_ = match("(?P<direction>e|se|sw|w|nw|ne)(?P<remaining>.*)", line)
            instruction.append(match_.group("direction"))
            line = match_.group("remaining")

        instructions.append(instruction)

    return instructions


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


if __name__ == "__main__":
    main("test.txt", 2208)
    main("input.txt")
