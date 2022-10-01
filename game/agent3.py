from queue import Empty
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
        self.success_rates = {} 
    
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
                # print(self.action_space)
                # print()
                for index, action in enumerate(self.action_space):
                    # print(index, action)
                    if action is not None:
                        agent2 = Agent2()
                        agent2.location = action

                        location = agent2.run_agent2_once(env_copy)
                        self.action_space[index] = location
                        # print(self.action_space)
                        # print(index, self.action_space[index])

                for ghost in env_copy.ghosts:
                    ghost.update_location(env_copy)
                    for index, action in self.action_space:
                        if action == ghost.get_location():
                            self.action_space[index] = None
                            # print("killed" + str(action))
                            # (self.action_space).pop(index)

            # print()
            # print(self.action_space)

            for index, action in enumerate(self.action_space):
                # print(index, action)
                if action is not None:
                    self.success_distances[self.action_space_copy[index]] = self.manhattan_distance(action, goal)

            # print(self.action_space)
            # print(self.success_distances)

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
            
    
    def run_agent3_tej(self, env):

        """
        @Nandini:
        The core logic for this should work I think but it's nearly impossible to run due to computational complexity. I wasn't able to run it on a small grid. 
        I think the right next step is to do the following:
        (1) Do iterative DFS so stop at the 4th or 5th level in the stack (just add extra parameter to functional call)
        (2) Then use a heuristic (i.e. manhattan distance) to see how far the last node is from the goal node
        (3) Then run trials to see which of the actions in agent action space simulations lead to closest to goal node
        (4) Select that as action and continue running agent3. Use agent2 to run simulations, but make DFS stop at certain depth.

        This will help with the efficiency. 
        """

        while self.isalive:
            if self.location == (final_variables.SIZE-1, final_variables.SIZE-1):
                return 1 

            # compute action space at current location 
            self.action_space = self.action_spaces(env)

            # loop through the entire action space to find success rate of each possible move
            # by calling agent2 to run environments from each action in the space and then adding
            # up the number of success to the dictionary entry for that move 
            for action in self.action_space:
                success, trials = 0, 2
                while trials > 0:
                    new_env = deepcopy(env)
                    agent2 = Agent2()
                    agent2.location = action 
                    goal = (final_variables.SIZE-1, final_variables.SIZE-1)
                    while agent2.isalive and agent2.location != goal:
                        path = agent2.plan_path(new_env, agent2.location)
                        if path[0] not in self.ghost_actionspace(new_env, self.nearest_visible_ghost(new_env)).keys():
                            agent2.location = action 
                        else:
                            path = agent2.plan_path(new_env, agent2.location)
                            if path[0] not in self.ghost_actionspace(new_env, self.nearest_visible_ghost(new_env)).keys():
                                agent2.location = action 
                            else:
                                agent2.location = agent2.move_agent_away_from_nearest_ghost(new_env, agent2.nearest_visible_ghost(new_env))
                        for ghost in new_env.ghosts:
                            ghost.update_location(new_env)
                            if agent2.location == ghost.get_location():
                                agent2.isalive = False 
                    
                    if agent2.location == (final_variables.SIZE-1, final_variables.SIZE-1):
                        success += 1       
                self.success_rates[action] = success/trials 
            
            # find the max success rate possible from the action space and make that move as the action for turn of agent3 simulation on environment
            max_success = 0 
            best = self.location 

            for action in self.success_rates:
                if self.success_rates[action] > max_success:
                    best = action 
                    max_success = self.success_rates[action]
            
            self.location = best 

            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 
                        # for debugging, print out the agent location and ghost locations
            print(f"\nAgent 2 Location:\t {self.location}")
            for i in range(len(env.ghosts)):
                print(f"Ghost {i} Location:\t {env.ghosts[i].location}")
            color_array = env.get_picture()
            color_array[self.location[0]][self.location[1]] = 3 
            picture = plt.imshow(color_array, cmap='Greys')
            plt.show()
        return 0 