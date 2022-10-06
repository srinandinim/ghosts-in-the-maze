import random
import constants 
from agent import Agent1, Agent2
from environment import Environment 

def simulation_statistics_agent1(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent1 = [] 
    for _ in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts) 
        agent1 = Agent1()
        rewards_agent1.append(agent1.run_agent1(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins 
    survival = wins / (wins + losses)
    print(f"Agent1: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")  
    return round(survival*100,2)

def simulation_statistics_agent1_video(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent1 = [] 
    for _ in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts) 
        agent1 = Agent1()
        rewards_agent1.append(agent1.run_agent1_video(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins 
    survival = wins / (wins + losses)
    print(f"Agent1: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")  
    return round(survival*100,2)

def simulation_statistics_agent2(num_simulations, num_ghosts):
    """
    run simulation n times and get statistics on survival, and more
    """
    rewards_agent1 = [] 
    for _ in range(num_simulations):
        env = Environment(num_ghosts=num_ghosts) 
        agent2 = Agent2()
        rewards_agent1.append(agent2.run_agent2(env))
    wins = sum(rewards_agent1)
    losses = len(rewards_agent1) - wins 
    survival = wins / (wins + losses)
    print(f"Agent2: Wins: {wins}\tLosses: {losses}\tSurvival Rate: {round(survival*100,2)}%")  
    return round(survival*100,2)

def lab_report_simulations(a1=False, a2=False, a3=False, a4=False, a5=False):
    """
    TODO: @Nandini, this needs to be updated to run on the same environment. 
    Not worrying about this right now because its not top priority, but 
    important for us to complete overall before lab report submission. 
    """

    random.seed(42) 

    a1_stats, a2_stats, a3_stats, a4_stats, a5_stats = {}, {}, {}, {}, {} 
    last_survival_rate, num_ghosts, max_ghosts = 100, 1, constants.SIZE[0] * constants.SIZE[1]
    a1_s = a2_s = a3_s = a4_s = a5_s = 0 

    while last_survival_rate > 0 and num_ghosts < max_ghosts: 
        print(f"\nTHE NUMBER OF CURRENT GHOSTS ARE: {num_ghosts}")
        
        if a1 == True: 
            a1_s = simulation_statistics_agent1(num_simulations=30, num_ghosts=num_ghosts)
            a1_stats[num_ghosts] = a1_s 
    
        if a2 == True:
            a2_s = simulation_statistics_agent2(num_simulations=100, num_ghosts=num_ghosts)
            a2_stats[num_ghosts] = a2_s
        
        last_survival_rate = min(last_survival_rate, max(a1_s, a2_s, a3_s, a4_s, a5_s))
        num_ghosts += 1
    
    return a1_stats, a2_stats, a3_stats, a4_stats, a5_stats

if __name__ == "__main__":
    """
    a1_stats, a2_stats, a3_stats, a4_stats, a5_stats = lab_report_simulations(a1=True, a2=True)
    print(f"Agent 1 Stats: {a1_stats}")
    print(f"Agent 1 Stats: {a2_stats}")
    """

    env = Environment(num_ghosts=5)
    a2 = Agent2()
    a2.run_agent2_debug(5)


