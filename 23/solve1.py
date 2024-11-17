#!/usr/bin/env python3

import re
import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    board = []
    for line in lines:
        board.append(list(line.strip()))
    return np.array(board)


def solve(board):
    board = np.pad(board, 1, constant_values="#")
    start = 1, np.argwhere(board[1] == ".")[0, 0]
    end = board.shape[0] - 2, np.argwhere(board[-2] == ".")[0, 0]

    segments = []
    dfs(board, start, end, segments)
    return max(segments)


def follow_trail(board, start):
    """
    Follow a trail until an intersection is reached.
    """
    distance = 0
    next_coords = get_adjacent(board, start)
    while len(next_coords) == 1:
        start = next_coords.pop()
        board[start] = "#"
        distance += 1
        next_coords = get_adjacent(board, start)
    return start, distance


def dfs(board, start, end, segments, step=0):
    """
    DFS but collapse trails between intersections.
    """
    board = board.copy()  # copy as a means to enumerate different paths

    start, distance = follow_trail(board, start)
    step += distance

    if start == end:
        segments.append(step)
        return

    for next_coord in get_adjacent(board, start):
        dfs(board, next_coord, end, segments, step + 1)


def get_adjacent(board, coord):
    """
    Get adjacent candidates, filter based on direction/walls.
    """
    next_coords = []
    for (dx, dy), direction in [
        ((0, 1), ">"),
        ((0, -1), "<"),
        ((1, 0), "v"),
        ((-1, 0), "^"),
    ]:
        x, y = coord
        next_coord = x + dx, y + dy
        if board[next_coord] == "." or board[next_coord] == direction:
            next_coords.append(next_coord)
    return next_coords


def main(filename, expected):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 94)
    main("input.txt")
