#!/usr/bin/env python3

from re import fullmatch


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def parse(data):
    valid_ranges_chunk, my_ticket_chunk, tickets_chunk = data.split("\n\n")
    valid_ranges = parse_valid_ranges(valid_ranges_chunk)
    my_ticket = parse_ticket(my_ticket_chunk.split("\n")[-1])
    tickets = tickets_chunk.strip().split("\n")
    tickets = [parse_ticket(ticket) for ticket in tickets[1:]]
    return valid_ranges, my_ticket, tickets


def parse_ticket(ticket):
    return tuple(map(int, ticket.split(",")))


def parse_valid_ranges(valid_ranges_chunk):
    valid_ranges = {}

    for valid_range in valid_ranges_chunk.split("\n"):
        match = fullmatch(
            (
                "(?P<field>.*): "
                "(?P<start_range_0>\d+)-(?P<end_range_0>\d+) or "
                "(?P<start_range_1>\d+)-(?P<end_range_1>\d+)"
            ),
            valid_range,
        )
        field = match.group("field")
        valid_ranges[f"{field}_0"] = range(
            int(match.group("start_range_0")),
            int(match.group("end_range_0")) + 1,
        )
        valid_ranges[f"{field}_1"] = range(
            int(match.group("start_range_1")),
            int(match.group("end_range_1")) + 1,
        )

    return valid_ranges


def solve(valid_ranges, my_ticket, tickets):
    """
    Find and summ invalid values across all tickets.
    """
    invalid_values = []

    for ticket in tickets:
        invalid_values.extend(get_invalid_values(valid_ranges, ticket))

    return sum(invalid_values)


def get_invalid_values(valid_ranges, ticket):
    """
    Collect the invalid values in a ticket.
    """
    invalid_values = []

    for value in ticket:
        if not valid_value(valid_ranges, value):
            invalid_values.append(value)

    return invalid_values


def valid_value(valid_ranges, value):
    """
    Check if the value is valid for at least one range.
    """
    for valid_range in valid_ranges.values():
        if value in valid_range:
            return True

    return False


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 71)
    main("input.txt")
