from copy import deepcopy
import time
import constants
from agent2li import Agent2LI
import matplotlib.pyplot as plt


class Agent3LI(Agent2LI):

    def __init__(self):
        super().__init__()
        self.actionspace = []

    def actionspaces(self, env):
        possible_valid_moves = self.get_valid_neighbors(
            self.location, env.effective_maze)
        possible_valid_moves.append(self.location)

        return possible_valid_moves

    def run_agent3(self, env):
        """
        # while the agent is alive 
            # if we reach end of maze, reward=+1
            # simulate agent 2 starting at each of the possible valid moves (2x) and store the success rate of each one
            # choose the next move based on the success of the move and how many times it was visited previously, if any
            # if the chosen move does not collide with a ghost, move there; otherwise, move away from the nearest ghost
            # update ghosts, and environment effective maze
            # if ghost intersects with agent, the agent dies and receives 0 reward 
        """
        starttime = time.time()

        visited = {}
        while time.time() <= (starttime + 240) and self.is_alive:
            visited[self.location] = visited.get(self.location, 0) + 1

            if self.is_success_state():
                return 1

            self.actionspace = self.actionspaces(env)

            # run k simulation and store success rate for each one
            moves_success = {}
            maximum_success = 0
            for action in self.actionspace:
                # updates
                for _ in range(2):
                    agent2 = Agent2LI()
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
                distance_heuristic = ((moves_success[key] + 1) / (self.manhattan_distance(
                    key, (constants.SIZE[0]-1, constants.SIZE[1]-1)) + 1)**(2))
                moves_success[key] = round(distance_heuristic, 3)

            action = max(moves_success, key=moves_success.get)
            # if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
            if action not in env.visible_ghosts.values() and visited.get(action, 0) <= 10:
                self.location = action
            else:
                self.location = self.move_agent_away_from_nearest_ghost(env)

            if self.is_failure_state(env):
                return 0
            env.step()

        return -1

    def run_agent3_video(self, env):
        video_frames = []
        video_name = "agent3_ghosts{}_".format(len(env.visible_ghosts))

        visited = {}
        while self.is_alive:
            video_frames.append(self.get_image_array(env))
            visited[self.location] = visited.get(self.location, 0) + 1

            if self.is_success_state():
                self.generate_video(video_name + "success", video_frames)
                return 1

            self.actionspace = self.actionspaces(env)

            # run k simulation and store success rate for each one
            moves_success = {}
            maximum_success = 0
            for action in self.actionspace:
                for _ in range(2):
                    agent2 = Agent2LI()
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
                distance_heuristic = ((moves_success[key] + 1) / (self.manhattan_distance(
                    key, (constants.SIZE[0]-1, constants.SIZE[1]-1)) + 1)**(2))
                moves_success[key] = round(distance_heuristic, 3)

            action = max(moves_success, key=moves_success.get)
            # if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
            if action not in env.visible_ghosts.values():
                self.location = action
            else:
                self.location = self.move_agent_away_from_nearest_ghost(env)

            if self.is_failure_state(env):
                self.is_alive = False
                self.generate_video(video_name + "failure", video_frames)
                return 0

            env.step()

    def run_agent3_debug(self, env):
        visited = {}
        while self.is_alive:
            print(f"The Agent's current location is: {self.location}")
            # env.debugging_all()
            visited[self.location] = visited.get(self.location, 0) + 1

            if self.is_success_state():
                return 1

            self.actionspace = self.actionspaces(env)

            # run k simulation and store success rate for each one
            moves_success = {}
            maximum_success = 0
            for action in self.actionspace:
                for _ in range(2):
                    agent2 = Agent2LI()
                    agent2.location = action
                    attempt_success = agent2.run_agent2_forecast(deepcopy(env))
                    moves_success[action] = moves_success.get(
                        action, 0) + attempt_success
                    maximum_success = max(
                        maximum_success, moves_success[action])

            print(f"Simulation Results: {moves_success}")
            # penalize states already visited, encouraging exploration, avoid local minima
            for key in moves_success.keys():
                if key in visited.keys():
                    moves_success[key] = moves_success[key] * \
                        0.6 ** (visited[key])
                distance_heuristic = ((moves_success[key] + 1) / (self.manhattan_distance(
                    key, (constants.SIZE[0]-1, constants.SIZE[1]-1)) + 1)**(2))
                moves_success[key] = round(distance_heuristic, 3)

            print(f"Simulation Results With Heuristics: {moves_success}")

            action = max(moves_success, key=moves_success.get)
            # if action not in self.ghost_actionspace(env, self.nearest_visible_ghost(env)).keys():
            if action not in env.visible_ghosts.values():
                self.location = action
            else:
                self.location = self.move_agent_away_from_nearest_ghost(env)

            print(f"The Agent's new location is: {self.location}")
            if self.is_failure_state(env):
                self.is_alive = False
                return 0

            color_array = self.get_image_array(env)
            plt.imshow(color_array, cmap='Greys')
            plt.show()

            env.step()
