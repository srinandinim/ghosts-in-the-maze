# Ghosts in the Maze
*Completed in collaboration between Tej Shah & Srinandini Marpaka*

## Description
Welcome to the 'ghosts-in-the-maze' simulator! In this project, we have developed 5 intelligent agents that can navigate mazes with ghosts. These agents are designed to operate in both high information (all ghost locations are known) and low information (only visible ghost locations are known) environments.

Our agents have a range of capabilities, from simple path planning to more advanced forecasting and decision-making. Agent 1 plans an optimal path once and follows it until it reaches a terminal state, while Agent 2 re-plans paths whenever a ghost is in the way. Agent 3 uses a curiosity heuristic and distance to end goal heuristic to forecast the future survivability of different actions, while Agent 4 uses a game tree and expected utility to minimize the distance to the nearest ghosts. Agent 5 is designed specifically for low information environments and includes a "memory" of previously seen ghosts.

We have tested our agents on mazes of various sizes, from small 5x5 grids to larger 51x51 grids, and our experimental results show that the agents rank as follows in terms of survival rate:

High information environments: Agent 1 < Agent 2 < Agent 3 <= Agent 4
Low information environments: Agent 1 < Agent 2 < Agent 3 <= Agent 4 <= Agent 5
Overall, our results suggest that our agents are generalizable and perform well across different grid sizes. Check out the rest of the README for more information on how to install and use the project."





