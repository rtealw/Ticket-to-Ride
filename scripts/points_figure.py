import matplotlib.pyplot as plt
import numpy as np

def read_file(filename1, filename2, agent_names=["Hungry", "Path", "OneStepThinker", "LongRouteJunkie"]):
    points_file1 = open(filename1, 'r')
    points_file2 = open(filename2, 'r')
    total_counts = {key : [] for key in agent_names + ['alpha']}
    alpha_counts = {key : 0 for key in agent_names + ['total']}

    all_games = []
    for game in points_file1:
        all_games += [eval(game)]
    for game in points_file2:
        all_games += [eval(game)]

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
    colors = ['gold', '#d55e00', '#56b4e9', '#009e73']
    agent_name_to_label = {
        "Hungry" : 'Hungry',
        "Path" : 'Path',
        "OneStepThinker" : 'One Step',
        "LongRouteJunkie" : 'Long Route'
    }
    for i in range(len(agent_names)):
        color = colors[i]
        agent_name = agent_names[i]
        label = agent_name_to_label[agent_name]
        plt.plot(counts['alpha'], counts[agent_name], label=label, color=color)
    plt.title("Proportion of Wins by Strategy and Points per Train")
    plt.xlabel("Points per Train (α)")
    plt.ylabel("Proportion of Wins")
    plt.xticks(np.arange(1,7.1,step=.5))
    plt.ylim(0, .45)
    plt.legend()
    plt.savefig(filename)
    plt.close()

def countAndPlot():
    counts = read_file(
        filename1='../../Ticket-to-Ride-Engine/output/point_table1.txt',
        filename2='../../Ticket-to-Ride-Engine/output/point_table2.txt'
    )
    plot(counts, filename="../paper/figures/points.eps")