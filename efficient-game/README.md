# ghosts-in-the-maze

## Synopsis
-- TBD -- 
- just add comments
- see if we can checkpoint the json at each ghost so in case it terminates we can just restart at the last position in the json
    - can just pull last set of statistics - I’ll prob add a method just so we input in the last file and it does the rest from there
- implemenent videos for the success/failure for each one
- update this document

## Class Structure
### Environment
- `init(self, num_ghosts=1)` → 
- `step(self)` →
- `make_maze(self, shape)` →  
- `get_inbounds_actionspace(self, position)` →
- `get_valid_neighbors(self, position, grid)` →
- `dfs(self, maze)` →
- `make_valid_maze(self)` →
- `generate_ghosts(self, num_ghosts=1)` →
- `update_ghost_locations(self, ghost_locations)` →
- `update_visible_ghosts(self, ghost_locations)` →
- `update_ghost_grid(self, ghost_locations)` →
- `update_visible_ghost_grid(self, ghost_locations)` →
- `update_ghosts(self)` →
- `effective_blocked_maze(self, maze_grid, ghost_grid)` → 