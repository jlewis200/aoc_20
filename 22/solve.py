#!/usr/bin/env python3

import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def parse(data):
    return list(map(parse_deck, data.split("\n\n")))


def parse_deck(deck):
    return list(map(int, deck.strip().split("\n")[1:]))


def play_round(deck_1, deck_2):
    card_1, card_2 = deck_1.pop(0), deck_2.pop(0)

    if card_1 > card_2:
        deck_1.extend((card_1, card_2))

    else:
        deck_2.extend((card_2, card_1))


def score(deck):
    total = 0

    for idx, card in enumerate(deck[::-1], start=1):
        total += idx * card

    return total


def solve(deck_1, deck_2):
    while len(deck_1) > 0 and len(deck_2) > 0:
        play_round(deck_1, deck_2)

    deck_1.extend(deck_2)
    return score(deck_1)


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 306)
    main("input.txt")
