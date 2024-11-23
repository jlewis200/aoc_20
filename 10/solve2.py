#!/usr/bin/env python3

import numpy as np
import networkx as nx


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    return list(map(int, lines))


def solve(numbers):
    """
    The joltage adapters only accept lower, so the only possible arragement is
    ascending.

    The number of paths through a node is equal to the sum of paths through
    it's predecessors.  Because this is a DAG, using a topological sort ensures
    the predecessors are completed before the ancestors.
    """
    numbers.append(0)
    numbers.append(max(numbers) + 3)
    graph = nx.DiGraph(get_edges(numbers))

    for node in numbers:
        graph.nodes[node]["paths"] = 0

    graph.nodes[0]["paths"] = 1

    for src in sorted(numbers):  # topological sort
        for dst in nx.neighbors(graph, src):
            graph.nodes[dst]["paths"] += graph.nodes[src]["paths"]

    return graph.nodes[max(numbers)]["paths"]


def get_edges(numbers):
    edges = []
    numbers = np.array(numbers)

    for src in numbers:
        differences = numbers - src
        dst_idxs = (differences >= 1) & (differences <= 3)
        dsts = numbers[dst_idxs]
        edges.extend((src, dst) for dst in dsts)

    return edges


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 8)
    main("test2.txt", 19208)
    main("input.txt")
