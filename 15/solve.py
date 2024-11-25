#!/usr/bin/env python3


def solve(numbers):
    record = {}
    record = warmup(numbers, record)

    idx = len(numbers) - 1
    next_number = numbers[-1]

    while idx < 2020:
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
    assert solve([0, 3, 6]) == 436
    assert solve([1, 3, 2]) == 1
    assert solve([2, 1, 3]) == 10
    assert solve([1, 2, 3]) == 27
    assert solve([2, 3, 1]) == 78
    assert solve([3, 2, 1]) == 438
    assert solve([3, 1, 2]) == 1836
    print(solve([7, 12, 1, 0, 16, 2]))


if __name__ == "__main__":
    main()
