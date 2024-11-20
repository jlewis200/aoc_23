#!/usr/bin/env python3

import re
from dataclasses import dataclass
from copy import deepcopy
import networkx as nx
import numpy as np
from copy import copy
from itertools import permutations, combinations


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    workflows = []
    parts = []

    target = workflows
    callback = parse_workflow

    for line in lines:
        if line == "\n":
            target = parts
            callback = parse_part
            continue

        target.append(callback(line))

    workflows = {workflow.name: workflow for workflow in workflows}

    return workflows, parts


def parse_workflow(line):
    match = re.search("(?P<name>.*){(?P<rules>.*).*}", line)
    name = match.group("name")
    rules = match.group("rules").split(",")
    return WorkFlow(name, rules)


def solve(workflows, parts):
    """
    Build a decision tree based on the rules.  Traverse each path to the accept
    leaves.  The rules along each path will induce constraints on the block of
    4-dimensional "part-space".  Shrink these blocks each time a rule is
    encounterd.  Finally, sum according to instructions.
    """
    collection = []
    dfs(workflows, "in", Block(), collection)
    return sum(map(lambda x: x.value, collection))


def dfs(graph, src, block, collection):
    if src == "A":
        collection.append(deepcopy(block))
        return

    if src == "R":
        return

    block = deepcopy(block)
    for rule in graph[src].rules:
        _block = deepcopy(block)
        if rule.operator is not None:
            _block.shrink(rule)
            block.shrink(rule.invert())
        dfs(graph, rule.destination, _block, collection)


@dataclass
class Block:
    xmin: int = 1
    mmin: int = 1
    amin: int = 1
    smin: int = 1
    xmax: int = 4000
    mmax: int = 4000
    amax: int = 4000
    smax: int = 4000

    def shrink(self, rule):
        if rule.operator == "<":
            setattr(self, f"{rule.attr}max", rule.value - 1)
        else:
            setattr(self, f"{rule.attr}min", rule.value + 1)

    @property
    def value(self):
        x = max(0, self.xmax - self.xmin + 1)
        m = max(0, self.mmax - self.mmin + 1)
        a = max(0, self.amax - self.amin + 1)
        s = max(0, self.smax - self.smin + 1)
        return x * m * a * s


@dataclass
class Part:

    x: int
    m: int
    a: int
    s: int


class WorkFlow:

    def __init__(self, name, rules):
        self.name = name
        self.rules = [Rule(rule) for rule in rules]
        self._rules = rules

    def evaluate(self, part):
        for rule in self.rules:
            destination = rule.evaluate(part)
            if destination is not None:
                return destination


class Rule:

    def __init__(self, rule):
        self.attr = None
        self.operator = None
        self.value = None
        self._rule = rule

        match = re.search(
            "(?P<attr>.*)(?P<operator>[>|<])(?P<value>\d+):(?P<destination>.*)", rule
        )

        try:
            self.attr = match.group("attr")
            self.operator = match.group("operator")
            self.value = int(match.group("value"))
            self.destination = match.group("destination")

        except AttributeError:
            self.destination = rule

    def invert(self):
        rule = copy(self)

        if rule.operator == "<":
            rule.operator = ">"
            rule.value -= 1

        elif rule.operator == ">":
            rule.operator = "<"
            rule.value += 1

        return rule

    def evaluate(self, part):
        """
        Return destination if rule matches, else None.
        """
        if self.operator == "<":
            return self.destination if getattr(part, self.attr) < self.value else None
        if self.operator == ">":
            return self.destination if getattr(part, self.attr) > self.value else None
        return self.destination


def parse_part(line):
    match = re.search("x=(?P<x>\d+).*m=(?P<m>\d+).*a=(?P<a>\d+).*s=(?P<s>\d+)", line)
    return Part(
        x=int(match.group("x")),
        m=int(match.group("m")),
        a=int(match.group("a")),
        s=int(match.group("s")),
    )


def main(filename="input.txt"):
    print(solve(*parse(read_file(filename))))


if __name__ == "__main__":
    main("test.txt")
    main()
