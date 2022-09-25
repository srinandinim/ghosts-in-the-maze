from game.environment import Environment 
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    env = Environment()
    env.get_picture()

    """
    Need to add functionality such that:
    1. environment of agent shown in photo
    2. current location of agent layered on maze environment
    3. current locations of ghosts layered on maze environment
    """
