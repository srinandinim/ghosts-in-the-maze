# ghosts-in-the-maze

## Synopsis
-- TBD -- 

## Notes

ACTION ITEMS: 

- A4: @Nandini, A4 is not always better than A3, feel free to play around with hyperparametesr if you want. But I think it's fine since we came up with a new technique and we can explain it in the lab report. Diminishing returns if we play around with this tbh.

- A5: @Nandini, build an Agent 5 that stores the memory. For example, suppose the following ghosts exist for an env with {ABCDE} GHOSTS. Possible boostrap A2:
    - Suppose at t, you observe {ABD}. You store {ABD} and locations in memory. Your memory has {ABD}
    - Suppose at t+1, you observe {BCD}. Store {BCD} and locations and mmemory, over-wrting locations of BD. Your memory has {ABCD}
    - Suppose at t+2, you observe {DE}. Store {DE} and locations in memory, ovewrting locations of D. Your memory has {ABCDE}
    - Suppose at t+3, you observe {}. Since 3 time-steps have passed, remove A from memory (note B and D are not remove since you saw it at t+1). Memory is {BCDE}

- A1_Low Information: @Nandini, don't need to run experiment, just use A1_high information results.
- A2_Low Information: @Nandini, set up this environment and run experiments on TMUX and get results.
- A3_Low Information: @Nandini, set up this environment an run experiments on multiple TMUX instances and get results.
- A3_High Information: @Nandini, run experiments on multiple TMUX instances and get results. 
- A4_Low Information: @Nandini, set up this environment and run experiments on multiple TMUX instances and get results.
- A4_High Information: @Nandini, run experiments on multiple TMUX instances and get results.
- A5_Low Information: @Nandini, set up environment run experiment on multiple TMUX and get results. 

- Success/Failure Video for Highest # of Ghosts on Largest Grid [Drive]
- 51 by 51: A1, A2, A4 [Drive]
- 30 by 30: A1, A2, A3, A4 [Drive]
- Low Environments

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