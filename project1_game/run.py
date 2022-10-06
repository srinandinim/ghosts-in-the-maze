from simulator import Environment
from agent1 import Agent1 

if __name__=="__main__":
    env = Environment() 
    a1 = Agent1()
    a1.run_agent1_verbose(env)
