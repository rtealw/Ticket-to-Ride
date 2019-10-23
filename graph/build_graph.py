import numpy as np
import pandas as pd

cities = ['vanc', 'seat', 'port', 'sanf', 'losa', 'elpa', 'phoe', 'lasv', 'sant', 'salt', 'hele', 'calg', 'winn', 'dulu', 'omah', 'denv', 'okla', 'dall', 'hous', 'newo', 'litt', 'sain', 'kans', 'chic', 'saul', 'toro', 'mont', 'bost', 'newy', 'wash', 'pitt', 'rale', 'char', 'miam', 'atla', 'nash']
num_cities = len(cities)
edge_lengths = pd.DataFrame(np.zeros((num_cities, num_cities)), index=cities, columns=cities)
is_double = pd.DataFrame(np.full((num_cities, num_cities), False), index=cities, columns=cities)
is_wild = is_double.copy()

edge_lengths['vanc']['seat']=1
edge_lengths['vanc']['calg']=3

edge_lengths['seat']['port']=1
edge_lengths['seat']['calg']=4
edge_lengths['seat']['hele']=6

edge_lengths['port']['salt']=6
edge_lengths['port']['sanf']=5

edge_lengths['sanf']['salt']=5
edge_lengths['sanf']['losa']=3

edge_lengths['losa']['lasv']=2
edge_lengths['losa']['phoe']=3
edge_lengths['losa']['elpa']=6

edge_lengths['phoe']['elpa']=3
edge_lengths['phoe']['sant']=3
edge_lengths['phoe']['denv']=5

edge_lengths['lasv']['salt']=3

edge_lengths['salt']['denv']=3
edge_lengths['salt']['hele']=3

edge_lengths['calg']['hele']=4
edge_lengths['calg']['winn']=6

edge_lengths['hele']['winn']=4
edge_lengths['hele']['dulu']=6
edge_lengths['hele']['omah']=5
edge_lengths['hele']['denv']=4

edge_lengths['elpa']['hous']=6
edge_lengths['elpa']['dall']=4
edge_lengths['elpa']['okla']=5
edge_lengths['elpa']['sant']=2

edge_lengths['sant']['okla']=3
edge_lengths['sant']['denv']=2

edge_lengths['denv']['okla']=4
edge_lengths['denv']['kans']=4
edge_lengths['denv']['omah']=4

edge_lengths['winn']['saul']=6
edge_lengths['winn']['dulu']=4

edge_lengths['dulu']['saul']=3
edge_lengths['dulu']['toro']=6
edge_lengths['dulu']['chic']=3
edge_lengths['dulu']['omah']=2

edge_lengths['omah']['chic']=4
edge_lengths['omah']['kans']=1

edge_lengths['kans']['sain']=2
edge_lengths['kans']['okla']=2

edge_lengths['okla']['litt']=2
edge_lengths['okla']['dall']=2

edge_lengths['dall']['litt']=2
edge_lengths['dall']['hous']=1

edge_lengths['hous']['newo']=2

edge_lengths['newo']['litt']=3
edge_lengths['newo']['atla']=4
edge_lengths['newo']['miam']=6

edge_lengths['litt']['nash']=3
edge_lengths['litt']['sain']=2

edge_lengths['sain']['nash']=2
edge_lengths['sain']['pitt']=5
edge_lengths['sain']['chic']=2

edge_lengths['chic']['pitt']=3
edge_lengths['chic']['toro']=4

edge_lengths['saul']['toro']=2
edge_lengths['saul']['mont']=5

edge_lengths['toro']['mont']=3
edge_lengths['toro']['pitt']=2

edge_lengths['pitt']['newy']=2
edge_lengths['pitt']['wash']=2
edge_lengths['pitt']['rale']=2
edge_lengths['pitt']['nash']=4

edge_lengths['nash']['rale']=3
edge_lengths['nash']['atla']=1

edge_lengths['atla']['miam']=5
edge_lengths['atla']['char']=2
edge_lengths['atla']['rale']=2

edge_lengths['miam']['char']=4

edge_lengths['char']['rale']=2

edge_lengths['rale']['wash']=2

edge_lengths['wash']['newy']=2

edge_lengths['newy']['bost']=2
edge_lengths['newy']['mont']=3

edge_lengths['bost']['mont']=2

is_double['vanc']['seat']=True
is_double['seat']['port']=True
is_double['port']['sanf']=True
is_double['sanf']['salt']=True
is_double['sanf']['losa']=True
is_double['salt']['denv']=True
is_double['denv']['kans']=True
is_double['kans']['omah']=True
is_double['kans']['sain']=True
is_double['kans']['okla']=True
is_double['omah']['dulu']=True
is_double['okla']['dall']=True
is_double['dall']['hous']=True
is_double['sain']['chic']=True
is_double['newo']['atla']=True
is_double['atla']['rale']=True
is_double['rale']['wash']=True
is_double['chic']['pitt']=True
is_double['pitt']['newy']=True
is_double['wash']['newy']=True
is_double['bost']['newy']=True
is_double['bost']['mont']=True

is_wild['vanc']['calg']=True
is_wild['vanc']['seat']=True
is_wild['seat']['port']=True
is_wild['seat']['calg']=True
is_wild['calg']['hele']=True
is_wild['losa']['lasv']=True
is_wild['losa']['phoe']=True
is_wild['phoe']['sant']=True
is_wild['phoe']['elpa']=True
is_wild['elpa']['sant']=True
is_wild['sant']['denv']=True
is_wild['hous']['newo']=True
is_wild['hous']['dall']=True
is_wild['dall']['litt']=True
is_wild['dall']['okla']=True
is_wild['okla']['litt']=True
is_wild['okla']['kans']=True
is_wild['kans']['omah']=True
is_wild['dulu']['omah']=True
is_wild['dulu']['saul']=True
is_wild['winn']['saul']=True
is_wild['saul']['toro']=True
is_wild['toro']['mont']=True
is_wild['toro']['pitt']=True
is_wild['mont']['bost']=True
is_wild['pitt']['wash']=True
is_wild['pitt']['rale']=True
is_wild['wash']['rale']=True
is_wild['rale']['char']=True
is_wild['rale']['atla']=True
is_wild['atla']['char']=True
is_wild['atla']['nash']=True
is_wild['sain']['nash']=True
is_wild['sain']['litt']=True

def get_reverse_edges(graph, cities, default):
    for city1 in cities:
        for city2 in cities:
            if graph[city1][city2] != default:
                graph[city2][city1] = edge_lengths[city1][city2]

get_reverse_edges(edge_lengths, cities, 0)
get_reverse_edges(is_double, cities, False)
get_reverse_edges(is_wild, cities, False)
#print(edge_lengths)
#print(is_double)
#print(is_wild)

pairs = [{'city1':'toro', 'city2': 'miam', 'min_path': 10},{'city1': 'dulu', 'city2': 'hous', 'min_path':  8},{'city1': 'chic', 'city2': 'sant', 'min_path':  9},
         {'city1':'denv', 'city2': 'pitt', 'min_path': 11},{'city1': 'vanc', 'city2': 'sant', 'min_path': 13},{'city1': 'hele', 'city2': 'losa', 'min_path':  8},
         {'city1':'mont', 'city2': 'atla', 'min_path':  9},{'city1': 'denv', 'city2': 'elpa', 'min_path':  4},{'city1': 'vanc', 'city2': 'mont', 'min_path': 20},
         {'city1':'port', 'city2': 'phoe', 'min_path': 11},{'city1': 'dall', 'city2': 'newy', 'min_path': 11},{'city1': 'saul', 'city2': 'nash', 'min_path':  8},
         {'city1':'newy', 'city2': 'atla', 'min_path':  6},{'city1': 'losa', 'city2': 'chic', 'min_path': 16},{'city1': 'sanf', 'city2': 'atla', 'min_path': 17},
         {'city1':'saul', 'city2': 'okla', 'min_path':  9},{'city1': 'calg', 'city2': 'salt', 'min_path':  7},{'city1': 'dulu', 'city2': 'elpa', 'min_path': 10},
         {'city1':'losa', 'city2': 'newy', 'min_path': 21},{'city1': 'mont', 'city2': 'newo', 'min_path': 13},{'city1': 'chic', 'city2': 'newo', 'min_path':  7},
         {'city1':'kans', 'city2': 'hous', 'min_path':  5},{'city1': 'calg', 'city2': 'phoe', 'min_path': 13},{'city1': 'losa', 'city2': 'miam', 'min_path': 20},
         {'city1':'port', 'city2': 'nash', 'min_path': 17},{'city1': 'seat', 'city2': 'newy', 'min_path': 22},{'city1': 'winn', 'city2': 'litt', 'min_path': 11},
         {'city1':'seat', 'city2': 'losa', 'min_path':  9},{'city1': 'bost', 'city2': 'miam', 'min_path': 12},{'city1': 'winn', 'city2': 'hous', 'min_path': 12}]

def min_path(pair):
    return pair['min_path']

pairs.sort(key=min_path)
for i in range(len(pairs)):
    pair = pairs[i]
    pair['number'] = str(i + 1).zfill(2)

edge_lengths.to_csv('edge_lengths.csv')
is_double.to_csv('is_double.csv')
is_wild.to_csv('is_wild.csv')
np.savetxt('pairs.csv', pairs, fmt="%s")
np.savetxt('cities.csv', cities, fmt="%s")