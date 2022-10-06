import game.run_agents as run_agents
import game.final_variables as final_variables
from game.environment import Environment

if __name__ == '__main__':  

    
    agent1_statistics = {}
    agent2_statistics = {}
    agent3_statistics = {}

    last_survival_rate, num_ghosts, maze_size = 100, 1, final_variables.SIZE * final_variables.SIZE
    while last_survival_rate > 0 and num_ghosts < 20:
        print(f"The number of ghosts are: {num_ghosts}")

        agent1_survival = run_agents.simulation_statistics_agent1(30, num_ghosts)
        agent1_statistics[num_ghosts] = agent1_survival 

        agent2_survival = run_agents.simulation_statistics_agent2(30, num_ghosts)
        agent2_statistics[num_ghosts] = agent2_survival 

        agent3_survival = run_agents.simulation_statistics_agent3(30, num_ghosts)
        agent3_statistics[num_ghosts] = agent3_survival  

        last_survival_rate = min(last_survival_rate, max(agent1_survival, agent2_survival, agent3_survival))

        num_ghosts += 1
        print("\n")
    print(f"Agent 1:\t{agent1_statistics}")
    print(f"Agent 2:\t{agent2_statistics}")
    print(f"Agent 3:\t{agent3_statistics}")
    
    
    
    # run_agents.simulation_statistics_agent1(num_simulations=100, num_ghosts=2)
    # run_agents.simulation_statistics_agent2(num_simulations=100, num_ghosts=2)
    # run_agents.simulation_statistics_agent3(num_simulations=30, num_ghosts=2)
    
    # run_agents.simulation_statistics_verbose_agent2(num_simulations=1, num_ghosts=5)