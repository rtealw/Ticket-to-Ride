import numpy as np
import pandas as pd
import csv
import scipy.stats
import resistance

import points_figure
import simulation_figures
import route_measures_figures
import resistance_figures
import metric_figure

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
        pair_resistance = resistance.find_resistance(resistance_graph, index1, index2)
        pair["resistance"] = pair_resistance
    return pairs

#points_figure.countAndPlot()
#
#simulation_figures.readGamesAndGenerateFigures("../../Ticket-to-Ride-Engine/output/games.txt", limit = 30)
#
#route_measures_figures.all_measures()
#
#pairs = find_resistance_between_pairs()
#resistance_figures.resistance_figure_no_props(pairs=pairs)
#results_aggregate = resistance_figures.resistance_figure_aggregate(pairs=pairs)
#results_two = resistance_figures.resistance_figure(pairs=pairs, num_players="two")
#results_four = resistance_figures.resistance_figure(pairs=pairs, num_players="four")
#
#metric_figure.get_metrics(results_two, results_four, results_aggregate)

results_file = open('input/results.txt', 'r')
results = eval(results_file.read())
results_file.close()

def orderXbyY(X, Y):
    ordered_X = [x for _, x in sorted(zip(Y,X), key = lambda pair: pair[0])]
    ordered_X.reverse()
    return ordered_X

import matplotlib.pyplot as plt
names_by_paths = orderXbyY(X=results['names'], Y=results['path_length'])
names_by_residuals = orderXbyY(X=results['names'], Y=results['distance'])
total = float(len(names_by_paths))
for name in names_by_paths:
    i = names_by_paths.index(name) + 1
    j = names_by_residuals.index(name) + 1
    xi = 0
    yi = 1 - i / total
    xj = .1
    yj = 1 - j / total
    plt.plot([xi, xj], [yi, yj], c='black', linestyle='-', marker='o')
    plt.text(x=xj+.01, y=yj-.01, s=name)
plt.tight_layout()
plt.axis('off')
plt.show()
