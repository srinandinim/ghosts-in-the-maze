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
        visited = {}
        while self.isalive:
            visited[self.location] = visited.get(self.location,0) + 1
            # if reached goal, then we're done
            if self.location == (final_variables.SIZE - 1, final_variables.SIZE - 1):
                #print("WON!")
                return 1

            # determine the agent's action spaces
            self.action_space = self.action_spaces(env)

            # add the DFS paths to the current action space
            a3paths = {}

            # run k simulation and store success rate for 
            moves_success = {}
            maximum_success = 0
            #print(moves_success)
            for action in self.action_space:
                for i in range(10):
                    agent2 = Agent2()
                    agent2.location = action
                    attempt_success = agent2.run_agent2_forecast(deepcopy(env))
                    moves_success[action] = moves_success.get(action, 0) + attempt_success
                    maximum_success = max(maximum_success, moves_success[action])
            
            #print(moves_success)
            #print(self.location)
            #print(visited)

            # penalize states already visited, encouraging exploration, avoid local minima
            for key in moves_success.keys():
                if key in visited.keys(): 
                    #print(f"Visited {key}, so cut in hafl!")
                    moves_success[key] = moves_success[key] * 0.6 **(visited[key])
                moves_success[key] = ((moves_success[key] + 1) / (self.manhattan_distance(key, final_variables.GOAL) + 1)**(2))
            #print(moves_success)

            action = max(moves_success, key=moves_success.get)
            if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
                self.location = action 
            else: 
                #print("MOVING AWAY FROM THE ENAREST GHOST")
                self.location = self.move_agent_away_from_nearest_ghost(env, self.nearest_visible_ghost(env)) 
            #print(self.location)
            #print("\n")

            

            
            
            

            

            """

            # for debugging, print out the agent location and ghost locations
            print(f"\nAgent 3 Location:\t {self.location}")
            for i in range(len(env.ghosts)):
                print(f"Ghost {i} Location:\t {env.ghosts[i].location}")
            color_array = env.get_picture()
            color_array[self.location[0]][self.location[1]] = 3 
            picture = plt.imshow(color_array, cmap='Greys')
            plt.show()
            highest_success_distances = {}
            for action, num_success in moves_success.items():
                if num_success == maximum_success:
                    highest_success_distances[action] = len(env.shortest_paths[action[0]][action[1]])
            
            self.location = min(highest_success_distances, key=highest_success_distances.get)
            """


            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    #print("DIED!")
                    return 0 

        return 0

    def run_agent3v2(self, env):
        visited = {}
        while self.isalive:

            visited[self.location] = visited.get(self.location,0) + 1
            
            if self.location == (final_variables.SIZE - 1, final_variables.SIZE - 1):
                print("WON!")
                return 1
            
            # run agent 2 simulations only when ghost is in action space to select best possible next step
            path = super().plan_path((0,0), env)

            # min distance to nearest ghost
            min_dist = self.manhattan_distance(self.location, self.nearest_visible_ghost(env))

            # run current plan if ghosts are not close by (manhattan distance=2)
            if min_dist < 2: 
                print("Existing Path")
                if path is None:
                    path = super().plan_path(self.location, env)
                self.location = path.pop(0)
            else: 
                print("Hill Climbing")
                # determine the agent's action spaces
                self.action_space = self.action_spaces(env)
                            # run k simulation and store success rate for 
                moves_success = {}
                maximum_success = 0
                print(moves_success)
                for action in self.action_space:
                    for _ in range(5):
                        agent2 = Agent2()
                        agent2.location = action
                        attempt_success = agent2.run_agent2(deepcopy(env))
                        moves_success[action] = moves_success.get(action, 0) + attempt_success
                        maximum_success = max(maximum_success, moves_success[action])
                if sum(moves_success.values()) == 0:
                    path = [self.move_agent_away_from_nearest_ghost(env, self.nearest_visible_ghost(env)) ]
                    self.location = path.pop()
                else: 
                    #print(moves_success)
                    #print(self.location)
                    #print(visited)

                    # penalize states already visited, encouraging exploration, avoid local minima
                    for key in moves_success.keys():
                        if key in visited.keys(): 
                            print(f"Visited {key}, so cut in hafl!")
                            moves_success[key] = moves_success[key] * 0.6 **(visited[key])
                        moves_success[key] = ((moves_success[key] + 1) / (self.manhattan_distance(key, final_variables.GOAL) + 1)**(2))
                    #print(moves_success)

                    action = max(moves_success, key=moves_success.get)
                    path = [action]
                    self.location = path.pop() 
            
            """
            print(f"\nAgent 3 Location:\t {self.location}")
            for i in range(len(env.ghosts)):
                print(f"Ghost {i} Location:\t {env.ghosts[i].location}")
            color_array = env.get_picture()
            color_array[self.location[0]][self.location[1]] = 3 
            picture = plt.imshow(color_array, cmap='Greys')
            plt.show()
            """
            
            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    print("DIED!")
                    return 0 

        return 0
