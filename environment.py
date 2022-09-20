from queue import Empty
from block import Block

class Environment:

    SIZE = 5
    BLOCKING_PROBABILITY = 0.28

    def __init__(self):
        self.generate_maze()
        while not self.validate_maze():
            self.generate_maze()

    def generate_maze(self):
        self.maze = [[Block(Environment.BLOCKING_PROBABILITY) for x in range(Environment.SIZE)] for y in range(Environment.SIZE)] 
        self.maze[0][0].set_blocked(False)
        self.maze[Environment.SIZE - 1][Environment.SIZE - 1].set_blocked(False)

    def validate_maze(self):
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        visited = [[0 for x in range(Environment.SIZE)] for y in range(Environment.SIZE)] 
        queue = []

        queue.append((0, 0))
        visited[0][0] = True
        while len(queue) > 0:
            curr = queue.pop(0)
            visited[curr[0]][curr[1]] = 1

            if curr[0] == curr[1] == Environment.SIZE - 1:
                return True
            
            for dir in directions:
                temp_x = curr[0] + dir[0]
                temp_y = curr[1] + dir[1]

                if temp_x >= 0 and temp_y >= 0 and temp_x < Environment.SIZE and temp_y < Environment.SIZE and visited[temp_x][temp_y] == 0:
                    if (self.maze[temp_x][temp_y]).get_blocked() == False:
                        queue.append((temp_x, temp_y))

        return False

    def __str__(self):
        return '\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.maze])