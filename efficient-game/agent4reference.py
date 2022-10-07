from agent import Agent
import constants 
import numpy as np 

class Agent4(Agent):
    """
    Develop an Agent4 that plays a min-max game where Agent maximizes some reward and an ensemble of ghost minimizes some reward (think of all the ghosts as one adversary). 

    def init
    def minimax
    """
    def sum_manhattan_distances_to_all_ghosts(self, env):
        distances = 0 
        for ghost_location in env.ghost_locations.values():
            distances += self.manhattan_distance(self.location, ghost_location)
        return distances 
    def minimax(self, env, depth, min_or_max):
        if depth == 0 or self.is_alive == False:
            return self.sum_manhattan_distances_to_all_ghosts(env)

        if min_or_max == "max":
            max_eval = -10000
            best_action = self.location
            valid_moves = self.get_valid_neighbors(self.location, env.maze_grid)
            for move in valid_moves: 
                env.create_temporary_ghost_locations(self.location, move)
                self.location = move
                eval = self.minimax(env, depth-1, "min")
                if eval > max_eval:
                    max_eval = eval
                    best_action = move
                env.reset_ghost_locations()
            self.location = best_action
            return max_eval

        if min_or_max == "min":
            min_eval = 10000
            for ghost_location in env.ghost_locations.values():
                move_possibilities = self.get_valid_neighbors(
                    ghost_location, env.maze_grid)
                for move in move_possibilities: 
                    env.create_temporary_ghost_locations(ghost_location, move)
                    eval = self.minimax(env, depth-1, "max")
                    env.reset_ghost_locations()
                    if eval < min_eval:
                        min_eval = eval
            return min_eval

    def move_agent_minimax(self, env):
        self.location = self.minimax(env, 5, 'max')
        return self.location
        
    def alpha_beta_pruning(self, env, depth, min_or_max, alpha, beta):
        if depth == 0 or self.is_alive == False:
            return self.sum_manhattan_distances_to_all_ghosts(env)

        if min_or_max == "max":
            max_eval = -10000
            valid_moves = self.get_valid_neighbors(self.location, env.maze_grid)
            for move in valid_moves: 
                env.create_temporary_ghost_locations(self.location, move)
                self.location = move
                eval = self.alpha_beta_pruning(env, depth-1, "min", alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                env.reset_ghost_locations()
                if eval >= beta:
                    return eval
                alpha = max(alpha, eval)
            return max_eval

        if min_or_max == "min":
            min_eval = 10000
            for ghost_location in env.ghost_locations.values():
                move_possibilities = self.get_valid_neighbors(
                    ghost_location, env.maze_grid)
                for move in move_possibilities: 
                    env.create_temporary_ghost_locations(ghost_location, move)
                    eval = self.alpha_beta_pruning(env, depth-1, "max", alpha, beta)
                    env.reset_ghost_locations()
                    if eval < min_eval:
                        min_eval = eval
                    if eval <= alpha:
                        return eval 
                    beta = min(beta, eval)
            return min_eval

    def move_agent_alpha_beta_pruning(self, env):
        self.location = self.alpha_beta_pruning(env, 3, "max", -10000, 10000)
        return self.location
    
    def expectimax(self, env, depth, min_or_max):
    
        """
        modfies minimax so that it computes expected probabilities and doesn't weight equal the ghost movements
        """
        
        if depth == 0 or self.is_alive == False:
            return self.sum_manhattan_distances_to_all_ghosts(env)

        if min_or_max == "max":
            max_eval = -10000
            best_action = self.location
            valid_moves = self.get_valid_neighbors(self.location, env.maze_grid)
            for move in valid_moves: 
                env.create_temporary_ghost_locations(self.location, move)
                self.location = move
                eval = self.expectimax(env, depth-1, "min")
                if eval > max_eval:
                    max_eval = eval
                    best_action = move
                env.reset_ghost_locations()
            self.location = best_action
            return max_eval

        if min_or_max == "min":
            prob_ghost_move_correctly = 0.2
            eval_total = 0
            for ghost_location in env.ghost_locations.values():
                move_possibilities = self.get_valid_neighbors(
                    ghost_location, env.maze_grid)
                for move in move_possibilities:
                    env.create_temporary_ghost_locations(ghost_location, move)
                    eval_total += prob_ghost_move_correctly*self.expectimax(env, depth-1, "max")
                    env.reset_ghost_locations()
            return eval_total

    def move_agent_expectimax(self, env):
        self.location = self.expectimax(env, 5, "max")
        return self.location

    def reward_matrix(self, env):
        reward_matrix = np.zeros_like(env.maze_grid)
        for i in range(constants.SIZE[0]):
            for j in range(constants.SIZE[0]):
                reward_matrix[i][j] = int(self.manhattan_distance(self.location, constants.SIZE) / (constants.SIZE[0]*constants.SIZE[1]))
        print(reward_matrix)

if __name__ == "__main__":
    env = Environment()
    a4 = Agent4()
    a4.reward_matrix(env)
        