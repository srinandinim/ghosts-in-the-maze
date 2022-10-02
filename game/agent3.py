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

        possible_moves = [ (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1) ]
        possible_valid_moves = []
        for move in possible_moves:
            if self.is_valid_position(move) and not env.maze[move[0]][move[1]].get_blocked():
                possible_valid_moves.append(move)

        if len(possible_valid_moves) == 0: 
            return self.location 
        
        return possible_valid_moves 

    def run_agent3_ws(self, env):
        """
        TODO: deal with the situation if we are simulating and it reaches the goal and now we are still trying to stimulate
        - fix might be 'and action is not goal' on the condiitonal after the first enumeration
        """

        goal = (final_variables.SIZE-1, final_variables.SIZE-1)

        while self.isalive:
            self.success_rates = {}
            if self.location == goal:
                return 1

            self.action_space = self.action_spaces(env)
            self.action_space_copy = deepcopy(self.action_space)

            action_agents = []
            for index, action in enumerate(self.action_space):
                agent2 = Agent2()
                agent2.location = action
                action_agents.append(deepcopy(agent2))

            env_copy = deepcopy(env)
            done = 0
            possible_moves = []
            while done != len(self.action_space_copy):
                for index, agent in enumerate(action_agents):
                    location = agent2.run_agent2_once(env_copy)
                    agent.location = location

                    if (location == goal):
                        possible_moves.append(self.action_space_copy[index])
                        done = done + 1
                for ghost in env_copy.ghosts:
                    ghost.update_location(env_copy)
                    for index, action in self.action_space:
                        if action == ghost.get_location():
                            done = done + 1
                            self.action_space[index] = None

            if len(possible_moves) == 0:
                self.location = self.run_agent2_once(env)
            else:
                self.location = random.choice(possible_moves)

            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 

        return 0

    def run_agent3(self, env):
        """
        TODO: deal with the situation if we are simulating and it reaches the goal and now we are still trying to stimulate
        - fix might be 'and action is not goal' on the condiitonal after the first enumeration
        """

        goal = (final_variables.SIZE-1, final_variables.SIZE-1)

        while self.isalive:
            self.success_rates = {}
            if self.location == goal:
                return 1

            self.action_space = self.action_spaces(env)
            self.action_space_copy = deepcopy(self.action_space)

            env_copy = deepcopy(env)
            for i in range(4):
                for index, action in enumerate(self.action_space):
                    if action is not None:
                        agent2 = Agent2()
                        agent2.location = action

                        location = agent2.run_agent2_once(env_copy)
                        self.action_space[index] = location

                for ghost in env_copy.ghosts:
                    ghost.update_location(env_copy)
                    for index, action in self.action_space:
                        if action == ghost.get_location():
                            self.action_space[index] = None

            for index, action in enumerate(self.action_space):
                if action is not None:
                    self.success_distances[self.action_space_copy[index]] = self.manhattan_distance(action, goal)

            if len(self.success_distances) == 0:
                self.location = self.run_agent2_once(env)
            else:
                lowest_distance_key = min(self.success_distances, key = self.success_distances.get)
                self.location = lowest_distance_key

            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 

        return 0 
            