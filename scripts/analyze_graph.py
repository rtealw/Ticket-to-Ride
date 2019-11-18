import numpy as np
import pandas as pd
import csv
from resistance import find_resistance
from resistance_figures import resistance_figure
from scipy.special import comb as choose
import matplotlib.pyplot as plt
import networkx as nx
from route_measures_figures import all_measures

def generate_resistance_graph(path="../graph/"):
    edge_lengths = pd.read_csv('{}edge_lengths.csv'.format(path), index_col=0)
    is_double = pd.read_csv('{}is_double.csv'.format(path), index_col=0)
    is_wild = pd.read_csv('{}is_wild.csv'.format(path), index_col=0)
    resistance_graph = np.array(edge_lengths - edge_lengths.mul(is_double) / 2)
    return resistance_graph

def find_resistance_between_pairs(path="../graph/"):
    resistance_graph = generate_resistance_graph(path=path) 
    cities = list(np.genfromtxt('{}cities.csv'.format(path), dtype=str))
    pairs = [eval(",".join(line)) for line in csv.reader(open('{}pairs.csv'.format(path)))]

    for pair in pairs:
        index1 = cities.index(pair["city1"])
        index2 = cities.index(pair["city2"])
        pair_resistance = find_resistance(resistance_graph, index1, index2)
        pair["resistance"] = pair_resistance
    return pairs

all_measures()

pairs = find_resistance_between_pairs()
resistance_figure(pairs=pairs, num_players="two")
resistance_figure(pairs=pairs, num_players="four")
