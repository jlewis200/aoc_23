#!/usr/bin/env python3

import re


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_instructions(lines):
    return lines[0].strip().split(",")


def hash_iterable(iterable):
    return [hash_chunk(chunk) for chunk in iterable]


def hash_chunk(chunk):
    value = 0
    for char in chunk:
        value = hash_char(char, value)
    return value


def hash_char(char, value):
    return ((value + ord(char)) * 17) % 256


def get_focus_powers(boxes):
    powers = []
    for box, lenses in enumerate(boxes, start=1):
        for position, lens in enumerate(lenses.values(), start=1):
            powers.append(box * position * lens)
    return powers


def get_boxes(instructions):
    boxes = [{} for idx in range(256)]
    for instruction in instructions:
        label, op, lens = re.match(r"([a-z]+)([=,-])(\d*)", instruction).groups()
        box = boxes[hash_chunk(label)]
        if op == "=":
            box[label] = int(lens)
        else:
            box.pop(label, None)
    return boxes


def main(filename="input.txt"):
    instructions = parse_instructions(read_file(filename))
    print(f"part 1:  {sum(hash_iterable(instructions))}")
    print(f"part 2:  {sum(get_focus_powers(get_boxes(instructions)))}")


if __name__ == "__main__":
    main("test.txt")
    main()
