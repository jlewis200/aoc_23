#!/usr/bin/env python3

import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    board = []
    for line in lines:
        board.append(list(line.strip()))
    return np.array(board)


def get_reachable(distances, steps):
    """
    Get the number of reachable squares.
    """
    if steps % 2 == 0:
        return distances[
            (distances >= 0) & (distances <= steps) & (distances % 2 == 0)
        ].shape[0]

    return distances[
        (distances >= 0) & (distances <= steps) & ((distances + 1) % 2 == 0)
    ].shape[0]


def get_distances(board, start, start_val):
    """
    Get the distances from start_val to each square on the board.
    """
    x, y = start
    distances = np.full_like(board, -1, dtype=int)
    distances[x, y] = start_val
    bfs(board, distances, (x, y))
    return distances


def bfs(board, distances, start):
    queue = [start]

    while len(queue) > 0:
        x, y = queue.pop(0)
        distance = distances[x, y]

        for x, y in [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]:
            if (
                x in range(board.shape[1])
                and y in range(board.shape[0])
                and board[x, y] == "."
                and distances[x, y] == -1
            ):
                distances[x, y] = distance + 1
                queue.append((x, y))


def solve(board, steps):
    x, y = np.argwhere(board == "S")[0]
    board[x, y] = "."
    distances = get_distances(board, (board.shape[0] // 2, board.shape[1] // 2), 0)
    return get_reachable(distances, steps)

    # divide into equal-sized chunks
    chunks = get_chunks(distances, distances.shape[0] // n_repeat)
    assert_repeating(chunks)

    rc = get_reachable_chunks(chunks, steps)
    pattern = rc[center, center - 1 : center + 1]


def main(filename, steps, expected=None):
    result = solve(parse(read_file(filename)), steps)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 6)
    main("input.txt", 64)
