#!/usr/bin/env python3

import re
import networkx as nx


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    graph = nx.Graph()

    for line in lines:
        match = re.search("(?P<src>.*):(?P<dsts>.*)", line)
        src = match.group("src")
        dsts = match.group("dsts").strip().split(" ")

        for dst in dsts:
            graph.add_edge(src, dst)

    return graph


def solve(graph):
    """
    If 3 edges can be cut to disconnect the graph, these 3 edges should have
    high centrality.  Cut the 3 highest centralities, ensure graph is
    disconnected, multiply sizes of connected components for answer.
    """
    centralities = nx.edge_betweenness_centrality(graph)
    centralities = [(centrality, edge) for edge, centrality in centralities.items()]
    centralities = sorted(centralities)

    graph.remove_edge(*centralities.pop(-1)[1])
    graph.remove_edge(*centralities.pop(-1)[1])
    graph.remove_edge(*centralities.pop(-1)[1])
    assert not nx.is_connected(graph)

    connected_components = list(nx.connected_components(graph))
    assert len(connected_components) == 2
    return len(connected_components[0]) * len(connected_components[1])


def main(filename="input.txt"):
    print(f"part 1:  {solve(parse(read_file(filename)))}")


if __name__ == "__main__":
    main("test.txt")
    main()
