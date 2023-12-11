#!/usr/bin/env python3

import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_universe(lines):
    return np.array([list(line.strip()) for line in lines])


def universe_str(universe):
    return "\n".join("".join(row) for row in universe)


def expand_universe(universe):
    universe = expand_vertical(universe)
    universe = expand_horizontal(universe)
    return universe


def expand_vertical(universe):
    rows = []
    for row in universe:
        rows.append(row)
        if (row == "#").sum() == 0:
            rows.append(row)
    return np.array(rows)            


def expand_horizontal(universe):
    return expand_vertical(universe.T).T


def get_distances(universe):
    distances = []
    galaxy_coords = list(map(tuple, np.argwhere(universe == "#")))
    for idx, coord_0 in enumerate(galaxy_coords[:-1], start=1):
        for coord_1 in galaxy_coords[idx:]:
            distances.append(get_distance(coord_0, coord_1))
    return distances


def get_distance(coord_0, coord_1):
    return abs(coord_1[0] - coord_0[0]) + abs(coord_1[1] - coord_0[1])


def main(filename="input.txt"):
    universe = parse_universe(read_file(filename))
    universe = expand_universe(universe)
    print(f"part 1:  {sum(get_distances(universe))}")
    print(f"part 2:  {None}")


if __name__ == "__main__":
    main("test.txt")
    main()
