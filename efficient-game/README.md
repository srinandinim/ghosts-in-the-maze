# ghosts-in-the-maze

## Synopsis
-- TBD -- 
- fix dfs issue with the simulations
- implemenent videos for the success/failure for each one
- a nice to have if you can is to export the lab simulation statistics with number of ghosts and survival rates into a bunch of JSONs and then create another scrip that parses those JSONs and use Matplotlib to make a graph of all the survival rates and agents on top of each other
- update this document

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