#!/usr/bin/env python3

import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_array(lines):
    return np.array([list(line.strip()) for line in lines])


def array_str(array):
    return "\n".join("".join(row) for row in array)


def shift_north(array):
    for idx, row in enumerate(array[1:], start=1):
        for jdx, col in enumerate(row):
            if col == "O":
                dst = get_empty_north(array, idx, jdx)
                array[idx, jdx] = "."
                array[dst, jdx] = "O"
    return array


def get_empty_north(array, idx, jdx):
    while idx > 0 and array[idx - 1, jdx] == ".":
        idx -= 1
    return idx


def get_load(array):
    load = 0
    for idx, row in enumerate(array[::-1], start=1):
        load += idx * (row == "O").sum()
    return load


def spin(array, rotations):
    for _ in range(rotations):
        for _ in range(4):  # rotate through 4 directions
            array = shift_north(array)
            array = np.rot90(array, k=-1)
    return array


def hash_array(array):
    return hash("".join(array.flatten()))


def find_hash_cycle(array):
    array_hash = hash_array(array)
    idx = 0
    cache = {}
    while array_hash not in cache:
        cache[array_hash] = idx
        array = spin(array, 1)
        array_hash = hash_array(array)
        idx += 1
    return cache[array_hash], idx - cache[array_hash]


def main(filename="input.txt"):
    array = parse_array(read_file(filename))
    print(f"part 1:  {get_load(shift_north(array.copy()))}")
    cycle_start, cycle_length = find_hash_cycle(array.copy())
    rotations = cycle_start + (1000000000 - cycle_start) % cycle_length
    print(f"part 2:  {get_load(spin(array.copy(), rotations))}")


if __name__ == "__main__":
    main("test.txt")
    main()
