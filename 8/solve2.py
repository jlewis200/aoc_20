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

    for idx, instruction in enumerate(instructions):
        operation, argument = instruction

        match operation:

            case "jmp":
                operation = "nop"

            case "nop":
                operation = "jmp"

        instruction = (operation, argument)
        modified_instructions = instructions.copy()
        modified_instructions[idx] = instruction

        is_infinite_loop, accumulator = infinite_loop(modified_instructions)
        if not is_infinite_loop:
            return accumulator


def infinite_loop(instructions):
    accumulator = 0
    executed = set()
    instruction_idx = 0
    valid_instructions = range(len(instructions))

    while instruction_idx not in executed and instruction_idx in valid_instructions:
        executed.add(instruction_idx)
        instruction_idx, accumulator = execute(
            instructions[instruction_idx],
            instruction_idx,
            accumulator,
        )

    return instruction_idx != len(instructions), accumulator


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
    main("test.txt", 8)
    main("input.txt")
