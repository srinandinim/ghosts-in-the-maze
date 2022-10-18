from copy import deepcopy
import time
import numpy as np
import constants
from agent4li import Agent4LI


class Agent5LI(Agent4LI):

    def __init__(self):
        super().__init__()

        # stores the memory
        self.ghosts_in_memory = {}

        # determines if path exists towards the end
        self.has_path = True

    def update_ghosts_in_memory(self, env):
        """
        removes ghosts that are above the current priority. 
        store ghosts in memory and update ghosts in memory with new priorities. 
        """

        for ghost, (priority, location) in self.ghosts_in_memory.items():
            self.ghosts_in_memory[ghost] = (
                priority + 1, location) if priority < constants.SIZE[0] else None

        for ghost, location in env.visible_ghosts.items():
            self.ghosts_in_memory[ghost] = (1, deepcopy(location))

        filtered = {k: v for k, v in self.ghosts_in_memory.items()
                    if v is not None}
        self.ghosts_in_memory = filtered

    def get_ghosts_in_memory_values(self):
        """
        find the locations of all ghosts that are stored in memory.
        """

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
        """
        Run a tree simulation and treat this situation as a game. 
        Suppose that Agent 1 is Player 1 and the Ensemble of Ghosts are player 2 moving according to some sample probability. 
        Then, we compute the expected utility for a particular action by propogating information up the relevant tree. 
        That will help us inform what is the best action that we should take. 
        """
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
        """
        We run tree search to get expected utility for every action it the agent's action space.
        We propogate that utility (which minimizes distance to k nearest ghosts) through heuristics
        that optimize the board for curiosity and reaching the end of the maze. Then, we greedily
        select the action that maximizes this new value with greedy hill climbing local search. 
        """
        starttime = time.time()

        visited = {(0, 0): 1}
        self.update_ghosts_in_memory(env)

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

            self.update_ghosts_in_memory(env)

        return -1

    def run_agent5_video(self, env):
        """
        We run tree search to get expected utility for every action it the agent's action space.
        We propogate that utility (which minimizes distance to k nearest ghosts) through heuristics
        that optimize the board for curiosity and reaching the end of the maze. Then, we greedily
        select the action that maximizes this new value with greedy hill climbing local search. 
        """
        starttime = time.time()

        visited = {(0, 0): 1}
        self.update_ghosts_in_memory(env)

        video_frames = []
        video_name = "agent5li_ghosts{}_".format(len(env.ghost_locations))

        while time.time() <= (starttime + 300) and self.is_alive:
            video_frames.append(self.get_image_array(env))
            if self.is_success_state():
                self.generate_video(video_name + "success", video_frames)
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
                self.generate_video(video_name + "failure", video_frames)
                return 0
            env.step()

            self.update_ghosts_in_memory(env)

        return -1