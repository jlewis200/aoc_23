#!/usr/bin/env python3

import re
import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    directions = []
    for line in lines:
        direction, dist, color = re.match("([A-Z]) (\d+) (.+)", line).groups()
        directions.append((direction, int(dist), color))
    return directions


def dig(instructions):
    idx, jdx = 0, 0
    coords = []
    for direction, dist, color in instructions:
        if direction == "U":
            while dist > 0:
                dist -= 1
                idx -= 1
                coords.append((idx, jdx))
        elif direction == "D":
            while dist > 0:
                dist -= 1
                idx += 1
                coords.append((idx, jdx))
        elif direction == "L":
            while dist > 0:
                dist -= 1
                jdx -= 1
                coords.append((idx, jdx))
        elif direction == "R":
            while dist > 0:
                dist -= 1
                jdx += 1
                coords.append((idx, jdx))

    coords = np.array(coords)
    board = np.full(
        (
            coords[:, 0].max() - coords[:, 0].min() + 1,
            coords[:, 1].max() - coords[:, 1].min() + 1,
        ),
        ".",
    )
    board[coords[:, 0], coords[:, 1]] = "#"
    board = np.roll(board, -coords[:, 0].min(), axis=0)
    board = np.roll(board, -coords[:, 1].min(), axis=1)

    board = np.pad(board, 1, constant_values=".")

    board = fill(board)
    return (board != " ").sum()


def fill(board):
    queue = [(0, 0)]
    while len(queue) > 0:
        pos = queue.pop(0)
        if board[pos] == ".":
            board[pos] = " "
            queue.append((pos[0] - 1, pos[1]))
            queue.append((pos[0] + 1, pos[1]))
            queue.append((pos[0], pos[1] - 1))
            queue.append((pos[0], pos[1] + 1))
    return board


def main(filename="input.txt"):
    print(dig(parse(read_file(filename))))


if __name__ == "__main__":
    main("test.txt")
    main("test2.txt")
    main("test3.txt")
    main()
