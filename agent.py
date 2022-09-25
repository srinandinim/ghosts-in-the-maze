from queue import Empty
from environment import Environment 
import final_variables


class Agent:
    DIRECTIONS = final_variables.DIRECTIONS

    def __init__(self):
        """
        initializes agents with location / survival status.
        """
        self.location = (0,0)
        self.isalive = True 
    
    def update_location(self, new_location):
        """        
        change the old location to new location
        """
        self.location = new_location 
    
    def is_valid_position(self, pos):
        """
        validates whether new position is in board
        """
        x, y = pos[0], pos[1]
        return x >= 0 and y >= 0 and x < Environment.SIZE and y < Environment.SIZE

class Agent1(Agent):

    def __init__(self):
        """
        intializes Agent1 with initialization method of Agent. 
        """
        super().__init__()

    def plan_path(self, env):
        """
        plans the path agent will then execute
        """

        # agent starts at top left and tries to reach bottom right
        source = (0,0)
        goal = (Environment.SIZE-1, Environment.SIZE-1)

        # use queue/visited/prev for running BFS for path planning
        queue = [source]
        visited = set(source)
        prev = ({source : None})

        # run BFS to find optimal path from start to end without ghosts
        previous = self.bfs(env, goal, queue, visited, prev)

        # finds optimal path from the BFS having stored prev pointers 
        path = self.path_from_pointers(source, goal, previous)

        # returns the optimal path, no planning again necessary
        return path 
    
    def bfs(self, env, goal, queue, visited, prev):
        """
        runs BFS and stores the prev pointers along path. 
        """
        while len(queue) > 0:
            parent = queue.pop(0)
            visited.add(parent)
            if parent == goal: 
                return prev

            for d in Environment.DIRECTIONS:
                x = parent[0] + d[0]
                y = parent[1] + d[1] 
                if self.is_valid_position(x,y) and (x,y) not in visited:
                    if env.maze[x][y].get_blocked() == False: 
                        queue.append((x,y))
                        prev[(x,y)] = parent
        return prev
    
    def path_from_pointers(self, source, goal, prev):
        """
        returns solution path from start to end node
        """
        path = [goal]
        current = goal
        while current != source:
            path.append(prev[current])
            current = prev[current]
        return list(reversed(path))

class Agent2(Agent):
    def __init__(self):
        """
        intializes Agent2 with initialization method of Agent. 
        """
        super().__init__()
    
    

                


