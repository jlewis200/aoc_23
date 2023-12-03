#!/usr/bin/env python3


import re
import numpy as np


def read_file(filename="input.txt"):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def clean_lines(lines):
    return [list(line.strip()) for line in lines]


def apply_row_slice_callback(array, callback):
    part_numbers = []
    for idx in range(0, array.shape[0] - 2):
        row_slice = array[idx : idx + 3]
        part_numbers += callback(row_slice)
    return part_numbers


def get_part_numbers(row_slice):
    part_numbers = []
    for match in re.finditer(r"\d+", "".join(row_slice[1])):
        idx, jdx = match.span()
        if is_part_number(row_slice[:, idx - 1 : jdx + 1]):
            part_numbers.append(int(match.group()))
    return part_numbers


def is_part_number(col_slice):
    flat_text = "".join(col_slice.flatten())
    return len(re.findall(r"[^\d.]", flat_text)) > 0


def get_gear_ratios(row_slice):
    gear_ratios = []
    for match in re.finditer(r"\*", "".join(row_slice[1])):
        gear_ratios += get_gear_ratio(row_slice, match.span()[0])
    return gear_ratios


def get_gear_ratio(row_slice, idx):
    numbers = []
    for jdx in range(3):
        numbers += list(re.finditer(r"\d+", "".join(row_slice[jdx])))
    gear_values = get_adjacent_numbers(numbers, idx)
    return [gear_values[0] * gear_values[1]] if len(gear_values) == 2 else []


def get_adjacent_numbers(numbers, idx):
    adjacent_numbers = []
    for number in numbers:
        start, end = number.span()
        if idx in range(start - 1, end + 1):
            adjacent_numbers.append(int(number.group()))
    return adjacent_numbers


def main():
    lines = read_file()
    lines = clean_lines(lines)
    array = np.pad(lines, 1, "constant", constant_values=".")
    part_numbers = apply_row_slice_callback(array, get_part_numbers)
    gear_ratios = apply_row_slice_callback(array, get_gear_ratios)
    print(f"part 1:  {sum(part_numbers)}")
    print(f"part 2:  {sum(gear_ratios)}")


if __name__ == "__main__":
    main()
