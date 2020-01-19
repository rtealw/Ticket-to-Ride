import matplotlib.pyplot as plt
import scipy
import numpy as np

def generate_figures(aggregate_results, var_to_name):
    x_names = ['path_length', 'resistance', 'distance']
    old_figsize = plt.rcParams['figure.figsize']
    for i in range(len(x_names)):
        plt.rcParams["figure.figsize"] = [4, 3]
        x = x_names[i]
        xs = aggregate_results[x]
        ys = aggregate_results['aggregate_proportion']
        if x == 'path_length':
            plt.xticks(np.arange(min(xs), max(xs)+1, 5))
        plt.scatter(x=xs, y= ys, color="black")
        plt.xlabel(var_to_name[x])
        y_name = 'Proportion of Wins'
        plt.ylabel(y_name)
        title = 'Destination Tickets by ' + var_to_name[x] + ' and Wins'
        r, p = get_correlation(xs, ys)
        subtitle0 = 'Pearson coefficient: ' + str(round_sig(r, 2))
        subtitle1 = 'p-value: ' + str(round_sig(p, 2))
        plt.title(title + '\n' + subtitle0 + '\n' + subtitle1)
        interval = np.linspace(min(xs), max(xs), 100)
        best_fit_func = np.poly1d(np.polyfit(xs, ys, deg=1))
        plt.plot(interval, best_fit_func(interval), color="black")
        plt.savefig("../paper/figures/correlation{}.eps".format(i), bbox_inches='tight')
        plt.close()
    plt.rcParams['figure.figsize'] = old_figsize

round_sig = lambda f,p: float(('%.' + str(p) + 'e') % f)

def get_metrics(results, results2, results3):
    var_to_name = {
        "resistance":"Resistance",
        "path_length":"Path Length",
        "two_proportion":"Two-Player Wins",
        "distance":"Residual",
        "four_proportion":"Four-Player Wins",
        "aggregate_proportion":"Overall Wins"
    }
 
    for key in results2.keys():
        if key not in results:
            results[key] = results2[key]
    for key in results3.keys():
        if key not in results:
            results[key] = results3[key]

    generate_figures(results3, var_to_name)
   
    row_variables = ["path_length", "resistance", "distance"]
    col_variables = ["two_proportion", "four_proportion", "aggregate_proportion"]

    table_colors = [["#ffffff"] * (1 + len(col_variables))]
    table_data = [[""] + [var_to_name[var] for var in col_variables]]

    for i in range(len(row_variables)):
        var1 = row_variables[i]
        color_row = ["#ffffff"]
        data_row = [var_to_name[var1]]
        for j in range(len(col_variables)):
            var2 = col_variables[j]
            r, p = get_correlation(results[var1], results[var2])
            color_row += ["#ffffff"]
            for n in range(10, 0, -1):
                if p < eval('1e-{}'.format(n)):
                    r = str(r) + '*'*(n//2)
                    break
            if p < 1E-5:
                color_row[-1]= "#607c3c"
            elif p < 1E-4:
                color_row[-1]= "#809c13"
            elif p < 1E-2:
                color_row[-1]= "#abc32f"

            data_row += [r]
        table_colors += [color_row]
        table_data += [data_row]

    fig = plt.figure(dpi=80)
    ax = fig.add_subplot(1,1,1)
    table = ax.table(cellText=table_data, cellColours=table_colors, colWidths=[.069,.1,.1, .1], cellLoc='center', loc='center')
    table.scale(2,4)
    ax.axis('off')
    plt.savefig("../paper/figures/pearsons_table.eps", bbox_inches='tight')
    plt.close()
    results_file = open("input/results.txt", "w")
    results_file.write(str(results))
    results_file.close()

def get_correlation(var1, var2):
    r, p = scipy.stats.pearsonr(var1, var2)
    return round(r, 3), p