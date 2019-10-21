import numpy as np
import pandas as pd
import csv
from resistance import find_resistance
from scipy.special import comb as choose
import matplotlib.pyplot as plt

def generate_resistance_graph():
    edge_lengths = pd.read_csv('graph/edge_lengths.csv', index_col=0)
    is_double = pd.read_csv('graph/is_double.csv', index_col=0)
    is_wild = pd.read_csv('graph/is_wild.csv', index_col=0)
    resistance_graph = np.array(edge_lengths)
    return resistance_graph

def find_resistance_between_pairs():
    resistance_graph = generate_resistance_graph()
    cities = list(np.genfromtxt('graph/cities.csv', dtype=str))
    pairs = [eval(",".join(line)) for line in csv.reader(open('graph/pairs.csv'))]

    for pair in pairs:
        index1 = cities.index(pair["city1"])
        index2 = cities.index(pair["city2"])
        pair_resistance = find_resistance(resistance_graph, index1, index2)
        pair["resistance"] = pair_resistance
    return pairs

def generate_figure(pairs):
    ys = []
    for pair in pairs:
        x, y = pair['resistance'], pair['min_path']
        ys.append(y)
        plt.scatter(x, y, s=2**8)
        label = pair['city1'] + '/' + pair['city2']
        plt.annotate(label.upper(),
                    (x,y),
                    textcoords="offset points",
                    xytext=(0,10),
                    ha='center',
                    rotation=(30),
                    fontsize=7,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white"))
    plt.yticks(range(min(ys), max(ys)+1, 2)) # integer y axis
    plt.show()

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

pairs = find_resistance_between_pairs()
generate_figure(pairs)