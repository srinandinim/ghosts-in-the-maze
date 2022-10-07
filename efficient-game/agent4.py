from copy import deepcopy
import constants
from agent import Agent
from agent2 import Agent2


class Agent4(Agent2):

    def __init__(self):
        super().__init__()
        self.actionspace = []

    def actionspaces(self, env):
        possible_valid_moves = self.get_valid_neighbors(
            self.location, env.effective_maze)
        possible_valid_moves.append(self.location)

        return possible_valid_moves

    def sum_manhattan_distances_to_all_ghosts(self, env):
        distances = 0 
        for ghost_location in env.ghost_locations.values():
            distances += self.manhattan_distance(self.location, ghost_location)
        return distances 

    def run_agent4(self, env):
        visited = {}
        while self.is_alive:
            visited[self.location] = visited.get(self.location, 0) + 1

            if self.location == (constants.SIZE[0]-1, constants.SIZE[1]-1):
                return 1

            self.actionspace = self.actionspaces(env)

            # run k simulation and store success rate for each one
            moves_success = {}
            maximum_success = 0
            for action in self.actionspace:
                for _ in range(2):
                    agent2 = Agent2()
                    agent2.location = action
                    attempt_success = agent2.run_agent2_forecast(deepcopy(env))
                    moves_success[action] = moves_success.get(action, 0) + attempt_success
                    maximum_success = max(maximum_success, moves_success[action])


            sum_manhattan_distances = self.sum_manhattan_distances_to_all_ghosts(env)

            # penalize states already visited, encouraging exploration, avoid local minima
            for key in moves_success.keys():
                if key in visited.keys():
                    moves_success[key] = moves_success[key] * 0.6 ** (visited[key]) - sum_manhattan_distances**(1/8)
                moves_success[key] = ((moves_success[key] + 1) / (self.manhattan_distance(key, (constants.SIZE[0]-1, constants.SIZE[1]-1)) + 1)**(2))

            action = max(moves_success, key=moves_success.get)
            # if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
            if action not in env.ghost_locations.values():
                self.location = action
            else:
                self.location = self.move_agent_away_from_nearest_ghost(env)

            if self.location in env.ghost_locations.values():
                self.is_alive = False
                return 0

            env.step()

    def run_agent3_video(self, env):
        video_frames = []
        video_name = "agent3_ghosts{}_".format(len(env.ghost_locations))

        visited = {}
        while self.is_alive:
            video_frames.append(self.get_image_array(env))
            visited[self.location] = visited.get(self.location, 0) + 1

            if self.location == (constants.SIZE[0]-1, constants.SIZE[1]-1):
                self.generate_video(video_name + "success", video_frames)
                return 1

            self.actionspace = self.actionspaces(env)

            # run k simulation and store success rate for each one
            moves_success = {}
            maximum_success = 0
            for action in self.actionspace:
                for _ in range(10):
                    agent2 = Agent2()
                    agent2.location = action
                    attempt_success = agent2.run_agent2_forecast(deepcopy(env))
                    moves_success[action] = moves_success.get(
                        action, 0) + attempt_success
                    maximum_success = max(
                        maximum_success, moves_success[action])

            # penalize states already visited, encouraging exploration, avoid local minima
            for key in moves_success.keys():
                if key in visited.keys():
                    moves_success[key] = moves_success[key] * \
                        0.6 ** (visited[key])
                moves_success[key] = ((moves_success[key] + 1) / (self.manhattan_distance(
                    key, (constants.SIZE[0]-1, constants.SIZE[1]-1)) + 1)**(2))

            action = max(moves_success, key=moves_success.get)
            if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
                self.location = action
            else:
                self.location = self.move_agent_away_from_nearest_ghost(env)

            if self.location in env.ghost_locations.values():
                self.is_alive = False
                self.generate_video(video_name + "failure", video_frames)
                return 0

            env.step()
