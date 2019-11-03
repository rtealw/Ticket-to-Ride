from route_measures import find_betweenness, find_current_flow
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
plt.rcParams['figure.figsize'] = 10, 5.8

def get_proportions(filename):
    text_file = open(filename, 'r')
    keys = eval(text_file.readline())
    props = eval(text_file.readline())
    text_file.close()
    return keys, props

def cities_to_nums(cities):
    city1, city2 = tuple(cities.lower().split("/"))
    original_cities = list(pd.read_csv('../graph/is_double.csv', index_col=0))
    original_index1 = original_cities.index(city1.replace(" ", "")[:4])
    original_index2 = original_cities.index(city2.replace(" ", "")[:4])

    return tuple(sorted([original_index1, original_index2]))

def get_list(keys, measure):
    route_measure = []
    for key in keys:
        key_measure = cities_to_nums(key)
        if key_measure not in measure:
            route_measure.append(measure[(key_measure[1], key_measure[0])])
        else:
            route_measure.append(measure[key_measure])
    return route_measure

def measure_figure(measure, xlabel, filename):
    keys, route_two = get_proportions("input/routes_two.txt")
    keys, route_four = get_proportions("input/routes_four.txt")
    route_measure = get_list(keys=keys, measure = measure)

    plt.scatter(x=route_measure, y=route_two, marker="h", s=2**6, color="brown", label="Two")
    plt.scatter(x=route_measure, y=route_four, marker="H", s=2**6, color="teal", label="Four")
    plt.title("Edges")
    plt.ylabel("Claims per Game")
    plt.xlabel(xlabel)
    plt.legend(title="Players")

    plt.savefig("../paper/figures/centrality_{}.eps".format(filename))
    plt.close()

betweenness = find_betweenness()
current_flow = find_current_flow()
measure_figure(measure=betweenness, xlabel="Betweenness Centrality", filename="betweenness")
measure_figure(measure=current_flow, xlabel="Current Flow Centrality", filename="current_flow")