# Log Notes 
## September 24, 2022 Tej's Working Session
- Added functionality to run an agent with n number of ghosts to run simulations. Code could be more modular though.
- Added functionality for ghosts so that you can find their location and move according to the assignment probabilities
- Added functionality to visualize the generated environment, will need to add visualization scripts for env, ghost, and agent later on.
- I noticed that we should use DFS, not BFS for validating the maze since we just need to show a path exists, not necessarly an optimal path. We want to save on space complexity and that's also one of the questions that Cowan has on Assignment 1. 
- We can reuse your BFS implementation for Agent 1, but I have went ahead and updated validate_maze to be DFS so that it's optimal.
- Also the TA on discord said "Many of the algorithms you have seen thus far use a closed list. Please do not use a literal list for the closed list, it will be inefficient. Checking whether a node is in the closed list or not should take constant time ... 20% deduction" so we need to make sure that we do not use an actual list for the visited set.  

## September 26, 2022 Nandini
- We should discuss the way we run the simulations. I was under the assumption that we run all the agents on the same board and the only factor that would not be the same is the agent's movement. 
- Figure out the way Python objects work (is there a way to store the locations into a set and have those automatically update when the locations change)
- For agent2, add that if the ghost is not in the immediate vicinity - keep it stay


# ghosts-in-the-maze

## 1.1 The Environment

### The Block Class
We create a `Block` class

# Monday October 3rd Tasks
0. In agent 1, just take the value from the lookup table. 
1. In the environment, implement shortests paths computed with DP memoization. 
2. Remove lists from Agent 2 and use a Heap to sort with Heapify.
3. Potentially implement tie breaker for Agent 2 heuristic. 
4. Update Agent 2 so that it only looks at the next step, not 1 step in the future. 
5. Add information from Agent 2 currently to support Agent 3. 
6. Move move_successes to accomodate for repeated locations in Agent 3. 
7. Any time that we are using a list, make it a priority Queue. 

## Agent 4 / Agent 5: 
1. For agent 3, tie-break equal reward equal lengths with distance away from nearest ghost farther away. 
2. For agent 5, you need to incorporate the last seen position of the agent into your improvement. 