#!/usr/bin/env python3

import numpy as np
import networkx as nx


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_board(lines):
    return np.array([list(line.strip()) for line in lines])


def arr_str(array):
    return "\n".join("".join(row) for row in array)


def build_graph(board):
    graph = nx.DiGraph()
    add_start(graph)
    add_end(board, graph)
    for idx in range(board.shape[0]):
        for jdx in range(board.shape[1]):
            add_north_edges(idx, jdx, board, graph)
            add_west_edges(idx, jdx, board, graph)
            add_south_edges(idx, jdx, board, graph)
            add_east_edges(idx, jdx, board, graph)
    return graph


def add_start(graph):
    src = "start"
    idx, jdx = 0, 0
    dst_0 = f"{idx} {jdx} H"
    dst_1 = f"{idx} {jdx} V"
    graph.add_edge(src, dst_0, weight=0)
    graph.add_edge(src, dst_1, weight=0)


def add_end(board, graph):
    idx, jdx = board.shape
    idx -= 1
    jdx -= 1
    src_0 = f"{idx} {jdx} H"
    src_1 = f"{idx} {jdx} V"
    dst = "end"
    graph.add_edge(src_0, dst, weight=0)
    graph.add_edge(src_1, dst, weight=0)


def add_east_edges(idx, jdx, board, graph):
    weight = 0
    for kdx in range(jdx + 1, jdx + 4):
        if kdx >= board.shape[1]:
            continue
        src = f"{idx} {jdx} H"
        dst = f"{idx} {kdx} V"
        weight += int(board[idx, kdx])
        graph.add_edge(src, dst, weight=weight)


def add_west_edges(idx, jdx, board, graph):
    weight = 0
    for kdx in range(jdx - 1, jdx - 4, -1):
        if kdx < 0:
            continue
        src = f"{idx} {jdx} H"
        dst = f"{idx} {kdx} V"
        weight += int(board[idx, kdx])
        graph.add_edge(src, dst, weight=weight)


def add_south_edges(idx, jdx, board, graph):
    weight = 0
    for kdx in range(idx + 1, idx + 4):
        if kdx >= board.shape[0]:
            continue
        src = f"{idx} {jdx} V"
        dst = f"{kdx} {jdx} H"
        weight += int(board[kdx, jdx])
        graph.add_edge(src, dst, weight=weight)


def add_north_edges(idx, jdx, board, graph):
    weight = 0
    for kdx in range(idx - 1, idx - 4, -1):
        if kdx < 0:
            continue
        src = f"{idx} {jdx} V"
        dst = f"{kdx} {jdx} H"
        weight += int(board[kdx, jdx])
        graph.add_edge(src, dst, weight=weight)


def get_shortest_path_weight(graph):
    path = nx.shortest_path(graph, source="start", target="end", weight="weight")
    return nx.path_weight(graph, path, weight="weight")


def main(filename="input.txt"):
    board = parse_board(read_file(filename))
    # print(arr_str(board))
    graph = build_graph(board)
    print(f"part 1:  {get_shortest_path_weight(graph)}")
    print(f"part 2:  {None}")


if __name__ == "__main__":
    main("test.txt")
    main()
