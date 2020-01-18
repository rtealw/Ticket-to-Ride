import matplotlib.pyplot as plt
import scipy
import resistance_figures
import numpy as np

def get_proportions_and_resistances(pairs, filename="../../Ticket-to-Ride-Engine/output/games.txt"):
    games_file = open(filename, 'r')
    tickets = {}
    for game_string in games_file:
        game = eval(game_string)
        for player in game['players']:
            for completed in game[player]['completed']:
                if completed not in tickets:
                    tickets[completed] = {'completed' : 0, 'uncompleted' : 0}
                tickets[completed]['completed'] += 1
            for uncompleted in game[player]['uncompleted']:
                if uncompleted not in tickets:
                    tickets[uncompleted] = {'completed' : 0, 'uncompleted' : 0}
                tickets[uncompleted]['uncompleted'] += 1

    proportions = []
    resistances = []
    for pair in pairs:
        ticket_name = resistance_figures.lengthen_edge(pair['city1'], pair['city2']).upper()    
        if ticket_name not in tickets:
            ticket_name = "/".join(ticket_name.split('/')[::-1])    
        completed = tickets[ticket_name]['completed']
        uncompleted = float(tickets[ticket_name]['uncompleted'])
        proportions += [completed / (completed + uncompleted)]
        resistances += [pair['resistance']]
    return proportions, resistances

def generate_completion_fig(pairs):
    old_figsize = plt.rcParams['figure.figsize']
    plt.rcParams["figure.figsize"] = [6, 5]
    y, x = get_proportions_and_resistances(pairs)
    plt.scatter(x=x, y=y, color="black")
    plt.xlabel("Resistance")
    plt.ylabel("Completions")

    round_sig = lambda f,p: float(('%.' + str(p) + 'e') % f)
    title = "Destination Tickets by Resistance and Completions"
    r, p = scipy.stats.pearsonr(x,y)
    subtitle0 = 'Pearson coefficient: ' + str(round_sig(r, 2))
    subtitle1 = 'p-value: ' + str(round_sig(p, 2))
    plt.title(title + '\n' + subtitle0 + '\n' + subtitle1)
    best_fit_func = np.poly1d(np.polyfit(x, y, deg=1))
    interval = np.linspace(min(x), max(x), 100)
    plt.plot(interval, best_fit_func(interval), color="black")
    plt.savefig("../paper/figures/completion.eps")
    plt.close()
    plt.rcParams['figure.figsize'] = old_figsize
