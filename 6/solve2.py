#!/usr/bin/env python3


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def parse(data):
    return data.strip().split("\n\n")


def solve(groups):
    yes_answers = 0

    for group in groups:
        answer_sets = []

        for person in group.split("\n"):
            answer_sets.append(set(person.strip()))

        if len(answer_sets) == 1:
            yes_answers += len(answer_sets[0])

        else:
            yes_answers += len(answer_sets[0].intersection(*answer_sets[1:]))

    return yes_answers


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 6)
    main("input.txt")
