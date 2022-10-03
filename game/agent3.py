import enum
from queue import Empty
import random
from game.agent import Agent
from game.environment import Environment 
import game.final_variables as final_variables
from game.agent2 import Agent2
from copy import deepcopy
import matplotlib.pyplot as plt
import time

class Agent3(Agent2):
    """
    Agent 3 forecasts.  At every timestep, Agent 3 considers each possible move it might take (including staying inplace), 
    and ‘simulates’ the future based on the rules of Agent 2 past that point.  For each possible move, this future is simulated 
    some number of times, and then Agent 3 chooses among the moves with greatest success rates in these simulations.  Agent 3 can 
    be thought of as Agent 2, plus the ability to imagine the future.

    Agent 3 requires multiple searches - you’ll want to ensure that your searches are efficient as possible so they don’t take much time.  
    Additionally, if Agent 3 decides there is no successful path in its projected future, what should it do with that information?  
    Does it guarantee that success is impossible?
    """
    def __init__(self):
        """
        initializes Agent3 with initialization of Agent1.
        """
        super().__init__()
        self.action_space = []
        self.prev = {} 
        self.success_distances = {}
    
    def action_spaces(self, env):
        """
        returns the actions possible from current location in maze. 
        """
        x = self.location[0]
        y = self.location[1]

        possible_moves = [ (x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1) ]
        possible_valid_moves = []
        for move in possible_moves:
            if self.is_valid_position(move) and not env.maze[move[0]][move[1]].get_blocked():
                possible_valid_moves.append(move)

        if len(possible_valid_moves) == 0: 
            return self.location 
        
        return possible_valid_moves 

    def run_agent3_t(self, env):
        goal = (final_variables.SIZE - 1, final_variables.SIZE - 1)
        print(env)
        
        while self.isalive:
            if self.location == goal:
                return 1

            action_space = self.action_spaces(env)
            og_action_space = deepcopy(action_space)

            env_copy = deepcopy(env)
            agents = {}

            done = 0
            moves_success = {}
            
            while done is not len(action_space):
                for index, action in enumerate(action_space):
                    og_action = og_action_space[index]
                    agent2 = agents.get(og_action, Agent2())
                    if agent2.isalive:
                        agent2.location = action
                        success, location = agent2.run_agent2_once(env_copy)

                        agents[og_action] = agent2

                        if success:
                            done = done + 1
                            moves_success[og_action] = moves_success.get(og_action, 0) + 1
                        else:
                            action_space[index] = location
                
                for ghost in env_copy.ghosts:
                    ghost.update_location(env_copy)
                    for _, agent2 in agents.items():
                        if agent2.location == ghost.get_location():
                            agent2.isalive = False 
                            done = done + 1
            
            if moves_success: 
                highest_success_action = max(moves_success, key = moves_success.get)
                self.location = highest_success_action
            else:
                self.run_agent2_once(env)

            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 

        return 0
    
    def run_agent3(self, env):
        goal = (final_variables.SIZE - 1, final_variables.SIZE - 1)
        print(env)
        
        while self.isalive:
            if self.location == goal:
                return 1

            action_space = self.action_spaces(env)
            moves_success = {}
            for i in range(4):
                for action in action_space:
                    agent2 = Agent2()
                    agent2.location = action
                    attempt_success = agent2.run_agent2(deepcopy(env))
                    moves_success[action] = moves_success.get(action, 0) + attempt_success
            
            print(moves_success)
            highest_success_action = max(moves_success, key = moves_success.get)
            self.location = highest_success_action
            print(self.location)
            print()

            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 

        return 0


            