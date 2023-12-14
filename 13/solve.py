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
    Fold top section over bottom section.  Return true if symmetrical.
    Slice, reverse top, truncate to common height, test equivalency.
    """
    top = array[:idx][::-1]
    bot = array[idx:]
    n_rows = min(top.shape[0], bot.shape[0])
    top = top[:n_rows]
    bot = bot[:n_rows]
    return (top == bot).all()


def check_left_right_fold(array, idx):
    """
    Fold left section over right section.  Return true if symmetrical.
    Slice, reverse left, truncate to common width, test equivalency.
    """
    left = array[:, :idx][:, ::-1]
    right = array[:, idx:]
    n_cols = min(left.shape[1], right.shape[1])
    left = left[:, :n_cols]
    right = right[:, :n_cols]
    return (left == right).all()


def get_fold_rows(array):
    return {row for row in range(1, array.shape[0]) if check_top_down_fold(array, row)}


def get_fold_cols(array):
    return {col for col in range(1, array.shape[1]) if check_left_right_fold(array, col)}


def get_value(rows, cols):
    return 100 * rows.pop() if len(rows) > 0 else cols.pop()


def get_summary(arrays):
    summary = 0
    for array in arrays:
        rows = get_fold_rows(array)
        cols = get_fold_cols(array)
        summary += get_value(rows, cols)
    return summary


def get_smudge_summary(arrays):
    summary = 0
    for array in arrays:
        rows = get_smudged_rows(array) - get_fold_rows(array)
        cols = get_smudged_cols(array) - get_fold_cols(array)
        summary += get_value(rows, cols)
    return summary


def smudges(array):
    for idx, row in enumerate(array):
        for jdx, col in enumerate(row):
            smudged = array.copy()
            smudged[idx, jdx] = "#" if col == "." else "."
            yield smudged


def get_smudged_rows(array):
    rows = set()
    for smudged in smudges(array):
        rows |= get_fold_rows(smudged)
    return rows


def get_smudged_cols(array):
    cols = set()
    for smudged in smudges(array):
        cols |= get_fold_cols(smudged)
    return cols


def main(filename="input.txt"):
    patterns = parse_patterns(read_file(filename))
    print(f"part 1:  {get_summary(patterns)}")
    print(f"part 2:  {get_smudge_summary(patterns)}")


if __name__ == "__main__":
    main("test.txt")
    main()
