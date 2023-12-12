#!/usr/bin/env python3

import re


class Group:
    
    cache = {}

    def __init__(self, seq, broken):
        self.seq = self.squeeze(seq)
        self.broken = broken
        self.count = 0
    
    def __str__(self):
        return f"{self.seq}  {self.broken}"

    def __repr__(self):
        return str(self)

    def squeeze(self, seq):
        """
        Squeeze consecutive ".", strip ".".
        """
        return re.sub(r"\.+", ".", seq, count=0).strip(".")

    def enumerate(self, seq, broken):
        seq = self.squeeze(seq)

        # check cache
        try:
            return self.cache[(seq, broken)]
        except:
            pass

        if seq.count("?") == 0:
            return self.is_valid(seq, broken)
        
        candidate_working = re.sub(r"\?", ".", seq, count=1)
        candidate_broken = re.sub(r"\?", "#", seq, count=1)
    
        count = self.enumerate(candidate_working, broken) + self.enumerate(candidate_broken, broken)
        
        # add to cache
        self.cache[(seq, broken)] = count

        return count

    def is_valid(self, seq, broken):
        valid_str = ".".join("#" * broke for broke in broken)
        return seq == valid_str

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
    seq = seq.strip(".")
    return Group(seq, broken)


def get_counts(groups):
    return [get_count(group) for group in groups]
       

def get_count(group):
    count = group.enumerate(group.seq, group.broken)
    print(count)
    return count

def unfold_groups(groups):
    for group in groups:
        group.unfold()

def main(filename="input.txt"):
    groups = parse_groups(read_file(filename))
    counts = get_counts(groups)
    print(f"part 1:  {sum(counts)}")
    unfold_groups(groups)
    #breakpoint()
    #counts = get_counts(groups)
    #print(f"part 2:  {None}")


if __name__ == "__main__":
    main("test.txt")
    main()
