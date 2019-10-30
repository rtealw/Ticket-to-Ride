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
    node_labels = {i : cities[i] for i in range(len(cities))}
    pos=nx.get_node_attributes(G,'pos')
    edge_labels = nx.get_edge_attributes(G,'weight')
    nx.draw(G, labels=node_labels)
    #nx.draw_networkx_edge_labels(G,pos=nx.spring_layout(G), edge_labels=edge_labels)
    plt.show()

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

generate_networkx_graph()