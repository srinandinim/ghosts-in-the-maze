"""
NOTE: AGENT2 is complete - no changes necessary for project. 
"""

from copy import deepcopy
from game.environment import Environment 
import game.final_variables as final_variables
from game.agent1 import Agent1
import time
import matplotlib.pyplot as plt

class Agent2(Agent1):

    """
    Agent  2  re-plans.   At  every  timestep,  Agent  2  recalculates  a  new  path  to  the  goal  based  on  the  current information,  
    and  executes  the  next  step  in  this  new  path.   Agent  2  is  constantly  updating  and  readjusting based on new information 
    about the ghosts.  Note, however, Agent 2 makes no projections about the future.  If all paths to the goal are currently blocked, Agent 2 
    attempts to move away from the nearest visible ghost (not occupying a blocked cell).

    Agent 2 requires multiple searches - you’ll want to ensure that your searches are efficient as possible so they don’t take much time.  
    Do you always need to replan?  When will the new plan be the same as the old plan, and as such you won’t need to recalculate?
    """

    def __init__(self):
        """
        intializes Agent2 with initialization method of Agent1. 
        """
        super().__init__()
        self.paths = {}
    
    def dfs(self, env, curr, visited, prev):
        """
        dfs to find a path from source to goal node.
        """ 
        visited.add(curr)
        if curr[0] == curr[1] == final_variables.SIZE:
            return True, prev
        
        for d in Environment.DIRECTIONS:
            x = curr[0] + d[0]
            y = curr[1] + d[1] 
            if self.is_valid_position((x,y)) and (x,y) not in visited:
                prev[(x,y)] = curr
                if env.maze[x][y].get_blocked() == False: 
                    reached_goal, _ = self.dfs(env, (x,y), visited, prev)
                    if reached_goal == True :
                        return True, prev 
        return False, prev
    
    def manhattan_distance(self, coord1, coord2):
        x = abs(coord2[0] - coord1[0])
        y = abs(coord2[1] - coord1[1])
        return x + y
    
    def nearest_visible_ghost(self, env):
        """
        finds nearest ghost position from current position
        will be used if all paths are blocked, then make sure to walk towards opposite direction
        """
        min_distance = final_variables.SIZE * final_variables.SIZE + 1 
        min_coords = (final_variables.SIZE, final_variables.SIZE)
        for ghost in env.ghosts:
            if not env.maze[ghost.location[0]][ghost.location[1]].get_blocked():
                dist = self.manhattan_distance(self.location, ghost.get_location())
                if dist < min_distance:
                    min_distance = dist 
                    min_coords = ghost.location 
        return min_coords  
    
    def ghost_actionspace(self, env, ghost_location):
        ghost_actions = {}
        for d in self.DIRECTIONS:
            dx = d[0] + ghost_location[0]
            dy = d[1] + ghost_location[1]
            new_pos = (dx, dy)
            if self.is_valid_position(new_pos):
                if env.maze[dx][dy].get_blocked():
                    ghost_actions[new_pos] = 0.5 
                else: ghost_actions[new_pos] = 1.0
        return ghost_actions 
    
    def ghost_current_locations(self, env):
        ghost_locations = set()
        for ghost in env.ghosts:
            ghost_locations.add(ghost.location)
        return ghost_locations 
    
    def plan_path(self, source, env):
        # agent starts at top left and tries to reach bottom right
        goal = (Environment.SIZE-1, Environment.SIZE-1)

        # use visited/prev for running BFS for path planning
        visited = set(source)
        prev = ({source : None})
        _, prev = self.dfs(env, source, visited, prev)

        path = super().path_from_pointers(source, goal, prev)
        return path 
    
    def move_agent_away_from_nearest_ghost(self, env, nearest_ghost):
        x = self.location[0]
        y = self.location[1]
        possible_moves = [ (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1) ]
        possible_valid_moves = []
        for move in possible_moves:
            if self.is_valid_position(move) and not env.maze[move[0]][move[1]].get_blocked():
                possible_valid_moves.append(move)
        if len(possible_valid_moves) == 0: 
            return self.location 
        
        distances = {}
        for possible_move in possible_valid_moves:
            distances[possible_move] = self.manhattan_distance(self.nearest_visible_ghost(env), possible_move)
        
        max_dist = 0
        max_move = self.location 
        for move, dist in distances.items():
            if dist > max_dist:
                max_dist = dist 
                max_move = move 
        return max_move 

    def run_agent2_verbose(self, env):
        super().print_environment(env)
        path = self.plan_path(self.location, env)
        paths = {self.location : deepcopy(path)}
        #print(f"Agent 2's Planned Path is: {path}")
        print(self.location)

        images = []
        video_name = "agent2_" + str(time.time())

        while self.isalive:
            if self.location == (final_variables.SIZE-1, final_variables.SIZE-1):
                print("\nSUCCESS (+1): THE AGENT REACHED THE GOAL!")
                color_array = env.get_picture()
                color_array[self.location[0]][self.location[1]] = 3 
                images.append(color_array)
                picture = plt.imshow(color_array, cmap='Greys')
                plt.show()
                self.generate_video(video_name, images)
                return 1 
            action = path.pop(0) 
            if action not in self.ghost_current_locations(env):
                self.location = action 
            else:
                print("Replanning!")
                if self.location in paths: 
                    path = deepcopy(paths[self.location])
                    #print(path)
                else: 
                    path = self.plan_path(self.location, env)
                    paths[self.location] = deepcopy(path) 
                    #print(path)
                path = self.plan_path(self.location, env)
                action = path.pop(0) 
                print(f"REPLANNING: Agent 2's Planned Path is: {path}")
                if action not in self.ghost_current_locations(env):
                    self.location = action 
                else:
                    print(f"MOVE AWAY FROM GHOST: New path is also in ghost danger zone!")
                    self.location = self.move_agent_away_from_nearest_ghost(env, self.nearest_visible_ghost(env))
            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    print("\nFAILURE (+0): THE AGENT GOT KILLED BY A GHOST")
                    print(f"Agent 1 Location: {self.location}\t Ghost Location: {ghost.get_location()}")
                    self.isalive = False 
                    color_array = env.get_picture()
                    color_array[self.location[0]][self.location[1]] = 3 
                    images.append(color_array)
                    picture = plt.imshow(color_array, cmap='Greys')
                    plt.show()
                    self.generate_video(video_name, images)
                    return 0 
            
            # for debugging, print out the agent location and ghost locations
            print(f"\nAgent 2 Location:\t {self.location}")
            for i in range(len(env.ghosts)):
                print(f"Ghost {i} Location:\t {env.ghosts[i].location}")
            color_array = env.get_picture()
            color_array[self.location[0]][self.location[1]] = 3 
            picture = plt.imshow(color_array, cmap='Greys')
            images.append(color_array)
            plt.show()

    def run_agent2(self, env):
        path = self.plan_path((0,0), env)
        self.paths = {self.location : deepcopy(path)}
        while self.isalive:
            #print(self.location)
            if self.location == (final_variables.SIZE-1, final_variables.SIZE-1):
                return 1 
            action = path.pop(0) 
            #if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():

            if action not in self.ghost_current_locations(env):
                self.location = action 
            else:
                if self.location in self.paths: 
                    path = deepcopy(self.paths[self.location])
                    #print(path)
                else: 
                    path = self.plan_path(self.location, env)
                    self.paths[self.location] = deepcopy(path) 
                    #print(path)
                #print(paths.keys())
                #print(paths.values())
  
                action = path.pop(0) 
                #if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
                if action not in self.ghost_current_locations(env):
                    self.location = action 
                else:
                    self.location = self.move_agent_away_from_nearest_ghost(env, self.nearest_visible_ghost(env))
            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 
        return 0 
    
    def run_agent2_forecast(self, env):
        path = super().plan_path((0,0), env)
        self.paths = {self.location : deepcopy(path)}
        while self.isalive:
            #print(self.location)
            if self.location == (final_variables.SIZE-1, final_variables.SIZE-1):
                return 1 
            action = path.pop(0) 
            if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():

            #if action not in self.ghost_current_locations(env):
                self.location = action 
            else:
                if self.location in self.paths: 
                    path = deepcopy(self.paths[self.location])
                    #print(path)
                else: 
                    path = self.plan_path(self.location, env)
                    self.paths[self.location] = deepcopy(path) 
                    #print(path)
                #print(paths.keys())
                #print(paths.values())
  
                action = path.pop(0) 
                if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
                #if action not in self.ghost_current_locations(env):
                    self.location = action 
                else:
                    self.location = self.move_agent_away_from_nearest_ghost(env, self.nearest_visible_ghost(env))
            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 
        return 0 