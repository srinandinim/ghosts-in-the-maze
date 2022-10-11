import json
import os
import matplotlib.pyplot as plt
import statistics as stat

import numpy as np

def get_stats(filename):
    with open(filename, 'r') as fp:
        file_content = json.load(fp)

    stats = []
    for object in file_content:
        if file_content[object]:
            stats.append(file_content[object])

    return stats


def get_graph(filename, save=False, dirname="visualizations/", graph_name=""):
    plt.title('Agents\' Success Rates')
    plt.xlabel('Number of Ghosts')
    plt.ylabel('Success Rate (%)')
    plt.grid(True)

    stats = get_stats(filename)
    line_colors = ["#f15854", "#faa43a", "#60bd68", "#5da5da", "#b276b2"]
    for i, agent_stats in enumerate(stats):
        plot_data = {}
        for key, value in agent_stats.items():
            plot_data[key] = value[0] if isinstance(value, list) else value

        x = []
        y = []

        mean = []
        stddev = []
        for key, value in plot_data.items():
            if int(key) % 5 == 0:
                x.append(int(key))
                y.append(value)

                wins = round(value * 3/10)
                losses = 30 - wins

                simulations = []
                for v in range(max(wins, losses)):
                    if v < wins: simulations.append(1)
                    if v < losses: simulations.append(0)
                
                mean.append(int(key))
                stddev.append(2 * stat.stdev(simulations))

        plt.plot(x, y, linewidth=2.0,
                 color=line_colors[i], marker='o', label="Agent {}".format(i + 1))
        plt.errorbar(x, y, yerr = stddev, linestyle='', color=line_colors[i])

    plt.legend()

    if save:
        if not os.path.exists(os.path.dirname(dirname)):
            os.makedirs(os.path.dirname(dirname))

        graph_name = "{}{}.png".format(dirname, graph_name)
        plt.savefig(graph_name, bbox_inches='tight')

    plt.show()
