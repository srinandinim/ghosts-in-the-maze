-- simulator.py

----- Block Class
--------- init(self, p)                      : cell starts blocked with probability p
--------- set_blocked(self, b)               : can manually make a block object blocked 
--------- get_blocked(self)                  : retrieves whether the cell is blocked
--------- str(self)                          : returns "T" if blocked, "F" otherwise  

----- Ghost Class
--------- init(self, p)                      : ghost starts at random location on board
--------- is_valid_position(self,pos)        : is a location in bounds of the board
--------- get_location(self)                 : returns ghost's current location 
--------- update_location(self)              : moves location of ghost per specification
--------- str(self)                          : prints out f"Ghost Location: {self.location}"
 
----- Environment Class
--------- init(self, num_ghosts=1)           : generates a a valid maze with num_ghosts
--------- is_valid_position(self,pos)        : is a location in bounds of the board
--------- generate_maze(self)                : generates a possible 51x51 maze of Blocks
--------- validate_maze(self)                : validates that 1 path exists from start to end
--------- dfs(self, curr, visited)           : runs DFS from source to end and return T if path exists
--------- get_picture(self)                  : renders current state of environment with obstacles, and ghosts
--------- render_ghosts(self, locs, array)   : change value in visualized array to correspond to ghosts
--------- render_path(self, locs, array)     : changes value in visualized array to correspond to path 
--------- str(self)                          : prints out T/F table of the entire state of the environment