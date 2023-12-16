#!/usr/bin/env python3

import sys
import numpy as np

sys.setrecursionlimit(9999)


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


class Board:
    def __init__(self, lines):
        self.board = np.array([list(line.strip()) for line in lines])
        self.energized = np.zeros_like(self.board, dtype=int)

    def __str__(self):
        array = np.full_like(self.board, ".")
        array[(self.energized > 0)] = "#"
        return "\n".join("".join(row) for row in array)

    def __repr__(self):
        return str(self)

    def clear_energized(self):
        self.energized[:] = 0

    def get_energized(self):
        return (self.energized > 0).sum()

    def get_max_energized(self):
        max_energized = 0
        for idx in range(self.board.shape[0]):
            self.clear_energized()
            self.walk_east(idx, 0)
            max_energized = max(max_energized, self.get_energized())
            self.clear_energized()
            self.walk_west(idx, self.board.shape[1] - 1)
            max_energized = max(max_energized, self.get_energized())
        for jdx in range(self.board.shape[1]):
            self.clear_energized()
            self.walk_south(0, jdx)
            max_energized = max(max_energized, self.get_energized())
            self.clear_energized()
            self.walk_north(self.board.shape[0] - 1, jdx)
            max_energized = max(max_energized, self.get_energized())
        return max_energized

    def valid_coords(self, idx, jdx):
        return idx in range(self.board.shape[0]) and jdx in range(self.board.shape[1])

    def walk_east(self, idx, jdx):
        if not self.valid_coords(idx, jdx) or self.visited_east(idx, jdx):
            return
        if self.board[idx, jdx] == "|":
            self.walk_north(idx - 1, jdx)
            self.walk_south(idx + 1, jdx)
        elif self.board[idx, jdx] == "\\":
            self.walk_south(idx + 1, jdx)
        elif self.board[idx, jdx] == "/":
            self.walk_north(idx - 1, jdx)
        else:
            self.walk_east(idx, jdx + 1)

    def walk_north(self, idx, jdx):
        if not self.valid_coords(idx, jdx) or self.visited_north(idx, jdx):
            return
        if self.board[idx, jdx] == "-":
            self.walk_west(idx, jdx - 1)
            self.walk_east(idx, jdx + 1)
        elif self.board[idx, jdx] == "\\":
            self.walk_west(idx, jdx - 1)
        elif self.board[idx, jdx] == "/":
            self.walk_east(idx, jdx + 1)
        else:
            self.walk_north(idx - 1, jdx)

    def walk_south(self, idx, jdx):
        if not self.valid_coords(idx, jdx) or self.visited_south(idx, jdx):
            return
        if self.board[idx, jdx] == "-":
            self.walk_west(idx, jdx - 1)
            self.walk_east(idx, jdx + 1)
        elif self.board[idx, jdx] == "\\":
            self.walk_east(idx, jdx + 1)
        elif self.board[idx, jdx] == "/":
            self.walk_west(idx, jdx - 1)
        else:
            self.walk_south(idx + 1, jdx)

    def walk_west(self, idx, jdx):
        if not self.valid_coords(idx, jdx) or self.visited_west(idx, jdx):
            return
        if self.board[idx, jdx] == "|":
            self.walk_north(idx - 1, jdx)
            self.walk_south(idx + 1, jdx)
        elif self.board[idx, jdx] == "\\":
            self.walk_north(idx - 1, jdx)
        elif self.board[idx, jdx] == "/":
            self.walk_south(idx + 1, jdx)
        else:
            self.walk_west(idx, jdx - 1)

    def visited_east(self, idx, jdx):
        """
        Return true if location has been visited while going east.
        Mark as visited.
        """
        res = (self.energized[idx, jdx] & 0b0001) > 0
        self.energized[idx, jdx] |= 0b0001
        return res

    def visited_north(self, idx, jdx):
        """
        Return true if location has been visited while going north.
        Mark as visited.
        """
        res = (self.energized[idx, jdx] & 0b0010) > 0
        self.energized[idx, jdx] |= 0b0010
        return res

    def visited_south(self, idx, jdx):
        """
        Return true if location has been visited while going south.
        Mark as visited.
        """
        res = (self.energized[idx, jdx] & 0b0100) > 0
        self.energized[idx, jdx] |= 0b0100
        return res

    def visited_west(self, idx, jdx):
        """
        Return true if location has been visited while going west.
        Mark as visited.
        """
        res = (self.energized[idx, jdx] & 0b1000) > 0
        self.energized[idx, jdx] |= 0b1000
        return res


def main(filename="input.txt"):
    board = Board(read_file(filename))
    board.walk_east(0, 0)
    print(f"part 1:  {board.get_energized()}")
    print(f"part 2:  {board.get_max_energized()}")


if __name__ == "__main__":
    main("test.txt")
    main()
