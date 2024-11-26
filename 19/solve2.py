#!/usr/bin/env python3

import re
from pprint import pprint


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def parse(data):
    rules_chunk, messages_chunk = data.split("\n\n")
    messages_chunk = messages_chunk.strip()

    rules = {}
    for rule in rules_chunk.split("\n"):
        match = re.fullmatch("(?P<rule_idx>\d+): (?P<remaining>.*)", rule)
        rule_idx = int(match.group("rule_idx"))
        remaining = match.group("remaining")

        if '"' not in remaining:
            rules[rule_idx] = []
            for branch in match.group("remaining").split("|"):
                rules[rule_idx].append(tuple(map(int, branch.split())))

        else:
            rules[rule_idx] = remaining.replace('"', "")

    messages = messages_chunk.split("\n")
    return rules, messages


def solve(rules, messages):
    """
    Consume each message according to rules.  If the result is empty, the entire
    message was consumed and the message is valid.  If characters remain, it is
    invalid.  If found to be None, the message could not be consumed.
    """
    valid = []

    for message in messages:
        if fully_consumed_message(consume_message(rules, [list(message)])):
            valid.append(message)

    return len(valid)


def consume_message(rules, messages, idx=0):
    """
    Recursively consume segments of a message until it is found to be
    unsatisfiable or no rules remain.
    """
    message_candidates = []

    # if the length of the incoming messages list is 0
    # the message has already been found to be invalid
    if len(messages) == 0:
        return []

    if isinstance(rules[idx], str):
        return base_case(rules[idx], messages)

    return inductive_case(rules, messages, idx)


def base_case(rule, messages):
    """
    Process the base case of a single character rule.
    """
    message_candidates = []

    # the messages need to be handled individually only in the base case
    for message in messages:
        if len(message) > 0 and rule == message[0]:
            message_candidates.append(message[1:])

    return message_candidates


def inductive_case(rules, messages, idx):
    """
    Attempt each rule branch.  If successful, return consumed messages.
    """
    message_candidates = []

    for rule_branch in rules[idx]:
        message_candidates.extend(attempt_branch(rules, messages.copy(), rule_branch))

    return message_candidates


def attempt_branch(rules, messages, rule_branch):
    """
    Attempt each sub-rule within a rule branch.

    For the rule below this function will be called twice:  once for '1 2 3'
    and again for '4 5 6'.

    0: 1 2 3 | 4 5 6
    """
    for idx in rule_branch:
        messages = consume_message(rules, messages, idx)
    return messages


def fully_consumed_message(messages):
    """
    A message has been fully consumed by some path through the rules if there
    are any messages of length 0 in the message candidate list.
    """
    zero_length_messages = (len(message) == 0 for message in messages)
    return any(zero_length_messages)


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 2)
    main("input.txt", 160)
    main("test2a.txt", 3)
    main("test2b.txt", 12)
    main("input2.txt", 357)
