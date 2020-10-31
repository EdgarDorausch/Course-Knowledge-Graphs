from io import UnsupportedOperation
from sys import argv
import networkx
import matplotlib
from matplotlib import pyplot as plt
import math
from typing import *


def read_graph(filename):
    with open(filename, 'r') as f:
        first_line = f.readline()
        num_of_vertecies = int(first_line)

        G = networkx.DiGraph()
        G.add_nodes_from(range(num_of_vertecies))

        for line in f.readlines():
            a, b = line.split(' ')
            first_vertex = int(a)
            second_vertex = int(b)
            G.add_edge(first_vertex, second_vertex)

        return G
        
def draw_graph(G):
    pos = networkx.layout.kamada_kawai_layout(G)

    node_sizes = [0 for i in range(len(G))]
    M = G.number_of_edges()
    edge_colors = range(2, M + 2)
    edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

    nodes = networkx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="blue")
    networkx.draw_networkx_labels(G, pos)

    networkx.draw_networkx_edges(
        G,
        pos,
        # node_size=node_sizes,
        arrowstyle="->",
    )
    plt.show()


def max_out_degree(G: networkx.DiGraph):
    max_degree = -1
    max_nodes = set()
    for node in G.nodes:
        if G.out_degree(node) > max_degree:
            max_degree = G.out_degree(node)
            max_nodes = {node}

        elif G.out_degree(node) == max_degree:
            max_nodes.add(node)

    return max_nodes
        

def min_in_degree(G: networkx.DiGraph):
    min_degree: Union[int, float] = math.inf
    min_nodes = set()
    for node in G.nodes:
        if G.in_degree(node) < min_degree:
            min_degree = G.in_degree(node)
            min_nodes = {node}

        elif G.in_degree(node) == min_degree:
            min_nodes.add(node)

    return min_nodes
        



if __name__ == "__main__":
    filename = argv[1]
    
    G = read_graph(filename)
    print('Max:', max_out_degree(G))
    print('Min:', min_in_degree(G))

    draw_graph(G)

    

