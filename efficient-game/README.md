# ghosts-in-the-maze

## Synopsis
-- TBD -- 
- also see if you can get the agents to run on the same environment. My scripting is not set up that way but if you can
- also when saving the results for the experiment for ghosts, maybe Dave it to the jsons periodically so that we don’t lose progress if the run ends
- can you add a BFS checker to environment
- just add comments and see if we can checkpoint the json at each ghost so in case it terminates we can just restart at the last position in the json
- implemenent videos for the success/failure for each one
- update this document
- DFS - build your own stack

## Class Structure
### Environment
- `init(self, num_ghosts=1)` → 
- `step(self)` →
- `make_maze(self, shape)` →  
- `get_inbounds_actionspace(self, position)` →
- `get_valid_neighbors(self, position, grid)` →
- `dfs(self, maze, current, visited)` →
- `is_valid_maze(self, maze)` →
- `make_valid_maze(self)` →
- `generate_ghosts(self, num_ghosts=1)` →
- `update_ghost_locations(self, ghost_locations)` →
- `update_visible_ghosts(self, ghost_locations)` →
- `update_ghost_grid(self, ghost_locations)` →
- `update_visible_ghost_grid(self, ghost_locations)` →
- `update_ghosts(self)` →
- `effective_blocked_maze(self, maze_grid, ghost_grid)` → 