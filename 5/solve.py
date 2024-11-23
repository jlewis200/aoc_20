#!/usr/bin/env python3


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    lines = map(str.strip, lines)
    return [(line[:7], line[7:]) for line in lines]


def solve(seat_codes):
    seat_ids = [get_seat_id(seat_code) for seat_code in seat_codes]
    return max(seat_ids)


def get_seat_id(seat_code):
    row, col = seat_code
    return (get_row(row) * 8) + get_col(col)


def get_row(row):
    row = row.replace("F", "0")
    row = row.replace("B", "1")
    return int(row, 2)


def get_col(col):
    col = col.replace("L", "0")
    col = col.replace("R", "1")
    return int(col, 2)


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 820)
    main("input.txt")
