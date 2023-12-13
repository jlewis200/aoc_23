#!/usr/bin/env python3

import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def parse_patterns(data):
    return [parse_pattern(section) for section in data.split("\n\n")]


def parse_pattern(section):
    return np.array([list(line) for line in section.split()])


def array_str(array):
    return "\n".join("".join(row) for row in array)


def check_top_down_fold(array, idx):
    """
    Fold top section over bottom section.  Ret true if symmetrical.
    Slice, reverse, truncate to common height.
    """
    top = array[:idx][::-1]
    bot = array[idx:]
    n_rows = min(top.shape[0], bot.shape[0])
    top = top[:n_rows]
    bot = bot[:n_rows]
    return (top == bot).all()


def check_left_right_fold(array, idx):
    """
    Fold left section over right section.  Ret true if symmetrical.
    Slice, reverse, truncate to common width.
    """
    left = array[:, :idx][:, ::-1]
    right = array[:, idx:]
    n_cols = min(left.shape[1], right.shape[1])
    left = left[:, :n_cols]
    right = right[:, :n_cols]
    return (left == right).all()


def find_fold_row(array):
    for row in range(1, array.shape[0]):
        if check_top_down_fold(array, row):
            return row
    return 0


def find_fold_col(array):
    for col in range(1, array.shape[1]):
        if check_left_right_fold(array, col):
            return col
    return 0


def get_summary(arrays):
    summary = 0
    for array in arrays:
        summary += find_fold_col(array)
        summary += 100 * find_fold_row(array)
    return summary


def main(filename="input.txt"):
    patterns = parse_patterns(read_file(filename))
    print(f"part 1:  {get_summary(patterns)}")
    # print(f"part 2:  {None}")


if __name__ == "__main__":
    main("test.txt")
    main()
