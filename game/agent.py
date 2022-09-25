from queue import Empty
from copy import deepcopy
from game.environment import Environment 
from game.block import Block 
import game.final_variables as final_variables
import matplotlib.pyplot as plt

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
            # for debugging, print out the agent location and ghost locations
            print(f"\nAgent 2 Location:\t {self.location}")
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

class Agent2(Agent1):
    """
    Agent  2  re-plans.   At  every  timestep,  Agent  2  recalculates  a  new  path  to  the  goal  based  on  the  current information,  
    and  executes  the  next  step  in  this  new  path.   Agent  2  is  constantly  updating  and  readjusting based on new information 
    about the ghosts.  Note, however, Agent 2 makes no projections about the future.  Ifall paths to the goal are currently blocked, Agent 2 
    attempts to move away from the nearest visible ghost (notoccupying a blocked cell).

    Agent 2 requires multiple searches - you’ll want to ensure that your searches are efficient as possible sothey don’t take much time.  
    Do you always need to replan?  When will the new plan be the same as theold plan, and as such you won’t need to recalculate?
    """

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

    def manhattan_distance(self, coord1, coord2):
        x = abs(coord2[0] - coord1[0])
        y = abs(coord2[1] - coord1[1])
        return x + y

    def nearest_visible_ghost(self, env):
        """
        finds nearest ghost position from current position
        will be used if all paths are blocked, then make sure to walk towards opposite direction
        """
        min_distance = final_variables.SIZE * final_variables.SIZE + 1 
        min_coords = (final_variables.SIZE, final_variables.SIZE)

        for ghost in env.ghosts:
            if not env.maze[ghost.location[0]][ghost.location[1]].get_blocked():
                dist = self.manhattan_distance(self.location, ghost.get_location())
                if dist < min_distance:
                    min_distance = dist 
                    min_coords = ghost.location 
        return min_coords  

    def ghost_actionspace(self, env, ghost_location):
        ghost_actions = {}
        for d in self.DIRECTIONS:
            dx = d[0] + ghost_location[0]
            dy = d[1] + ghost_location[1]
            new_pos = (dx, dy)
            if self.is_valid_position(new_pos):
                if env.maze[dx][dy].get_blocked():
                    ghost_actions[new_pos] = 0.5 
                else: ghost_actions[new_pos] = 1.0
        return ghost_actions 

    def plan_path(self, env, source):
        # agent starts at top left and tries to reach bottom right
        goal = (Environment.SIZE-1, Environment.SIZE-1)

        # use queue/visited/prev for running BFS for path planning
        visited = set(source)
        prev = ({source : None})

        _, prev = self.dfs(env, source, visited, prev)
        path = super().path_from_pointers(source, goal, prev)
        return path 
    
    def move_agent_away_from_nearest_ghost(self, env, nearest_ghost):
        x = self.location[0]
        y = self.location[1]

        possible_moves = [ (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1) ]
        possible_valid_moves = []
        for move in possible_moves:
            if self.is_valid_position(move) and not env.maze[move[0]][move[1]].get_blocked():
                possible_valid_moves.append(move)

        if len(possible_valid_moves) == 0: 
            return self.location 
        
        distances = {}
        for possible_move in possible_valid_moves:
            distances[possible_move] = self.manhattan_distance(self.nearest_visible_ghost(env), possible_move)
        
        max_dist = 0
        max_move = self.location 
        for move, dist in distances.items():
            if dist > max_dist:
                max_dist = dist 
                max_move = move 
        return max_move 

    def run_agent2_verbose(self, env):
        """
        @Nandini - can you add functionality "if all paths to the goal are currently blocked"
        I think I am only checking one possible path with DFS and then moving away from nearest ghost. 
        """
        super().print_environment(env)
        path = self.plan_path(env, self.location)

        print(f"Agent 2's Planned Path is: {path}")
        print(self.location)

        while self.isalive:
            if self.location == (final_variables.SIZE-1, final_variables.SIZE-1):
                print("\nSUCCESS (+1): THE AGENT REACHED THE GOAL!")
                return 1 
            action = path.pop(0) 
            if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
                self.location = action 
            else:
                path = self.plan_path(env, self.location)
                action = path.pop(0) 
                print(f"REPLANNING: Agent 2's Planned Path is: {path}")
                if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
                    self.location = action 
                else:
                    print(f"MOVE AWAY FROM GHOST: New path is also in ghost danger zone!")
                    self.location = self.move_agent_away_from_nearest_ghost(env, self.nearest_visible_ghost(env))
            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    print("\nFAILURE (+0): THE AGENT GOT KILLED BY A GHOST")
                    print(f"Agent 1 Location: {self.location}\t Ghost Location: {ghost.get_location()}")
                    self.isalive = False 
                    return 0 
            
            # for debugging, print out the agent location and ghost locations
            print(f"\nAgent 2 Location:\t {self.location}")
            for i in range(len(env.ghosts)):
                print(f"Ghost {i} Location:\t {env.ghosts[i].location}")
            color_array = env.get_picture()
            color_array[self.location[0]][self.location[1]] = 3 
            picture = plt.imshow(color_array, cmap='Greys')
            plt.show()

    def run_agent2(self, env):
        path = self.plan_path(env, self.location)
        while self.isalive:
            if self.location == (final_variables.SIZE-1, final_variables.SIZE-1):
                return 1 
            action = path.pop(0) 
            if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
                self.location = action 
            else:
                path = self.plan_path(env, self.location)
                action = path.pop(0) 
                if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
                    self.location = action 
                else:
                    self.location = self.move_agent_away_from_nearest_ghost(env, self.nearest_visible_ghost(env))
            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 
        return 0 

class Agent3(Agent2):
    """
    Agent 3 forecasts.  At every timestep, Agent 3 considers each possible move it might take (including staying inplace), 
    and ‘simulates’ the future based on the rules of Agent 2 past that point.  For each possible move, thisfuture is simulated 
    some number of times, and then Agent 3 chooses among the moves with greatest successrates in these simulations.  Agent 3 can 
    be thought of as Agent 2, plus the ability to imagine the future.

    Agent 3 requires multiple searches - you’ll want to ensure that your searches are efficient as possible sothey don’t take much time.  
    Additionally, if Agent 3 decides there is no successful path in its projectedfuture, what should it do with that information?  
    Does it guarantee that success is impossible?
    """
    def __init__(self):
        """
        initializes Agent3 with initialization of Agent1.
        """
        super().__init__()
        self.action_space = []
        self.prev = {} 
        self.success_rates = {} 
    
    def action_spaces(self, env):
        """
        returns the actions possible from current location in maze. 
        """
        x = self.location[0]
        y = self.location[1]

        possible_moves = [ (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1) ]
        possible_valid_moves = []
        for move in possible_moves:
            if self.is_valid_position(move) and not env.maze[move[0]][move[1]].get_blocked():
                possible_valid_moves.append(move)

        if len(possible_valid_moves) == 0: 
            return self.location 
        
        return possible_valid_moves 
    
    def run_agent3(self, env):

        """
        @Nandini:
        The core logic for this should work I think but it's nearly impossible to run due to computational complexity. I wasn't able to run it on a small grid. 
        I think the right next step is to do the following:
        (1) Do iterative DFS so stop at the 4th or 5th level in the stack (just add extra parameter to functional call)
        (2) Then use a heuristic (i.e. manhattan distance) to see how far the last node is from the goal node
        (3) Then run trials to see which of the actions in agent action space simulations lead to closest to goal node
        (4) Select that as action and continue running agent3. Use agent2 to run simulations, but make DFS stop at certain depth.

        This will help with the efficiency. 
        """

        while self.isalive:
            if self.location == (final_variables.SIZE-1, final_variables.SIZE-1):
                return 1 

            # compute action space at current location 
            self.action_space = self.action_spaces(env)

            # loop through the entire action space to find success rate of each possible move
            # by calling agent2 to run environments from each action in the space and then adding
            # up the number of success to the dictionary entry for that move 
            for action in self.action_space:
                success, trials = 0, 2
                while trials > 0:
                    new_env = deepcopy(env)
                    agent2 = Agent2()
                    agent2.location = action 
                    goal = (final_variables.SIZE-1, final_variables.SIZE-1)
                    while agent2.isalive and agent2.location != goal:
                        path = agent2.plan_path(new_env, agent2.location)
                        if path[0] not in self.ghost_actionspace(new_env, self.nearest_visible_ghost(new_env)).keys():
                            agent2.location = action 
                        else:
                            path = agent2.plan_path(new_env, agent2.location)
                            if path[0] not in self.ghost_actionspace(new_env, self.nearest_visible_ghost(new_env)).keys():
                                agent2.location = action 
                            else:
                                agent2.location = agent2.move_agent_away_from_nearest_ghost(new_env, agent2.nearest_visible_ghost(new_env))
                        for ghost in new_env.ghosts:
                            ghost.update_location(new_env)
                            if agent2.location == ghost.get_location():
                                agent2.isalive = False 
                    
                    if agent2.location == (final_variables.SIZE-1, final_variables.SIZE-1):
                        success += 1       
                self.success_rates[action] = success/trials 
            
            # find the max success rate possible from the action space and make that move as the action for turn of agent3 simulation on environment
            max_success = 0 
            best = self.location 

            for action in self.success_rates:
                if self.success_rates[action] > max_success:
                    best = action 
                    max_success = self.success_rates[action]
            
            self.location = best 

            for ghost in env.ghosts:
                ghost.update_location(env)
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 
                        # for debugging, print out the agent location and ghost locations
            print(f"\nAgent 2 Location:\t {self.location}")
            for i in range(len(env.ghosts)):
                print(f"Ghost {i} Location:\t {env.ghosts[i].location}")
            color_array = env.get_picture()
            color_array[self.location[0]][self.location[1]] = 3 
            picture = plt.imshow(color_array, cmap='Greys')
            plt.show()
        return 0 
