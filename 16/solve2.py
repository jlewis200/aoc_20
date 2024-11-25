#!/usr/bin/env python3

from re import fullmatch
import numpy as np


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
        valid_ranges[field] = (
            range(
                int(match.group("start_range_0")),
                int(match.group("end_range_0")) + 1,
            ),
            range(
                int(match.group("start_range_1")),
                int(match.group("end_range_1")) + 1,
            ),
        )

    return valid_ranges


def solve(valid_ranges, my_ticket, tickets):
    """
    Get valid tickets, find plausible column candidates, perform process of
    elimination to find true column map, find prod of fields starting with
    'departure'.
    """
    valid_tickets = get_valid_tickets(valid_ranges, tickets)
    candidates = get_candidates(valid_ranges, valid_tickets, my_ticket)
    field_map = eliminate(candidates)
    product = 1

    for field, (idx, *_) in field_map.items():
        if field.startswith("departure"):
            product *= my_ticket[idx]

    return product


def eliminate(candidates):
    """
    Treat candidate sets with one element as solved.  Remove from all other
    candidate sets.  Repeat until each candidate set has only a single
    candidate.
    """
    while any(len(candidate) > 1 for candidate in candidates.values()):

        for field, candidate in candidates.items():
            if len(candidate) == 1:
                remove_confirmed(candidates, *candidate)

    return candidates


def remove_confirmed(candidates, value):
    """
    Remove a value from any set with more than one candidate.
    """
    for field, candidate in candidates.items():
        if len(candidate) > 1 and value in candidate:
            candidate.remove(value)


def get_candidates(valid_ranges, tickets, my_ticket):
    """
    Get a dictionary mapping field name to ticket column indices containing no
    invalid values for the field ranges.
    """
    tickets = np.array(tickets)
    candidates = {field: set(range(len(valid_ranges))) for field in valid_ranges}

    for field, valid_range in valid_ranges.items():
        for idx, col in enumerate(tickets.T):
            if not all(valid_value(valid_range, value) for value in col):
                candidates[field].remove(idx)

    return candidates


def valid_value(valid_range, value):
    """
    Check if a value is within one of the range pairs.
    """
    range_0, range_1 = valid_range
    return value in range_0 or value in range_1


def get_valid_tickets(valid_ranges, tickets):
    """
    Find the tickets containing plausible values.
    """
    return [ticket for ticket in tickets if valid_ticket(valid_ranges, ticket)]


def valid_ticket(valid_ranges, ticket):
    """
    Return false if any ticket value is outside of every range.
    """
    for value in ticket:
        if all(
            not valid_value(valid_range, value) for valid_range in valid_ranges.values()
        ):
            return False
    return True


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test2.txt")
    main("input.txt", 964373157673)
