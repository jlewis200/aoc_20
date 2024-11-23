#!/usr/bin/env python3

from re import fullmatch


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    instructions = []

    for line in lines:
        match = fullmatch("(?P<action>[A-Z]{1})(?P<value>\d+)", line.strip())
        instructions.append(
            (
                match.group("action"),
                int(match.group("value")),
            )
        )

    return instructions


def solve(instructions):
    direction = 0
    y, x = 0, 0
    direction_action_map = {
        0: "E",
        90: "N",
        180: "W",
        270: "S",
    }

    for action, value in instructions:

        if action == "F":
            y, x, direction = do_action(
                direction_action_map[direction],
                value,
                y,
                x,
                direction,
            )

        else:
            y, x, direction = do_action(action, value, y, x, direction)

    return abs(y) + abs(x)


def do_action(action, value, y, x, direction):
    match action:

        case "N":
            y -= value

        case "S":
            y += value

        case "W":
            x -= value

        case "E":
            x += value

        case "L":
            direction += value

        case "R":
            direction -= value

    direction %= 360
    assert direction in (0, 90, 180, 270)

    return y, x, direction


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 25)
    main("input.txt")
