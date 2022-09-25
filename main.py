from venv import create
from black import Set
from environment import Environment
from agent import Agent, Agent1 
from ghost import Ghost 

def run_agent1_verbose(env, ghosts):
    print_environment(env)

    agent1 = Agent1()
    plan = agent1.plan_path(env)
    plan_idx = 1

    print(f"Agent 1's Planned Optimal Path is: {plan}")
            
    # return 1 if the agent reaches goal node, otherwise +0 
    while agent1.isalive and plan_idx <= len(plan):

        # if we successfully reached the goal node, return +1
        if agent1.location == (Environment.SIZE-1, Environment.SIZE-1):
            print("\nSUCCESS (+1): THE AGENT REACHED THE GOAL!")
            return 1

        # based on the plan, determine what is the next best action
        action = plan[plan_idx]
        plan_idx += 1
        agent1.location = action 

        # update ghosts location and make agent die if it touches ghost 
        for ghost in ghosts:
            ghost.update_location(env)
            if agent1.location == ghost.get_location():
                print("\nFAILURE (+0): THE AGENT GOT KILLED BY A GHOST")
                print(f"Agent 1 Location: {agent1.location}\t Ghost Location: {ghost.get_location()}")
                agent1.isalive = False 
                return 0 
    
        # for debugging, print out the agent location and ghost locations
        print(f"\nAgent 1 Location:\t {agent1.location}")
        for i in range(len(ghosts)):
            print(f"Ghost {i} Location:\t {ghosts[i].location}")

def run_agent1(env, ghosts):
    agent1 = Agent1()
    plan = agent1.plan_path(env)
    plan_idx = 1

    while agent1.isalive and plan_idx <= len(plan):
        if agent1.location == (Environment.SIZE-1, Environment.SIZE-1):
            return 1

        action = plan[plan_idx]
        plan_idx += 1
        agent1.location = action 

        for ghost in ghosts:
            ghost.update_location(env)
            if agent1.location == ghost.get_location():
                agent1.isalive = False 
                return 0 

def simulation_agent1(num_simulations, num_ghosts):
    agent1_rewards = [] 
    for _ in range(num_simulations):
        env = Environment() 
        ghosts = [Ghost() for _ in range(num_ghosts)]
        agent1_rewards.append(run_agent1_verbose(env, ghosts))
    agent1_survival_rate = sum(agent1_rewards) / len(agent1_rewards)
    return agent1_survival_rate

def print_environment(env):
    print("\nThe environment can be seen below:")
    print("----------------------------------")
    print(env)    
    print("----------------------------------\n")

if __name__ == '__main__':  
    num_simulations = 1000
    num_ghosts = 3 
    agent1_survival_rate = simulation_agent1(num_simulations, num_ghosts)
    print(f" \n{num_ghosts} Ghosts\t5x5 Maze\t Agent1\nIn {num_simulations} simulations, Agent 1's survival_rate was {agent1_survival_rate * 100:.2f} %\n")

