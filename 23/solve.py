#!/usr/bin/env python3

from collections import deque
import numpy as np


class Node:

    max_value = 0
    min_value = 2**32

    def __init__(self, value):
        self.l = self
        self.r = self
        self.value = int(value)
        Node.max_value = max(self.value, Node.max_value)
        Node.min_value = min(self.value, Node.min_value)

    def __repr__(self):
        r_string = f"{self.value}"

        node = self.r
        while node != self:
            r_string += f"{node.value}"
            node = node.r

        return r_string

    def unlink(self):
        """
        Unlink this section of 3 nodes.
        """
        inside_left = self
        inside_right = self.r.r

        outside_left = inside_left.l
        outside_right = inside_right.r

        outside_left.r = outside_right
        outside_right.l = outside_left

    def relink(self, outside_left):
        """
        Relink this section of 3 nodes to the right of outside_left.

        outside_left  <--> outside_right
        outside_left  <--> inside_left <--> center <--> inside_right <--> outside_right
        """
        outside_right = outside_left.r

        inside_left = self
        inside_right = self.r.r

        outside_left.r = inside_left
        inside_left.l = outside_left

        outside_right.l = inside_right
        inside_right.r = outside_right

    def append(self, other):
        """
        Treat self as the head of the list and append other to the end (left).
        """
        other.r = self
        other.l = self.l

        self.l.r = other
        self.l = other

    def __contains__(self, value):
        """
        Return true if value is equal to this node or it's two right neighbors.
        """
        return value == self.value or value == self.r.value or value == self.r.r.value


def initialize_nodes(sequence):
    """
    All of the values in sequence are contiguous and start near 0 so nodes can
    be a list that we use as a dictionary, but without the overhead of hashing
    the key.
    """
    sequence = deque(sequence)
    nodes = [None] * (len(sequence) + 2)
    root = Node(sequence.popleft())
    nodes[root.value] = root

    while len(sequence) > 0:
        node = Node(sequence.popleft())
        root.append(node)
        nodes[node.value] = node

    return nodes, root


def solve(sequence, rounds):
    nodes, node = initialize_nodes(sequence)

    for _ in range(rounds):
        node = perform_round(nodes, node)

    return str(nodes[1])[1:]


def perform_round(nodes, node):
    chunk = node.r
    chunk.unlink()
    chunk.relink(nodes[get_destination(node, chunk)])
    return node.r


def get_destination(node, chunk):
    destination = decrement(node.value, node)

    while destination in chunk:
        destination = decrement(destination, node)

    return destination


def decrement(value, node):
    value -= 1

    if value < node.min_value:
        value = node.max_value

    return value


def wrap(sequence, target):
    """
    Wrap the sequence until the target is at the head of the list.
    """
    while sequence[0] != target:
        sequence.append(sequence.pop(0))


if __name__ == "__main__":
    assert solve("389125467", 10) == "92658374"
    assert solve("389125467", 100) == "67384529"
    assert solve("193467258", 100) == "25468379"
    print(solve("193467258", 100))
    # assert solve("389125467", 10_000_000) == 149245887792
    # solve("193467258", 10_000_000)
