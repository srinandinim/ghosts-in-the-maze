import matplotlib.pyplot as plt
from agent import Agent


class Agent1(Agent):

    def __init__(self):
        super().__init__()

    def run_agent1(self, env):
        """
        # plan once using BFS 
        # while the agent is alive 
            # if we reach end of maze, reward=+1
            # agent takes the next action in plan  
            # update ghosts, and environment effective maze
            # if ghost intersects with agent, the agent dies and recieves 0 reward 
        """
        plan = super().plan_path(env, (0, 0))
        while self.is_alive:
            if self.is_success_state():
                return 1
            self.location = plan.pop(0)
            if self.is_failure_state(env):
                return 0
            env.step()

    def run_agent1_video(self, env):
        video_frames = []
        video_name = "agent1_ghosts{}_".format(len(env.ghost_locations))

        plan = super().plan_path(env, (0, 0))
        while self.is_alive:
            video_frames.append(self.get_image_array(env))
            if self.is_success_state():
                self.generate_video(video_name + "success", video_frames)
                return 1
            self.location = plan.pop(0)
            if self.is_failure_state(env):
                self.generate_video(video_name + "failure", video_frames)
                return 0
            env.step()

    def run_agent1_debug(self, env):
        plan = super().plan_path(env, (0, 0))
        print(f"This is the Agent's plan: {plan}")

        while self.is_alive:

            print(f"The Agent's current location is: {self.location}")
            # env.debugging_all()

            if self.is_success_state():
                print("WIN!")
                return 1

            print(
                f"OLD LOCATION: {old_location}\t potential ghosts that swap: {potential_ghosts_that_swap}")

            action = plan.pop(0)
            print(f"This is the Agent's next action: {action}")
            self.location = action

            env.debugging_print_all_ghost_locations()

            color_array = self.get_image_array(env)
            plt.imshow(color_array, cmap='Greys')
            plt.show()

            if self.is_failure_state(env):
                print("LOSS!")
                self.is_alive = False
                return 0

            env.step()
