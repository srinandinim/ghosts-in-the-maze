from copy import deepcopy
import time
from agent2li import Agent2LI
from agent3li import Agent3LI
from agent4li import Agent4LI
from environment import Environment


def simulation_statistics_agent2(num_simulations, num_ghosts, environments=[]):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent2 = []
    for i in range(num_simulations):
        env = deepcopy(environments[i]) if environments else Environment(
            num_ghosts=num_ghosts)
        agent2 = Agent2LI()
        rewards_agent2.append(agent2.run_agent2(env))
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
    runtimes = []
    for i in range(num_simulations):
        start_time = time.time()
        env = deepcopy(environments[i]) if environments else Environment(
            num_ghosts=num_ghosts)
        agent3 = Agent3LI()
        result = agent3.run_agent3(env)
        rewards_agent3.append(1 if result == 1 else 0)
        if result == -1:
            timeouts = timeouts + 1
        runtimes.append(round(time.time() - start_time, 5))
    wins = sum(rewards_agent3)
    losses = len(rewards_agent3) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent3: Wins: {wins}\tLosses: {losses}\tTimouts: {timeouts}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2), timeouts, runtimes

def simulation_statistics_agent4(num_simulations, num_ghosts, environments=[]):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent4 = []
    timeouts = 0
    runtimes = []
    for i in range(num_simulations):
        start_time = time.time()
        env = deepcopy(environments[i]) if environments else Environment(
            num_ghosts=num_ghosts)
        agent4 = Agent4LI(env)
        result = agent4.run_agent4(env)
        rewards_agent4.append(1 if result == 1 else 0)
        if result == -1:
            timeouts = timeouts + 1
        runtimes.append(round(time.time() - start_time, 5))
    wins = sum(rewards_agent4)
    losses = len(rewards_agent4) - wins
    survival = wins / (wins + losses)
    print(
        f"Agent4: Wins: {wins}\tLosses: {losses}\tTimouts: {timeouts}\tSurvival Rate: {round(survival*100,2)}%")
    return round(survival*100, 2), timeouts, runtimes

if __name__ == "__main__":
    simulation_statistics_agent2(1, 1)
    simulation_statistics_agent3(1, 2)
    simulation_statistics_agent4(1, 2)