from environment import Environment
from agent import Agent, Agent1 

def create_game():
    env = Environment() 
    agent1 = Agent1() 

if __name__ == '__main__':
    env = Environment()
    agent1 = Agent1()
    path = (agent1.plan_path(env))
    

    print(env)
    print(path)

    env.get_picture()
