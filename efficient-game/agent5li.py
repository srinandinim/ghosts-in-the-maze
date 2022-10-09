from copy import deepcopy

import numpy as np
import constants
from agent4li import Agent4LI


class Agent5LI(Agent4LI):

    def __init__(self):
        super().__init__()
        self.ghosts_in_memory = {}
        self.has_path = True

    def update_ghosts_in_memory(self, env):
        for ghost, (priority, location) in self.ghosts_in_memory.items():
            self.ghosts_in_memory[ghost] = (priority + 1, location) if priority < constants.SIZE[0] else None

        for ghost, location in env.visible_ghosts.items():
            self.ghosts_in_memory[ghost] = (1, deepcopy(location))

        filtered = {k: v for k, v in self.ghosts_in_memory.items()
                    if v is not None}
        self.ghosts_in_memory = filtered

    def get_ghosts_in_memory_values(self):
        ghost_locations = set()
        for _, (_, location) in self.ghosts_in_memory.items():
            ghost_locations.add(location)

        return ghost_locations

    def get_knearestghosts(self, k):
        """
        given {ghost1:location_tuple, ..., ghostn:location_tuple}
        return {ghosti:location_tuple, ..., ghostk:location_tuple} 
        closest k ghosts to self.location per manhattan distance
        """
        k = min(k, len(self.get_ghosts_in_memory_values()))
        distances = {}
        for ghost, (priority, location) in self.ghosts_in_memory.items():
            distances[ghost] = self.manhattan_distance(
                self.location, location) * priority

        # sort descending by value, then select k-lowest values
        distances = sorted(distances.items(), key=lambda kv: kv[1])[:k]

        nearestkghosts = {}
        for ghost, dist in distances:
            nearestkghosts[ghost] = dist

        return nearestkghosts

    def tree_search(self, env, depth, min_or_max):
        if depth == 1 or self.is_alive == False:
            knn_mdsum = self.knn_mdsum(self.get_knearestghosts(k=10))
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

            if best_action not in self.get_ghosts_in_memory_values():
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

    def run_agent5(self, env):
        visited = {(0, 0): 1}
        self.update_ghosts_in_memory(env)

        while self.is_alive:
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

            self.update_ghosts_in_memory(env)

        return -1