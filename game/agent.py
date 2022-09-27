from game.environment import Environment 
import game.final_variables as final_variables

class Agent:
    DIRECTIONS = final_variables.DIRECTIONS

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
