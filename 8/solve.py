#!/usr/bin/env python3

import re
from math import lcm


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def add_children(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"Node:  {self.value}"

    def __repr__(self):
        return str(self)


class GhostPath:
    def __init__(self, directions, start, terminal_callback):
        self.directions = directions.copy()
        self.start = start
        self.terminal_callback = terminal_callback
        self.steps = self._get_steps()

    def _get_steps(self):
        """
        This was originally written to handle cycles with multiple terminals and
        cycles starting from arbitrary (2nd, 3rd, 4th) terminals.  Those cases
        don't appear in the input data, so this was simplified.
        """
        step = 0
        node = self.start
        while not self.terminal_callback(node):
            step += 1
            node = self._get_next_node(node)
        return step

    def _get_direction(self):
        direction = self.directions.pop(0)
        self.directions.append(direction)
        return direction

    def _get_next_node(self, node):
        return node.left if self._get_direction() == "L" else node.right


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_directions(lines):
    directions = list(lines.pop(0).strip())
    lines.pop(0)
    return directions


def parse_graph(lines):
    nodes = {}
    for line in lines:
        parse_nodes(line, nodes)
    return nodes


def parse_nodes(line, nodes):
    src, left, right = re.findall(r"[A-Z0-9]+", line)
    for node in (src, left, right):
        if node not in nodes:
            nodes[node] = Node(node)
    nodes[src].add_children(nodes[left], nodes[right])


def follow_directions(directions, start, end="ZZZ"):
    terminal_callback = lambda node: node.value == end
    return GhostPath(directions, start, terminal_callback).steps


def get_starts(nodes):
    return {node for node in nodes.values() if node.value.endswith("A")}


def follow_ghost_directions(directions, starts):
    terminal_callback = lambda node: node.value.endswith("Z")
    paths = [GhostPath(directions, start, terminal_callback) for start in starts]
    return [path.steps for path in paths]


def main(filename="input.txt"):
    lines = read_file(filename)
    directions = parse_directions(lines)
    nodes = parse_graph(lines)
    print(f"part 1:  {follow_directions(directions, nodes['AAA'])}")
    print(f"part 2:  {lcm(*follow_ghost_directions(directions, get_starts(nodes)))}")


if __name__ == "__main__":
    main()
