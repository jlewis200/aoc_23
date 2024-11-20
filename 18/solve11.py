#!/usr/bin/env python3

import re
import itertools
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
    """
    Vertical points to test for interior location defined by:
    - endpoints of vertical sections
    - vertical interval of endpoint min + 1 and max - 1
    - intervals must be split into smallest chunks in case of overlap
    - intervals can't contain any of the individual endpoints

    Each individual endpoint must be tested for interiority:
    - if it lies on an active horizontal interval
    - if it has an odd number horizontal intervals above/below

    Each interval must be tested for interiority
    - if it has an odd number horizontal intervals above/below

    The vertical intervals should not overlap with a horizontal interval if chunked.

    That almost worked, but there are edge cases where a point may have an odd number
    of intervals above and even below (or vice versa) when a corner occurrs ata the
    same x coord.  An example is (1, 1) in the sample input:  1 above, 4 below.

    The core idea here is to find the points of inflection along the x and y
    axes, and build a variable sized grid from these points.  The very large
    distances of part 2 can be compressed between these points and represented
    as an easy to calculate rectangular area.  From there a regular bfs to
    determine interior/exterior points can be used.  The key to this approach
    is the compression of the large distances.
    """
    
    # collect the endpoints of the vertical and horizontal segments
    vertical_intervals = []
    horizontal_intervals = []
    y, x = 0, 0

    direction_map = {
        "0": "R",
        "1": "D",
        "2": "L",
        "3": "U",
    }

    for direction, dist, color in instructions:

        dist_dir = re.search("[0-9a-fA-F]+", color).group()
        direction = direction_map[dist_dir[-1]]
        dist = int(dist_dir[:-1], base=0x10)

        if direction == "U":
            vertical_intervals.append((x, y, y - dist))
            y -= dist

        elif direction == "D":
            vertical_intervals.append((x, y, y + dist))
            y += dist

        elif direction == "L":
            horizontal_intervals.append((y, x, x - dist))
            x -= dist

        elif direction == "R":
            horizontal_intervals.append((y, x, x + dist))
            x += dist

    vertical_intervals = sort_coords(vertical_intervals)
    horizontal_intervals = sort_coords(horizontal_intervals)

    
    testable_x = get_testable(horizontal_intervals)
    testable_x, sizes_x = get_ranges(testable_x)

    testable_y = get_testable(vertical_intervals)
    testable_y, sizes_y = get_ranges(testable_y)

    map_x = {coord: idx for idx, coord in enumerate(testable_x)}
    map_y = {coord: idx for idx, coord in enumerate(testable_y)}

    board = np.full(
        (len(testable_x) + 2, len(testable_y) + 2),
        None,
    )

    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            board[x, y] = {
                "reachable": True,
                "border": False,
            }

    for x in testable_x:
        for y in testable_y:
            board[map_x[x], map_y[y]] = {
                "width": sizes_x[x],
                "height": sizes_y[y],
                "area": sizes_x[x] * sizes_y[y],
                "reachable": True,
                "border": False,
            }

    idx, jdx = testable_x.index(0), testable_y.index(0)
    x, y = 0, 0


    for direction, dist, color in instructions:

        dist_dir = re.search("[0-9a-fA-F]+", color).group()
        direction = direction_map[dist_dir[-1]]
        dist = int(dist_dir[:-1], base=0x10)

        if direction == "U":
            y_stop = y - dist
            while y != y_stop:
                jdx -= 1
                y -= board[idx, jdx]["height"]
                board[idx, jdx]["border"] = True

        elif direction == "D":
            y_stop = y + dist
            while y != y_stop:
                jdx += 1
                y += board[idx, jdx]["height"]
                board[idx, jdx]["border"] = True

        elif direction == "L":
            x_stop = x - dist
            while x != x_stop:
                idx -= 1
                x -= board[idx, jdx]["width"]
                board[idx, jdx]["border"] = True

        elif direction == "R":
            x_stop = x + dist
            while x != x_stop:
                idx += 1
                x += board[idx, jdx]["width"]
                board[idx, jdx]["border"] = True

    board = np.roll(board, 1, axis=0)
    board = np.roll(board, 1, axis=1)

    queue = [(0, 0)]
    while len(queue) > 0:
        pos = queue.pop(0)
        try:
            if not board[pos]["border"] and board[pos]["reachable"]:
                board[pos]["reachable"] = False
                queue.append((pos[0] - 1, pos[1]))
                queue.append((pos[0] + 1, pos[1]))
                queue.append((pos[0], pos[1] - 1))
                queue.append((pos[0], pos[1] + 1))
        except:
            pass

    print_board(board)
    area = 0
    for element in board.flatten():
        if element["reachable"]:
            area += element["area"]
    print(area)
    breakpoint()


def print_board(board):
    for idx in range(board.shape[1]):
        for jdx in range(board.shape[0]):
            char = " "
            if board[jdx, idx]["border"]:
                char = "#"
            elif not board[jdx, idx]["reachable"]:
                char = "-"

            print(char, end="")
        print()
    print()


def get_testable(intervals):
    testable = set()
    for interval in intervals:
        testable.add(interval[1])
        testable.add(interval[2])
    return sorted(list(testable))


def get_ranges(testable):
    """
    Testing one point in the range is sufficient due to the chunking, but the
    size of the range is still required.  Individual endpoints are considered
    to be a range of size 1.
    """
    sizes = {point: 1 for point in testable}
    range_points = []
    for start, end in np.lib.stride_tricks.sliding_window_view(testable, 2):
        range_point = start + 1
        range_size = end - range_point

        # this accounts for a a U with an edge of length 2 by not clobbering endpoint sizes
        if range_size > 0:
            range_points.append(range_point)
            sizes[range_point] = range_size

    testable.extend(range_points)
    return sorted(list(set(testable))), sizes


def sort_coords(intervals):
    return [(a, min(b, c), max(b, c)) for a, b, c in intervals]


def main(filename="input.txt"):
    print(dig(parse(read_file(filename))))


if __name__ == "__main__":
    main("test.txt")
    main()
