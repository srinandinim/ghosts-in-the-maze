import random
from copy import deepcopy
import numpy as np
import constants as constants


class Environment:

    def __init__(self, num_ghosts=1):
        # sets up maze_grid
        self.maze_grid = self.make_valid_maze()

        # sets up ghost_grid, ghost_locations
        self.generate_ghosts(num_ghosts)

        # sets up visible_ghost_locations
        self.update_visible_ghosts(self.ghost_locations)

        # sets up visible_ghosts_grid
        self.visible_ghosts_grid = self.update_visible_ghost_grid(
            self.visible_ghosts)

        # sets up the effective grid (maze and ghost overlay)
        self.effective_blocked_maze(self.maze_grid, self.ghost_grid)

    def step(self):
        """
        updates environment for 1 step:
        updates all_ghosts, all_ghosts_grid, visible_ghosts, visible_ghosts_grid
        updates the effective maze 
        """
        self.update_ghosts()
        self.effective_blocked_maze(self.maze_grid, self.ghost_grid)

    def make_maze(self, shape):
        """
        generates a np.int array of grid_size
        with 28% probability, make a cell blocked
        representation: {blocked:1, unblocked:0}
        manually sets top left/bottom right unblocked
        """
        maze = np.random.randint(1, 100, size=shape)
        maze = np.where(maze <= 28, 1, 0)
        maze[0][0], maze[shape[0]-1][shape[1]-1] = 0, 0
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
        inbounds_actionspace = self.get_inbounds_actionspace(position)
        neighbors = list(
            filter(lambda x: grid[x[0]][x[1]] == 0, inbounds_actionspace))
        return neighbors

    def dfs(self, maze):
        """
        runs dfs to see if a path exists from top left corner
        to the bottom right corner of the maze. 
        """
        stack = [(0, 0)]
        visited = set()

        while stack:
            current = stack.pop()
            if current == (constants.SIZE[0]-1, constants.SIZE[1]-1):
                return True

            visited.add(current)
            neighbors = self.get_valid_neighbors(current, maze)
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)

        return False

    def make_valid_maze(self):
        """
        generates mazes until at least 1 path exists 
        from the top left to the bottom right with DFS.
        """
        maze = self.make_maze(constants.SIZE)
        while self.dfs(maze) == False:
            maze = self.make_maze(constants.SIZE)
        return maze

    def generate_ghosts(self, num_ghosts=1):
        """
        generates num_ghosts randomly on the board 
        stores {ghost#: ghost_location} in dictionary
        """
        self.ghost_locations = {}
        for i in range(num_ghosts):
            self.ghost_locations[i] = (np.random.randint(
                0, constants.SIZE[0]-1), np.random.randint(0, constants.SIZE[1]-1))
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

            if self.maze_grid[action[0]][action[1]] == 1:
                if random.random() <= 0.5:
                    self.ghost_locations[ghost] = action
                else:
                    self.ghost_locations[ghost] = location
            else:
                self.ghost_locations[ghost] = action

    def update_visible_ghosts(self, ghost_locations):
        """
        stores all visible ghosts in visible ghosts dict
        """
        self.visible_ghosts = {}
        for ghost in ghost_locations.keys():
            location = ghost_locations[ghost]
            if self.maze_grid[location[0]][location[1]] == 0:
                self.visible_ghosts[deepcopy(ghost)] = deepcopy(location)

    def update_visible_ghost_grid(self, ghost_locations):
        """
        creates a grid with same size of maze
        1 for every location where VISIBLE ghost exists
        0 everywhere VISIBLE ghost doesn't exist
        """
        ghost_grid = np.zeros_like(self.maze_grid)
        for value in ghost_locations.values():
            ghost_grid[value[0]][value[1]] = 1
        return ghost_grid

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

    def update_visible_ghost_grid(self, ghost_locations):
        ghost_grid = np.zeros_like(self.maze_grid)
        for value in ghost_locations.values():
            ghost_grid[value[0]][value[1]] = 1
        return ghost_grid

    def update_ghosts(self):
        """
        updates the ghost location and effective ghost grid
        updates the visible ghost, visible ghost grid
        """
        self.update_ghost_locations(self.ghost_locations)
        self.update_visible_ghosts(self.ghost_locations)
        self.ghost_grid = self.update_ghost_grid(self.ghost_locations)
        self.visible_ghosts_grid = self.update_visible_ghost_grid(
            self.visible_ghosts)

    def effective_blocked_maze(self, maze_grid, ghost_grid):
        """
        takes ghost grid and maze grid and overlaps
        them each other to return the effective blocked maze
        """
        self.effective_maze = np.zeros_like(maze_grid)
        self.effective_maze[maze_grid == 1] = 1
        self.effective_maze[ghost_grid == 1] = 1

    def debugging_print_maze_grid(self):
        print(f"THIS IS THE CURRENT MAZE GRID (0: Unblocked, 1: Blocked)\n")
        print(self.maze_grid)
        print("\n")

    def debugging_print_all_ghost_grid(self):
        print(f"THIS IS THE CURRENT GHOST GRID (0: No Ghost, 1: Ghost Present)")
        print(self.ghost_grid)
        print("\n")

    def debugging_print_all_ghost_locations(self):
        print(f"THESE ARE ALL THE CURRENT GHOST LOCATIONS (number:location)")
        print(self.ghost_locations)
        print("\n")

    def debugging_print_visible_ghost_grid(self):
        print(f"THIS IS THE CURRENT VISIBLE GHOST GRID (0: No Ghost, 1: Ghost Present)")
        print(self.visible_ghosts_grid)
        print("\n")

    def debugging_print_visible_ghost_locations(self):
        print(f"THESE ARE ALL THE VISIBLE GHOST LOCATIONS (number:location)")
        print(self.visible_ghosts)
        print("\n")

    def debugging_effective_maze(self):
        print(f"THE EFFECTIVE MAZE (GHOST/BLOCKS OVERLAY) (0:Unblocked,1:Blocked)")
        print(self.effective_maze)
        print("\n")

    def debugging_all(self):
        self.debugging_print_maze_grid()
        self.debugging_print_all_ghost_grid()
        self.debugging_print_all_ghost_locations()
        self.debugging_print_visible_ghost_grid()
        self.debugging_print_visible_ghost_locations()
        self.debugging_effective_maze()
