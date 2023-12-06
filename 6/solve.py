#!/usr/bin/env python3

import re
import numpy as np


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_races(lines):
    times = map(int, re.findall(r"\d+", lines.pop(0)))
    distances = map(int, re.findall(r"\d+", lines.pop(0)))
    return list(zip(times, distances))


def parse_race(lines):
    time = lines.pop(0).replace(" ", "")
    time = int(re.search(r"\d+", time).group())
    distance = lines.pop(0).replace(" ", "")
    distance = int(re.search(r"\d+", distance).group())
    return time, distance


def get_win_counts(races):
    return [get_win_count(race) for race in races]


def get_win_count(race):
    time, distance = race
    exceed_threshold = 0
    for speed in range(time + 1):
        movement_time = time - speed
        distance_travelled = movement_time * speed
        exceed_threshold += distance_travelled > distance
    return exceed_threshold


def main(filename="input.txt"):
    win_counts = get_win_counts(parse_races(read_file(filename)))
    win_count = get_win_count(parse_race(read_file(filename)))
    print(f"part 1:  {np.prod(win_counts)}")
    print(f"part 2:  {win_count}")


if __name__ == "__main__":
    main()
