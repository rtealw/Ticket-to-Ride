import matplotlib.pyplot as plt
import numpy as np

def read_file(filename, agent_names=["Hungry", "Path", "OneStepThinker", "LongRouteJunkie"]):
    points_file = open(filename, 'r')
    total_counts = {key : [] for key in agent_names + ['alpha']}
    alpha_counts = {key : 0 for key in agent_names + ['total']}

    all_games = [eval(game) for game in points_file]
    current_point_table = all_games[0]['point_table']
    for i in range(len(all_games) + 1):

        if i >= len(all_games) or all_games[i]['point_table'] != current_point_table:
            total_counts['alpha'] += [round(current_point_table[1], 3)]
            for agent_name in agent_names:
                total_counts[agent_name] += [float(alpha_counts[agent_name])/alpha_counts['total']]
            
            if i < len(all_games):
                current_point_table = all_games[i]['point_table']
                alpha_counts = {key : 0 for key in agent_names + ['total']}
        
        if i < len(all_games):            
            game = all_games[i]
            for winner in game['winners']:
                if winner not in alpha_counts:
                    winner = agent_names[winner]
                alpha_counts[winner] += 1
                alpha_counts['total'] += 1
    return total_counts


def plot(counts, filename, agent_names=["Hungry", "Path", "OneStepThinker", "LongRouteJunkie"]):
    for agent_name in agent_names:
        plt.plot(counts['alpha'], counts[agent_name], label=agent_name)
    plt.title("Proportion of Wins by Strategy and Points per Train")
    plt.xlabel("Points per Train")
    plt.ylabel("Proportion of Wins")
    plt.xticks(np.arange(1,5.1,step=.2))
    plt.legend()
    plt.savefig(filename)
    plt.close()

def countAndPlot():
    counts = read_file(filename='../../Ticket-to-Ride-Engine/output/point_tables.txt')
    plot(counts, filename="../paper/figures/points.eps")