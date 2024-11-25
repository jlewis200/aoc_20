#!/usr/bin/env python3

from re import search
import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    chunks = []

    for line in lines:
        match = search("mask = (?P<mask>[10X]+)", line)
        if match is not None:
            chunk = []
            chunks.append(chunk)
            mask = match.group("mask")
            mask = mask.replace("X", "2")
            mask = list(map(int, mask))
            chunk.append(mask)

        match = search("mem\[(?P<address>\d+)\] = (?P<value>\d+)", line)
        if match is not None:
            address = int(match.group("address"))
            address = list(map(int, f"{address:036b}"))
            chunk.append(
                (
                    address,
                    int(match.group("value")),
                )
            )

    return chunks


def solve(chunks):
    memory = {}

    for chunk in chunks:
        mask = chunk.pop(0)

        while len(chunk) > 0:
            address, value = chunk.pop(0)
            address = apply_mask(address, mask)
            write_memory(memory, address, value)

    return sum(memory.values())


def write_memory(memory, address, value):
    for address in generate_addresses(address):
        memory[str(address)] = value


def generate_addresses(address):
    addresses = [address]
    address_count = None

    while len(addresses) != address_count:
        address_count = len(addresses)
        addresses_ = []

        for address in addresses:

            try:
                idx = address.index(2)
                address_0 = address.copy()
                address_1 = address.copy()
                address_0[idx] = 0
                address_1[idx] = 1
                addresses_.append(address_0)
                addresses_.append(address_1)

            except ValueError:
                addresses_.append(address)

        addresses = addresses_

    return addresses


def apply_mask(address, mask):
    """
    If X is mapped to 2, the mask can be applied by taking max.

    Truth table:

    address  |  mask  |  masked-address
    ---------------------------------
       0     |   0    |        0
       0     |   1    |        1
       0     |   2    |        2
       1     |   0    |        1
       1     |   1    |        1
       1     |   2    |        2
    """
    masked_address = []

    for address_bit, mask_bit in zip(address, mask):
        masked_address.append(max(address_bit, mask_bit))

    return masked_address


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test2.txt", 208)
    main("input.txt")
