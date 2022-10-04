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

    def run_agent3(self, env):        
        while self.isalive:
            if self.location == (final_variables.SIZE - 1, final_variables.SIZE - 1):
                return 1

            self.action_space = self.action_spaces(env)

            moves_success = {}
            maximum_success = 0
            for action in self.action_space:
                for i in range(5):
                    agent2 = Agent2()
                    agent2.location = action
                    attempt_success = agent2.run_agent2(deepcopy(env))
                    moves_success[action] = moves_success.get(action, 0) + attempt_success
                    maximum_success = max(maximum_success, moves_success[action])

            highest_success_distances = {}
            for action, num_success in moves_success.items():
                if num_success == maximum_success:
                    highest_success_distances[action] = len(env.shortest_paths[action[0]][action[1]])
            
            self.location = min(highest_success_distances, key=highest_success_distances.get)

            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 

        return 0


            