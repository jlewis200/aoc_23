#!/usr/bin/env python3

import re
from dataclasses import dataclass


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

    accept = []
    reject = []

    for part in parts:

        destination = "in"
        while destination not in ("A", "R"):
            destination = workflows[destination].evaluate(part)

        if destination == "A":
            accept.append(part)
        elif destination == "R":
            reject.append(part)
        else:
            raise ValueError("this shouldn't happen")

    rating = 0
    for part in accept:
        rating += part.x + part.m + part.a + part.s

    return rating


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

        match = re.search(
            "(P?<attr>.*)(P?<operator>[>|<])(P?<value>\d+);(P?<destinationjk>.*)", rule
        )

        try:
            match = re.search(
                "(?P<attr>.*)(?P<operator>[>|<])(?P<value>\d+):(?P<destination>.*)",
                rule,
            )
            self.attr = match.group("attr")
            self.operator = match.group("operator")
            self.value = int(match.group("value"))
            self.destination = match.group("destination")

        except AttributeError:
            self.destination = rule

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
