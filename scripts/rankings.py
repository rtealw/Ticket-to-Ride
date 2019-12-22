import matplotlib.pyplot as plt


def orderXbyY(X, Y):
    ordered_X = [x for _, x in sorted(zip(Y,X), key = lambda pair: pair[0])]
    ordered_X.reverse()
    return ordered_X


def generate_rankings(input_file='input/results.txt', output_file='../paper/figures/rankings.eps'):
    results_file = open(input_file, 'r')
    results = eval(results_file.read())
    results_file.close()

    names_by_paths = orderXbyY(X=results['names'], Y=results['path_length'])
    names_by_residuals = orderXbyY(X=results['names'], Y=results['distance'])
    total = float(len(names_by_paths))
    colors = results['colors']
    colors.reverse()
    plt.figure(figsize=(4,5))
    for name in names_by_paths:
        i = names_by_paths.index(name) + 1
        j = names_by_residuals.index(name) + 1
        color = colors[i-1]
        xi = 0
        yi = 1 - i / total
        xj = 1
        yj = 1 - j / total
        plt.plot([xi, xj], [yi, yj], c=color, linestyle='-', marker='o', markevery=[0])
        plt.plot([xi, xj], [yi, yj], c=color, linestyle='-', marker='s', markevery=[1])
        plt.text(x=xj+.2, y=yj-.013, s=name, c='black')
    plt.scatter(x=6,y=0,s=.001, c='white')
    plt.axis('off')
    plt.savefig(output_file)
