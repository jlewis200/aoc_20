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
    y, x = 0, 0
    w_y, w_x = 1, 10
    direction_action_map = {
        0: "E",
        90: "N",
        180: "W",
        270: "S",
    }

    for action, value in instructions:

        if action == "F":
            y += w_y * value
            x += w_x * value

        else:
            w_y, w_x = do_action(action, value, w_y, w_x)

    return abs(y) + abs(x)


def do_action(action, value, y, x):
    match action:

        case "N":
            y += value

        case "S":
            y -= value

        case "W":
            x -= value

        case "E":
            x += value

        case "L" | "R":
            y, x = rotate(y, x, action, value)

    return y, x


def rotate(y, x, action, value):
    """
    Convert a right rotation into an equivalent left rotation.
    Rotate by swapping x/y and muliplying x by -1.
    """
    if action == "R":
        value = -value
        value %= 360

    assert value in (90, 180, 270)

    for _ in range(value // 90):
        y, x = x, -y

    return y, x


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 286)
    main("input.txt", 28591)
