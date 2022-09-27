from game.environment import Environment 
import game.final_variables as final_variables
from game.agent import Agent
import matplotlib.pyplot as plt

class Agent1(Agent):

    """
    Agent  1  plans  a  the  shortest  path  through  the  maze  and  executes  it,  ignoring  the  ghosts.   
    This  agent  is incredibly efficient - it only has to plan a path once - but it makes no adjustments 
    or updates due to a changing environment.
    """

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
                if self.is_valid_position( (x,y) ) and (x,y) not in visited:
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

    def run_agent1_verbose(self, env):

        """
        allows you to run agent on environment, returns +1 if successful, +0 for other terminations
        """
        super().print_environment(env)
        plan = self.plan_path(env)

        print(f"Agent 1's Planned Optimal Path is: {plan}")
        print(self.location)

        while self.isalive:
            if self.location == (final_variables.SIZE-1, final_variables.SIZE-1):
                print("\nSUCCESS (+1): THE AGENT REACHED THE GOAL!")
                return 1 
            action = plan.pop(0) 
            self.location = action 
            for ghost in env.ghosts:
                ghost.update_location(env) 
                if self.location == ghost.get_location():
                    print("\nFAILURE (+0): THE AGENT GOT KILLED BY A GHOST")
                    print(f"Agent 1 Location: {self.location}\t Ghost Location: {ghost.get_location()}")
                    self.isalive = False 
                    return 0 
            # for debugging, print out the agent location and ghost locations
            print(f"\nAgent 1 Location:\t {self.location}")
            for i in range(len(env.ghosts)):
                print(f"Ghost {i} Location:\t {env.ghosts[i].location}")
            color_array = env.get_picture()
            color_array[self.location[0]][self.location[1]] = 3 
            picture = plt.imshow(color_array, cmap='Greys')
            plt.show()
        return 0 

    def run_agent1(self, env):
        """
        allows you to run agent on environment, returns +1 if successful, +0 for other terminations
        """
        plan = self.plan_path(env)
        while self.isalive:
            if self.location == (final_variables.SIZE-1, final_variables.SIZE-1):
                return 1 
            action = plan.pop(0) 
            self.location = action 
            for ghost in env.ghosts:
                ghost.update_location(env) 
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 
        return 0