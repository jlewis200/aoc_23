#!/usr/bin/env python3

import re
import networkx as nx


class Interval:
    
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __and__(self, other):
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        if start > end:
            return None
        return Interval(start, end)

    def __str__(self):
        return f"Interval({self.start}, {self.end})"

    def __repr__(self):
        return str(self)
        
    def __contains__(self, value):
        return value >= self.start and value <= self.end

    def __add__(self, value):
        return Interval(self.start + value, self.end + value)

    def __sub__(self, value):
        return Interval(self.start - value, self.end - value)

class Transform:
    
    def __init__(self, src_interval, shift):
        self.src_interval = src_interval
        self.dst_interval = src_interval + shift
        self.shift = shift

    def forward(self, value):
        return value + self.shift

    def backward(self, value):
        return value - self.shift

    def __str__(self):
        return f"Transform\n" \
               f"    id:  {id(self)}\n" \
               f"    src_interval:  {self.src_interval}\n" \
               f"    dst_interval:  {self.dst_interval}\n" \
               f"    shift:  {self.shift}" 

    def __repr__(self):
        return str(self)
 
def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_lines(lines):
    lines.append('\n')
    return parse_seeds(lines), parse_intervals(lines)


def parse_seeds(lines):
    seeds = re.findall(r"\d+", lines.pop(0))
    lines.pop(0)
    seeds = list(map(int, seeds))
    seed_intervals = []
    for idx in range(0, len(seeds), 2):
        start = seeds[idx]
        end = seeds[idx] + seeds[idx + 1] - 1
        seed_intervals.append(Interval(start, end))
    return seed_intervals


def parse_intervals(lines):
    srcs = []
    dsts = []
    while len(lines) > 0:
        src, dst = parse_interval(lines)
        srcs.append(src)
        dsts.append(dst)
    return srcs, dsts


def parse_interval(lines):
    srcs = []
    dsts = []
    line = lines.pop(0)
    line = lines.pop(0)
    while line != '\n':
        dst, src, length = parse_map_values(line)
        srcs.append(Interval(src, src + length - 1))
        dsts.append(Interval(dst, dst + length - 1))
        line = lines.pop(0)
    return srcs, dsts


def parse_map_values(line):
    return list(map(int, re.findall(r"\d+", line)))


def get_graph(seed_intervals, src_intervals, dst_intervals):
    graph = nx.DiGraph()
    
    # map seed_interval to first src_interval
    for seed_interval in seed_intervals:
        for src_interval, dst_interval in zip(src_intervals[0], dst_intervals[0]):
            intersection = seed_interval & src_interval
            if intersection is not None:
                shift = dst_interval.start - src_interval.start
                transform = Transform(intersection, shift)
                graph.add_node(transform)
   
    # map src_intervals to dst_intervals
    for idx in range(1, len(src_intervals)):
        for src_interval, dst_interval in zip(src_intervals[idx], dst_intervals[idx]):
            # add an edge between every intersection of dst_interval already in the graph which isn't absorbed by the input of a previous layer
            # every 
            intersection = dst_interval & src_interval
            if intersection is not None:
                shift = dst_interval.start - src_interval.start
                transform = Transform(intersection, shift)
                graph.add_node(transform)


    breakpoint()


def main(filename="input.txt"):
    seed_intervals, (src_intervals, dst_intervals) = parse_lines(read_file(filename))
    print(seed_intervals)
    print(src_intervals)
    print(dst_intervals)

    graph = get_graph(seed_intervals, src_intervals, dst_intervals)

    breakpoint()
    #locations = forward(maps, seeds)
    #print(locations)

    #seeds = backward(maps, locations)
    #print(seeds)

    #locations = forward(maps, seeds)
    #print(locations)

    #seeds = backward(maps, locations)
    #print(seeds)
 
    ##print(f"part 1:  {min(locations)}")


if __name__ == "__main__":
    main("test.txt")
    #main()
