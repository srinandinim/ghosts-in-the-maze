import json
import time
import constants
import visualizations
from agent1 import Agent1
from agent2 import Agent2
from agent3 import Agent3
from environment import Environment

import os
import json 
import codecs

def simulation_statistics_agent1(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent1 = []
    for _ in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts)
        agent1 = Agent1()
        rewards_agent1.append(agent1.run_agent1(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent1: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2)

def simulation_statistics_agent1_video(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    captures a video of the game
    """
    rewards_agent1 = []
    for _ in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts)
        agent1 = Agent1()
        rewards_agent1.append(agent1.run_agent1_video(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent1: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2)

def simulation_statistics_agent2(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent1 = []
    for _ in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts)
        agent2 = Agent2()
        rewards_agent1.append(agent2.run_agent2(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent2: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2)


def simulation_statistics_agent2_video(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    captures a video of the game
    """
    rewards_agent1 = []
    for _ in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts)
        agent2 = Agent2()
        rewards_agent1.append(agent2.run_agent2_video(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent2: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2)

def simulation_statistics_agent3(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent1 = []
    for _ in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts)
        agent3 = Agent3()
        rewards_agent1.append(agent3.run_agent3(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent3: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2)


def simulation_statistics_agent3_video(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    captures a video of the game
    """
    rewards_agent1 = []
    for _ in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts)
        agent3 = Agent3()
        rewards_agent1.append(agent3.run_agent3_video(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent3: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2)

def lab_report_simulations(a1=False, a2=False, a3=False, a4=False, a5=False):
    """
    TODO: @Nandini, this needs to be updated to run on the same environment. 
    Not worrying about this right now because its not top priority, but 
    important for us to complete overall before lab report submission. 
    """

    survival_rates = {}
    for i in range(1, 5):
        path = '/experiments/a' + str(i) + '_stats.json'
        if os.path.exists(os.path.dirname(path)):
            with codecs.open(path, 'r', encoding='utf-8') as f:
                survival_rates[i] = json.load(f)
    print("these are the survival rates:")
    print(survival_rates)


    a1_stats, a2_stats, a3_stats, a4_stats, a5_stats = {}, {}, {}, {}, {}
    last_survival_rate, num_ghosts, max_ghosts = 100, 1, constants.SIZE[0] * constants.SIZE[1]
    num_simulations = 30
    a1_s = a2_s = a3_s = a4_s = a5_s = 0

    while last_survival_rate > 0 and num_ghosts < 5:
        print(f"\nTHE NUMBER OF CURRENT GHOSTS ARE: {num_ghosts}")

        if a1 == True:
            a1_s = simulation_statistics_agent1(
                num_simulations=num_simulations, num_ghosts=num_ghosts)
            a1_stats[num_ghosts] = a1_s

        if a2 == True:
            a2_s = simulation_statistics_agent2(
                num_simulations=num_simulations, num_ghosts=num_ghosts)
            a2_stats[num_ghosts] = a2_s

        # if a3 == True:
        #     a3_s = simulation_statistics_agent3(
        #         num_simulations=num_simulations, num_ghosts=num_ghosts)
        #     a3_stats[num_ghosts] = a3_s

        last_survival_rate = min(last_survival_rate, max(a1_s, a2_s, a3_s, a4_s, a5_s))
        num_ghosts += 1

    return a1_stats, a2_stats, a3_stats, a4_stats, a5_stats

def save_dict_to_json(dict, file_name):
    path = './experiments/' + str(file_name) + '_' + '.json'
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(str(json.dumps(dict, ensure_ascii=False)))    

def lab_report_visualizations(a1_stats=None, a2_stats=None, a3_stats=None, a4_stats=None, a5_stats=None):
    file_content = {'a1_stats': a1_stats, 'a2_stats': a2_stats, 'a3_stats': a3_stats, 'a4_stats': a4_stats, 'a5_stats': a5_stats}

    timestamp = time.time()
    filename = "experiments/simulation_statistics{}.json".format(timestamp)
    with open(filename, 'w') as fp:
        json.dump(file_content, fp)

    visualizations.get_graph(filename, save=True, graph_name="result_statistics{}".format(timestamp))

if __name__ == "__main__":
    a1_stats, a2_stats, a3_stats, a4_stats, a5_stats = lab_report_simulations(a1=True, a2=True, a3=False)
    print(f"Agent 1 Stats: {a1_stats}")
    print(f"Agent 2 Stats: {a2_stats}")
    print(f"Agent 3 Stats: {a3_stats}")

    lab_report_visualizations(a1_stats=a1_stats, a2_stats=a2_stats, a3_stats=a3_stats)

    # visualizations.get_graph("visualizations/overall_statistics.json" , save=True, graph_name="sample")
