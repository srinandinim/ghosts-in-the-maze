import game.run_agents as run_agents
from game.environment import Environment

if __name__ == '__main__':  
<<<<<<< HEAD
    #run_agents.simulation_statistics_agent1(num_simulations=1000, num_ghosts=5)
    #run_agents.simulation_statistics_agent2(num_simulations=1000, num_ghosts=5)
    #run_agents.simulation_statistics_agent3(num_simulations=100, num_ghosts=2)
=======
    run_agents.simulation_statistics_agent1(num_simulations=1000, num_ghosts=5)
    run_agents.simulation_statistics_agent2(num_simulations=1000, num_ghosts=5)
    run_agents.simulation_statistics_agent3(num_simulations=500, num_ghosts=5)
>>>>>>> b2961d41c730545e822e2a6ac50e86403d894381

    # run_agents.simulation_statistics_verbose_agent1(num_simulations=1, num_ghosts=2)
    # run_agents.simulation_statistics_verbose_agent2(num_simulations=1, num_ghosts=2)

    env = Environment() 
    # for path in env.shortest_paths:
    #     print(path)