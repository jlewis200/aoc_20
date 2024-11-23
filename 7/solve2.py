#!/usr/bin/env python3

from re import search
import networkx as nx


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    edges = []

    for line in lines:
        pattern = "(?P<src>.+) bags contain (?P<remaining>.+)"
        match = search(pattern, line)
        src = match.group("src")
        remaining = match.group("remaining")

        for dst in remaining.split(","):
            match = search("(?P<count>\d+) (?P<dst>.+) bag", dst)

            if match is not None:
                dst = match.group("dst")
                count = int(match.group("count"))
                edges.append((src, dst, {"count": count}))

    return edges


def solve(edges):
    graph = nx.DiGraph(edges)
    return count_children(graph, "shiny gold")


def count_children(graph, node):
    """
    Recursively count child nodes.
    """
    n_children = 0

    for src, dst, data in graph.edges(node, data=True):
        child_count = data["count"]
        n_children += child_count
        n_children += child_count * count_children(graph, dst)

    return n_children


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 32)
    main("test2.txt", 126)
    main("input.txt")
