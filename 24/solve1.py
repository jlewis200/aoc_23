#!/usr/bin/env python3

import re


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):

    pairs = []

    for line in lines:
        x0, y0, z0, x1, y1, z1 = map(int, re.split("[,@]", line))
        pairs.append(((x0, y0, z0), (x1, y1, z1)))

    return pairs


def solve(coords, min_val, max_val):
    """
    Check for pairwise crosses.
    """
    crosses = 0
    for idx, ball_0 in enumerate(coords, start=1):
        for ball_1 in coords[idx:]:
            x, y = get_intersection(ball_0, ball_1)
            if x is None or y is None:
                continue
            if within_range(x, y, min_val, max_val):
                crosses += 1
    return crosses


def within_range(x, y, min_val, max_val):
    """
    Check if a crossing occurs within the "box."
    """
    return x >= min_val and x <= max_val and y >= min_val and y <= max_val


def get_future(ball, t):
    """
    Find future position of a snowball at time t.
    """
    (x, y, z), (vx, vy, vz) = ball
    return x + vx * t, y + vy * t


def get_intersection(ball_0, ball_1):
    """
    If two paths cross, it means the snowballs occupied the same location, but
    at possibly different times.  Solve for the times first, and then
    extrapolate what the position would be for a ball at that time.  If either
    has negative time, it is not counted.  If the denominator is zero, this
    indicates the paths are parallel.
    """
    (x_0, y_0, z_0), (vx_0, vy_0, vz_0) = ball_0
    (x_1, y_1, z_1), (vx_1, vy_1, vz_1) = ball_1

    try:
        t_0 = ((x_1 - x_0) + ((vx_1 * (y_0 - y_1)) / vy_1)) / (
            vx_0 - (vx_1 * vy_0 / vy_1)
        )
        t_1 = ((x_0 - x_1) + ((vx_0 * (y_1 - y_0)) / vy_0)) / (
            vx_1 - (vx_0 * vy_1 / vy_0)
        )
    except ZeroDivisionError:
        return None, None

    if t_0 < 0 or t_1 < 0:
        return None, None

    return get_future(ball_0, t_0)


def main(filename="input.txt", min_val=7, max_val=27):
    print(solve(parse(read_file(filename)), min_val, max_val))


if __name__ == "__main__":
    main("test.txt", 7, 27)
    main(min_val=200000000000000, max_val=400000000000000)
