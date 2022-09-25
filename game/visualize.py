from game.environment import Environment 
from game.agent import Agent, Agent1, Agent2
from game.ghost import Ghost 
import matplotlib.pyplot as plt
import numpy as np

def get_current_observation_photo(env, agent):
    array = [[1 if str(cell)=="T" else 0 for cell in row] for row in env.maze] 
    ghost_locations = [(ghost.location[0], ghost.location[1]) for ghost in env.ghosts]
    array = env.render_ghosts(ghost_locations, array)
    array[agent.location[0]][agent.location[1]] = 3
    fig, ax = plt.subplots()
    picture = plt.imshow(array, cmap='binary')
    plt.show()
    return picture


