#!/usr/bin/env python3

#import re
import regex


class Group:
    
    def __init__(self, seq, broken):
        self.seq = seq
        self.broken = broken
        self.count = 0
    
    def __str__(self):
        return f"{self.seq}  {self.broken}"

    def __repr__(self):
        return str(self)

    def unfold(self):
        self.seq = self.squeeze("?".join(self.seq for _ in range(5)))
        self.broken = self.broken * 5

    def squeeze(self, seq):
        """
        Squeeze consecutive ".", strip ".".
        """
        return regex.sub(r"\.+", ".", seq, count=0).strip(".")



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
    return get_count_recursive("." + group.seq + ".", group.broken, {})


def get_count_recursive(seq, broken, cache):
    if len(broken) == 0:
        if seq.count("#") == 0:
            return 1
        else:
            return 0
    if len(seq) == 0:
        return 0

    try:
        return cache[(seq, broken)]
    except:
        pass

    count = 0
    fcb = 999999 if seq.find("#") == -1 else seq.find("#")
    for match in regex.finditer(f"[?.]([?#]{{{broken[0]}}})[?.]", seq, overlapped=True):
        # abort if match moves past first concrete broken "#"
        if match.span()[0] > fcb:
            break
        count += get_count_recursive(seq[match.span()[1]-1:], broken[1:], cache)

    cache[(seq, broken)] = count
    return count


def unfold_groups(groups):
    for group in groups:
        group.unfold()


def main(filename="input.txt"):
    groups = parse_groups(read_file(filename))
    counts = get_counts(groups)
    print(f"part 1:  {counts = }")
    print(f"part 1:  {sum(counts)}")
    
    unfold_groups(groups)
    counts = get_counts(groups)
    print(f"part 2:  {counts = }")
    print(f"part 2:  {sum(counts)}")


if __name__ == "__main__":
    main("test.txt")
    main()
