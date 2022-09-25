import random 
from block import Block
from environment import Environment 

class Ghost:
    DIRECTIONS = [[0,1], [1,0], [0,-1], [-1,0]]

    def __init__(self):
        """
        initializes ghost with location on board.
        """
        x = random.randint(0, Environment.SIZE-1)
        y = random.randint(0, Environment.SIZE-1)
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
        return x >= 0 and y >= 0 and x < Environment.SIZE and y < Environment.SIZE

    def update_location(self, env):
        """
        randomly chooses to go left, right, up, or down 
        """
        choice = random.randint(0,3)
        x = Ghost.DIRECTIONS[choice][0] + self.location[0]
        y = Ghost.DIRECTIONS[choice][1] + self.location[1]

        # makes sure that the direction ghost is going is in a valid direciton 
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

            

