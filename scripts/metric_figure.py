import matplotlib.pyplot as plt
import scipy

def get_metrics(results, results_aux):
    for key in results_aux.keys():
        if key not in results:
            results[key] = results_aux[key]

    var_to_name = {
        "resistance":"Resistance",
        "path_length":"Path Length",
        "two_proportion":"Two-Player Wins",
        "distance":"Distance",
        "four_proportion":"Four-Player Wins"
    }
    
    variables = [
        "path_length",
        "resistance",
        "distance",
        "two_proportion",
        "four_proportion"
    ]

    table_colors = [["#ffffff"] * len(variables)]
    table_data = [[""] + [var_to_name[var] for var in variables[1:]]]

    for i in range(len(results.keys())-1):
        var1 = variables[i]
        color_row = ["#ffffff"]
        data_row = [var_to_name[var1]]
        for j in range(i):
            color_row += ["#ffffff"]
            data_row += [""]
        for j in range(i+1, len(results.keys())):
            var2 = variables[j]
            r, p = get_correlation(results[var1], results[var2])
            color_row += ["#ffee82"]
            if p < 1E-3:
                r = str(r) + '***'
                color_row[-1]= "#b31313"
            elif p < 1E-2:
                r = str(r) + '**'
                color_row[-1]= "#ff9000"
            elif p < 1E-1:
                r = str(r) + '*' 
                color_row[-1]= "#fdda16"

            data_row += [r]
        table_colors += [color_row]
        table_data += [data_row]

    fig = plt.figure(dpi=80)
    ax = fig.add_subplot(1,1,1)
    table = ax.table(cellText=table_data, cellColours=table_colors, loc='center')
    table.set_fontsize(14)
    table.scale(1,4)
    ax.axis('off')
    plt.savefig("../paper/figures/pearsons_table.eps", bbox_inches='tight')

def get_correlation(var1, var2):
    r, p = scipy.stats.pearsonr(var1, var2)
    return round(r, 3), p