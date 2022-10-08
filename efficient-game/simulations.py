import json
import os
import time
from copy import deepcopy
import constants
import visualizations
from agent1 import Agent1
from agent2 import Agent2
from agent3 import Agent3
from agent4 import Agent4
from environment import Environment


def simulation_statistics_agent1(num_simulations, num_ghosts, environments=[]):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent1 = []
    for i in range(num_simulations):
        env = deepcopy(environments[i]) if environments else Environment(
            num_ghosts=num_ghosts)
        agent1 = Agent1()
        rewards_agent1.append(agent1.run_agent1(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent1: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2)


def simulation_statistics_agent1_video(num_simulations, num_ghosts, environments=[]):
    """
    run simulation n times and get statistics on survival, and more
    captures a video of the game
    """
    rewards_agent1 = []
    for i in range(num_simulations):
        env = deepcopy(environments[i]) if environments else Environment(
            num_ghosts=num_ghosts)
        agent1 = Agent1()
        rewards_agent1.append(agent1.run_agent1_video(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent1: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2)


def simulation_statistics_agent2(num_simulations, num_ghosts, environments=[]):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent1 = []
    for i in range(num_simulations):
        env = deepcopy(environments[i]) if environments else Environment(
            num_ghosts=num_ghosts)
        agent2 = Agent2()
        rewards_agent1.append(agent2.run_agent2(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent2: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2)


def simulation_statistics_agent2_video(num_simulations, num_ghosts, environments=[]):
    """
    run simulation n times and get statistics on survival, and more
    captures a video of the game
    """
    rewards_agent2 = []
    for i in range(num_simulations):
        env = deepcopy(environments[i]) if environments else Environment(
            num_ghosts=num_ghosts)
        agent2 = Agent2()
        rewards_agent2.append(agent2.run_agent2_video(env))
    wins = sum(rewards_agent2)
    losses = len(rewards_agent2) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent2: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2)


def simulation_statistics_agent3(num_simulations, num_ghosts, environments=[]):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent3 = []
    timeouts = 0
    for i in range(num_simulations):
        env = deepcopy(environments[i]) if environments else Environment(
            num_ghosts=num_ghosts)
        agent3 = Agent3()
        result = agent3.run_agent3(env)
        rewards_agent3.append(1 if result == 1 else 0)
        if result == -1:
            timeouts = timeouts + 1
    wins = sum(rewards_agent3)
    losses = len(rewards_agent3) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent3: Wins: {wins}\tLosses: {losses}\tTimouts: {timeouts}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2), timeouts


def simulation_statistics_agent3_video(num_simulations, num_ghosts, environments=[]):
    """
    run simulation n times and get statistics on survival, and more
    captures a video of the game
    """
    rewards_agent3 = []
    for i in range(num_simulations):
        env = deepcopy(environments[i]) if environments else Environment(
            num_ghosts=num_ghosts)
        agent3 = Agent3()
        rewards_agent3.append(agent3.run_agent3_video(env))
    wins = sum(rewards_agent3)
    losses = len(rewards_agent3) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent3: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2)


def simulation_statistics_agent4(num_simulations, num_ghosts, environments=[]):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent4 = []
    timeouts = 0
    for i in range(num_simulations):
        env = deepcopy(environments[i]) if environments else Environment(
            num_ghosts=num_ghosts)
        agent4 = Agent4(env)
        result = agent4.run_agent4(env)
        rewards_agent4.append(1 if result == 1 else 0)
        if result == -1:
            timeouts = timeouts + 1
    wins = sum(rewards_agent4)
    losses = len(rewards_agent4) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent4: Wins: {wins}\tLosses: {losses}\tTimouts: {timeouts}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2), timeouts


def save_simulation_statistics(timestamp, a1_stats=None, a2_stats=None, a3_stats=None, a4_stats=None, a5_stats=None):
    file_content = {'a1_stats': a1_stats, 'a2_stats': a2_stats,
                    'a3_stats': a3_stats, 'a4_stats': a4_stats, 'a5_stats': a5_stats}

    dirname = "experiments/"
    if not os.path.exists(os.path.dirname(dirname)):
        os.makedirs(os.path.dirname(dirname))

    filename = "{}simulation_statistics{}.json".format(dirname, timestamp)
    with open(filename, 'w') as fp:
        json.dump(file_content, fp)


def visualize_simulation_statistics(timestamp):
    dirname = "experiments/"
    filename = "{}simulation_statistics{}.json".format(dirname, timestamp)

    visualizations.get_graph(
        filename, save=True, graph_name="result_statistics{}".format(timestamp))


def lab_report_simulations(a1=False, a2=False, a3=False, a4=False, a5=False):
    a1_stats, a2_stats, a3_stats, a4_stats, a5_stats = {}, {}, {}, {}, {}
    last_survival_rate, num_ghosts, max_ghosts = 100, 1, constants.SIZE[0] * \
        constants.SIZE[1]
    num_simulations = 30
    a1_s = a2_s = a3_s = a4_s = a5_s = 0

    start_time = time.time()
    while last_survival_rate > 0 and num_ghosts < max_ghosts:
        print(f"\nTHE NUMBER OF CURRENT GHOSTS ARE: {num_ghosts}")

        environments = []
        # for _ in range(num_simulations):
        #     environments.append(Environment(num_ghosts=num_ghosts))

        if a1 == True:
            a1_s = simulation_statistics_agent1(
                num_simulations=num_simulations, num_ghosts=num_ghosts, environments=environments)
            a1_stats[num_ghosts] = a1_s

        if a2 == True:
            a2_s = simulation_statistics_agent2(
                num_simulations=num_simulations, num_ghosts=num_ghosts, environments=environments)
            a2_stats[num_ghosts] = a2_s

        if a3 == True:
            a3_s, timeouts = simulation_statistics_agent3(
                num_simulations=num_simulations, num_ghosts=num_ghosts, environments=environments)
            a3_stats[num_ghosts] = [a3_s, timeouts]

        if a4 == True:
            a4_s, timeouts = simulation_statistics_agent4(
                num_simulations=num_simulations, num_ghosts=num_ghosts, environments=environments)
            a4_stats[num_ghosts] = [a4_s, timeouts]

        save_simulation_statistics(timestamp=start_time, a1_stats=a1_stats,
                                   a2_stats=a2_stats, a3_stats=a3_stats, a4_stats=a4_stats, a5_stats=a5_stats)

        last_survival_rate = min(
            last_survival_rate, max(a1_s, a2_s, a3_s, a4_s, a5_s))
        num_ghosts += 1

    # visualize_simulation_statistics(timestamp=start_time)

    return a1_stats, a2_stats, a3_stats, a4_stats, a5_stats


if __name__ == "__main__":
    # start = time.time()
    a1_stats, a2_stats, a3_stats, a4_stats, a5_stats = lab_report_simulations(
        a1=False, a2=False, a3=True, a4=False)
    # print(f"Agent 1 Stats: {a1_stats}")
    # print(f"Agent 2 Stats: {a2_stats}")
    # print(f"Agent 3 Stats: {a3_stats}")
    # print(f"Agent 4 Stats: {a4_stats}")

    # end = time.time()
    # print(end - start)
