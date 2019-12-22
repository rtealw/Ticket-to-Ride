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
import rankings

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

points_figure.countAndPlot()

simulation_figures.readGamesAndGenerateFigures("../../Ticket-to-Ride-Engine/output/games.txt", limit = 30)

route_measures_figures.all_measures()

pairs = find_resistance_between_pairs()
resistance_figures.resistance_figure_no_props(pairs=pairs)
results_aggregate = resistance_figures.resistance_figure_aggregate(pairs=pairs, cmapname='autumn')
results_two = resistance_figures.resistance_figure(pairs=pairs, num_players="two")
results_four = resistance_figures.resistance_figure(pairs=pairs, num_players="four")

metric_figure.get_metrics(results_two, results_four, results_aggregate)

rankings.generate_rankings()
