#!/usr/bin/env python3

import re


class Group:
    
    def __init__(self, seq, broken):
        self.seq = "." + seq + "."
        self.broken = broken
        self.count = 0
    
    def __str__(self):
        return f"{self.seq}  {self.broken}"

    def __repr__(self):
        return str(self)

    def unfold(self):
        self.seq = self.squeeze("?".join(self.seq for _ in range(5)))
        self.broken = self.broken * 5


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_groups(lines):
    return [parse_group(line) for line in lines]


def parse_group(line):
    seq, broken = line.strip().split()
    broken = tuple(map(int, broken.split(",")))
    return Group(seq, broken)


def get_counts(groups):
    return [get_count(group) for group in groups]
       

def get_count(group):
    return get_count_recursive(group.seq, group.broken)


def truncate(seq, broken_length):
    """
    Truncate a sequence by discarding all characters occurring before the first
    match of specified length.

    truncate("#.##.###.####", 3) -> "###.####"

    Return empty sequence if no match.
    
    truncate("#.##.###.####", 5) -> ""
    """
    match = re.search(f"([?#]{{{broken_length}}}[?.])", seq)
    if match is None:
        return ""
    return seq[match.span()[0]:]


def consume(seq, broken_length):
    """
    Truncate a sequence by discarding all characters occurring before the first
    match of specified length and the characters in the match itself.

    truncate("#.##.###.####", 3) -> "####"

    Return empty sequence if no match.
    
    truncate("#.##.###.####", 5) -> ""
    """
    match = re.search(f"([?#]{{{broken_length}}}[?.])", seq)
    if match is None:
        return None
    return seq[match.span()[1]:]



def get_count_recursive(seq, broken, indent=0):
    if seq is None:
        return 0
    if len(broken) == 0:
        #print("broken == 0")
        return 1
    if len(seq) == 0:
        return 0

    length = broken[0]
    count = 0
    while True:
        seq = truncate(seq, length) 
        print((" " * indent) + f"└─{seq[::-1]}  {broken} {count = }")
        res = get_count_recursive(consume(seq, length), broken[1:], indent + 2)
        count += res
        seq = seq[1:]
        if len(seq) == 0 or res == 0:
            break
    return count


def unfold_groups(groups):
    for group in groups:
        group.unfold()


def main(filename="input.txt"):
    groups = parse_groups(read_file(filename))
    counts = get_counts(groups[-1:])
    print(f"part 1:  {counts = }")
    print(f"part 1:  {sum(counts)}")
    
    #unfold_groups(groups)
    #breakpoint()
    #counts = get_counts(groups)
    #print(f"part 2:  {None}")


if __name__ == "__main__":
    main("test.txt")
    #main()
