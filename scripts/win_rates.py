import matplotlib.pyplot as plt

def generate_total_wins_plot(filename, ):
    agent_names = ["Hungry", "Path", "OneStepThinker", "LongRouteJunkie"]
    games_file = open(filename, 'r')
    stats = {
        "Hungry" : 0, "Path" : 0, "OneStepThinker" : 0, "LongRouteJunkie" : 0,
        "games" : 0, "winners" : 0
    }
    agent_name_to_label = {
        "Hungry" : 'Hungry',
        "Path" : 'Path',
        "OneStepThinker" : 'One Step',
        "LongRouteJunkie" : 'Long Route'
    }
    for game in games_file:
        eval_game = eval(game)
        stats['games'] += 1
        for i in eval_game['winners']:
            stats['winners'] += 1
            winner = i
            if winner not in agent_names:
                winner = agent_names[i]
            stats[winner] += 1
    games_file.close()

    height = [float(stats[i]) / stats['games'] for i in agent_names]
    labels = [agent_name_to_label[i] for i in agent_names]
    colors = ['gold', '#d55e00', '#56b4e9', '#009e73']

    plt.bar(x=labels, height = height, width=.69, color=colors)
    plt.title("Wins by Strategy in 20,000 Games")
    plt.xlabel("Strategy")
    plt.ylabel("Win Rate")
    plt.savefig("../paper/figures/win_rates.eps")
