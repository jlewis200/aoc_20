#!/usr/bin/env python3

import re


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
        consumed_message = consume_message(rules, list(message))
        if consumed_message is not None and len(consumed_message) == 0:
            valid.append(message)

    return len(valid)


def consume_message(rules, message, idx=0):
    """
    Recursively consume segments of a message until it is found to be
    unsatisfiable or no rules remain.
    """
    if message is None:
        return None

    if isinstance(rules[idx], str):
        return base_case(rules[idx], message)

    return inductive_case(rules, message, idx)


def base_case(rule, message):
    """
    Process the base case of a single character rule.
    """
    if rule == message[0]:
        return message[1:]


def inductive_case(rules, message, idx):
    """
    Attempt each rule branch.  If successful, return consumed message.
    """
    for rule_branch in rules[idx]:
        message_candidate = attempt_branch(rules, message.copy(), rule_branch)
        if message_candidate is not None:
            return message_candidate


def attempt_branch(rules, message, rule_branch):
    """
    Attempt each sub-rule within a rule branch.

    For the rule below this function will be called twice:  once for '1 2 3'
    and again for '4 5 6'.

    0: 1 2 3 | 4 5 6
    """
    for idx in rule_branch:
        message = consume_message(rules, message, idx)
    return message


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 2)
    main("input.txt", 160)
