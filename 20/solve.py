#!/usr/bin/env python3

from re import fullmatch
import numpy as np


class Tile:

    def __init__(self, data, tile_id):
        self.array = np.array(data)
        self.tile_id = tile_id
        self.u = None
        self.d = None
        self.l = None
        self.r = None

    def __repr__(self):
        return (
            f"tile_id: {self.tile_id}\n"
            f"u: {self._get_neighbor_id(self.u)}\n"
            f"d: {self._get_neighbor_id(self.d)}\n"
            f"l: {self._get_neighbor_id(self.l)}\n"
            f"r: {self._get_neighbor_id(self.r)}\n"
            f"{self._array_string()}"
        )

    def __getitem__(self, key):
        return self.array[key]

    @staticmethod
    def _get_neighbor_id(neighbor):
        return neighbor.tile_id if neighbor is not None else None

    def _array_string(self):
        return "\n".join("".join(row) for row in self.array)

    def flip(self):
        self.array = np.fliplr(self.array)

    def rotate(self):
        self.array = np.rot90(self.array)

    def adjacency_count(self):
        return sum(
            (
                self.u is not None,
                self.d is not None,
                self.l is not None,
                self.r is not None,
            )
        )


def solve(tiles):
    """
    Arrange the tiles and find product of corner ids.
    """
    place_tiles(tiles)
    product = 1

    for tile in tiles:
        if tile.adjacency_count() == 2:
            product *= tile.tile_id

    return product


def place_tiles(tiles):
    """
    Place each tile.  Once a tile is placed, it's orientation is not changed,
    only the tiles which have not been placed yet are re-orineted.
    """
    tiles = tiles.copy()
    oriented_tiles = {tiles.pop(0)}

    while len(tiles) > 0:
        tile = tiles.pop(0)

        if place_tile(oriented_tiles, tile):
            oriented_tiles.add(tile)

        else:
            tiles.append(tile)


def place_tile(oriented_tiles, tile):
    """
    Try finding a shared edge between tile and the oriented tiles.  If a
    shared edge is found, link both tiles to each other.  Return true if at
    least one shared edge was found.  If no shared edges were found, flip or
    rotate and try again.  Return false if no orientation has a shared edge.
    This would be the case if no adjacent tile has been oriented yet.
    """
    for rotation in range(4):
        for flip in range(2):
            tile_placed = False

            # link as many oriented tiles as possible, return true if any match
            for oriented_tile in oriented_tiles:
                tile_placed |= link_tiles(oriented_tile, tile)

            if tile_placed:
                return True

            tile.flip()
        tile.rotate()

    return False


def link_tiles(tile_0, tile_1):
    """
    Link tiles if an edge matches.  Two tiles can only be linked once, and this
    assumes the first matching edge is the only possible orientation that will
    match.  That may not be the case, but multiple orientation possibilities
    will be solved with backtracking through recursion if that becomes a
    problem.
    """
    if (tile_0[0] == tile_1[-1]).all():
        tile_0.u = tile_1
        tile_1.d = tile_0
        return True

    if (tile_0[-1] == tile_1[0]).all():
        tile_0.d = tile_1
        tile_1.u = tile_0
        return True

    if (tile_0[:, 0] == tile_1[:, -1]).all():
        tile_0.r = tile_1
        tile_1.l = tile_0
        return True

    if (tile_0[:, -1] == tile_1[:, 0]).all():
        tile_0.l = tile_1
        tile_1.r = tile_0
        return True

    return False


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def parse(data):
    tiles = []

    for tile in data.strip().split("\n\n"):
        lines = tile.split("\n")
        match = fullmatch("Tile (?P<tile_id>\d+):", lines.pop(0))
        tile_id = int(match.group("tile_id"))
        tiles.append(
            Tile(
                [list(line.strip()) for line in lines],
                tile_id,
            )
        )

    return tiles


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 20899048083289)
    main("input.txt")
