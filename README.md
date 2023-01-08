# Graduate AI Project 1: Ghosts-In-The-Maze
This project involves building a simulator for the "Ghosts in the Maze" game and developing intelligent agents to play the game in high and low information environments. The project was completed in collaboration between Tej Shah and Srinandini Marpaka.

Lab Report: https://github.com/srinandinim/ghosts-in-the-maze/blob/master/lab-report/tej-nandini-final.pdf

Agent Video Simulations: https://github.com/srinandinim/ghosts-in-the-maze/tree/master/videos

## Motivation
Can we make even the most efficient algorithms better than they already are? Can we encode inductive biases, human priors, or logical reasoning into these algorithms? Can we optimize our algorithms with respect to some objectives or constraints? In terms of performance, how good is good enough – can we trade off optimality for efficiency? Can we re-frame these algorithms to work in non-obvious settings? In short, can we make our algorithms informed? In this module, we discussed the following key ideas: uninformed search, informed search, classical planning, adversarial search/games, local search, and constraint satisfaction. 

## The Simulator
Suppose an agent is in a maze with walls blocked with 0.28 probability. There always exists a path from the start node (top left corner) to the goal node (bottom right corner), and the agent can move in any one of the four cardinal directions so long as the move is not invalid (out of bounds or occupies a blocked wall). Ghosts exist in the maze, move according to determined rules, and can kill the agent if both entities occupy the same location within the maze. In the high information environment, the locations of all ghosts are known to the agent. In the low information environment, only the locations of ghosts that are visible to the agent are known. As the number of ghosts in the maze increases, how does the survivability of the agents’ fare in complete and partial information settings? Can you build progressively better agents in partial and complete information settings? How do you collect data as the maze size scales and build efficient agents? 

## The Agents
A1 plans once, ignoring ghosts, using BFS. A2 re-plans whenever a ghost is one action away, using BFS, maximally moving away from the nearest ghost if no path exists. A3 selects states less frequently visited with high MCTS survivability and closer distance to the goal. A4 selects states less frequently visited with high Expectimax utilities and closer distances to the goal. A5 is A4 augmented with "memory" of recently seen ghosts.

## Experimental Results
The agents were run on high information (HI) and low information (LI) environments for grid sizes of 5x5, 10x10, 15x15, 20x20, 30x30, and 51x51. The experimental results indicate that the survival of the agents generally rank as follows for HI environments: Agent 1 < Agent 2 < Agent 3 ≤ Agent 4. The experimental results also indicate that the survival of the agents generally rank as follows for LI environments: Agent 1 < Agent 2 < Agent 3 ≤ Agent 4 ≤ Agent 5. Similar performance curves were observed in different-sized grids, suggesting that the agents developed are generalizable and agnostic to grid size in terms of success rate.
