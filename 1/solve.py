#!/usr/bin/env python3


REPLACEMENTS = [
    ("one", "o1e"),
    ("two", "t2o"),
    ("three", "t3e"),
    ("four", "f4r"),
    ("five", "f5e"),
    ("six", "s6x"),
    ("seven", "s7n"),
    ("eight", "e8t"),
    ("nine", "n9e"),
]


def read_file(filename="input.txt"):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def replace_words(lines):
    new_lines = []
    for line in lines:
        for replacement in REPLACEMENTS:
            line = line.replace(*replacement)
        new_lines.append(line)
    return new_lines


def split_lines(lines):
    return [list(line) for line in lines]


def clean_lines(lines):
    for line in lines:
        while not line[0].isdigit():
            line.pop(0)
        while not line[-1].isdigit():
            line.pop(-1)


def extract_pair(line):
    return int(line[0] + line[-1])


def extract_pairs(lines):
    return [extract_pair(line) for line in lines]


def sum_lines(lines):
    lines = split_lines(lines)
    clean_lines(lines)
    return sum(extract_pairs(lines))


def main():
    lines = read_file()
    lines_numeric = replace_words(lines)
    print(f"part 1:  {sum_lines(lines)}")
    print(f"part 2:  {sum_lines(lines_numeric)}")


if __name__ == "__main__":
    main()
