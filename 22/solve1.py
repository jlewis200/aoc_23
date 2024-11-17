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
    coords = sort_block_endpoints(coords)
    coords = sort_blocks(coords)
    coords = lower(coords)
    block_map = get_block_map(coords)
    graph = build_graph(coords, block_map)
    return len(get_removable(graph))


def get_block_map(coords):
    """
    Create a 3 dimensional array of the blocks.  Represent each block by filling
    the array with a unique index indicating the locations each block occupies.
    Begin index at 1.
    """
    coord_max = coords.max()
    block = np.zeros((coords.max(),) * 3, dtype=int)

    for idx, (src, dst) in enumerate(coords, start=1):
        x_min, x_max, y_min, y_max, z_min, z_max = get_coords(src, dst)
        block[x_min:x_max, y_min:y_max, z_min:z_max] = idx

    return block


def build_graph(coords, block):
    """
    Build a directed graph where an edge from src to dst indicates dst supports
    src.
    """
    graph = nx.DiGraph()

    for idx, (src, dst) in enumerate(coords, start=1):
        x_min, x_max, y_min, y_max, z_min, z_max = get_coords(src, dst)
        supports = np.unique(block[x_min:x_max, y_min:y_max, z_min - 1])

        for support in supports:
            graph.add_edge(idx, support)

    return graph


def get_removable(graph):
    """
    Find the removable blocks.
    """
    graph.remove_node(0)  # remove ground as a supporting node
    return {node for node in graph.nodes if is_removable(graph, node)}


def is_removable(graph, node):
    """
    A block is removable if:
    - it doesn't support another block
    - every supported block has another support
    """
    all_supported = True
    for predecessor in graph.predecessors(node):
        if len(list(graph.successors(predecessor))) < 2:
            all_supported = False
    return all_supported


def get_coords(src, dst):
    """
    Extract coordinates from source and destination.
    """
    x_min, x_max = min(src[0], dst[0]), max(src[0], dst[0]) + 1
    y_min, y_max = min(src[1], dst[1]), max(src[1], dst[1]) + 1
    z_min, z_max = min(src[2], dst[2]), max(src[2], dst[2]) + 1
    return x_min, x_max, y_min, y_max, z_min, z_max


def lower(coords):
    """
    Lower the blocks to ground/supporting-blocks.
    """
    coord_max = coords.max()
    height = np.zeros((coord_max, coord_max), dtype=int)
    lowered_coords = []
    for src, dst in coords:
        src, dst = lower_block(height, src, dst)
        lowered_coords.append((src, dst))
    return np.array(lowered_coords)


def lower_block(height, src, dst):
    """
    Find the hight of highest existing lower block, add 1, annotate new max on
    the height max.
    """
    x_min, x_max = min(src[0], dst[0]), max(src[0], dst[0]) + 1
    y_min, y_max = min(src[1], dst[1]), max(src[1], dst[1]) + 1
    z_min = height[x_min:x_max, y_min:y_max].max() + 1
    z_diff = src[2] - z_min
    src -= np.array([0, 0, z_diff])
    dst -= np.array([0, 0, z_diff])
    height[x_min:x_max, y_min:y_max] = z_min + (dst[2] - src[2])
    return src, dst


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
    main("test.txt", 5)
    main("input.txt", 424)
