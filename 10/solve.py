#!/usr/bin/env python3

import numpy as np
import networkx as nx
from time import sleep


class Position(tuple):
    @property
    def north(self):
        return Position((max(0, self[0] - 1), self[1]))

    @property
    def south(self):
        return Position((self[0] + 1, self[1]))

    @property
    def west(self):
        return Position((self[0], max(0, self[1] - 1)))

    @property
    def east(self):
        return Position((self[0], self[1] + 1))


class PipeGraph(nx.Graph):
    CONNECT_NORTH = {"┐", "┌", "│", "S"}
    CONNECT_SOUTH = {"┘", "└", "│", "S"}
    CONNECT_WEST = {"┌", "└", "─", "S"}
    CONNECT_EAST = {"┐", "┘", "─", "S"}
    CHAR_MAP = {
        "|": "│",
        "-": "─",
        "L": "└",
        "J": "┘",
        "F": "┌",
        "7": "┐",
    }
    EXPAND_CHAR_MAP = {
        "│": np.array(
            (
                ["│", " "],
                ["│", " "],
            )
        ),
        "─": np.array(
            (
                ["─", "─"],
                [" ", " "],
            )
        ),
        "└": np.array(
            (
                ["└", "─"],
                [" ", " "],
            )
        ),
        "┘": np.array(
            (
                ["┘", " "],
                [" ", " "],
            )
        ),
        "┌": np.array(
            (
                ["┌", "─"],
                ["│", " "],
            )
        ),
        "┐": np.array(
            (
                ["┐", " "],
                ["│", " "],
            )
        ),
        ".": np.array(
            (
                [".", " "],
                [" ", " "],
            )
        ),
    }
    TRAVERSABLE = {".", " "}

    def __init__(self, board):
        super().__init__()
        self.queue = None
        self.board = np.pad(board, 1, constant_values=".")
        self.start = self._get_start()
        self._replace_chars()
        self._replace_start()
        self._bfs()
        self._replace_junk()

    def get_path_length(self):
        return len(self.nodes)

    def _get_start(self):
        return Position(map(int, np.where(self.board == "S")))

    def _replace_chars(self):
        for old, new in self.CHAR_MAP.items():
            self.board[self.board == old] = new
            print(self)
            sleep(0.01)


    def _replace_start(self):
        if self._connected_north(self.start):
            if self._connected_south(self.start):
                self.board[self.start] = "│"
            elif self._connected_west(self.start):
                self.board[self.start] = "┘"
            elif self._connected_east(self.start):
                self.board[self.start] = "└"
        elif self._connected_south(self.start):
            if self._connected_west(self.start):
                self.board[self.start] = "┐"
            elif self._connected_east(self.start):
                self.board[self.start] = "┌"
        else:
            self.board[self.start] = "─"
        print(self)
        sleep(0.01)

    def _bfs(self):
        self.add_node(self.start)
        self.queue = [self.start]
        while len(self.queue) > 0:
            pos = self.queue.pop(0)
            self._check_north(pos)
            self._check_south(pos)
            self._check_west(pos)
            self._check_east(pos)

    def _check_north(self, pos):
        if self._connected_north(pos) and pos.north not in self.nodes:
            self.add_edge(pos, pos.north)
            self.queue.append(pos.north)

    def _check_south(self, pos):
        if self._connected_south(pos) and pos.south not in self.nodes:
            self.add_edge(pos, pos.south)
            self.queue.append(pos.south)

    def _check_west(self, pos):
        if self._connected_west(pos) and pos.west not in self.nodes:
            self.add_edge(pos, pos.west)
            self.queue.append(pos.west)

    def _check_east(self, pos):
        if self._connected_east(pos) and pos.east not in self.nodes:
            self.add_edge(pos, pos.east)
            self.queue.append(pos.east)

    def _connected_north(self, pos):
        return (
            self.board[pos] in self.CONNECT_SOUTH
            and self.board[pos.north] in self.CONNECT_NORTH
        )

    def _connected_south(self, pos):
        return (
            self.board[pos] in self.CONNECT_NORTH
            and self.board[pos.south] in self.CONNECT_SOUTH
        )

    def _connected_west(self, pos):
        return (
            self.board[pos] in self.CONNECT_EAST
            and self.board[pos.west] in self.CONNECT_WEST
        )

    def _connected_east(self, pos):
        return (
            self.board[pos] in self.CONNECT_WEST
            and self.board[pos.east] in self.CONNECT_EAST
        )

    def _replace_junk(self):
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                if (row, col) not in self.nodes:
                    self.board[row, col] = "."
                    print(self)
                    sleep(0.01)

    def get_internal_area(self):
        self.board = self._expand()
        self._bfs_external()
        return (self.board == ".").sum()

    def _expand(self):
        expanded_board = np.empty(
            (self.board.shape[0] * 2, self.board.shape[1] * 2), dtype=self.board.dtype
        )
        for idx, row in enumerate(self.board):
            idx *= 2
            for jdx, col in enumerate(row):
                jdx *= 2
                expanded_board[idx : idx + 2, jdx : jdx + 2] = self.EXPAND_CHAR_MAP[col]
        return expanded_board

    def _bfs_external(self):
        self.queue = [Position((0, 0))]
        while len(self.queue) > 0:
            pos = self.queue.pop(0)
            self._bfs_external_north(pos)
            self._bfs_external_south(pos)
            self._bfs_external_west(pos)
            self._bfs_external_east(pos)
            print(self)
            sleep(0.01)

    def _bfs_external_north(self, pos):
        if self.board[pos.north] in self.TRAVERSABLE:
            self.board[pos.north] = "O"
            self.queue.append(pos.north)

    def _bfs_external_south(self, pos):
        if pos.south[0] < self.board.shape[0] and self.board[pos.south] in self.TRAVERSABLE:
            self.board[pos.south] = "O"
            self.queue.append(pos.south)

    def _bfs_external_west(self, pos):
        if self.board[pos.west] in self.TRAVERSABLE:
            self.board[pos.west] = "O"
            self.queue.append(pos.west)

    def _bfs_external_east(self, pos):
        if pos.east[1] < self.board.shape[1] and self.board[pos.east] in self.TRAVERSABLE:
            self.board[pos.east] = "O"
            self.queue.append(pos.east)

    def __str__(self):
        return "\n".join("".join(row) for row in self.board)

    def __repr__(self):
        return str(self)


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_board(lines):
    return np.array([list(line.strip()) for line in lines])


def main(filename="input.txt"):
    board = parse_board(read_file(filename))
    graph = PipeGraph(board)
    print(f"part 1:  {graph.get_path_length() // 2}")
    print(graph)
    print(f"part 2:  {graph.get_internal_area()}")
    print(graph)


if __name__ == "__main__":
    main("test4.txt")
    #main()
