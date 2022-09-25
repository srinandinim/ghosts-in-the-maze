import game.run_agents as run_agents

if __name__ == '__main__':  
    run_agents.simulation_statistics(num_simulations=1000, num_ghosts=5)
    run_agents.simulation_statistics_verbose(num_simulations=1000, num_ghosts=5)

