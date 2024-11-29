#!/usr/bin/env python3

from re import match


def extract_coords(instruction):
    y, x = 0, 0

    for direction in instruction:
        dy, dx = get_delta(direction)
        y += dy
        x += dx

    return y, x


def get_delta(direction):

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
    coords = set()

    for instruction in instructions:
        coord = extract_coords(instruction)

        if coord in coords:
            coords.remove(coord)

        else:
            coords.add(coord)

    return len(coords)


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
    main("test.txt", 10)
    main("input.txt")
