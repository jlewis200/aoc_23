#!/usr/bin/env python3

import numpy as np
import networkx as nx


class Position(tuple):
    @property
    def north(self):
        return Position((self[0] - 1, self[1]))

    @property
    def south(self):
        return Position((self[0] + 1, self[1]))

    @property
    def west(self):
        return Position((self[0], self[1] - 1))

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
    EXTERNAL_TRAVERSABLE = {".", " "}

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

    def _expand(self):
        new_board = []
        for row in self.board:
            new_row_0 = []
            new_row_1 = []
            for col in row:
                if col == "│":
                    new_row_0 += ["│", " "]
                    new_row_1 += ["│", " "]
                elif col == "─":
                    new_row_0 += ["─", "─"]
                    new_row_1 += [" ", " "]
                elif col == "└":
                    new_row_0 += ["└", "─"]
                    new_row_1 += [" ", " "]
                elif col == "┘":
                    new_row_0 += ["┘", " "]
                    new_row_1 += [" ", " "]
                elif col == "┌":
                    new_row_0 += ["┌", "─"]
                    new_row_1 += ["│", " "]
                elif col == "┐":
                    new_row_0 += ["┐", " "]
                    new_row_1 += ["│", " "]
                elif col == ".":
                    new_row_0 += [".", " "]
                    new_row_1 += [" ", " "]
            new_board.append(new_row_0)
            new_board.append(new_row_1)
        self.board = np.array(new_board)

    def get_internal_area(self):
        self._expand()
        self._bfs_external()
        return (self.board == ".").sum()

    def _bfs_external(self):
        self.queue = [Position((0, 0))]
        while len(self.queue) > 0:
            pos = self.queue.pop(0)
            self._bfs_external_north(pos)
            self._bfs_external_south(pos)
            self._bfs_external_west(pos)
            self._bfs_external_east(pos)

    def _bfs_external_north(self, pos):
        if self.board[pos.north] in self.EXTERNAL_TRAVERSABLE:
            self.board[pos.north] = "O"
            self.queue.append(pos.north)

    def _bfs_external_south(self, pos):
        if self.board[pos.south] in self.EXTERNAL_TRAVERSABLE:
            self.board[pos.south] = "O"
            self.queue.append(pos.south)

    def _bfs_external_west(self, pos):
        if self.board[pos.west] in self.EXTERNAL_TRAVERSABLE:
            self.board[pos.west] = "O"
            self.queue.append(pos.west)

    def _bfs_external_east(self, pos):
        if self.board[pos.east] in self.EXTERNAL_TRAVERSABLE:
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
    main()
