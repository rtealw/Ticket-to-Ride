from betweenness import find_betweenness
import matplotlib.pyplot as plt
import pandas as pd
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

def get_list(keys, betweenness):
    route_betweenness = []
    for key in keys:
        key_betweenness = cities_to_nums(key)
        route_betweenness.append(betweenness[key_betweenness])
    return route_betweenness

def betweenness_figure():
    betweenness = find_betweenness(weight="weights", count_double=False)
    keys, route_two = get_proportions("input/routes_two.txt")
    keys, route_four = get_proportions("input/routes_four.txt")
    route_betweenness = get_list(keys=keys, betweenness=betweenness)

    plt.scatter(x=route_two, y=route_betweenness, marker="h", s=2**6, color="brown", label="Two")
    plt.scatter(x=route_four, y=route_betweenness, marker="H", s=2**6, color="teal", label="Four")
    plt.title("Claims per Game vs. Betweenness Centrality")
    plt.xlabel("Claims per Game")
    plt.ylabel("Betweenness Centrality")
    plt.legend(title="Players")

    plt.savefig("../paper/figures/betweenness.eps")
