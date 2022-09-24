# Log Notes 
## September 24, 2022 Tej's Working Session
- I noticed that we should use DFS, not BFS for validating the maze since we just need to show a path exists, not necessarly an optimal path. We want to save on space complexity and that's also one of the questions that Cowan has on Assignment 1. 
- We can reuse your BFS implementation for Agent 1, but I have went ahead and updated validate_maze to be DFS so that it's optimal.
- Also the TA on discord said "Many of the algorithms you have seen thus far use a closed list. Please do not use a literal list for the closed list, it will be inefficient. Checking whether a node is in the closed list or not should take constant time ... 20% deduction" so we need to make sure that we do not use an actual list for the visited set.  

# ghosts-in-the-maze

## 1.1 The Environment

### The Block Class
We create a `Block` class 