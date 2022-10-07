import json
import matplotlib.pyplot as plt


def get_stats(filename):
    with open(filename, 'r') as fp:
        file_content = json.load(fp)

    stats = []
    for object in file_content:
        if file_content[object]:
            stats.append(file_content[object])

    return stats


def get_graph(filename, save=False, graph_name=""):
    plt.title('Agents\' Success Rates')
    plt.xlabel('Number of Ghosts')
    plt.ylabel('Success Rate (%)')
    plt.grid(True)

    stats = get_stats(filename)
    line_colors = ["#f15854", "#faa43a", "#60bd68", "#5da5da", "#b276b2"]
    for i, agent_stats in enumerate(stats):
        plt.plot(agent_stats.keys(), agent_stats.values(), linewidth=2.0,
                 color=line_colors[i], marker='o', label="Agent {}".format(i + 1))

    plt.legend()

    if save:
        figure_name = "visualizations/{}.png".format(graph_name)
        plt.savefig(figure_name, bbox_inches='tight')

    plt.show()
