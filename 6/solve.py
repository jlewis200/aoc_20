#!/usr/bin/env python3


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def parse(data):
    return data.split("\n\n")


def solve(groups):
    yes_answers = 0

    for group in groups:
        group = group.replace("\n", "")
        yes_answers += len(set(group))

    return yes_answers


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 11)
    main("input.txt")
