#!/usr/bin/env python3

from re import search


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    instructions = []

    for line in lines:
        operation, argument = line.split()
        instructions.append((operation, int(argument)))

    return instructions


def solve(instructions):
    accumulator = 0
    executed = set()
    instruction_idx = 0

    while instruction_idx not in executed:
        executed.add(instruction_idx)
        instruction_idx, accumulator = execute(
            instructions[instruction_idx],
            instruction_idx,
            accumulator,
        )

    return accumulator


def execute(instruction, instruction_idx, accumulator):
    operation, argument = instruction

    match operation:

        case "acc":
            accumulator += argument
            instruction_idx += 1

        case "jmp":
            instruction_idx += argument

        case "nop":
            instruction_idx += 1

    return instruction_idx, accumulator


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 5)
    main("input.txt")
