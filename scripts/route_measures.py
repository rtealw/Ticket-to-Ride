import pandas as pd
import networkx as nx
import numpy as np
from termcolor import cprint

def generate_networkx_graph(path="../graph/"):
    edge_lengths = pd.read_csv('{}edge_lengths.csv'.format(path), index_col=0)
    is_double = pd.read_csv('{}is_double.csv'.format(path), index_col=0)
    G = nx.MultiGraph()
    cities = list(edge_lengths)
    for i in range(len(edge_lengths)):
        city1 = cities[i]
        for j in range(i+1, len(edge_lengths)):
            city2 = cities[j]
            weight = edge_lengths[city1][city2]
            if weight > 0:
                G.add_edge(i, j, weight=weight)
                if is_double[city1][city2]:
                    G.add_edge(i, j, weight=weight)
    return G

def hash_edge(node1, node2):
    return tuple(sorted([node1, node2]))

def get_st_num_edge(paths, multiplicities):
    st_num_edge = {}
    for path_index in range(len(paths)):
        path = paths[path_index]
        for start_index in range(len(path)-1):
            node1 = path[start_index]
            node2 = path[start_index+1]
            edge = hash_edge(node1, node2)
            if edge not in st_num_edge:
                st_num_edge[edge] = 0
            st_num_edge[edge] += multiplicities[path_index]
    return st_num_edge

def get_multiplicities(paths, count_double = True, filepath = '../graph/'):
    is_double = pd.read_csv('{}is_double.csv'.format(filepath), index_col=0)
    cities = list(is_double)
    multiplicities = [1] * len(paths)
    for path_index in range(len(paths)):
        path = paths[path_index]
        for start_index in range(len(path)-1):
            node1 = path[start_index]
            node2 = path[start_index+1]
            if is_double[cities[node1]][cities[node2]] and count_double:
                multiplicities[path_index] *= 2
    return multiplicities

def find_betweenness(weight="weight", count_double=True):
    G = generate_networkx_graph()
    betweenness = {}
    edges = []
    for s in range(len(G)):
        for t in range(s+1, len(G)):
            paths = list(nx.all_shortest_paths(G, source=s, target=t, weight=weight))
            multiplicities = get_multiplicities(paths, count_double=count_double)
            st_num = sum(multiplicities)
            st_num_edge = get_st_num_edge(paths, multiplicities)
            for edge in st_num_edge.keys():
                if edge not in betweenness:
                    betweenness[edge] = 0
                betweenness[edge] += float(st_num_edge[edge])/st_num
            edges.append((s,t))
    # Normalize
    for edge in edges:
        if edge not in betweenness:
            betweenness[edge] = 0
        else:
            betweenness[edge] *= float(2)/(len(G) * (len(G) - 1))
    return betweenness

def find_current_flow():
    G = generate_networkx_graph()
    return nx.edge_current_flow_betweenness_centrality(G=G, weight="weight")

def test_find_betweenness(tolerance=1e-5):
    print("Testing unweighted, single-edge betweenness...")
    G = generate_networkx_graph()
    networkx_betweenness = nx.edge_betweenness_centrality(G=G, normalized=True, weight="weight")
    simple_betweenness = find_betweenness(weight="random", count_double=False)
    for edge in networkx_betweenness.keys():
        hashed_edge = hash_edge(edge[0], edge[1])
        if np.absolute(networkx_betweenness[edge] - simple_betweenness[hashed_edge]) > tolerance:
            cprint("Failed :(", "red")
            print("Edge:", edge)
            print("Networkx: ", end= " ")
            cprint(networkx_betweenness[edge], "red")
            print("Simple: ", end=" ")
            cprint(simple_betweenness[edge], "red")
            return
    cprint("Passed :)", "green")

if __name__ == "__main__":
    test_find_betweenness()
