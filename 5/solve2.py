#!/usr/bin/env python3

import re
import networkx as nx


class Mapper:

    def __init__(self, rangers):
        self.map_ranges = [MapRange(*ranger) for ranger in rangers]
    
    def forward(self, value):
        for map_range in self.map_ranges:
            try:
                return map_range.forward(value)
            except ValueError:
                pass
        return value

    def backward(self, value):
        for map_range in self.map_ranges:
            try:
                return map_range.backward(value)
            except ValueError:
                pass
        return value


class MapRange:
    
    def __init__(self, dst, src, length):
        dst, src, length = map(int, (dst, src, length))
        self.src_range = range(src, src + length)
        self.dst_range = range(dst, dst + length)
        self.shift = dst - src

    def forward(self, value):
        if value in self.src_range:
            return value + self.shift
        else:
            raise ValueError

    def backward(self, value):
        if value in self.dst_range:
            return value - self.shift
        else:
            raise ValueError


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_lines(lines):
    lines.append('\n')
    return parse_seeds(lines), parse_maps(lines)


def parse_seeds(lines):
    seeds = re.findall(r"\d+", lines.pop(0))
    lines.pop(0)
    seeds = list(map(int, seeds))
    for idx in range(1, len(seeds), 2):
        seeds[idx] += seeds[idx - 1] - 1
    return [range(seeds[idx], seeds[idx + 1]) for idx in range(0, len(seeds), 2)]


def parse_maps(lines):
    mappers = []
    while len(lines) > 0:
        mappers.append(parse_map(lines))
    return mappers


def parse_map(lines):
    map_ranges = []
    name = lines.pop(0)
    line = lines.pop(0)
    while line != '\n':
        map_ranges.append(parse_map_values(line))
        line = lines.pop(0)
    return Mapper(map_ranges)


def parse_map_values(line):
    return re.findall(r"\d+", line)


def forward(mappers, seeds):
    values = seeds.copy()
    for mapper in mappers:
        next_values = []
        for value in values:
            next_values.append(mapper.forward(value))
        values = next_values 
    return values


def backward(mappers, locations):
    values = locations.copy()
    for mapper in mappers[::-1]:
        next_values = []
        for value in values:
            next_values.append(mapper.backward(value))
        values = next_values
    return values


def solve2(mappers, seed_ranges):
    locations = forward(mappers, [seed_range.start for seed_range in seed_ranges])
    for idx, mapper in enumerate(mappers):
        for map_range in mapper.map_ranges:
            value = map_range.src_range.start
            seed = backward(mappers[:idx], [value])
            location = forward(mappers[idx:], [value])
            assert location == forward(mappers, seed) # sanity check
            if any(seed[0] in seed_range for seed_range in seed_ranges):
                locations.append(location[0])
    return locations


def main(filename="input.txt"):
    seed_ranges, mappers = parse_lines(read_file(filename))
    print(f"part 2:  {min(solve2(mappers, seed_ranges))}")


if __name__ == "__main__":
    main()
