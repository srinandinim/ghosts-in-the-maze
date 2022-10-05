from game.environment import Environment
from game.agent1 import Agent1
from game.agent2 import Agent2
from game.agent3 import Agent3
import argparse 

parser = argparse.ArgumentParser(description='runs agents and experiments')
parser.add_argument('--num_sims', metavar='num_simulations', type=int, help='the number of environment simulations agent runs through')
parser.add_argument('--num_ghosts', metavar='num_simulations', type=int, help='number of ghosts in the environment')
parser.add_argument('--vv', metavar='verbose', type=str, help='lets you run the agents verbosely')
args = parser.parse_args()

num_ghosts = args.num_ghosts 
num_simulations = args.num_sims 

def simulation_statistics_agent1(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent1 = [] 
    for i in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts) 
        agent1 = Agent1()
        rewards_agent1.append(agent1.run_agent1(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins 
    survival = wins / (wins + losses)
    print(f"Agent1: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")  
    return round(survival*100,2)

def simulation_statistics_agent2(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent2 = [] 
    for i in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts) 
        agent2 = Agent2()
        rewards_agent2.append(agent2.run_agent2(env))
    wins = sum(rewards_agent2)
    losses = len(rewards_agent2) - wins 
    survival = wins / (wins + losses)
    print(f"Agent2: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")  
    return round(survival*100,2)

def simulation_statistics_agent3(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent3 = [] 
    for i in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts) 
        agent3 = Agent3()
        rewards_agent3.append(agent3.run_agent3(env))
    wins = sum(rewards_agent3)
    losses = len(rewards_agent3) - wins 
    survival = wins / (wins + losses)
    print(f"Agent3: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")  
    return round(survival*100,2)

def simulation_statistics_verbose_agent1(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent1 = [] 
    for i in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts) 
        agent1 = Agent1()
        rewards_agent1.append(agent1.run_agent1_verbose(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins 
    survival = wins / (wins + losses)
    survival = round(survival, 2)
    print(f"Agent1: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")  

def simulation_statistics_verbose_agent2(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent2 = [] 
    for i in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts) 
        agent2 = Agent2()
        rewards_agent2.append(agent2.run_agent2_verbose(env))
    wins = sum(rewards_agent2)
    losses = len(rewards_agent2) - wins 
    survival = wins / (wins + losses)
    print(f"Agent2: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")  