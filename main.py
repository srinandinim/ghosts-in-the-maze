from venv import create
from environment import Environment
from agent import Agent, Agent1 
from ghost import Ghost 

def create_game():
    env = Environment() 
    agent1 = Agent1() 
    ghost = Ghost()

    path = agent1.plan_path(env)

    print(env)
    print(path)

    for i in range(10):
        print(ghost.get_location())
        ghost.update_location(env)

    env.get_picture()

if __name__ == '__main__':
    create_game()


