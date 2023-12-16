#!/usr/bin/env python3

# import re
import regex


class Group:
    def __init__(self, seq, broken):
        self.seq = seq
        self.broken = broken

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


def unfold_groups(groups):
    for group in groups:
        group.unfold()


def get_count_recursive(seq, broken, cache):
    if get_termination_value(seq, broken) is not None:
        return get_termination_value(seq, broken)
    if (seq, broken) not in cache:
        cache[(seq, broken)] = dfs(seq, broken, cache)
    return cache[(seq, broken)]


def get_termination_value(seq, broken):
    if len(broken) == 0:
        if seq.count("#") == 0:
            return 1
        return 0
    if len(seq) == 0:
        return 0
    return None


def get_leftmost(seq, sub):
    """
    find() but default value is len(seq).
    """
    return len(seq) if seq.find(sub) == -1 else seq.find(sub)


def get_pattern(length):
    return f"[?.]([?#]{{{length}}})[?.]"


def dfs(seq, broken, cache):
    count = 0
    for match in regex.finditer(get_pattern(broken[0]), seq, overlapped=True):
        if match.span()[0] > get_leftmost(seq, "#"):
            break
        count += get_count_recursive(seq[match.span()[1] - 1 :], broken[1:], cache)
    return count


def main(filename="input.txt"):
    groups = parse_groups(read_file(filename))
    print(f"part 1:  {sum(get_counts(groups))}")
    unfold_groups(groups)
    print(f"part 2:  {sum(get_counts(groups))}")


if __name__ == "__main__":
    main("test.txt")
    main()
