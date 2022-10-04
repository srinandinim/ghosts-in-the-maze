from game.environment import Environment 
import game.final_variables as final_variables
from game.agent import Agent
import time

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
        
    def run_agent1(self, env):
        """
        allows you to run agent on environment, returns +1 if successful, +0 for other terminations
        """
        plan = env.shortest_paths[0][0]
        while self.isalive:
            if self.location == final_variables.GOAL:
                return 1 
            action = plan.pop(0) 
            self.location = action 
            for ghost in env.ghosts:
                ghost.update_location(env) 
                if self.location == ghost.get_location():
                    self.isalive = False 
                    return 0 
        return 0

    def run_agent1_verbose(self, env):
        """
        allows you to run agent on environment, returns +1 if successful, +0 for other terminations
        """
        super().print_environment(env)
        plan = self.plan_path(env)

        print(f"Agent 1's Planned Optimal Path is: {plan}")
        print(self.location)

        images = []
        video_name = "agent1_" + str(time.time())

        while self.isalive:
            if self.location == (final_variables.SIZE-1, final_variables.SIZE-1):
                print("\nSUCCESS (+1): THE AGENT REACHED THE GOAL!")
                self.generate_video(video_name, images)
                return 1 
            action = plan.pop(0) 
            self.location = action 
            for ghost in env.ghosts:
                ghost.update_location(env) 
                if self.location == ghost.get_location():
                    print("\nFAILURE (+0): THE AGENT GOT KILLED BY A GHOST")
                    print(f"Agent 1 Location: {self.location}\t Ghost Location: {ghost.get_location()}")
                    self.isalive = False 
                    self.generate_video(video_name, images)
                    return 0 
            # for debugging, print out the agent location and ghost locations
            print(f"\nAgent 1 Location:\t {self.location}")
            for i in range(len(env.ghosts)):
                print(f"Ghost {i} Location:\t {env.ghosts[i].location}")

            color_array = env.get_picture()
            color_array[self.location[0]][self.location[1]] = 3 
            images.append(color_array)

        return 0