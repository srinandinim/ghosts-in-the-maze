# Ghosts in the Maze
This project involves building a simulator for the "Ghosts in the Maze" game and developing intelligent agents to play the game in high and low information environments. The project was completed in collaboration between Tej Shah and Srinandini Marpaka.

## Simulator
The game is played on a grid, where the goal is for the agent to reach the end of the maze while avoiding ghosts. In the high information environment, the locations of all ghosts are known to the agent. In the low information environment, only the locations of ghosts that are visible to the agent are known.

## Agents
Five intelligent agents were developed for this project:

1. Agent 1 plans an optimal path once, ignoring ghosts, and executes actions in its path until it reaches a terminal state.
2. Agent 2 re-plans paths whenever a ghost is obstructing its current path to the end of the maze and it maximally moves away from the nearest ghost if no path to the end of the maze with the ghosts exists.
3. Agent 3 forecasts the future survivability by running Agent 2 for each possible action it can take, and then processes that survivability with a curiosity heuristic and distance to end goal heuristic; then, Agent 3 uses these processed results for greedy hill climbing local search.
4. Agent 4 forecasts the future by computing the expected utility of action using a game tree (Player 1: Agent, Player 2: Ensemble of Ghosts) which tries to minimize the distance to the $k$ nearest ghosts; those statistics are then processed to curiosity and distance to end goal heuristics; then, Agent 4 uses the processed results for greedy hill climbing local search.
5. Agent 5 was built to work for a lower information environment by augmenting Agent 4 with a "memory" of the most recent ghosts that have been seen.

## Experimental Results
The agents were run on high information (HI) and low information (LI) environments for grid sizes of 5x5, 10x10, 15x15, 20x20, 30x30, and 51x51. The experimental results indicate that the survival of the agents generally rank as follows for HI environments: Agent 1 < Agent 2 < Agent 3 ≤ Agent 4. The experimental results also indicate that the survival of the agents generally rank as follows for LI environments: Agent 1 < Agent 2 < Agent 3 ≤ Agent 4 ≤ Agent 5. Similar performance curves were observed in different-sized grids, suggesting that the agents developed are generalizable and agnostic to grid size in terms of success rate.
