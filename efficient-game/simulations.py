from agent import Agent1 
from environment import Environment 

if __name__ == "__main__":

    rewards = []
    for i in range(1):
        env = Environment(num_ghosts=5)
        a1  = Agent1()
        rewards.append(a1.run_agent1_debug(env))
    print(sum(rewards))