import sys
import numpy as np
from configure import *

class Environment:
    def __init__(self,startTuple,endTuple):
        # file = 'empirical_maze2.txt'
        # with open(file,'r') as f:
        #     self.maze=[line.split()[0] for line in f]
        #print(self.maze)
        #a list of tuples of valid state
        self.valid_states=[]
        self.ll_block=[]
        #buradan uzunluk degisecek
        self.v_initial=np.zeros((env_width,env_height))
        
        self.target_coord_tup=endTuple
        self.start_coord_tup=startTuple
        self.curr_state=self.start_coord_tup
        self.num_row=len(self.v_initial)
        self.num_col=len(self.v_initial[0])

        for row in range(self.num_row):
            for col in range(self.num_col):
                self.valid_states.append((row,col))

        self.ll_block = self.generateRandomObstacleCoordinats()
        #print('valid states {0}'.format(self.valid_states))
        #print('start tuple = {}'.format(self.start_coord_tup))
        #print('target tuple = {}'.format(self.target_coord_tup))
        #print('block : {0}'.format(self.ll_block))
        #print(self.v_initial)
    def step(self,action):
        #print(action)
        row=self.curr_state[0]
        col=self.curr_state[1]

        if self.curr_state==self.target_coord_tup:
            return self.curr_state,5,1

        next_state=()
        isterm=0
        #up
        if action==0:
            next_state=(row,max(col-1,0))
            if (row,col-1) in self.ll_block:
                next_state=(row,col)
        # left
        elif action==1:
            next_state=(max(row-1,0),col)
            if (row-1,col) in self.ll_block:
                next_state=(row,col)
        # down 
        elif action==2:
            next_state=(row,min(self.num_col-1,col+1))
            if (row,col+1) in self.ll_block:
                next_state=(row,col)
        # right
        elif action==3:
            next_state=(min(row+1,self.num_row-1),col)
            if (row+1,col) in self.ll_block:
                next_state=(row,col)
        # up right cross
        elif action==4:
            next_state=(min(row+1,self.num_row-1),max(col-1,0))
            if next_state in self.ll_block:
                next_state=(row,col)
        #up left cross
        elif action==5:
            next_state=(max(row-1,0),max(col-1,0))
            if next_state in self.ll_block:
                next_state=(row,col)
        #down right cross
        elif action==6:
            next_state=(min(row+1,self.num_row-1),min(self.num_col-1,col+1))
            if next_state in self.ll_block:
                next_state=(row,col)
        #down left cross 
        else :
            next_state=(max(row-1,0),min(self.num_col-1,col+1))
            if next_state in self.ll_block:
                next_state=(row,col)
        self.curr_state=next_state
        if next_state==self.target_coord_tup:
            isterm=1
        return next_state,-1,isterm

    def reset(self):
        self.curr_state=self.start_coord_tup
        return

    def generateRandomObstacleCoordinats(self):
        finishPixel,startPixel =self.target_coord_tup,self.start_coord_tup
        obstacleAmount = int(self.num_col*self.num_row*randomPixelRatio) 
        
        xList = np.random.randint(self.num_row,size=obstacleAmount)
        yList =  np.random.randint(self.num_col,size=obstacleAmount)
        obstacleCoordinats = []
        f = open("./entities/obstacle.txt", "w")
        try:
            for i in range(obstacleAmount):
                newObstacle = (xList[i] ,yList[i])
                if not(newObstacle == startPixel) and not(newObstacle == finishPixel) and newObstacle not in obstacleCoordinats:
                    obstacleCoordinats.append(newObstacle)
                    try:
                        self.valid_states.remove(newObstacle)
                    except :
                        print(newObstacle)
                   
                    self.v_initial[xList[i]][yList[i]]=float("inf")
                    # f.write("({}, {}, K)\n".format(xList[i], yList[i]))
            for row in range(self.num_row):
                for col in range(self.num_col):
                    i = (row,col)
                    if( i in obstacleCoordinats):
                        f.write("({}, {}, O)\n".format(row, col))
                    elif(i == startPixel):
                        f.write("({}, {}, S)\n".format(row, col))
                    elif(i==finishPixel):
                        f.write("({}, {}, T)\n".format(row, col))
                    else:
                        f.write("({}, {}, R)\n".format(row, col))
            #print(obstacleCoordinats)
            #for testing 
            # for i in range(obstacleAmount):
            #     if newObstacle == startPixel or newObstacle == finishPixel:
            #         print("cakisiyor......")
        except :
            e = sys.exc_info()[0]
            print(e)
            print("Dosyaya yazarken veyahut random atama yapilirken bir hata olustu!")
        finally:
            f.close();
            print("matris obstacle.txt teye yazildi")
            return obstacleCoordinats
# if __name__ == "__main__":
#     envrn=Environment(sys.argv[1])
#     with open(sys.argv[3],'r') as f:
#         action_seq=[map(int,line.split(' ')) for line in f]
#     print('hello {0}'.format(action_seq))
#     with open(sys.argv[2],'w') as f:
#         for actions in action_seq[0]:
#             next_state,reward,istarget=envrn.step(actions)
#             f.write('{} {} {} {}\n'.format(next_state[0],next_state[1],reward,istarget))

