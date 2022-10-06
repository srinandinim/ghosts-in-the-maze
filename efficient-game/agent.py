import time
import constants 
from copy import deepcopy 
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Agent:

    def __init__(self):
        self.location = (0,0)
        self.is_alive = True 
    
    def get_valid_neighbors(self, pos, grid):
        """
        gets all valid neighbors in-bound
        and they are not blocked by path
        specify WHICH GRID:
        - self.maze_grid
        - self.effective_maze 
        """
        x, y = pos[0], pos[1]
        
        left = (x-1, y) if x > 0 else None 
        right = (x+1, y) if x < constants.SIZE[0]-1 else None 
        up = (x, y-1) if y > 0 else None 
        down = (x, y+1) if y < constants.SIZE[1]-1 else None 

        return list(filter(lambda x: x != None and grid[x[0]][x[1]] == 0, [left, right, up, down]))

    def bfs(self, env, goal, queue, visited, prev):
        """
        runs BFS on grid and stores prev pointers to restore path.
        """
        while len(queue) > 0:
            #print(queue)
            parent = queue.pop(0)
            visited.add(parent)
            if parent == goal: 
                return prev
            neighbors = self.get_valid_neighbors(parent, env.maze_grid)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    prev[neighbor] = parent 
        return prev 

    def path_from_pointers(self, source, goal, prev):
        """
        returns solution path from start to end node
        """
        path = [goal]
        current = goal
        while current != source:
            path.append(prev[current])
            current = prev[current]
        return list(reversed(path))

    def plan_path(self, env, source=(0,0)):
        """
        plans path agent will to get to end from source.
        """
        # use queue/visited/prev for running BFS for path planning
        queue = [source]
        visited = set(source)
        prev = ({source : None})

        # run BFS to find optimal path from start to end without ghosts
        previous = self.bfs(env, (constants.SIZE[0]-1, constants.SIZE[1]-1), queue, visited, prev)

        # finds optimal path from the BFS having stored prev pointers 
        path = self.path_from_pointers(source, (constants.SIZE[0]-1, constants.SIZE[1]-1), previous)

        # returns the optimal path from source to destination 
        return path 

    def manhattan_distance(self, coord1, coord2):
        """
        calculates manhattan distance between two coordinates
        """
        x = abs(coord2[0] - coord1[0])
        y = abs(coord2[1] - coord1[1])
        return x + y

    def get_image_array(self, env):

        """
        0: unblocked cell
        1: blocked cell
        2: cell with ghost
        3: agent location 
        """
        color_array = deepcopy(env.maze_grid)
        color_array[env.ghost_grid==1] = 2 
        color_array[self.location[0]][self.location[1]] = 3 
        return color_array 

    def generate_video(self, video_name, images):
        """
        generates video of agent's moves
        """
        frames = []
        fig = plt.figure()
        for i in range(len(images)):
            frames.append([plt.imshow(images[i], cmap='Greys',animated=True)])

        plt.close()

        ani = animation.ArtistAnimation(fig, frames, interval=120, blit=True, repeat=False)
        ani.save("replays/" + video_name + '.mp4')

class Agent1(Agent):

    def __init__(self):
        super().__init__() 

    def run_agent1(self, env):
        """
        # plan once using BFS 
        # while the agent is alive 
            # if we reach end of maze, reward=+1
            # agent takes the next action in plan 
            # update ghosts, and environment effective maze
            # if ghost intersects with agent, the agent dies and recieves 0 reward 
        """
        plan = super().plan_path(env, (0,0))
        while self.is_alive: 
            if self.location == (constants.SIZE[0]-1, constants.SIZE[1]-1): 
                return 1 
            self.location = plan.pop(0)
            if self.location in env.ghost_locations.values():
                self.is_alive = False 
                return 0 
            env.step() 

    def run_agent1_video(self, env):
        video_frames = []
        video_name = "agent1_" + str(time.time())

        plan = super().plan_path(env, (0,0))
        while self.is_alive: 
            video_frames.append(self.get_image_array(env))
            if self.location == (constants.SIZE[0]-1, constants.SIZE[1]-1): 
                self.generate_video(video_name, video_frames)
                return 1 
            self.location = plan.pop(0)
            if self.location in env.ghost_locations.values():
                self.is_alive = False 
                self.generate_video(video_name, video_frames)
                return 0 
            env.step()
        
    def run_agent1_debug(self, env):

        plan = super().plan_path(env, (0,0))
        print(f"This is the Agent's plan: {plan}")

        while self.is_alive:

            print(f"The Agent's current location is: {self.location}")
            env.debugging_all()

            if self.location == (constants.SIZE[0]-1, constants.SIZE[1]-1): 
                print("WIN!")
                return 1 
            
            action = plan.pop(0)  
            print(f"This is the Agent's next action: {action}")
            self.location = action 

            env.debugging_print_all_ghost_locations()

            color_array = self.get_image_array(env)
            plt.imshow(color_array,cmap='Greys')
            plt.show()

            if self.location in env.ghost_locations.values():
                print("LOSS!")
                self.is_alive = False 
                return 0 
            
            env.step() 

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
            neighbors = self.get_valid_neighbors(parent, env.effective_grid)
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
        min_distance = constants.SIZE[0] * constants.size[1] + 1 
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
        path = super().plan_path(env, self.location)
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
                        else: self.location = self.move_agent_away_from_nearest_ghost(env)
                    else: self.location = self.move_agent_away_from_nearest_ghost(env)
            else: self.location = self.move_agent_away_from_nearest_ghost(env)

            if self.location in env.ghost_locations.values():
                self.is_alive = False 
                return 0 


