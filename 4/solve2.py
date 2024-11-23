#!/usr/bin/env python3

from re import fullmatch


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

    for passport in passports:
        if valid(passport):
            n_valid += 1

    return n_valid


def valid(passport):
    required_fields = {
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
    }

    if len(required_fields & passport.keys()) == len(required_fields):
        return (
            valid_birth(passport)
            and valid_issue(passport)
            and valid_expiration(passport)
            and valid_height(passport)
            and valid_hair(passport)
            and valid_eye(passport)
            and valid_pid(passport)
        )
    return False


def valid_birth(passport):
    year = int(passport["byr"])
    return year in range(1920, 2002 + 1)


def valid_issue(passport):
    year = int(passport["iyr"])
    return year in range(2010, 2020 + 1)


def valid_expiration(passport):
    year = int(passport["eyr"])
    return year in range(2020, 2030 + 1)


def valid_height(passport):
    height = passport["hgt"]
    match = fullmatch("(?P<value>\d+)(?P<unit>.+)", height)

    if match is not None:
        value = int(match.group("value"))
        unit = match.group("unit")

        if unit == "in":
            return value in range(59, 76 + 1)

        elif unit == "cm":
            return value in range(150, 193 + 1)

    return False


def valid_hair(passport):
    hair = passport["hcl"]
    match = fullmatch("#[a-f0-9]{6}", hair)
    return match is not None


def valid_eye(passport):
    eye = passport["ecl"]
    return eye in [
        "amb",
        "blu",
        "brn",
        "gry",
        "grn",
        "hzl",
        "oth",
    ]


def valid_pid(passport):
    pid = passport["pid"]
    match = fullmatch("\d{9}", pid)
    return match is not None


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test2.txt", 4)
    main("input.txt")
