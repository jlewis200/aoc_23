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


def solve(board, steps):
    """
    Eventually the patterns stabilize into left/right/up/down and 4 corners,
    both in terms of number of reachable and number of steps to reach a given
    square within a tile.  The patterns are dependent on the direction of
    travel, so the leftward repeating pattern is different that the rightward
    pattern, although the total number of reachable remains the same.

    The internal area of the checkerboard pattern can be calculated by

     internal area:
        y = y distance of last full tile from center
        a = reachable in central tile
        b = reachable in off-center tile

        internal_area = (y + 1)**2 * a + y**2 * b


    [[   0    0    0    0    0    0    0    0    0    0    0]
     [   0    0    0    0    0  807    0    0    0    0    0]
     [   0    0    0    0 2567 7112 2548    0    0    0    0]
     [   0    0    0 2567 7231 7451 7225 2548    0    0    0]
     [   0    0 2567 7231 7451 7344 7451 7225 2548    0    0]
     [   0  811 7123 7451 7344 7451 7344 7451 7106  793    0]
     [   0    0 2540 7236 7451 7344 7451 7225 2555    0    0]
     [   0    0    0 2540 7236 7451 7225 2555    0    0    0]
     [   0    0    0    0 2540 7117 2555    0    0    0    0]
     [   0    0    0    0    0  797    0    0    0    0    0]
     [   0    0    0    0    0    0    0    0    0    0    0]]


    The total number of steps mod the board size gives number of tiles in a single
    direction which can then be used as a shortcut to find the measurement y.

    The edge area can be calculated separately by multiplying the number of
    reachable by manhattan distance from center.

    Also needed are the up/down/left/right sections.
    """

    x, y = np.argwhere(board == "S")[0]
    board[x, y] = "."
    n_repeat = 13
    center = n_repeat // 2
    step = board.shape[0]
    board = np.tile(board, (n_repeat, n_repeat)).copy()
    distances = get_distances(board, (board.shape[0] // 2, board.shape[1] // 2), 0)

    # divide into equal-sized chunks
    chunks = get_chunks(distances, distances.shape[0] // n_repeat)
    assert_repeating(chunks)

    rc = get_reachable_chunks(chunks, steps)
    pattern = rc[center, center - 1 : center + 1]

    chunks, y = get_end_chunk(chunks, step, steps)
    rc = get_reachable_chunks(chunks, steps)

    # get the internal area of repeating checkerboard pattern
    a = pattern[1]
    b = pattern[0]
    total = ((y + 1) ** 2 * a) + (y**2 * b)

    # zero out central area, add up/down left/right
    rc[center, center] = 0
    total += rc[center].sum()
    total += rc[:, center].sum()

    # add corner areas
    total += get_corner_area(rc[center + 1, : center + 1 :][::-1], y)
    total += get_corner_area(rc[center - 1, center:], y)
    total += get_corner_area(rc[center + 1, center:], y)
    total += get_corner_area(rc[center - 1, : center + 1 :][::-1], y)
    return total


def get_corner_area(queue, y):
    """
    Calculate the area of a corner.
    """
    total = 0
    queue = queue.tolist()
    while len(queue) > 0:
        total += y * queue.pop(0)
        y += 1
    return total


def get_reachable_chunks(chunks, steps):
    """
    Get the number of reachable squares for each chunk as a 2-d array.
    """
    reachable_chunks = []

    for y in range(chunks.shape[1]):
        row = []
        for x in range(chunks.shape[0]):
            row.append(get_reachable(chunks[x, y], steps))
        reachable_chunks.append(row)

    return np.array(reachable_chunks)


def get_end_chunk(chunk, delta, steps):
    """
    The number of repeats must be a multiple of two to ensure proper tiling.

    An arbitrary offset of 4 is chosen to ensure the edges vary between 0 and
    the repeating pattern.
    """
    zero_mask = chunk == -1
    repeats = (steps) // delta
    repeats -= repeats % 2
    repeats -= 4
    end_chunk = chunk + (repeats * delta)
    end_chunk[zero_mask] = -1
    return end_chunk, repeats


def get_chunks(distances, step):
    """
    Split a tiled distances array into a  4-d chunked distances array.
    """
    chunks = []

    for y in range(0, distances.shape[1], step):
        row = []
        for x in range(0, distances.shape[0], step):
            row.append(distances[x : x + step, y : y + step])
        chunks.append(row)

    return np.array(chunks)


def assert_repeating(chunks):
    """
    Assert we have reached a stable repeating pattern.
    """
    chunks = normalize_chunks(chunks.copy())
    center = chunks.shape[0] // 2

    assert (chunks[0, 0] == chunks[0, center - 1]).all()  # top left section
    assert (chunks[0, -1] == chunks[0, center + 1]).all()  # bottom left section
    assert (chunks[-1, 0] == chunks[-1, center - 1]).all()  # top left section
    assert (chunks[-1, -1] == chunks[-1, center + 1]).all()  # bottom right section

    assert (chunks[center, 0] == chunks[center, 1]).all()  # central top
    assert (chunks[center, -1] == chunks[center, -2]).all()  # central bottom
    assert (chunks[0, center] == chunks[1, center]).all()  # central left
    assert (chunks[-1, center] == chunks[-2, center]).all()  # central right


def normalize_chunks(chunks):
    """
    Normalize each chunk of a tiled distances array.
    """
    normalized = []

    for y in range(chunks.shape[1]):
        row = []
        for x in range(chunks.shape[0]):
            row.append(normalize(chunks[x, y]))
        normalized.append(row)

    return np.array(normalized)


def normalize(chunk):
    """
    Normalize the distances towards 0.
    """
    non_negative = chunk >= 0
    min_val = chunk[non_negative].min()
    chunk[non_negative] -= min_val
    return chunk


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


def main(filename, steps, expected=None):
    result = solve(parse(read_file(filename)), steps)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 100, 6536)
    main("test.txt", 500, 167004)
    main("test.txt", 1000, 668697)
    main("test.txt", 5000, 16733044)
    main("input.txt", 26501365, 605492675373144)
