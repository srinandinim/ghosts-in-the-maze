from queue import Empty
from game.environment import Environment 
import game.final_variables as final_variables

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
    
    def print_environment(self, env):
        """
        allows you to print the environment
        """
        print("\nThe environment can be seen below:")
        print("----------------------------------")
        print(env)    
        print("----------------------------------\n")
    
    def simulation_statistics(self, num_simulations, num_ghosts):
        """
        run simulation n times and get statistics on survival, and more
        """
        rewards_agent1 = [] 
        for i in range(num_simulations):
            env = Environment(num_ghosts=num_ghosts) 
            agent1 = Agent1()  



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

class Agent2(Agent1):
    def __init__(self):
        """
        intializes Agent2 with initialization method of Agent1. 
        """
        super().__init__()
    
    def dfs(self, env, curr, visited, prev):
        """
        dfs to find a path from source to goal node.
        """ 
        visited.add(curr)
        if curr[0] == curr[1] == final_variables.SIZE:
            return True 
        
        for d in Environment.DIRECTIONS:
            x = curr[0] + d[0]
            y = curr[1] + d[1] 
            if self.is_valid_position((x,y)) and (x,y) not in visited:
                prev[(x,y)] = curr
                if env.maze[x][y].get_blocked() == False: 
                    reached_goal, _ = self.dfs(env, (x,y), visited, prev)
                    if reached_goal == True :
                        return True, prev 
        return False, prev

    def plan_path(self, env):
        # agent starts at top left and tries to reach bottom right
        source = (0,0)
        goal = (Environment.SIZE-1, Environment.SIZE-1)

        # use queue/visited/prev for running BFS for path planning
        visited = set(source)
        prev = ({source : None})

        _, prev = self.dfs(env, source, visited, prev)
        path = super().path_from_pointers(source, goal, prev)
        return path 