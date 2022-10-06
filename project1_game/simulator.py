import random
import constants 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 

class Block:
    def __init__(self, probability):
        """
        initializes cell to be blocked based on probability p.
        """
        if random.random() <= probability:
            self.blocked = True
        else:
            self.blocked = False
    
    def get_blocked(self):
        """
        get_blocked retrieves whether block is blocked (T/F).
        """
        return self.blocked

    def set_blocked(self, b):
        """
        set_blocked makes a block blocked (T/F). 
        """
        self.blocked = b

    def __str__(self):
        """
        returns first char (T/F) if block is blocked.
        """
        return str(self.blocked)[0]

class Ghost:
    DIRECTIONS = constants.DIRECTIONS

    def __init__(self):
        """
        initializes ghost with location on board.
        """
        x = random.randint(0, constants.SIZE-1)
        y = random.randint(0, constants.SIZE-1)
        self.location = (x,y)
    
    def get_location(self):
        """
        returns the location of ghost on board.
        """
        return self.location 
    
    def is_valid_position(self, pos):
        """
        validates whether new position is in board
        """
        x, y = pos[0], pos[1]
        return x >= 0 and y >= 0 and x < constants.SIZE and y < constants.SIZE

    def update_location(self, env):
        """
        randomly chooses to go left, right, up, or down 
        """
        choice = random.randint(0,3)
        x = Ghost.DIRECTIONS[choice][0] + self.location[0]
        y = Ghost.DIRECTIONS[choice][1] + self.location[1]

        # makes sure that the direction ghost is going is in a valid direction 
        while not (self.is_valid_position((x,y))):
            choice = random.randint(0,3)
            x = Ghost.DIRECTIONS[choice][0] + self.location[0]
            y = Ghost.DIRECTIONS[choice][1] + self.location[1]

        # if new location is unblocked, move there
        if env.maze[x][y].get_blocked() == False:
            self.location = (x,y)
        
        # otherwise, move into new location w/ p=0.5
        else:
            if random.random() <= 0.5:
                self.location = (x,y)
            else: 
                self.location = self.location 
    
    def __str__(self):
        return f"Ghost Exists at Location {self.location}"

class Environment:
    SIZE = constants.SIZE
    BLOCKING_PROBABILITY = constants.BLOCKING_PROBABILITY
    DIRECTIONS = constants.DIRECTIONS 
    
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
        prev = {current : None}
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

    def render_ghosts(self, locs, array):
        """
        renders ghosts to image of maze
        """
        for ghost in locs:
            array[ghost[0]][ghost[1]] = 3
        return array
    
    def render_path(self, path, array):
        """
        renders path to the maze image
        """
        for coord in path:
            array[coord[0]][coord[1]] = 2
        return array

    def __str__(self):
        return '\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.maze])

class Agent: 
    DIRECTIONS = constants.DIRECTIONS
    
    def __init__(self):
        """
        initializes agents with location / survival status.
        """
        self.location = (0,0)
        self.isalive = True 
    
    def update_location(self, new_location):
        """        
        change the old location to new location
        """
        self.location = new_location 
    
    def is_valid_position(self, pos):
        """
        validates whether new position is in board
        """
        x, y = pos[0], pos[1]
        return x >= 0 and y >= 0 and x < Environment.SIZE and y < Environment.SIZE
    
    def print_environment(self, env):
        """
        allows you to print the environment
        """
        print("\nThe environment can be seen below:")
        print("----------------------------------")
        print(env)    
        print("----------------------------------\n")

    def generate_video(self, video_name, images):
        """
        generates video of agent's moves
        """
        frames = []
        fig = plt.figure()
        for i in range(len(images)):
            frames.append([plt.imshow(images[i], cmap='Greys',animated=True)])

        plt.close()

        ani = animation.ArtistAnimation(fig, frames, interval=3000, blit=True, repeat=False)
        ani.save("replays/" + video_name + '.mp4')