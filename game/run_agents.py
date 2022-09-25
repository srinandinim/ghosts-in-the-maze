from game.environment import Environment
from game.agent import Agent, Agent1, Agent2
import argparse 

parser = argparse.ArgumentParser(description='runs agents and experiments')
parser.add_argument('--num_sims', metavar='num_simulations', type=int, help='the number of environment simulations agent runs through')
parser.add_argument('--num_ghosts', metavar='num_simulations', type=int, help='number of ghosts in the environment')
parser.add_argument('--vv', metavar='verbose', type=str, help='lets you run the agents verbosely')
args = parser.parse_args()

num_ghosts = args.num_ghosts 
num_simulations = args.num_sims 

def simulation_statistics(num_simulations, num_ghosts):
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
    print(f"Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")  

def simulation_statistics_verbose(num_simulations, num_ghosts):
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
    print(f"Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")  


