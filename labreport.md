# Lab Report

## Grey Boxed Questions

### Q[1.1] The Environment
To verify that a maze is valid, we will make sure that at least one path exists from the start of the maze to the end of the maze. To verify the existence of the paths, we will use Depth First Search (DFS). We choose DFS as opposed to Breadth First Search (BFS) because we only need to verify that a path exists the start to the end of the maze, not necessarily an optimal one. By choosing DFS over BFS we save significantly on space complexity. Note that the worst case time compleixty of BFS and DFS will still be the same. 

### Q[1.4] Agent 2
Agent2 does not need to always replan. Agent2 will continue on the current planned path it is on UNLESS a ghost nearby intersects with the Agent2 action-space. There is no issue with going forwards with the current planned path if the Agent2 knows that it will surive. At the point a ghost intersects with the Agent2 action space, Agent2 will re-plan its path.

To make sure our searches are efficient, we pre-compute an optimal path from a particular node to the end destination for every open location in maze if it exists with Bottom Up Dynamic Programming and BFS. These pre-computed paths are  stored in Environment. 

Then, whenever we need to re-plan an agent, we simply find the optimal path from a particular position for the agent using the lookup table for the optimal path. If that new path still has the problem of a ghost intersecting with the next action in its path, then Agent2 will back away from the ghosts.   

### Q[1.4] Agent 3
If Agent 3 decides that there is no successful path in its projected future, it will simply run the pre-computed most optimal path from that location stored in the lookup table. This does not guarnetee that success is impossible - it is possible for the agent to have a successful path in the projected future if we run more simulations. 






## Core Agent Logic

### Agent 1
- Environment pre-computes all optimal paths from every open location to end node
- Agent1 uses the dp lookup table from environment to compute path from (0,0) to end node
- Agent1 executes every action in the planned path sequence until it reaches the goal or it dies by running into a ghost

### Agent 2
- Environment pre-computes all optimal paths from every open location to end node
- Agent2 uses the dp lookup table from environment to compute path from (0,0) to end node
- Agent2 executes every action in the planned path sequence until it reaches the goal OR a ghost is blocking the next action the agent takes
    - If the ghost is blocking the next action, the agent replans path based on dp lookup table from current position to end node
    - If the new planned path's 1st action also is blocked by a ghost, the agent moves away from the closest ghost per manhattan distance

### Agent 3
- Environment pre-computes all optimal paths from every open location to end node
- Starting from (0,0), Agent3 uses a hill climbing approach for search towards the end node. Run path until intersected with ghost.
    - For every possible action that Agent3 can take, Agent3 runs Agent2 k times and stores which action led to the most successes. 
        - Agent2 will also have the additinoal ability to not run a path if the closest ghost actionspace intersects with agent actinospace.
    - Agent3 will select the action that has the highest success rate in k simulations and has the shortest path in the DP path table. 