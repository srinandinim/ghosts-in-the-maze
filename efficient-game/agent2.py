import time
import constants 
from copy import deepcopy 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from agent import Agent 

class Agent2(Agent):

    def __init__(self):
        super().__init__() 
        self.has_path = True 
    
    def modified_bfs(self, env, goal, queue, visited, prev):
        """
        runs BFS on grid and stores prev pointers to restore path.
        also modifies standard BFS to determine if successful. 
        returns tuple: (T/F if successful, previous pointers if yes, else [])
        we use the effective grid for BFS
        """
        while len(queue) > 0:
            #print(queue)
            parent = queue.pop(0)
            visited.add(parent)
            if parent == goal: 
                return True, prev
            neighbors = self.get_valid_neighbors(parent, env.effective_maze)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    prev[neighbor] = parent 
        return False, []  
    
    def modified_plan_path(self, env, source):
        """
        return planned successul path if it exists 
        """
        # use queue/visited/prev for running BFS for path planning
        queue = [source]
        visited = set(source)
        prev = ({source : None})

        # run BFS to find optimal path from start to end without ghosts
        success, previous = self.modified_bfs(env, (constants.SIZE[0]-1, constants.SIZE[1]-1), queue, visited, prev)

        # finds optimal path from the BFS having stored prev pointers, if path exists 
        if success == True:
            path = self.path_from_pointers(source, (constants.SIZE[0]-1, constants.SIZE[1]-1), previous)
            return path 
        else: return [] 
        
    def nearest_visible_ghost(self, env):
        """
        finds coordinates of nearest ghost from current position
        """
        # maximum upper bound on distance for ghosts in the maze, for dist/coords
        min_distance = constants.SIZE[0] * constants.SIZE[1] + 1 
        min_coordinates = constants.SIZE 

        # for every ghost, compute manhattan distance to agent and 
        # retrieve the coordinates of the ghost with min distance to agent
        for ghost in env.visible_ghosts.keys():
            dist = self.manhattan_distance(env.visible_ghosts[ghost], self.location) 
            if dist < min_distance:
                min_distance = dist 
                min_coordinates = env.visible_ghosts[ghost] 
        return min_coordinates 
    
    def move_agent_away_from_nearest_ghost(self, env):

        # retrieves possible valid moves from current location 
        possible_valid_moves = self.get_valid_neighbors(self.location, env.effective_maze)
        if len(possible_valid_moves) == 0: return self.location 

        # computes how far away nearest ghost is in the local action space 
        distances = {} 
        for possible_move in possible_valid_moves:
            distances[possible_move] = self.manhattan_distance(possible_move, self.nearest_visible_ghost(env))
        
        # make the move that moves you farthest away from the ghost 
        max_dist = 0
        max_move = self.location 
        for move, dist in distances.items():
            if dist> max_dist:
                max_dist = dist
                max_move = move 
        return max_move 

    def run_agent2(self, env):
        path = self.modified_plan_path(env, self.location)
        while self.is_alive == True:
            if self.location == (constants.SIZE[0]-1, constants.SIZE[1]-1): 
                return 1 
            if self.has_path == False:
                path = self.modified_plan_path(env, self.location)
            self.has_path = False 
            if len(path) > 0:
                action = path.pop(0)
                if action not in env.ghost_locations.values():
                    self.location = action 
                    self.has_path = True 
                else:
                    path = self.modified_plan_path(env, self.location)
                    if len(path) > 0:
                        action = path.pop(0)
                        if action not in env.ghost_locations.values():
                            self.location = action 
                            self.has_path = True 
                        else:
                            self.location = self.move_agent_away_from_nearest_ghost(env)
                    else: 
                        self.location = self.move_agent_away_from_nearest_ghost(env)
            else: 
                self.location = self.move_agent_away_from_nearest_ghost(env)

            if self.location in env.ghost_locations.values():
                self.is_alive = False 
                return 0 
        
            env.step() 

    def run_agent2_video(self, env):
        video_frames = []
        video_name = "agent2_" + str(time.time())
        path = self.modified_plan_path(env, self.location)
        while self.is_alive == True:
            video_frames.append(self.get_image_array(env))
            if self.location == (constants.SIZE[0]-1, constants.SIZE[1]-1): 
                self.generate_video(video_name, video_frames)
                return 1 
            if self.has_path == False:
                path = self.modified_plan_path(env, self.location)
            self.has_path = False 
            if len(path) > 0:
                action = path.pop(0)
                if action not in env.ghost_locations.values():
                    self.location = action 
                    self.has_path = True 
                else:
                    path = self.modified_plan_path(env, self.location)
                    if len(path) > 0:
                        action = path.pop(0)
                        if action not in env.ghost_locations.values():
                            self.location = action 
                            self.has_path = True 
                        else:
                            self.location = self.move_agent_away_from_nearest_ghost(env)
                    else: 
                        self.location = self.move_agent_away_from_nearest_ghost(env)
            else: 
                self.location = self.move_agent_away_from_nearest_ghost(env)

            if self.location in env.ghost_locations.values():
                self.is_alive = False 
                self.generate_video(video_name, video_frames)
                return 0 
        
            env.step() 


    def run_agent2_debug(self, env):
        path = self.modified_plan_path(env, self.location)
        print(f"This is the Agent's plan: {path}")

        while self.is_alive == True:
            print(f"The Agent's current location is: {self.location}")
            env.debugging_all()

            if self.location == (constants.SIZE[0]-1, constants.SIZE[1]-1): 
                return 1 

            if self.has_path == False:
                print("NO PATH EXISTS, REPLANNING!")
                path = self.modified_plan_path(env, self.location)
                print(f"NEW PATH IS NOW: {path}")
            self.has_path = False 

            if len(path) > 0:
                action = path.pop(0)
                if action not in env.ghost_locations.values():
                    self.location = action 
                    self.has_path = True 
                else:
                    print("GHOST IS IN THE LOCATION OF ACTION! REPLANNING:")
                    path = self.modified_plan_path(env, self.location)
                    print(f"NEW PATH IS NOW: {path}")
                    if len(path) > 0:
                        action = path.pop(0)
                        if action not in env.ghost_locations.values():
                            self.location = action 
                            self.has_path = True 
                        else:
                            print("GHOST IS IN THE LOCATION OF ACTION AGAIN!") 
                            self.location = self.move_agent_away_from_nearest_ghost(env)
                            print("MOVE AWAY FROM THE NEAREST GHOST")
                    else: 
                        print("NO PATH EXISTS, MOVING AWAY FROM NEAREST GHOST!") 
                        self.location = self.move_agent_away_from_nearest_ghost(env)
            else: 
                print("NO PATH EXISTS, MOVING AWAY FROM NEAREST GHOST!")
                self.location = self.move_agent_away_from_nearest_ghost(env)

            if self.location in env.ghost_locations.values():
                self.is_alive = False 
                return 0 
            
            color_array = self.get_image_array(env)
            plt.imshow(color_array,cmap='Greys')
            plt.show()

            env.step() 


