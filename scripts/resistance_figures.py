import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
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
    return cmap(standardized_prop), current_prop

def resistance_figure_no_props(pairs):
    xs, ys = [], []
    fig, ax = plt.subplots()
    for pair in pairs:
        x, y, number = pair['resistance'], pair['min_path'], pair['number']
        xs.append(x)
        ys.append(y)
        edge = lengthen_edge(pair['city1'], pair['city2'])
        label = "{} {}".format(number, edge)
        ax.annotate(number, (x,y), ha='center', va='center', fontsize=8,
                    bbox=dict(boxstyle="circle,pad=0.3", fc='white'))
        ax.scatter(x,y, s=2, label=label) 

    interval = np.linspace(min(xs), max(xs), 100)
    best_fit_func = np.poly1d(np.polyfit(xs, ys, deg=1))
    plt.plot(interval, best_fit_func(interval), color="black")

    plt.xlim(min(xs) * .5, max(xs) * 1.1)
    plt.ylim(min(ys) * .5, max(ys) * 1.1)
    plt.yticks(range(min(ys), max(ys)+1, 2)) # integer y axis
    plt.title("Destination Tickets by Reward and Difficulty")
    plt.ylabel("Length of Minimum Path")
    plt.xlabel("Effective Resistance")
    legend = ax.legend(
        bbox_to_anchor = (1, 1.01),
        handlelength = 0, 
        handletextpad=0,
        fontsize=7.5
    )
    for item in legend.legendHandles:
        item.set_visible(False)

    plt.tight_layout()
    plt.savefig("../paper/figures/resistance.eps")
    plt.close()

    distances=get_distance(best_fit_func, xs, ys)
    return  {
        'resistance': xs, 
        'path_length': ys,
        'distance' : distances
    }

def resistance_figure(pairs, num_players):
    xs, ys, props = [], [], []
    win_props = []
    fig, ax = plt.subplots()
    cmap = plt.cm.get_cmap('RdYlGn')
    keys, props = get_proportions("input/tickets_{}.txt".format(num_players))
    for pair in pairs:
        x, y, number = pair['resistance'], pair['min_path'], pair['number']
        xs.append(x)
        ys.append(y)
        edge = lengthen_edge(pair['city1'], pair['city2'])
        label = "{} {}".format(number, edge)
        color, current_prop = get_color(cmap=cmap, edge=edge, keys=keys, props=props)
        win_props += [current_prop]
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

    distances=get_distance(best_fit_func, xs, ys)
    win_label = str(num_players) + '_proportion'
    return  {
        'resistance': xs, 
        'path_length': ys,
        win_label : win_props,
        'distance' : distances
    }

def get_distance(best_fit_func, xs, ys):
    # Distance = (| a*x1 + b*y1 + c |) / (sqrt( a*a + b*b))
    distances = []
    a = best_fit_func[1]
    b = -1
    c = best_fit_func[0]
    for i in range(len(xs)):
        x = xs[i]
        y = ys[i]
        predicted_y = best_fit_func(x)
        distance = np.abs(a * x + b*y + c) / np.sqrt(a**2 + b**2)
        if predicted_y > y:
            distance *= -1
        distances += [distance]
    return distances
    