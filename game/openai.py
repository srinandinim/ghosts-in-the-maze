"""
Develop a pac-man derivative simulator with numpy. 
- The environment is a 51x51 maze-like square grid. There are blocked (1) and unblocked cells (0) in the environment and the agent can move among blocked cells but not unblocked.
- Starting with an empty 51 x 51 square grid, iterate through each cell, and with probability 0.28 make it blocked, with probability 0.72 make it unblocked.
- If there is no path that exists from (0,0) to (50,50) in the maze with DFS, then reject that maze and keep re-generating the maze until a good maze exists. 

The agent is going to start in the upper left corner, and attempt to navigate to the lower right corner. The agent can move in the cardinal directions (up/down/left/right), but only between unblocked squares, and cannot move outside the 51x51 grid. At any time, the agent can ‘see’ the entirety of the maze, and use this information to plan a path.

Unfortunately for the agent, the maze is full of ghosts. Each ghosts starts at a random location in the maze that is reachable from the upper left corner (so that no ghost gets walled off).If the agent enters a cell with a ghost (or a ghost enters the agent’s cell), the agent dies. This is to be avoided. The ghosts move according to simple rules: at every timestep, a ghost picks one of its neighbors (up/down/left/right); if the picked neighbor is unblocked, the ghost moves to that cell; if the picked neighbor is blocked, the ghost either stays in place with probability 0.5, or moves into the blocked cell with probability 0.5. (These rules apply even if the ghost is currently within a blocked cell.) Every time the agent moves, the ghosts move according to the above rule. If the agent touches a ghost, the agent dies.
"""
import numpy as np
import random
import pprint
import matplotlib.pyplot as plt
import copy


class Maze():
    """
    Maze class, which contains the grid and the ghosts.
    """
    def __init__(self, size, block_prob=0.3):
        self.size = size
        self.grid = self.init_grid()

        # Game will not start unless a path to the goal is possible
        path_found = False
        while not path_found:
            self.block_grid(block_prob)
            path_found = self.path_to_goal()
            print("path found: {0}".format(path_found)) # just to check that it is generating a new grid

        self.ghosts_location = self.init_ghosts()

        self.agent_location = (0,0)

    def init_grid(self):
        grid = np.zeros((self.size, self.size))
        return grid

    def block_grid(self, block_prob=0.3):
        self.grid = np.random.choice(a=[1, 0], size=(self.size, self.size), p=[block_prob, 1-block_prob])

    @staticmethod
    def is_blocked(cell):
        blocked_cells = [1]
        return cell in blocked_cells

    @staticmethod
    def is_unblocked(cell):
        unblocked_cells = [0]
        return cell in unblocked_cells

    def path_to_goal(self):
        start = (0, 0)
        goal = (self.size-1, self.size-1)
        return self.depth_first_search(start, goal)

    def depth_first_search(self, start, goal):
        """
        Find a path from start to goal if possible.
        input: start = tuple = (x, y)
               goal = tuple = (x, y)
               grid = 2D numpy array
               visited = 2D numpy array
        output: found = boolean
                grid = 2D numpy array
        """
        found, path = self.dfs_rec(start=start, goal=goal, grid=self.grid.copy(), visited=np.full((self.size, self.size), False))
        return found

    @staticmethod
    def dfs_rec(grid, visited, x, y, start, goal):
        """
        Recursive function to find a path from start to goal with DFS.
        input: start = tuple = (x, y)
               goal = tuple = (x, y)
               grid = 2D numpy array
               visited = 2D numpy array
        output: found = boolean
                grid = 2D numpy array
        """
        size = grid.shape[0]
        if x < 0 or x >= size or y < 0 or y >= size:
            return False, grid

        if visited[x][y] == True:
            return False, grid

        if Maze.is_blocked(grid[x][y]):
            return False, grid

        if x == goal[0] and y == goal[1]:
            return True, grid

        visited[x][y] = True
        grid[x][y] = 2

        found, grid = Maze.dfs_rec(grid, visited, x+1, y, start, goal)
        if found:
            return True, grid

        found, grid = Maze.dfs_rec(grid, visited, x-1, y, start, goal)
        if found:
            return True, grid

        found, grid = Maze.dfs_rec(grid, visited, x, y+1, start, goal)
        if found:
            return True, grid

        found, grid = Maze.dfs_rec(grid, visited, x, y-1, start, goal)
        if found:
            return True, grid

        grid[x][y] = 0
        return False, grid

    def init_ghosts(self):
        num_ghosts = self.size * self.size
        ghosts = np.full((num_ghosts, 2), False)

        num_ghosts_init = 0
        while num_ghosts_init < num_ghosts:
            x = random.randint(0, self.size-1)
            y = random.randint(0, self.size-1)
            if not Maze.is_blocked(self.grid[x][y]) and not self.depth_first_search((0,0), (x,y)):
                # Add ghost
                ghosts[num_ghosts_init] = (x, y)
                num_ghosts_init += 1

        return ghosts

    def make_move(self, action):
        next_state = copy.deepcopy(self)

        if action == 'up':
            next_state.agent_location = (self.agent_location[0], self.agent_location[1]-1)
        elif action == 'right':
            next_state.agent_location = (self.agent_location[0]+1, self.agent_location[1])
        elif action == 'down':
            next_state.agent_location = (self.agent_location[0], self.agent_location[1]+1)
        elif action == 'left':
            next_state.agent_location = (self.agent_location[0]-1, self.agent_location[1])

        # Check if move is valid
        if not self.is_valid_move(next_state.agent_location):
            return None

        # Check if a ghost is at the agent's next location. If so, agent dies.
        for i in range(self.ghosts_location.shape[0]):
            if next_state.agent_location == self.ghosts_location[i]:
                next_state.alive = False
                break

        # Move a ghost
        for i in range(self.ghosts_location.shape[0]):
            next_state.ghosts_location[i] = self.move_ghost(self.ghosts_location[i])

        return next_state

    def move_ghost(self, ghost):
        """
        Move a ghost according to the probabilistic rules.
        """
        # 1. Pick random neighbor
        dir_choices = ['up', 'down', 'left', 'right']
        next_dir = random.choice(dir_choices)
        next_state = copy.deepcopy(self)

        if next_dir == 'up':
            next_state.ghosts_location = (ghost[0], ghost[1]-1)
        elif next_dir == 'right':
            next_state.ghosts_location = (ghost[0]+1, ghost[1])
        elif next_dir == 'down':
            next_state.ghosts_location = (ghost[0], ghost[1]+1)
        elif next_dir == 'left':
            next_state.ghosts_location = (ghost[0]-1, ghost[1])

        # 2. Check if move is valid
        if not self.is_valid_move(next_state.ghosts_location):
            # 3. If not, either move to the blocked cell with probability 0.5 or stay put with probability 0.5
            if random.random() < 0.5:
                return next_state.ghosts_location

        # 4. If so, move that way
        return next_state.ghosts_location

    def is_valid_move(self, cell):
        """
        Check if the cell is in the grid and not blocked.
        """
        x, y = cell
        if 0 <= x < self.size and 0 <= y < self.size:
            if not Maze.is_blocked(self.grid[x][y]):
                return True
        return False

    def is_goal(self):
        goal = (self.size-1, self.size-1)
        if self.agent_location[0] == goal[0] and self.agent_location[1] == goal[1]:
            return True
        return False

    def is_alive(self):
        return self.alive

    def get_grid(self):
        return self.grid

    def __str__(self):
        return pprint.pformat(self.grid)


def test_Maze():
    """
    Test the functionality of Maze.
    """
    size = 5
    maze = Maze(size)
    print("Grid:")
    print(maze)
    print("Ghosts:")
    print(maze.ghosts_location)
    return maze


def test_path_to_goal():
    """
    Test the functionality of Maze.
    """
    size = 51
    block_prob = 0.3
    maze = Maze(size, block_prob)
    print("Grid:")
    print(maze)
    print("Ghosts:")
    print(maze.ghosts_location)
    return maze


def print_maze(grid):
    """
    Print the maze.
    """
    plt.imshow(grid, cmap="Set2", interpolation="nearest")
    plt.show()


if __name__ == "__main__":
    maze = test_Maze()
    print(maze.get_grid())
    print_maze(maze.get_grid())

    # Testing transitions
    action = 'down'
    next_state = maze.make_move(action)
    print("Agent: {0}".format(next_state.agent_location))
    print("Ghost 1: {0}".format(next_state.ghosts_location[0]))
    print("Ghost 2: {0}".format(next_state.ghosts_location[1]))
    print("Ghost 3: {0}".format(next_state.ghosts_location[2]))
    print("Ghost 4: {0}".format(next_state.ghosts_location[3]))
    # print(next_state)
    # print(next_state.ghosts_location)
    # print(next_state.get_grid())
    # print_maze(next_state.get_grid())

    action = 'right'
    next_state = next_state.make_move(action)
    print("Agent: {0}".format(next_state.agent_location))
    print("Ghost 1: {0}".format(next_state.ghosts_location[0]))
    print("Ghost 2: {0}".format(next_state.ghosts_location[1]))
    print("Ghost 3: {0}".format(next_state.ghosts_location[2]))
    print("Ghost 4: {0}".format(next_state.ghosts_location[3]))
    # print(next_state)
    # print(next_state.ghosts_location)
    # print(next_state.get_grid())
    # print_maze(next_state.get_grid())

    action = 'down'
    next_state = next_state.make_move(action)
    print("Agent: {0}".format(next_state.agent_location))
    print("Ghost 1: {0}".format(next_state.ghosts_location[0]))
    print("Ghost 2: {0}".format(next_state.ghosts_location[1]))
    print("Ghost 3: {0}".format(next_state.ghosts_location[2]))
    print("Ghost 4: {0}".format(next_state.ghosts_location[3]))
    # print(next_state)
    # print(next_state.ghosts_location)
    # print(next_state.get_grid())
    # print_maze(next_state.get_grid())