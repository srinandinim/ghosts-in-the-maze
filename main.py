import game.run_agents as run_agents
from game.agent import Agent, Agent1, Agent2
from game.environment import Environment

if __name__ == '__main__':  
    #run_agents.simulation_statistics(num_simulations=1032, num_ghosts=5)
    # run_agents.simulation_statistics_verbose(num_simulations=1000, num_ghosts=5)

    env = Environment(num_ghosts=2)
    agent2 = Agent2() 
    path = agent2.run_agent2_verbose(env)

