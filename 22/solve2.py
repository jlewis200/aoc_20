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
    """ "
    Play a single round of the game.  Play a sub-game or terminate the round
    as appropriate.  Return true if player 1 wins.
    """
    card_1, card_2 = deck_1.pop(0), deck_2.pop(0)

    if len(deck_1) >= card_1 and len(deck_2) >= card_2:
        return inductive_case(deck_1, deck_2, card_1, card_2)

    else:
        return base_case(deck_1, deck_2, card_1, card_2)


def inductive_case(deck_1, deck_2, card_1, card_2):
    """
    The inductive case winner is determined by the winner of the subgame.
    """
    if play_game(deck_1[:card_1], deck_2[:card_2]):
        deck_1.extend((card_1, card_2))
        return True

    else:
        deck_2.extend((card_2, card_1))
        return False


def base_case(deck_1, deck_2, card_1, card_2):
    """
    The base case winner is determined from card value as in part 1.
    """
    if card_1 > card_2:
        deck_1.extend((card_1, card_2))
        return True

    else:
        deck_2.extend((card_2, card_1))
        return False


def play_game(deck_1, deck_2, states=None):
    """
    Return true if player 1 wins.
    """
    if states is None:
        states = set()

    while len(deck_1) > 0 and len(deck_2) > 0:
        # player 1 wins if duplicate state
        state = hash_state(deck_1, deck_2)
        if state in states:
            return True

        states.add(state)
        res = play_round(deck_1, deck_2)

    return res


def hash_state(deck_1, deck_2):
    """
    Get hash of deck states.
    """
    return hash((tuple(deck_1), tuple(deck_2)))


def score(deck):
    total = 0

    for idx, card in enumerate(deck[::-1], start=1):
        total += idx * card

    return total


def solve(deck_1, deck_2):

    if play_game(deck_1, deck_2):
        return score(deck_1)
    return score(deck_2)


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 291)
    main("test_infinite_loop.txt", 105)
    main("input.txt")
