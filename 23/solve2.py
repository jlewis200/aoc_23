#!/usr/bin/env python3

import re
import numpy as np
import networkx as nx


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    """
    Parese board, replace slopes with level ground.
    """
    board = []
    for line in lines:
        board.append(list(line.strip()))
    board = np.pad(board, 1, constant_values="#")
    board[np.nonzero(np.isin(board, ("^", "v", "<", ">")))] = "."
    return board


def solve(board):
    """
    Build the graph and find max path length.
    """
    start = 1, np.argwhere(board[1] == ".")[0, 0]
    end = board.shape[0] - 2, np.argwhere(board[-2] == ".")[0, 0]
    graph = build_graph(board, start)
    return get_max_path_length(graph, start, end)


def build_graph(board, start):
    """
    Find intersections and path length between.
    """
    nodes = get_intersections(board, start)
    return nx.Graph(get_edges(board, nodes))


def get_max_path_length(graph, start, end):
    """
    Enumerate all paths and find maximal length.
    """
    max_path_length = 0

    for path in nx.all_simple_paths(graph, start, end):
        length = nx.path_weight(graph, path, "weight")
        if length > max_path_length:
            max_path_length = length

    return max_path_length


def get_adjacent(board, coord):
    """
    Get the next candidate coordinates, filter "#" squares.
    """
    x, y = coord
    adjacent = []
    for dx, dy in [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
    ]:
        next_coord = x + dx, y + dy
        if board[next_coord] in (".", "O"):
            adjacent.append(next_coord)
    return adjacent


def get_edges(board, nodes):
    """
    Find all edges between all nodes.
    """
    edges = []
    for node in nodes:
        edges.extend(get_node_edges(board.copy(), node))
    return edges


def get_node_edges(board, node):
    """
    Find all edges from this node/intersection to adjacent nodes.
    """
    board[node] = "#"
    edges = []

    for next_coord in get_adjacent(board, node):
        end, distance = follow_trail(board, next_coord)
        if end != next_coord:
            edges.append((node, end, {"weight": distance}))

    return edges


def get_intersections(board, start):
    """
    Find the coordinates of all intersections.
    """
    intersections = []
    queue = [start]

    while len(queue) > 0:
        start = queue.pop(0)
        if board[start] == "O":
            continue

        board[start] = "O"
        next_coords = get_adjacent(board, start)
        queue.extend(next_coords)

        if len(next_coords) > 2:
            intersections.append(start)

    return intersections


def follow_trail(board, start):
    """
    Follow trail until an intersection is reached, return endpoint and distance
    travelled.
    """
    step = 0
    next_coords = [start]

    while len(next_coords) == 1:
        start = next_coords.pop(0)
        board[start] = "#"
        next_coords.extend(get_adjacent(board, start))
        step += 1

    return start, step


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 154)
    main("input.txt")
