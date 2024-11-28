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

    def trim(self):
        self.array = self.array[1:-1, 1:-1]


def solve(tiles):
    """
    Arrange the tiles and find roughness.
    """
    place_tiles(tiles)
    image = exctract_image(tiles)
    return get_roughness(image)


def get_roughness(image):
    """
    Sum the number of active pixels in the image and subtract the active
    monster pixels.
    """
    monster = get_monster()
    return image.sum() - (count_monsters(image, monster) * monster.sum())


def count_monsters(image, monster):
    """
    Enumerate the orientations until one or more monsters are found.  Return
    monster count.
    """
    for image in orientation_generator(image):
        n_monsters = convolve_monster(image, monster)

        if n_monsters > 0:
            return n_monsters


def convolve_monster(image, monster):
    """
    Find the number of monsters in the current image orientation.  Monsters
    are detected by performing a 2-d convolution between the monster and image.
    A monster is present when the value of the convolution is equal to the sum
    of pixels in the monster.
    """
    monster_pixel_count = monster.sum()
    n_monsters = 0

    for image_slice in image_slice_generator(image, monster.shape):
        n_matches = (image_slice * monster).sum()
        if n_matches == monster_pixel_count:
            n_monsters += 1

    return n_monsters


def get_monster():
    """
    Construct the monster as a 2-d array of 0 and 1.
    """
    monster = (
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    )
    monster = list(map(list, monster))
    monster = np.array(monster)
    monster[monster == " "] = 0
    monster[monster == "#"] = 1
    return monster.astype(int)


def exctract_image(tiles):
    """
    Extract image from the oriented tiles.
    """
    trim_tiles(tiles)
    tile = get_top_left(tiles)
    tiles = []

    while tile is not None:
        tile_ = tile

        while tile_.r is not None:
            tile_.r.array = np.hstack((tile_.array, tile_.r.array))
            tile_ = tile_.r

        tiles.append(tile_)
        tile = tile.d

    tile = np.vstack(tuple(tile.array for tile in tiles))
    tile[tile == "."] = 0
    tile[tile == "#"] = 1
    return tile.astype(int)


def trim_tiles(tiles):
    """
    Trim the boarder from the tiles.
    """
    for tile in tiles:
        tile.trim()


def get_top_left(tiles):
    """
    Return a reference to the top left tile.
    """
    for tile in tiles:
        if tile.u is None and tile.l is None:
            return tile


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
    for array in orientation_generator(tile.array):
        tile.array = array
        tile_placed = False

        # link as many oriented tiles as possible, return true if any match
        for oriented_tile in oriented_tiles:
            tile_placed |= link_tiles(oriented_tile, tile)

        if tile_placed:
            return True

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
        tile_0.l = tile_1
        tile_1.r = tile_0
        return True

    if (tile_0[:, -1] == tile_1[:, 0]).all():
        tile_0.r = tile_1
        tile_1.l = tile_0
        return True

    return False


def orientation_generator(image):
    """
    Generate each orientation of a numpy array.
    """
    for rotation in range(4):
        for flip in range(2):
            yield image

            image = np.fliplr(image)
        image = np.rot90(image)


def image_slice_generator(image, monster_shape):
    """
    Generate the slices of the image to perform a 2-d convolution.
    """
    for y in range(image.shape[0] - monster_shape[0] + 1):
        y_end = y + monster_shape[0]

        for x in range(image.shape[1] - monster_shape[1] + 1):
            x_end = x + monster_shape[1]

            yield image[y:y_end, x:x_end]


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
    main("test.txt", 273)
    main("input.txt")
