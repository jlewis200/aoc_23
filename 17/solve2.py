#!/usr/bin/env python3

import numpy as np
import networkx as nx


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_board(lines):
    return np.array([list(map(int, list(line.strip()))) for line in lines])


def arr_str(array):
    return "\n".join("".join(str(col) for col in row) for row in array)


def build_graph(board, min_dst=1, max_dst=3):
    graph = nx.DiGraph()
    add_start(graph)
    add_end(board, graph)
    for idx in range(board.shape[0]):
        for jdx in range(board.shape[1]):
            add_north_edges(idx, jdx, board, graph, min_dst, max_dst)
            add_west_edges(idx, jdx, board, graph, min_dst, max_dst)
            add_south_edges(idx, jdx, board, graph, min_dst, max_dst)
            add_east_edges(idx, jdx, board, graph, min_dst, max_dst)
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


def add_east_edges(idx, jdx, board, graph, min_dst=1, max_dst=3):
    weight = board[idx, jdx + 1 : jdx + min_dst].sum()
    for kdx in range(jdx + min_dst, jdx + max_dst + 1):
        if kdx >= board.shape[1]:
            continue
        src = f"{idx} {jdx} H"
        dst = f"{idx} {kdx} V"
        weight += int(board[idx, kdx])
        graph.add_edge(src, dst, weight=weight)


def add_west_edges(idx, jdx, board, graph, min_dst=1, max_dst=3):
    weight = board[idx, max(0, jdx - min_dst + 1) : jdx].sum()
    for kdx in range(jdx - min_dst, jdx - max_dst - 1, -1):
        if kdx < 0:
            continue
        src = f"{idx} {jdx} H"
        dst = f"{idx} {kdx} V"
        weight += int(board[idx, kdx])
        graph.add_edge(src, dst, weight=weight)


def add_south_edges(idx, jdx, board, graph, min_dst=1, max_dst=3):
    weight = board[idx + 1 : idx + min_dst, jdx].sum()
    for kdx in range(idx + min_dst, idx + max_dst + 1):
        if kdx >= board.shape[0]:
            continue
        src = f"{idx} {jdx} V"
        dst = f"{kdx} {jdx} H"
        weight += int(board[kdx, jdx])
        graph.add_edge(src, dst, weight=weight)


def add_north_edges(idx, jdx, board, graph, min_dst=1, max_dst=3):
    weight = board[max(0, idx - min_dst + 1) : idx, jdx].sum()
    for kdx in range(idx - min_dst, idx - max_dst - 1, -1):
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
    print(f"part 1:  {get_shortest_path_weight(build_graph(board))}")
    print(f"part 2:  {get_shortest_path_weight(build_graph(board, 4, 10))}")


if __name__ == "__main__":
    main("test.txt")
    main("test2.txt")
    main()
