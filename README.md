# ghosts-in-the-maze
*Completed in collaboration between Tej Shah & Srinandini Marpaka*

## Overview
We build a *ghosts-in-the-maze* simulator and develop 5 different intelligent agents for High Information (all ghost locations are known) and partially observable Low Information environments (only visible ghost locations are known). Agent 1 plans an optimal path once, ignoring ghosts, and executes actions in its path until it reaches a terminal state. Agent 2 re-plans paths whenever a ghost is obstructing its current path to the end of the maze and it maximally moves away from the nearest ghost if no path to the end of the maze with the ghosts exists. Agent 3 forecasts the future survivability by running Agent 2 for each possible action it can take, and then processes that survivability with a curiosity heuristic and distance to end goal heuristic; then, Agent 3 uses these processed results for greedy hill climbing local search. Agent 4 forecasts the future by computing the expected utility of action using a game tree (Player 1: Agent, Player 2: Ensemble of Ghosts) which tries to minimize the distance to the $k$ nearest ghosts; those statistics are then processed to curiosity and distance to end goal heuristics; then, Agent 4 uses the processed results for greedy hill climbing local search. We build Agent 5 to work for a lower information environment by augmenting Agent 4 with a "memory" of the most recent ghosts that have been seen. We run our agents on High Information (HI) and Low Information (LI) environments for $5 \times 5, 10 \times 10, 15 \times 15, 20 \times 20, 30 \times 30$, and $51 \times 51$ grids. Our experimental results indicate that the survival of the agents rank generally as follows for HI environments: $A1 < A2 < A3 \leq A4$. Our experimental results indicate that the survival of the agents rank generally as follows for LI environments: $A1 < A2 < A3 \leq A4 \leq A5$. We observe similar performance curves in different-sized grids, suggesting that the agents we developed are generalizable and agnostic to grid size in terms of success rate. 

## Simulation Examples
Agent 1: https://user-images.githubusercontent.com/29678422/196339355-f2b5c5e5-cee5-40ec-89be-01506282df10.mp4
Agent 2 [HI]: https://user-images.githubusercontent.com/29678422/196339592-7687f035-d3b5-4a22-890a-e30e01154ba8.mp4
Agent 3 [HI]: https://user-images.githubusercontent.com/29678422/196339616-088fa852-efbe-44e2-9beb-c70fcc7f323e.mp4
Agent 4 [HI]: https://user-images.githubusercontent.com/29678422/196339638-f3206312-46fb-4c59-a23c-191c0cc7aa31.mp4
Agent 5 [LI]: https://user-images.githubusercontent.com/29678422/196339658-208a5749-25b6-4c51-aecc-170891370c8a.mp4


