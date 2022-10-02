import game.run_agents as run_agents
from game.environment import Environment

if __name__ == '__main__':  
    # run_agents.simulation_statistics_agent1(num_simulations=20, num_ghosts=5)
    # run_agents.simulation_statistics_agent2(num_simulations=20, num_ghosts=5)
    # run_agents.simulation_statistics_agent3(num_simulations=1, num_ghosts=2)

    # run_agents.simulation_statistics_verbose_agent1(num_simulations=1, num_ghosts=2)
    # run_agents.simulation_statistics_verbose_agent2(num_simulations=1, num_ghosts=2)

    env = Environment(num_ghosts=1)
    print(env)
    print(env.sb_paths())

    """
    env = Environment(num_ghosts=1)
    agent3 = Agent3()
    agent3.run_agent3(env)
    """
