#!/usr/bin/env python3

import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_histories(lines):
    return np.array([list(map(int, line.split())) for line in lines])


def get_extrapolations(histories, extrapolation_callback):
    return [extrapolation_callback(history) for history in histories]


def extrapolate_forward(diff):
    if np.all(diff == 0):
        return 0
    return diff[-1] + extrapolate_forward(np.diff(diff))


def extrapolcate_backward(diff):
    if np.all(diff == 0):
        return 0
    return diff[0] - extrapolcate_backward(np.diff(diff))


def main(filename="input.txt"):
    histories = parse_histories(read_file(filename))
    print(f"part 1:  {sum(get_extrapolations(histories, extrapolate_forward))}")
    print(f"part 2:  {sum(get_extrapolations(histories, extrapolcate_backward))}")


if __name__ == "__main__":
    main("test.txt")
    main()
