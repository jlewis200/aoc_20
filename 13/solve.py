#!/usr/bin/env python3

from re import fullmatch


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    initial = int(lines.pop(0))
    buses = []

    for bus in lines.pop(0).split(","):

        if bus == "x":
            continue

        buses.append(int(bus))

    return initial, buses


def solve(initial, buses):
    time = initial

    while True:
        for bus in buses:
            if time % bus == 0:
                waiting_time = time - initial
                return waiting_time * bus

        time += 1


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 295)
    main("input.txt")
