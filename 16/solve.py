#!/usr/bin/env python3

import numpy as np
import sys
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

    def get_energized(self):
        self.energized[0, 0] = 0b0001
        self.walk_east(0, -1, True)
        return (self.energized > 0).sum()

    def valid_coords(self, idx, jdx):
        return idx in range(self.board.shape[0]) and jdx in range(self.board.shape[1])

    def walk_east(self, idx, jdx, skip_check=False):
        jdx += 1
        if not skip_check:
            if not self.valid_coords(idx, jdx) or self.visited_east(idx, jdx):
                return
        if self.board[idx, jdx] == "|":
            self.walk_north(idx, jdx)
            self.walk_south(idx, jdx)
        elif self.board[idx, jdx] == "\\":
            self.walk_south(idx, jdx)
        elif self.board[idx, jdx] == "/":
            self.walk_north(idx, jdx)
        else:
            self.walk_east(idx, jdx)

    def walk_north(self, idx, jdx):
        idx -= 1
        if not self.valid_coords(idx, jdx) or self.visited_north(idx, jdx):
            return
        if self.board[idx, jdx] == "-":
            self.walk_west(idx, jdx)
            self.walk_east(idx, jdx)
        elif self.board[idx, jdx] == "\\":
            self.walk_west(idx, jdx)
        elif self.board[idx, jdx] == "/":
            self.walk_east(idx, jdx)
        else:
            self.walk_north(idx, jdx)

    def walk_south(self, idx, jdx):
        idx += 1
        if not self.valid_coords(idx, jdx) or self.visited_south(idx, jdx):
            return
        if self.board[idx, jdx] == "-":
            self.walk_west(idx, jdx)
            self.walk_east(idx, jdx)
        elif self.board[idx, jdx] == "\\":
            self.walk_east(idx, jdx)
        elif self.board[idx, jdx] == "/":
            self.walk_west(idx, jdx)
        else:
            self.walk_south(idx, jdx)


    def walk_west(self, idx, jdx):
        jdx -= 1
        if not self.valid_coords(idx, jdx) or self.visited_west(idx, jdx):
            return
        if self.board[idx, jdx] == "|":
            self.walk_north(idx, jdx)
            self.walk_south(idx, jdx)
        elif self.board[idx, jdx] == "\\":
            self.walk_north(idx, jdx)
        elif self.board[idx, jdx] == "/":
            self.walk_south(idx, jdx)
        else:
            self.walk_west(idx, jdx)

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
    print(f"part 1:  {board.get_energized()}")
    print(board)
    breakpoint()
    print(f"part 2:  {None}")


if __name__ == "__main__":
    main("test.txt")
    main()
