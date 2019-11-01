import numpy as np
import pandas as pd
import csv
from resistance import find_resistance
from generate_figures import generate_figure
from scipy.special import comb as choose
import matplotlib.pyplot as plt
import networkx as nx

def generate_resistance_graph(path="../graph/"):
    edge_lengths = pd.read_csv('{}edge_lengths.csv'.format(path), index_col=0)
    is_double = pd.read_csv('{}is_double.csv'.format(path), index_col=0)
    is_wild = pd.read_csv('{}is_wild.csv'.format(path), index_col=0)
    resistance_graph = np.array(edge_lengths)
    return resistance_graph

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

def find_resistance_between_pairs(path="../graph/"):
    resistance_graph = generate_resistance_graph() 
    cities = list(np.genfromtxt('{}cities.csv'.format(path), dtype=str))
    pairs = [eval(",".join(line)) for line in csv.reader(open('{}pairs.csv'.format(path)))]

    for pair in pairs:
        index1 = cities.index(pair["city1"])
        index2 = cities.index(pair["city2"])
        pair_resistance = find_resistance(resistance_graph, index1, index2)
        pair["resistance"] = pair_resistance
    return pairs

def hash_edge(node1, node2):
    return tuple(sorted([node1, node2]))
#    return "/".join(str(node) for node in sorted([node1, node2]))

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
#    
#    print(networkx_betweenness)
    betweenness = {}
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
    # normalize
    for edge in betweenness.keys():
        betweenness[edge] *= float(2)/(len(G) * (len(G) - 1))
    return betweenness

def test_betweenness(tolerance=1e-5):
    G = generate_networkx_graph()
    networkx_betweenness = nx.algorithms.centrality.edge_betweenness_centrality(G=G, normalized=True, weight="weight")
    simple_betweenness = find_betweenness(weight="random", count_double=False)
    for edge in networkx_betweenness.keys():
        if np.absolute(networkx_betweenness[edge] - simple_betweenness[edge]) > tolerance:
            print("Edge:", edge)
            print("Networkx:", networkx_betweenness[edge])
            print("Simple:", simple_betweenness[edge])
            raise "Networkx and simple betweenness are not the same"


def find_probability_pair():
    ways_no_pair = 0
    # Choose between 0 and 2 locomotives and then remaining colors
    for num_locomotives in range(3):
        num_not_loco = 5 - num_locomotives
        ways_no_pair += 12 ** (num_not_loco) * choose(8, num_not_loco) * choose(14, num_locomotives)
    ways = choose(110, 5)
    probability_no_pair = ways_no_pair / ways
    return 1 - probability_no_pair

#print(find_probability_pair())


# ASSUMPTIONS
## The ratio of colors is independent between turns
## A player will not use locomotives to buy routes

#pairs = find_resistance_between_pairs()
#generate_figure(pairs=pairs, num_players="two")
#generate_figure(pairs=pairs, num_players="four")

#test_betweenness()
betweenness = find_betweenness()
print(betweenness)