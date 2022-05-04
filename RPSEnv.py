# M E 369P - Team 4 - Short n' Clean 
# Allen Hewson, Brenda Miltos, Marcie Legarde, Pranay Srivastava
# RPS Environment File for Reinforcement Learning

#from gym import Env
#from gym.spaces import Discrete, Box
import numpy as np
import random
from copy import copy


class RPSEnv: #(Env):
    # inspo: https://www.youtube.com/watch?v=9_91p4SuiA4
    # https://github.com/koushik4/RockPaperScissors/blob/master/probabilities.py
    # WE MARKOVIN

    def __init__(self): # generate initial environment
        #self.action_space = Discrete(3)
        init_index = random.randint(0,2)
        self.state = [0,0,0]
        self.state[init_index] = 1
        self.transition = [[1/3,1/3,1/3],[1/3,1/3,1/3],[1/3,1/3,1/3]]
        self.previous_user_action = init_index
        self.prediction = self.state.index(max(self.state)) # 0, 1, 2
        self.reward_value = 0.2

    def step(self, user_action): # apply action and return new time_step
        #value_dict = {0:'R', 1:'P', 2:'S'}
        action_dict = {0:1, 1:2, 2:1}

        reward = self.reward_value if self.prediction is user_action else -self.reward_value
        previous_row = copy(self.transition[self.previous_user_action]) # THIS IS A REFERENCE AHHH
        #print(previous_row)

        for play in range(0,3):
            key = True
            if play is self.prediction:
                self.transition[self.previous_user_action][play] += reward
                key = False
            else:
                self.transition[self.previous_user_action][play] -= reward/2

            if not 0 <= self.transition[self.previous_user_action][play] <= 1:
                if self.transition[self.previous_user_action][play] < 0:
                    reward = -previous_row[play]
                    self.transition[self.previous_user_action][play] = 0
                elif self.transition[self.previous_user_action][play] > 1:
                    reward = 1-previous_row[play]
                    self.transition[self.previous_user_action][play] = 1
                if key: reward *= -2
                #print(reward, play)
                
                for i in range(0,len(previous_row)):
                    if i < play:
                        if i is self.prediction:
                            reward_compare = reward
                        else: 
                            reward_compare = -reward/2
                        #print(reward_compare)

                        if abs(self.transition[self.previous_user_action][i]-previous_row[i]) > abs(reward_compare):
                            self.transition[self.previous_user_action][i] = previous_row[i] + reward_compare

        # print("NEW TRANSITION", self.transition)
        self.previous_user_action = user_action
        # sums = []
        # for row in range(0,len(self.transition)):
        #     sums.append(sum(self.transition[row]))
        
        # markov chain operation to calculate new state and determine likely prediction
        # converting to np.arrays here as easier to work with
        state_np, transition_np = np.array(self.state), np.array(self.transition)
        self.state = np.matmul(state_np, transition_np).tolist()
        self.prediction = self.state.index(max(self.state))
        self.action = action_dict[self.prediction]

        return self.prediction, self.action, self.previous_user_action #, sums

    def reset(): # return initial time step
        pass



# TEST
test = RPSEnv()
#user_action = [0,1,1]
total, correct = 0,0
ceiling = 20
for i in range(0,ceiling):
    user_action = 2
    #user_action = [0,1,1,2,2,1][random.randint(0,2)] 
    #user_action = random.randint(0,2)
    print("User:", user_action)
    print("State:", test.state)
    print("Transition:", test.transition)
    predicted, action, previous = test.step(user_action)
    print("PREDICTED", predicted)
    print("COMPUTER ACTION", action)
    print("USER ACTION DETECTED", previous)
    total += 1
    if user_action is predicted:
        correct = correct + 1 

    print("\n")

print("\nPERCENTAGE: ",(correct/total)*100)


    # BASING OFF MARKOV CHAIN COULD BE COOL WAIT SHIT BAYES MIGHT BE BETTER GUESS IM LEARNING ALL OF STAT TODAY

    # state and transition matrix


# INSPIRATIONS:
# https://towardsdatascience.com/how-to-win-over-70-matches-in-rock-paper-scissors-3e17e67e0dab
# https://www.youtube.com/watch?v=bD6V3rcr_54


# class RPSEnvAnotherOne(Env):
#     # state = user throw (?)
#     # action = computer throw


#     def __init__(self): # generate initial environment
#         self.action_space = Discrete(3) # 0=R, 1=P, 2=S
#         #self.operation_space = Box(low=np.array([0]), high=np.array([100])) # array for percentages?
#         #self.state = random.randint(0,2) # initial assumption for user throw

#         combos = ['RR', 'RP', 'RS', 'PR', 'PP', 'PS', 'SR', 'SP', 'SS']
#         self.state = {}

#         for combo in combos:
#             self.state[combo] = {'R': [1/3, 0], 'P': [1/3, 0], 'S': [1/3, 0]} # creates dictionary for matrix, with count

        
#         pass
#     def step(self, user_action, combo): # apply action and return new time_step
#         #action_dict = {0:'R', 1:'P', 2:'S'} # bruh do i also have to accountr for a none case?
#         action_dict = {'R':'P', 'P':'S', 'S':'R'}
#         state_dict = {'RR':0, 'RP':1, 'RS':-1, 'PR':-1, 'PP':0, 'PS':1, 'SR':1, 'SP':-1, 'SS':0 }

#         # recalculate probabilities
#         self.state[combo][user_action][1] += 1 # increases count of occurence by 1

#         total_count = sum([self.state[combo][potential_action][1] for potential_action in action_dict])
#         for potential_action in action_dict:
#             self.matrix[combo][potential_action][0] = self.matrix[combo][potential_action][1] / total_count
        
#         # action application and reward calculation

#         else:
#             raise ValueError("'action' should be 0, 1, or 2.")


#         pass
#     def reset(): # return initial time step
#         pass