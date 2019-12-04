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
    
    row_variables = ["path_length", "resistance", "distance"]
    col_variables = ["two_proportion", "four_proportion"]

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
    table = ax.table(cellText=table_data, cellColours=table_colors, colWidths=[.1,.15,.15], cellLoc='center', loc='center')
    table.scale(2,4)
    ax.axis('off')
    plt.savefig("../paper/figures/pearsons_table.eps", bbox_inches='tight')

def get_correlation(var1, var2):
    r, p = scipy.stats.pearsonr(var1, var2)
    return round(r, 3), p