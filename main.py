from venv import create
from black import Set
from environment import Environment
from agent import Agent, Agent1 
from ghost import Ghost 

def run_agent1_verbose(env, ghosts):
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


def print_environment(env):
    print("The environment can be seen below:")
    print("----------------------------------")
    print(env)    
    print("----------------------------------")

if __name__ == '__main__':
    survival_rates = [] 
    num_simulations = 100000
    for i in range(num_simulations):
        num_ghosts = 5
        env = Environment() 
        ghosts = [Ghost() for i in range(num_ghosts)] 

        # print_environment(env)
        survival_rates.append(run_agent1(env, ghosts))
    survival_rate = sum(survival_rates)/len(survival_rates)
    print(f" \n5 Ghosts, 5x5 Maze, Agent1\nIn {num_simulations} simulations, Agent 1's survival_rate was {survival_rate}%")

