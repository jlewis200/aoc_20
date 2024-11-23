#!/usr/bin/env python3

from re import search
import networkx as nx


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    edges = []

    for line in lines:
        pattern = "(?P<dst>.+) bags contain (?P<remaining>.+)"
        match = search(pattern, line)
        dst = match.group("dst")
        remaining = match.group("remaining")

        for src in remaining.split(","):
            match = search("(?P<count>\d+) (?P<src>.+) bag", src)

            if match is not None:
                src = match.group("src")
                count = match.group("count")
                edges.append((src, dst, {"count": count}))

    return edges


def solve(edges):
    graph = nx.DiGraph(edges)
    return len(nx.descendants(graph, "shiny gold"))


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 4)
    main("input.txt")
