#!/usr/bin/env python3

import re


class Mapper:

    def __init__(self, rangers):
        self.map_ranges = [MapRange(*ranger) for ranger in rangers]
    
    def map_value(self, value):
        for map_range in self.map_ranges:
            try:
                return map_range.map_value(value)
            except ValueError:
                pass
        return value


class MapRange:
    
    def __init__(self, dst, src, length):
        dst, src, length = map(int, (dst, src, length))
        self.range = range(src, src + length)
        self.src = src
        self.dst = dst
        self.length = length

    def map_value(self, value):
        if value in self.range:
            return value - self.src + self.dst
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
    return map(int, seeds)


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


def map_seeds(mappers, seeds):
    locations = []
    for seed in seeds:
        for mapper in mappers:
            seed = mapper.map_value(seed)
        locations.append(seed)
    return locations


def main(filename="input.txt"):
    seeds, maps = parse_lines(read_file(filename))
    locations = map_seeds(maps, seeds)
    print(f"part 1:  {min(locations)}")
    breakpoint()
    print(f"part 2:  {sum(get_card_counts(matches))}")


if __name__ == "__main__":
    #main("test.txt")
    main()
