#!/usr/bin/env python3


def solve(numbers):
    record = {}
    record = warmup(numbers, record)

    idx = len(numbers) - 1
    next_number = numbers[-1]
    zero_count = 0

    while idx < 30000000:
        number = next_number

        if number in record:
            next_number = idx - record[number]

        else:
            next_number = 0

        record[number] = idx
        idx += 1

    return number


def warmup(numbers, record):
    for idx, number in enumerate(numbers[:-1]):
        record[number] = idx
    return record


def main():
    print(solve([7, 12, 1, 0, 16, 2]))


if __name__ == "__main__":
    main()
