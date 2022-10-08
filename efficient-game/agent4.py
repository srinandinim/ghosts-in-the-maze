from copy import deepcopy
from email import message
import constants
from agent import Agent
from agent2 import Agent2
from environment import Environment
import numpy as np 
import matplotlib.pyplot as plt 

class Agent4(Agent2):

    def __init__(self, env):
        super().__init__()
        self.distance_rewards = self.distance_rewards(env)

    def knn_mdsum(self, knn_ghosts):
        """
        given {ghost:location_tuple}, sums all distance from agent location.
        """
        distance = 0 
        for md_knn_g in knn_ghosts.values():
            distance += md_knn_g
        return distance 

    def get_knearestghosts(self, env, k):
        """
        given {ghost1:location_tuple, ..., ghostn:location_tuple}
        return {ghosti:location_tuple, ..., ghostk:location_tuple} 
        closest k ghosts to self.location per manhattan distance
        """
        k = min(k, len(env.temp_ghosts))
        distances = {}
        for ghost in env.temp_ghosts.keys():
            distances[ghost] = self.manhattan_distance(self.location, env.ghost_locations[ghost])
        
        # sort descending by value, then select k-lowest values
        distances = sorted(distances.items(), key=lambda kv: kv[1])[:k]
        
        nearestkghosts = {}
        for ghost,dist in distances:
            nearestkghosts[ghost] = dist
        
        return nearestkghosts

    def distance_rewards(self, env):
        end_dist = constants.SIZE[0] * constants.SIZE[1] + 1
        array = np.array([[round( (end_dist / self.manhattan_distance(constants.SIZE, (i, j)))**(1/3), 2) for j in range(constants.SIZE[1])] for i in range(constants.SIZE[0])])
        array[constants.SIZE[0]-1][constants.SIZE[1]-1] = 1000.000
        return array

    def expectimax(self, env, depth, min_or_max):
        
        #print(f"\nThe depth is {depth} and it is {min_or_max}'s turn! Current agent location is {self.location}")
        
        if depth == 0 or self.is_alive == False: 
            x, y = self.location[0], self.location[1]
            knn_ghosts = self.get_knearestghosts(env, k=5)
            knn_mdsum = self.knn_mdsum(knn_ghosts)
            #print(f"REWARD DISTANCE: {self.distance_rewards[x][y]}, GHOST PENALTY: {knn_mdsum}, (x,y) = {(x,y)}")
            evaluation = self.distance_rewards[x][y] - knn_mdsum 
            if self.is_alive == False: 
                evaluation *= 3
            evaluation = round(evaluation, 3)
            return evaluation 
        
        if min_or_max == "max":

            #print("MAX: THIS IS THE AGENT'S TURN!")
            
            # store current max_eval, current best action
            max_eval = -float("inf")
            best_action = self.location 

            # forecast evaluation values for future states in neighors
            #env.debugging_print_maze_grid()
            valid_moves = self.get_valid_neighbors(self.location, env.maze_grid) + [self.location]

            #print(f"THE NEIGHBORS EVALUATED ARE {valid_moves}")
            for move in valid_moves:

                # move to neighbor and evaluate that value 
                self.location = move 
                val = self.expectimax(deepcopy(env), depth-1, "min")

                #print(f"THE VALUE OF {move} is {val}")

                # if neighbor has better value, update max_eval, best_action
                if val > max_eval: 
                    max_eval, best_action = val, move 
            
            # change the location of agent to the best action 
            self.location = best_action 

            #print(f"Based on that, the agent's new location is {self.location}")

            # if the location conflicts with a temp ghosts location, then agent dies
            if self.location in env.temp_ghosts.values():

                #print("THE AGENT DIED!")

                # the agent died in the simulation of where the ghost is!
                self.is_alive = False 


            # return the highest value of the evaluation 
            return max_eval 
        
        if min_or_max == "min":

            #print("MIN: THIS IS THE ENSEMBLE OF GHOST'S TURN!")

            # store current min_eval 
            min_eval = float("inf")

            #print(f"THE TEMP GHOST LOCATIONS ARE {env.temp_ghosts}")

            # update the temporary ghosts locations
            env.update_temp_ghosts()

            #print(f"THE UPDATE TEMP GHOST LOCATIONS ARE {env.temp_ghosts}")

            # evaluate current enviornment 
            val = self.expectimax(deepcopy(env), depth-1, "max")

            #print(f"The value of the current environment is as follows: {val}")

            # update min_eval
            if val < min_eval:
                min_eval = val 
            
            #print(f"The minimum evaluatoin of all the environments is {min_eval}")
            
            # return the minimum value of the evaluation
            return min_eval 

    def run_agent4(self, env):
        visited = {}
        while self.is_alive:
            if self.is_success_state(): 
                return 1 
            neighbors = self.get_valid_neighbors(self.location, env.effective_maze)
            #print(f"The neighbors are: {neighbors}")
            original_location = self.location 
            evaluation_scores = {}
            for neighbor in neighbors:
                self.location = neighbor 
                evaluation_scores[neighbor] = self.expectimax(env, 9, 'max')
                if neighbor in visited: 
                    evaluation_scores[neighbor] = round(self.expectimax(env, 9, 'max') - 1.5 * visited[neighbor], 3)

            #print(f"The evaluation scores are: {evaluation_scores}")
            self.location = original_location 
            self.is_alive = True 

            maxKey, maxValue = self.location, -float("inf")
            for key, value in evaluation_scores.items():
                if visited.get(key, 0) <= 10 and evaluation_scores[key] > maxValue: 
                    maxKey = key 
                    maxValue = value
            
            self.location = maxKey 
            visited[maxKey] = visited.get(maxKey, 0) + 1

            if self.is_failure_state(env):
                return 0 
            
            #color_array = self.get_image_array(env)
            #plt.imshow(color_array, cmap='Greys')
            #plt.show()

            env.step()


"""
env = Environment(num_ghosts=3) 
env.debugging_print_maze_grid()
a4 = Agent4(env)
a4.run_agent4(env)
"""




#rewards_distance = a4.distance_rewards(env)
#print(rewards_distance)3
#print(a4.distance_rewards)
#print(a4.location)
#env.debugging_print_all_ghost_grid()
#env.debugging_print_all_ghost_locations()
##knn = a4.get_knearestghosts(env, k=4)
#print(knn)
#print(a4.knn_mdsum(knn))