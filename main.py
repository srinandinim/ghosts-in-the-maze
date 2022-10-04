import game.run_agents as run_agents
from game.environment import Environment

if __name__ == '__main__':  
    run_agents.simulation_statistics_agent1(num_simulations=1000, num_ghosts=5)
    run_agents.simulation_statistics_agent2(num_simulations=1000, num_ghosts=5)
    run_agents.simulation_statistics_agent3(num_simulations=500, num_ghosts=5)

    # run_agents.simulation_statistics_verbose_agent1(num_simulations=1, num_ghosts=2)
    # run_agents.simulation_statistics_verbose_agent2(num_simulations=1, num_ghosts=2)
