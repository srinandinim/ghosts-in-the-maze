from block import Block

class Environment:

    SIZE = 5
    BLOCKING_PROBABILITY = 0.28

    def __init__(self):
        self.generate_maze()
        while not self.validate_maze_blocking() and self.validate_maze_path():
            self.generate_maze()

        for j in range(5):
            for i in range(5):
                print(self.maze[i][j])

    def generate_maze(self):
        self.maze = [[Block(Environment.BLOCKING_PROBABILITY) for x in range(Environment.SIZE)] for y in range(Environment.SIZE)] 
        self.maze[0][0].set_blocked(False)
        self.maze[Environment.SIZE - 1][Environment.SIZE - 1].set_blocked(False)

    # based on the idea of 1.5 * .28 = .42
    def validate_maze_blocking(self):
        blocked_cells = 0
        for j in range(Environment.SIZE):
            for i in range(Environment.SIZE):
                if (self.maze[i][j]).get_blocked() == True:
                    blocked_cells+=1

        if Environment.SIZE**2 * Environment.BLOCKING_PROBABILITY * 1.5 <= blocked_cells:
            return False

        return True

    def validate_maze_path(self):
        # TODO: implement bfs
        return True

