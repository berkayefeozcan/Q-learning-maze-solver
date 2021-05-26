from environment import Environment
import sys
import numpy as np
import random as rand
import time
from configure import episodeAmount
class Qlearning:
    def __init__(self,env,epsilon,lr):
        self.q_dict={}
        self.env=env
        self.learn_rate=lr
        self.episilon = epsilon
        for each_val_state in self.env.valid_states:
            self.q_dict[each_val_state]=np.zeros(8)
        #print(self.q_dict)
        return

    def select_action(self,state):
        rand_value=rand.uniform(0,1)
        if rand_value>self.episilon:
            return self.q_dict[state].argmax()
        else:
            return rand.randint(0,7)

    def q_learn(self):
        total=0
        d = {}
        # en kisa yol
        shorthestPath = {}
        i = 0
        c = True
        longest = 0
        shortest = 0
        steps = []
        all_costs = []

        for episode in range(0,episodeAmount):
            curr_episode_len=0
            cost = 0 
            self.env.reset()
            #while curr_episode_len < (int(sys.argv[6])):
            while(True):
                prev_state=self.env.curr_state
                action=self.select_action(self.env.curr_state)
                next_state,reward,istarget=self.env.step(action)
                #print(next_state)
                self.q_dict[prev_state][action]=((1-self.learn_rate)*self.q_dict[prev_state][action]) + (self.learn_rate * (reward + (self.q_dict[next_state].max())))
                d[i] = next_state
                i+=1
                # eger hedefe varilmissa
                if istarget:
                    if c == True:
                        for j in range(len(d)):
                            shorthestPath[j] = d[j]
                        c = False
                        longest = len(d)
                        shortest = len(d)

                    # Checking if the currently found route is shorter
                    if len(d) < len(shorthestPath):
                    # Saving the number of steps for the shortest route
                        shortest = len(d)
                        shorthestPath = {}
                        # Reassigning the dictionary
                        for j in range(len(d)):
                            shorthestPath[j] = d[j]

                    # Saving the number of steps for the longest route
                    if len(d) > longest:
                        longest = len(d)
                    break
                curr_episode_len+=1
                cost+=reward

           
            steps+=[curr_episode_len]
            all_costs+=[cost]
            total+=curr_episode_len
            d = {}
            i = 0  
            print("episode {} step sayisi {}".format(episode+1,curr_episode_len))
        #print(shorthestPath)
        #print("Average length per episode {}".format(float(total/episodeAmount)))
        return shorthestPath,steps,all_costs

    def write_to_fle(self):
        with open(sys.argv[2],'w') as v_file, open(sys.argv[3],'w') as q_file, open(sys.argv[4],'w') as p_file:
            for cell in self.q_dict:
                v_file.write('{} {} {}\n'.format(cell[0],cell[1],self.q_dict[cell].max()))
                p_file.write('{} {} {}\n'.format(cell[0],cell[1],float(self.q_dict[cell].argmax())))
                for action,value in enumerate(self.q_dict[cell]):
                    q_file.write('{} {} {} {}\n'.format(cell[0],cell[1],action,value))
        return



# if __name__=="__main__":
#     start_time = time.time()
#     learn_rate=float(sys.argv[7])
#     epsilon=float(sys.argv[9])
#     env=Environment(sys.argv[1])
#     q_dict=init()
#     q_learn()
#     write_to_fle()
#     print("--- %s seconds ---" % (time.time() - start_time))