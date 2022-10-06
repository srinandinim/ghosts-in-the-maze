import constants as constants
import numpy as np 

class Environment:

    def __init__(self):
        self.maze = self.make_valid_maze()

    def make_maze(self, shape):
        maze = np.random.randint(1, 100, size=shape)
        maze = np.where(maze <= 28, 1, 0)
        maze[0][0], maze[shape[0]-1][shape[1]-1]= 0, 0
        return maze 

    def make_valid_maze(self):
        maze = self.make_maze(constants.SIZE)
        while self.is_valid_maze(maze) == False:
            maze = self.make_maze(constants.SIZE)
        return maze 
    
    def dfs(self, maze, current, visited):
        if current == (constants.SIZE[0]-1, constants.SIZE[1]-1):
            return True
        visited.add(current)
        neighbors = self.get_neighbors(current, maze)
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

    def get_neighbors(self, position, grid):
        """
        Get non-blocked neighbors of position (x,y).
        """
        x, y = position[0], position[1]

        left = (x-1, y) if x > 0 else None 
        right = (x+1, y) if x < constants.SIZE[0]-1 else None 
        up = (x, y-1) if y > 0 else None 
        down = (x, y+1) if y < constants.SIZE[1]-1 else None 

        neighbors = list(filter(lambda x: x != None and grid[x[0]][x[1]] == 0, [left, right, up, down]))

        return neighbors

env = Environment() 
print(env.maze)
print(env.get_neighbors((1,0), env.maze))



