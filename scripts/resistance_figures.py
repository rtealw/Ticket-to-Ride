import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['figure.figsize'] = 10, 5.8

LONG_CITIES = ['ATLANTA', 'BOSTON', 'CALGARY', 'CHARLESTON', 'CHICAGO', 'DALLAS', 'DENVER', 'DULUTH', 'EL PASO', 'HELENA', 'HOUSTON', 'KANSAS CITY', 'LAS VEGAS', 'LITTLE ROCK', 'LOS ANGELES', 'MIAMI', 'MONTREAL', 'NASHVILLE', 'NEW ORLEANS', 'NEW YORK', 'OKLAHOMA CITY', 'OMAHA', 'PHOENIX', 'PITTSBURGH', 'PORTLAND', 'RALEIGH', 'SAINT LOUIS', 'SALT LAKE CITY', 'SAN FRANCISCO', 'SANTA FE', 'SAULT ST. MARIE', 'SEATTLE', 'TORONTO', 'VANCOUVER', 'WASHINGTON', 'WINNIPEG']
SHORT_CITIES = [city.replace(" ", "")[:4] for city in LONG_CITIES]

def lengthen_edge(city1, city2):
    new_edge = ""
    for city in sorted([city1, city2]):
        long_city = LONG_CITIES[SHORT_CITIES.index(city.upper())]
        new_city = ""
        for word in long_city.split(" "):
            new_city += word.capitalize() + " "
        new_edge += new_city[:-1] + "/"
    return new_edge[:-1]

def get_proportions(filename):
    text_file = open(filename, 'r')
    keys = eval(text_file.readline())
    props = eval(text_file.readline())
    text_file.close()
    return keys, props

def get_color(cmap, edge, keys, props):
    current_prop = props[keys.index(edge.upper())]
    standardized_prop = (current_prop - min(props)) / (max(props) - min(props))
    return cmap(standardized_prop)

def resistance_figure(pairs, num_players):
    xs, ys, props = [], [], []
    fig, ax = plt.subplots()
    cmap = plt.cm.get_cmap('RdYlGn')
    keys, props = get_proportions("input/tickets_{}.txt".format(num_players))
    for pair in pairs:
        x, y, number = pair['resistance'], pair['min_path'], pair['number']
        xs.append(x)
        ys.append(y)
        edge = lengthen_edge(pair['city1'], pair['city2'])
        label = "{} {}".format(number, edge)
        color = get_color(cmap=cmap, edge=edge, keys=keys, props=props)
        ax.annotate(number, (x,y), ha='center', va='center', fontsize=8,
                           bbox=dict(boxstyle="circle,pad=0.3", fc=color))
        ax.scatter(x,y, s=2, label=label)

    interval = np.linspace(min(xs), max(xs), 100)
    best_fit_func = np.poly1d(np.polyfit(xs, ys, deg=1))

    plt.plot(interval, best_fit_func(interval), color="black")

    # Shrink current axis
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    plt.xlim(min(xs) * .5, max(xs) * 1.1)
    plt.ylim(min(ys) * .5, max(ys) * 1.1)
    plt.yticks(range(min(ys), max(ys)+1, 2)) # integer y axis
    title = "Destination Tickets by Reward vs. Difficulty"
    subtitle = "Colored by Proportion of {} Player Wins".format(num_players.capitalize())
    plt.title("{}\n{}".format(title, subtitle))
    plt.xlabel("Effective Resistance")
    plt.ylabel("Length of Minimum Path")
    legend = ax.legend(
        bbox_to_anchor = (1, 1.01),
        handlelength = 0, 
        handletextpad=0,
        fontsize=7.4
    )
    for item in legend.legendHandles:
        item.set_visible(False)

    cbaxes = fig.add_axes([.05, box.y0, 0.01, box.height])
    cbar = fig.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=ax, cax=cbaxes)
    cbar_labels = [min(props) + x * (max(props) - min(props))/5 for x in range(6)]
    cbar.ax.set_yticklabels([str(round(label, 2))[1:] for label in cbar_labels])
    cbar.ax.yaxis.set_ticks_position('left')
    cbar.ax.set_label("Proportion of Wins")
 
    plt.savefig("../paper/figures/resistance_{}.eps".format(num_players))
    plt.close()
