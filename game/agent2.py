from copy import deepcopy

import matplotlib.pyplot as plt

import game.final_variables as final_variables
from game.agent1 import Agent1
from game.environment import Environment


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
        self.has_path = True
    
    def plan_path(self, env, source):
        """
        plans the path agent will then execute using BFS
        """
        # use queue/visited/prev for running BFS for path planning
        queue = [source]
        visited = set(source)
        prev = ({source : None})

        # run BFS to find optimal path from start to end when considering ghosts
        success, previous = self.bfs(env, final_variables.GOAL, queue, visited, prev)
        if success:
            return self.path_from_pointers(source, final_variables.GOAL, previous)[1:]

        return [] 

    def bfs(self, env, goal, queue, visited, prev):
        """
        runs BFS and stores the prev pointers along path. 
        """
        while len(queue) > 0:
            parent = queue.pop(0)
            visited.add(parent)
            if parent == goal: 
                return True, prev
            for d in Environment.DIRECTIONS:
                x = parent[0] + d[0]
                y = parent[1] + d[1] 
                if self.is_valid_position( (x,y) ) and (x,y) not in visited:
                    if env.maze[x][y].get_blocked() == False and not any((x,y) == ghost.location for ghost in env.ghosts): 
                        queue.append((x,y))
                        prev[(x,y)] = parent
        return False, []
    
    def manhattan_distance(self, coord1, coord2):
        """
        calculates manhattan distance between two locations
        """
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

    def move_agent_away_from_nearest_ghost(self, env):
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

    def run_agent2(self, env):
        path = self.plan_path(env, self.location)
        while self.isalive:
            if self.location == final_variables.GOAL:
                return 1 

            if self.has_path == False:
                path = self.plan_path(env, self.location)

            self.has_path = False
            if path:
                action = path.pop(0)
                if action not in env.get_ghosts_locations():
                    self.location = action
                    self.has_path = True
                else:
                    path = self.plan_path(env, self.location)
                    if path:
                        action = path.pop(0)
                        if action not in env.get_ghosts_locations():
                            self.location = action 
                            self.has_path = True
                        else:
                            self.location = self.move_agent_away_from_nearest_ghost(env)
                    else:
                        self.location = self.move_agent_away_from_nearest_ghost(env)
            else:
                self.location = self.move_agent_away_from_nearest_ghost(env)

            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 
        return 0 

    def run_agent2_verbose(self, env):
        self.print_environment(env)
        path = self.plan_path(env, self.location)

        print(f"\nAgent 2 Location: {self.location}")
        print(f"Ghost Location: {env.get_ghosts_locations()}")
        print(f"PLANNING: Agent 2's Planned Path is: {path}")
        color_array = env.get_picture()
        color_array[self.location[0]][self.location[1]] = 3 
        plt.imshow(color_array, cmap='Greys')
        plt.show()

        self.has_path = True
        while self.isalive:
            if self.location == final_variables.GOAL:
                print("\nSUCCESS (+1): THE AGENT REACHED THE GOAL!")
                color_array = env.get_picture()
                color_array[self.location[0]][self.location[1]] = 3 
                plt.imshow(color_array, cmap='Greys')
                plt.show()
                return 1 

            if self.has_path == False:
                path = self.plan_path(env, self.location)
                print(f"REPLANNING: Agent 2's Planned Path is: {path}")

            self.has_path = False
            if path:
                action = path.pop(0)
                if action not in env.get_ghosts_locations():
                    self.location = action
                    self.has_path  = True
                else:
                    path = self.plan_path(env, self.location)
                    print(f"REPLANNING: Agent 2's Planned Path is: {path}")
                    if path:
                        action = path.pop(0)
                        if action not in env.get_ghosts_locations():
                            self.location = action 
                            self.has_path  = True
                        else:
                            print(f"MOVE AWAY FROM GHOST: New path is in ghost danger zone!")
                            self.location = self.move_agent_away_from_nearest_ghost(env)
                    else:
                        print(f"MOVE AWAY FROM GHOST: No path to reach the end at the moment")
                        self.location = self.move_agent_away_from_nearest_ghost(env)
            else:
                print(f"MOVE AWAY FROM GHOST: No path to reach the end at the moment")
                self.location = self.move_agent_away_from_nearest_ghost(env)

            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    print("\nFAILURE (+0): THE AGENT GOT KILLED BY A GHOST")
                    self.isalive = False 
                    return 0 

            print(f"\nAgent 2 Location:\t {self.location}")
            for i in range(len(env.ghosts)):
                print(f"Ghost {i} Location:\t {env.ghosts[i].location}")
            color_array = env.get_picture()
            color_array[self.location[0]][self.location[1]] = 3 
            plt.imshow(color_array, cmap='Greys')
            plt.show()
        return 0 
    
    def ghost_actionspace(self, env, ghost_location):
        ghost_actions = {}
        for d in self.DIRECTIONS:
            dx = d[0] + ghost_location[0]
            dy = d[1] + ghost_location[1]
            new_pos = (dx, dy)
            if self.is_valid_position(new_pos):
                if env.maze[dx][dy].get_blocked():
                    ghost_actions[new_pos] = 0.5 
                else: 
                    ghost_actions[new_pos] = 1.0
        return ghost_actions 

    def run_agent2_forecast(self, env):
        path = self.plan_path(env, self.location)
        while self.isalive:
            if self.location == final_variables.GOAL:
                return 1 

            if self.has_path == False:
                path = self.plan_path(env, self.location)

            self.has_path = False
            if path:
                action = path.pop(0)
                if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
                    self.location = action
                    self.has_path = True
                else:
                    path = self.plan_path(env, self.location)
                    if path:
                        action = path.pop(0)
                        if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
                            self.location = action 
                            self.has_path = True
                        else:
                            self.location = self.move_agent_away_from_nearest_ghost(env)
                    else:
                        self.location = self.move_agent_away_from_nearest_ghost(env)
            else:
                self.location = self.move_agent_away_from_nearest_ghost(env)

            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 
        return 0 