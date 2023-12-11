#!/usr/bin/env python3

import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_universe(lines):
    return np.array([list(line.strip()) for line in lines])


def universe_str(universe):
    return "\n".join("".join(row) for row in universe)


def expand_vertical(universe, expansion, coords):
    empty_rows = np.argwhere((universe == "#").sum(axis=1) == 0).flatten()
    for empty_row in empty_rows[::-1]:
        for coord in coords:
            if coord[0] > empty_row:
                coord[0] += expansion


def expand_horizontal(universe, expansion, coords):
    empty_cols = np.argwhere((universe == "#").sum(axis=0) == 0).flatten()
    for empty_col in empty_cols[::-1]:
        for coord in coords:
            if coord[1] > empty_col:
                coord[1] += expansion


def get_distances(galaxy_coords):
    distances = []
    for idx, coord_0 in enumerate(galaxy_coords[:-1], start=1):
        for coord_1 in galaxy_coords[idx:]:
            distances.append(get_distance(coord_0, coord_1))
    return distances


def get_distance(coord_0, coord_1):
    return abs(coord_1[0] - coord_0[0]) + abs(coord_1[1] - coord_0[1])


def get_coords(universe, expansion=1):
    coords = list(map(list, np.argwhere(universe == "#")))
    expand_horizontal(universe, expansion, coords)
    expand_vertical(universe, expansion, coords)
    return coords


def main(filename="input.txt"):
    universe = parse_universe(read_file(filename))
    print(f"expansion 1:  {sum(get_distances(get_coords(universe)))}")
    print(f"expansion 10:  {sum(get_distances(get_coords(universe, 9)))}")
    print(f"expansion 100:  {sum(get_distances(get_coords(universe, 99)))}")
    print(f"expansion 1000000:  {sum(get_distances(get_coords(universe, 999999)))}")


if __name__ == "__main__":
    main("test.txt")
    main()
