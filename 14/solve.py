#!/usr/bin/env python3

from re import search


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    chunks = []

    for line in lines:
        match = search("mask = (?P<mask>[10X]+)", line)
        if match is not None:
            chunk = []
            chunks.append(chunk)
            chunk.append(match.group("mask"))

        match = search("mem\[(?P<address>\d+)\] = (?P<value>\d+)", line)
        if match is not None:
            chunk.append(
                (
                    int(match.group("address")),
                    int(match.group("value")),
                )
            )

    return chunks


def solve(chunks):
    memory = {}

    for chunk in chunks:
        or_mask, and_mask = get_masks(chunk.pop(0))

        while len(chunk) > 0:
            address, value = chunk.pop(0)
            value |= or_mask
            value &= and_mask
            memory[address] = value

    return sum(memory.values())


def get_masks(mask):
    or_mask = int(mask.replace("X", "0"), 0b10)
    and_mask = int(mask.replace("X", "1"), 0b10)
    return or_mask, and_mask


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 165)
    main("input.txt")
