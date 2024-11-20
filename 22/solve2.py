#!/usr/bin/env python3

import re
import numpy as np
import networkx as nx


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    segments = []
    for line in lines:
        coords = re.split("[,~]", line.strip())
        x0, y0, z0, x1, y1, z1 = map(int, coords)
        segments.append(((x0, y0, z0), (x1, y1, z1)))
    return np.array(segments)


def solve(coords):
    """
    Sum number of blocks moved if each block is destroyed individually.
    """
    coords, _ = lower(coords)
    n_moved = 0

    for idx in range(len(coords)):
        n_moved += lower(coords[:idx].tolist() + coords[idx + 1 :].tolist())[1]

    return n_moved


def get_coords(src, dst):
    """
    Extract sorted coordinates from source and destination.
    """
    x_min, x_max = min(src[0], dst[0]), max(src[0], dst[0]) + 1
    y_min, y_max = min(src[1], dst[1]), max(src[1], dst[1]) + 1
    z_min, z_max = min(src[2], dst[2]), max(src[2], dst[2]) + 1
    return x_min, x_max, y_min, y_max, z_min, z_max


def lower(coords):
    """
    Lower the blocks.  Count number of blocks moved.
    """
    coords = sort_block_endpoints(coords)
    coords = sort_blocks(coords)
    coord_max = coords.max()

    height = np.zeros((coord_max, coord_max), dtype=int)

    n_moved = 0
    coords_ = []
    for src, dst in coords:
        x_min, x_max = min(src[0], dst[0]), max(src[0], dst[0]) + 1
        y_min, y_max = min(src[1], dst[1]), max(src[1], dst[1]) + 1
        z_min = height[x_min:x_max, y_min:y_max].max() + 1
        z_diff = src[2] - z_min

        src_ = src - np.array([0, 0, z_diff])
        dst_ = dst - np.array([0, 0, z_diff])
        coords_.append((src_, dst_))

        height[x_min:x_max, y_min:y_max] = z_min + (dst[2] - src[2])

        if (src != src_).any():
            n_moved += 1

    return np.array(coords_), n_moved


def sort_blocks(coords):
    """
    Sort blocks by lowest z-axis.
    """
    key = lambda x: x[0, 2]
    return np.array(sorted(coords, key=key))


def sort_block_endpoints(coords):
    """
    Sort each block's start/end coords by z-axis.  This ensures the top/bottom
    are in predictable locations:  smaller at index 0.
    """
    sorted_coords = []
    for src, dst in coords:
        if src[-1] > dst[-1]:
            src, dst = dst, src
        sorted_coords.append((src, dst))
    return np.array(sorted_coords)


def main(filename, expected=None):
    """
    Solve and check expected value if provided.
    """
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 7)
    main("input.txt", 55483)
