#!/usr/bin/env python3


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def parse(data):
    passports = data.split("\n\n")
    passports_data = []

    for passport in passports:
        records = passport.split()

        parsed = {}
        for record in records:
            key, value = record.split(":")
            parsed[key] = value

        passports_data.append(parsed)

    return passports_data


def solve(passports):
    n_valid = 0

    required_fields = {
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
        # "cid",
    }

    for passport in passports:
        if len(required_fields & passport.keys()) == len(required_fields):
            n_valid += 1

    return n_valid


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 2)
    main("input.txt")
