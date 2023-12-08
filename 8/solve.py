#!/usr/bin/env python3

import re


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def add_children(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return (
            f"Node:  {self.value}\n"
            f"    Left:   {self.left.value}\n"
            f"    Right:  {self.right.value}\n"
        )

    def __repr__(self):
        return str(self)


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_directions(lines):
    directions = list(lines.pop(0).strip())
    lines.pop(0)
    return directions


def parse_network(lines):
    nodes = {}
    for line in lines:
        parse_nodes(line, nodes)
    return nodes


def parse_nodes(line, nodes):
    src, left, right = re.findall(r"[A-Z]+", line)
    for node in (src, left, right):
        if node not in nodes:
            nodes[node] = Node(node)
    nodes[src].add_children(nodes[left], nodes[right])


def follow_directions(directions, start, end="ZZZ"):
    steps = 0
    while start.value != end:
        steps += 1
        direction = directions.pop(0)
        directions.append(direction)
        start = start.left if direction == "L" else start.right
    return steps


def main(filename="input.txt"):
    lines = read_file(filename)
    directions = parse_directions(lines)
    nodes = parse_network(lines)
    print(f"part 1:  {follow_directions(directions, nodes['AAA'])}")


if __name__ == "__main__":
    main("test1.txt")
    main("test2.txt")
    main()
