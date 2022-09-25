from queue import Empty
from game.block import Block
from game.ghost import Ghost 
import numpy as np 
import matplotlib.pyplot as plt
import game.final_variables as final_variables

class Environment:

    SIZE = final_variables.SIZE
    BLOCKING_PROBABILITY = final_variables.BLOCKING_PROBABILITY
    DIRECTIONS = final_variables.DIRECTIONS

    def __init__(self, num_ghosts=1):
        """
        generates mazes until valid maze retrieved
        """
        self.generate_maze()
        while not self.validate_maze():
            self.generate_maze()
        self.ghosts = [Ghost() for _ in range(num_ghosts)]
    
    def is_valid_position(self, pos):
        """
        validates whether new position is in board
        """
        x, y = pos[0], pos[1]
        return x >= 0 and y >= 0 and x < Environment.SIZE and y < Environment.SIZE

    def generate_maze(self):
        """
        generates mazes of blocks based on size and blocking probability
        initializes top left and bottom right to be unblocked blocks
        """
        self.maze = [[Block(Environment.BLOCKING_PROBABILITY) for x in range(Environment.SIZE)] for y in range(Environment.SIZE)] 
        self.maze[0][0].set_blocked(False)
        self.maze[Environment.SIZE - 1][Environment.SIZE - 1].set_blocked(False)

    def validate_maze(self):
        """
        maze is valid if there is >= 1 path from top left (s) to bottom right (g). 
        run DFS to validate whether path s->g exists to validate the maze.   
        we only care that a path EXISTS, not necessarily optimal path 
        hence, DFS is better than BFS for validation of optimal path
        """
        current = (0,0)
        visited = set() 
        return self.dfs(current, visited)

    def dfs(self, curr, visited):
        """
        dfs to see is path from source node to bottom right goal node
        """
        visited.add(curr)
        if curr[0] == curr[1] == Environment.SIZE - 1:
            return True 
        
        for d in Environment.DIRECTIONS:
            x = curr[0] + d[0]
            y = curr[1] + d[1] 
            if self.is_valid_position((x,y)) and (x,y) not in visited:
                if self.maze[x][y].get_blocked() == False: 
                    if self.dfs((x,y), visited) == True:
                        return True 
        return False 

    def bfs(self, visited, queue):
        """
        bfs to see is path from source node to bottom right goal node. 
        """
        while len(queue) > 0:
            curr = queue.pop(0)
            visited.add(curr)

            if curr[0] == curr[1] == Environment.SIZE - 1:
                return True 
            
            for d in Environment.DIRECTIONS:
                x = curr[0] + d[0]
                y = curr[1] + d[1] 
                if self.is_valid_position((x,y)) and (x,y) not in visited:
                    if self.maze[x][y].get_blocked() == False: 
                        queue.append((x, y))
        return False 

    def get_picture(self):
        """
        renders image of generated environment
        """
        array = [[1 if str(cell)=="T" else 0 for cell in row] for row in self.maze] 
        ghost_locations = [(ghost.location[0], ghost.location[1]) for ghost in self.ghosts]
        array = self.render_ghosts(ghost_locations, array)
        fig, ax = plt.subplots()
        picture = plt.imshow(array, cmap='binary')
        # plt.show()
        return array
    
    def render_ghosts(self, locations, array):
        """
        adds ghosts to image of maze
        """
        for ghost in locations:
            array[ghost[0]][ghost[1]] = 2
        return array

    def __str__(self):
        return '\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.maze])
