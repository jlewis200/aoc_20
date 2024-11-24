#!/usr/bin/env python3

from math import lcm


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    initial = int(lines.pop(0))
    buses = []

    for bus in lines.pop(0).split(","):

        if bus == "x":
            buses.append(None)
            continue

        buses.append(int(bus))

    return buses


def solve(buses):
    cycles = []
    bus_0 = buses.pop(0)

    for idx, bus_1 in enumerate(buses, start=1):
        if bus_1 is None:
            continue

        cycles.append(get_cycle_parameters(bus_0, bus_1, idx))

    t, _ = merge_cycles(cycles).pop(0)
    return t


def merge_cycles(cycles):
    """
    The cycles are merged to create cycles with larger cycle lengths.

    The idea is to pick two cycles and increment each until they share the same
    value.  At this point a new cycle can be made with the current value as the
    first match and the cycle length as the least common multiple of the
    original cycle lengths.

    The new cycle is added back to the queue and the process repeats until one
    cycle remains.  The first match of the final cycle is the first point where
    all bus delay requirements are met.
    """
    while len(cycles) > 1:
        val_0, len_0 = cycles.pop(0)
        val_1, len_1 = cycles.pop(0)

        while val_0 != val_1:
            if val_0 > val_1:
                val_0, val_1 = val_1, val_0
                len_0, len_1 = len_1, len_0

            val_0 += len_0

        cycles.append((val_0, lcm(len_0, len_1)))

    return cycles


def get_cycle_parameters(bus_0, bus_1, delta):
    """
    Find the first two timesteps where bus_0 and bus_1 meet the relative
    departure delay specified by the puzzle.

    The relative departure delays occur at intervals following:
        first_match + k * cycle_length

    For example if bus_0 = 2, bus_1 = 3, and the departure delay is 1:
        first_match = 2
        second_match = 8
        cycle_length = 6

    So the matches occur at 2, 8, 14, 20, etc...
    """
    time_steps = []
    val_0, val_1 = bus_0, bus_1

    while len(time_steps) < 2:

        if val_1 - val_0 == delta:
            time_steps.append(val_0)

        # increment val_0 if it's too far from val_1
        if val_0 < (val_1 - delta):
            val_0 += bus_0

        # increment val_1 if it's too close to val_0
        else:
            val_1 += bus_1

    first_match = time_steps.pop(0)
    cycle_length = time_steps.pop(0) - first_match
    return first_match, cycle_length


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    assert solve([2, 3, 5, 7]) == 158
    assert solve([17, None, 13, 19]) == 3417
    assert solve([67, 7, 59, 61]) == 754018
    assert solve([67, None, 7, 59, 61]) == 779210
    assert solve([67, 7, None, 59, 61]) == 1261476
    assert solve([1789, 37, 47, 1889]) == 1202161486
    main("test.txt", 1068781)
    main("input.txt")
