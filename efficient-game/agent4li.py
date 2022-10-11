from copy import deepcopy
from pydoc import visiblename
import time
import constants
from agent2li import Agent2LI
import numpy as np
import matplotlib.pyplot as plt


class Agent4LI(Agent2LI):

    def __init__(self):
        super().__init__()

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
        k = min(k, len(env.temp_visible_ghosts))
        distances = {}
        for ghost in env.temp_visible_ghosts.keys():
            if ghost in env.visible_ghosts.keys():
                distances[ghost] = self.manhattan_distance(
                    self.location, env.visible_ghosts[ghost])

        # sort descending by value, then select k-lowest values
        distances = sorted(distances.items(), key=lambda kv: kv[1])[:k]

        nearestkghosts = {}
        for ghost, dist in distances:
            nearestkghosts[ghost] = dist

        return nearestkghosts

    def distance_rewards(self, env):
        end_dist = constants.SIZE[0] * constants.SIZE[1] + 1
        array = np.array([[round((end_dist / self.manhattan_distance(constants.SIZE, (i, j)))**(1/3), 2)
                         for j in range(constants.SIZE[1])] for i in range(constants.SIZE[0])])
        array[constants.SIZE[0]-1][constants.SIZE[1]-1] = 1000.000
        return array

    def tree_search(self, env, depth, min_or_max):
        if depth == 1 or self.is_alive == False:
            knn_mdsum = self.knn_mdsum(self.get_knearestghosts(env, k=10))
            evaluation = -knn_mdsum
            if self.is_alive == False:
                evaluation = 0.00100
            return evaluation

        if min_or_max == "max":
            max_eval, best_action = -float("inf"), self.location
            valid_moves = self.get_valid_neighbors(
                self.location, env.maze_grid) + [self.location]
            for move in valid_moves:
                self.location = move
                val = self.tree_search(deepcopy(env), depth-1, "min")
                if val > max_eval:
                    max_eval, best_action = val, move

            if best_action not in env.visible_ghosts.values():
                self.location = best_action
            else:
                self.location = self.move_agent_away_from_nearest_ghost(env)

            if self.location in env.temp_visible_ghosts.values():
                self.is_alive = False

            return max_eval

        if min_or_max == "min":
            min_eval = float("inf")
            env.update_temp_visible_ghosts()
            val = self.tree_search(deepcopy(env), depth-1, "max")
            if val < min_eval:
                min_eval = val
            return min_eval

    def run_agent4_debug(self, env):
        # have a visited set to account for curiosity
        visited = {(0, 0): 1}
        while self.is_alive:

            # if we have reached the end, assume we're done.
            if self.is_success_state():
                return 1

            # get the neighbors and current location of the maze to get evaluation scores
            neighbors = self.get_valid_neighbors(
                self.location, env.effective_maze) + [self.location]

            print(f"The neighbors are: {neighbors}")

            # keeps track of evaluation score and original location
            original_location = self.location
            evaluation_scores = {}

            # gets an evaluation for all the states in the board
            for neighbor in neighbors:
                self.location = neighbor

                # knn distance to ghost heuristic:
                # evaluates locations based on max distance to knn ghosts
                # higher values is a better position for the score
                neighbor_score = 1 / self.tree_search(env, 7, 'max')

                print(
                    f"The initial evaluation of {neighbor} is {neighbor_score}")

                # curisoity heuristic: penalize revisiting states that are already visited
                if neighbor in visited:
                    neighbor_score = neighbor_score * \
                        0.6 ** (visited[neighbor])
                    print(
                        f"The number of visits for {neighbor} is {visited[neighbor]} so normalized score is {neighbor_score}")

                md = self.manhattan_distance(self.location, constants.SIZE)
                neighbor_score = ((neighbor_score + 1) / (md + 1)**(2))
                # distance heuristic: increase evaluation of scores that get you closer to the goal
                print(
                    f"The manhattan distance to end is {md} so new neighbor_score is {neighbor_score}")

                # stores the evaluation of the neighbor in evaluation scores
                evaluation_scores[neighbor] = round(neighbor_score, 4)

            print(f"The evaluation scores are: {evaluation_scores}")
            self.location = original_location
            self.is_alive = True

            # find the maxAction that maximizes the evaluation
            maxKey, maxValue = self.location, -float("inf")
            for key, value in evaluation_scores.items():
                # cannot revisit a state that is already visited 10 times!
                if visited.get(key, 0) <= 10 and evaluation_scores[key] > maxValue:
                    maxKey = key
                    maxValue = value

            # Take the maxAction that maximizes evaluation and add to visited set
            self.location = maxKey

            visited[maxKey] = visited.get(maxKey, 0) + 1

            if self.is_failure_state(env):
                return 0

            color_array = self.get_image_array(env)
            plt.imshow(color_array, cmap='Greys')
            plt.show()

            env.step()

    def run_agent4(self, env):
        starttime = time.time()

        visited = {(0, 0): 1}
        while time.time() <= (starttime + 300) and self.is_alive:
            if self.is_success_state():
                return 1
            neighbors = self.get_valid_neighbors(
                self.location, env.effective_maze) + [self.location]

            original_location = self.location
            evaluation_scores = {}

            for neighbor in neighbors:
                self.location = neighbor
                knn_kdd = self.tree_search(env, 9, 'max')
                evaluation = max(0.00100, knn_kdd)
                # print(evaluation)
                neighbor_score = abs(1 / (evaluation + 1)**(5))

                if neighbor in visited:
                    neighbor_score = neighbor_score * \
                        0.6 ** (visited[neighbor])
                md = self.manhattan_distance(self.location, constants.SIZE)
                neighbor_score = ((neighbor_score + 1) / (md + 1)**(1))
                neighbor_score += abs(1 / (evaluation+1)) * 15
                evaluation_scores[neighbor] = round(neighbor_score, 6)

            self.location = original_location
            self.is_alive = True

            maxKey, maxValue = self.location, -float("inf")
            for key, value in evaluation_scores.items():
                if visited.get(key, 0) <= 15 and evaluation_scores[key] > maxValue:
                    maxKey = key
                    maxValue = value

            if maxKey not in env.visible_ghosts.values():
                self.location = maxKey
            else:
                self.location = self.move_agent_away_from_nearest_ghost(env)
            visited[maxKey] = visited.get(maxKey, 0) + 1
            if self.is_failure_state(env):
                return 0
            env.step()

        return -1
