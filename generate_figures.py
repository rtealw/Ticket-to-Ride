import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['figure.figsize'] = 10, 5.8

def generate_figure(pairs):
    xs, ys = [], []
    ax = plt.subplot()
    for pair in pairs:
        x, y, number = pair['resistance'], pair['min_path'], pair['number']
        xs.append(x)
        ys.append(y)
        label = '{} {}/{}'.format(number, pair['city1'], pair['city2']).upper()
        ax.scatter(x,y, s=2, label=label)
        ax.annotate(number, (x,y), ha='center', va='center', fontsize=8,
                           bbox=dict(boxstyle="circle,pad=0.3", fc="white"))

    interval = np.linspace(min(xs), max(xs), 100)
    best_fit_func = np.poly1d(np.polyfit(xs, ys, deg=1))
    plt.plot(interval, best_fit_func(interval), color="black")

    # Shrink current axis
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    plt.xlim(min(xs) * .5, max(xs) * 1.1)
    plt.ylim(min(ys) * .5, max(ys) * 1.1)
    plt.yticks(range(min(ys), max(ys)+1, 2)) # integer y axis
    plt.title("Destination Tickets by Reward and Difficulty")
    plt.xlabel("Effective Resistance")
    plt.ylabel("Length of Minimum Path")
    legend = ax.legend(
        bbox_to_anchor = (1, 1),
        handlelength = 0, 
        handletextpad=0,
        fontsize=7
    )
    for item in legend.legendHandles:
        item.set_visible(False)
    plt.savefig("paper/figures/resistance.eps")