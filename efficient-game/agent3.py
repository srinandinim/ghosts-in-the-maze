from copy import deepcopy
import constants
from agent import Agent
from agent2 import Agent2

class Agent3(Agent2):

    def __init__(self):
        super().__init__()
        self.actionspace = []

    def actionspaces(self, env):
        possible_valid_moves = self.get_valid_neighbors(
            self.location, env.effective_maze)
        possible_valid_moves.append(self.location)

        return possible_valid_moves

    def run_agent3(self, env):
        visited = {}
        while self.is_alive:
            visited[self.location] = visited.get(self.location, 0) + 1

            if self.location == (constants.SIZE[0]-1, constants.SIZE[1]-1):
                return 1

            self.actionspace = self.actionspaces(env)

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
                return 0

            env.step()