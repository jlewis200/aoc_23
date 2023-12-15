#!/usr/bin/env python3


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


def main(filename="input.txt"):
    instructions = parse_instructions(read_file(filename))
    print(f"part 1:  {sum(hash_iterable(instructions))}")
    print(f"part 2:  {None}")


if __name__ == "__main__":
    main("test.txt")
    main()
