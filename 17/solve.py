#!/usr/bin/env python3

import numpy as np
import networkx as nx


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_board(lines):
    return np.array([list(map(int, list(line.strip()))) for line in lines])


class CrucibleGraph(nx.DiGraph):
    def __init__(self, board, min_dst=1, max_dst=3):
        super().__init__()
        self.board = board
        self.min_dst = min_dst
        self.max_dst = max_dst
        self.build_graph()

    def build_graph(self):
        self.add_start()
        self.add_end()
        for idx in range(self.board.shape[0]):
            for jdx in range(self.board.shape[1]):
                self.add_north_edges(idx, jdx)
                self.add_west_edges(idx, jdx)
                self.add_south_edges(idx, jdx)
                self.add_east_edges(idx, jdx)

    def add_start(self):
        self.add_edge("start", self.h_node(0, 0), weight=0)
        self.add_edge("start", self.v_node(0, 0), weight=0)

    def add_end(self):
        idx = self.board.shape[0] - 1
        jdx = self.board.shape[1] - 1
        self.add_edge(self.h_node(idx, jdx), "end", weight=0)
        self.add_edge(self.v_node(idx, jdx), "end", weight=0)

    def add_east_edges(self, idx, jdx):
        weight = self.board[idx, jdx + 1 : jdx + self.min_dst].sum()
        for kdx in range(jdx + self.min_dst, jdx + self.max_dst + 1):
            if kdx >= self.board.shape[1]:
                break
            weight += self.board[idx, kdx]
            self.add_edge(self.h_node(idx, jdx), self.v_node(idx, kdx), weight=weight)

    def add_west_edges(self, idx, jdx):
        weight = self.board[idx, max(0, jdx - self.min_dst + 1) : jdx].sum()
        for kdx in range(jdx - self.min_dst, jdx - self.max_dst - 1, -1):
            if kdx < 0:
                break
            weight += self.board[idx, kdx]
            self.add_edge(self.h_node(idx, jdx), self.v_node(idx, kdx), weight=weight)

    def add_south_edges(self, idx, jdx):
        weight = self.board[idx + 1 : idx + self.min_dst, jdx].sum()
        for kdx in range(idx + self.min_dst, idx + self.max_dst + 1):
            if kdx >= self.board.shape[0]:
                break
            weight += self.board[kdx, jdx]
            self.add_edge(self.v_node(idx, jdx), self.h_node(kdx, jdx), weight=weight)

    def add_north_edges(self, idx, jdx):
        weight = self.board[max(0, idx - self.min_dst + 1) : idx, jdx].sum()
        for kdx in range(idx - self.min_dst, idx - self.max_dst - 1, -1):
            if kdx < 0:
                break
            weight += self.board[kdx, jdx]
            self.add_edge(self.v_node(idx, jdx), self.h_node(kdx, jdx), weight=weight)

    def get_shortest_path_weight(self):
        path = nx.shortest_path(self, source="start", target="end", weight="weight")
        return nx.path_weight(self, path, weight="weight")

    @staticmethod
    def h_node(idx, jdx):
        return f"{idx} {jdx} H"

    @staticmethod
    def v_node(idx, jdx):
        return f"{idx} {jdx} V"

    def __str__(self):
        return "\n".join("".join(str(col) for col in row) for row in self.board)


def main(filename="input.txt"):
    board = parse_board(read_file(filename))
    print(f"part 1:  {CrucibleGraph(board).get_shortest_path_weight()}")
    print(f"part 2:  {CrucibleGraph(board, 4, 10).get_shortest_path_weight()}")


if __name__ == "__main__":
    main("test.txt")
    main("test2.txt")
    main()
