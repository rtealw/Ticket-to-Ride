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

def betweenness_figure(num_players):
    betweenness = find_betweenness(weight="weights", count_double=False)
    keys, route_props = get_proportions("input/routes_{}.txt".format(num_players))
    route_betweenness = get_list(keys=keys, betweenness=betweenness)
    plt.scatter(x=route_props, y=route_betweenness)
    plt.show()


betweenness_figure(num_players="two")