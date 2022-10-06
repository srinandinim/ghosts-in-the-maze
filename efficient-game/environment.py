import constants as constants
import numpy as np 
import random 

class Environment:

    def __init__(self, num_ghosts=1):
        self.maze_grid = self.make_valid_maze()
        self.generate_ghosts(num_ghosts=1)
        self.update_ghost_locations(self.ghost_locations)

    def make_maze(self, shape):
        """
        generates a np.int array of grid_size
        with 28% probability, make a cell blocked
        representation: {blocked:1, unblocked:0}
        manually sets top left/bottom right unblocked
        """
        maze = np.random.randint(1, 100, size=shape)
        maze = np.where(maze <= 28, 1, 0)
        maze[0][0], maze[shape[0]-1][shape[1]-1]= 0, 0
        return maze 
    
    def dfs(self, maze, current, visited):
        """
        runs dfs to see if a path exists from current location
        to the bottom right corner of the maze. 
        """
        if current == (constants.SIZE[0]-1, constants.SIZE[1]-1):
            return True
        visited.add(current)
        neighbors = self.get_valid_neighbors(current, maze)
        for neighbor in neighbors:
            if neighbor not in visited and self.dfs(maze, neighbor, visited) == True:
                return True
        return False

    def is_valid_maze(self, maze):
        """
        The maze is valid if a path exists from top left to bottom right of maze. 
        You can only pass through locations where matrix is 0, since 1 is blocked. 
        Return true if a path exists from top left to bottom right. Use DFS. 
        """
        visited = set()
        return self.dfs(maze, (0, 0), visited)      

    def make_valid_maze(self):
        """
        generates mazes until at least 1 path exists 
        from the top left to the bottom right with DFS.
        """
        maze = self.make_maze(constants.SIZE)
        while self.is_valid_maze(maze) == False:
            maze = self.make_maze(constants.SIZE)
        return maze 

    def get_inbounds_actionspace(self, position):
        """
        for an agent or ghost, find all valid positions
        that are within dimensions of the maze. 
        """
        x, y = position[0], position[1]
        left = (x-1, y) if x > 0 else None 
        right = (x+1, y) if x < constants.SIZE[0]-1 else None 
        up = (x, y-1) if y > 0 else None 
        down = (x, y+1) if y < constants.SIZE[1]-1 else None 
        return list(filter(lambda x: x != None, [left, right, up, down]))

    def get_valid_neighbors(self, position, grid):
        """
        for position (x,y) finds all valid neighbors
        for an agent that are in-bounds and do not hit wall.
        """
        x, y = position[0], position[1]
        inbounds_actionspace = self.get_inbounds_actionspace(position)
        neighbors = list(filter(lambda x: grid[x[0]][x[1]] == 0, inbounds_actionspace))
        return neighbors

    def generate_ghosts(self, num_ghosts=1):
        """
        generates num_ghosts randomly on the board 
        stores {ghost#: ghost_location} in dictionary
        """
        self.ghost_locations = {}
        for i in range(num_ghosts):
            self.ghost_locations[i] = (np.random.randint(0, constants.SIZE[0]-1), np.random.randint(0, constants.SIZE[1]-1))
        self.ghost_grid = self.update_ghost_grid(self.ghost_locations)

    def update_ghost_locations(self, ghost_locations):
        """
        updates location of every ghost in grid
        1. randomly select possibly action direction
        2. validate that move is in bounds 
        3. otherwise, keep randomly selecting action.
        4. if action is in unblocked cell, move there
        5. otherwise, move into cell with p=0.5
        """
        for ghost in ghost_locations.keys():
            location = ghost_locations[ghost]
            possible_inbound_actions = self.get_inbounds_actionspace(location) 

            choice = np.random.randint(0, len(possible_inbound_actions))
            action = possible_inbound_actions[choice]

            if self.maze[action[0]][action[1]] == 1: 
                if random.random() <= 0.5:
                    self.ghost_locations[ghost] = action 
                else: self.ghost_locations[ghost] = location 
            else: self.ghost_locations[ghost] = action 

    def update_ghost_grid(self, ghost_locations):
        """
        creates a grid with same size of maze
        1 for every location where ghost exists
        0 everywhere ghost doesn't exist
        """
        ghost_grid = np.zeros_like(self.maze_grid)
        for value in ghost_locations.values():
            ghost_grid[value[0]][value[1]] = 1
        return ghost_grid 

env = Environment() 
print(env.maze_grid)
print(env.ghost_grid)
print(env.ghost_locations)




