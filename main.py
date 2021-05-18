import random
import numpy as np
import tkinter as tk
from tkinter import ttk
import time  # Time is needed to slow down the agent and to see how he runs
from PIL import Image, ImageTk  # For adding images into the canvas widget
from path import Environment
from agent import QLearningTable
from configure import episodeAmount,env_height,env_width,randomPixelRatio,startPageTitle,startPageResolation,XCBOptions,YCBOptions

class HomePage(tk.Tk, object):
    def __init__(self):
        super(HomePage, self).__init__()       
        #self.configure(bg="white")
        self.startPosition = [tk.StringVar(value=0),tk.StringVar(value=0)]
        self.endPosition = [tk.StringVar(value=0),tk.StringVar(value=0)]
        self.title(startPageTitle)
        self.geometry(startPageResolation)
        self.create_widgets()

    def create_widgets(self):
        self.startButton =  tk.Button(self,text="baslat",command=self.startQLearning)
        self.startButton.place(x = 190,y = 130)    
        self.startPositionLabel= tk.Label(self,text = "Başlangıç konumu :").place(x = 40,y = 60)
        self.endPositionLabel = tk.Label(self,text="Bitiş Konumu          :").place(x=40,y=100)
        self.startPositionComboBoxX = ttk.Combobox(self,values=XCBOptions,textvariable=self.startPosition[0],width=5)
        self.startPositionComboBoxX.place(x=150,y=60)
        self.startPositionComboBoxX.current(0)
        self.startPositionComboBoxY = ttk.Combobox(self,values=YCBOptions,textvariable=self.startPosition[1],width=5)
        self.startPositionComboBoxY.place(x=210,y=60)
        self.startPositionComboBoxY.current(0)
        # hedef konum labirentin sonuna yaikin olmasi acisindan degerler ters donduruluyor.
        self.endPositionComboBoxX = ttk.Combobox(self,values=XCBOptions[::-1],textvariable=self.endPosition[0],width=5)
        self.endPositionComboBoxX.place(x=150,y=100)
        self.endPositionComboBoxX.current(0)
        self.endPositionComboBoxY = ttk.Combobox(self,values=YCBOptions[::-1],textvariable=self.endPosition[1],width=5)
        self.endPositionComboBoxY.place(x=210,y=100)
        self.endPositionComboBoxY.current(0)
    def startQLearning(self):
        self.destroy()
        startPixel = [int(self.startPosition[0].get()),int(self.startPosition[1].get())]
        finishPixel = [int(self.endPosition[0].get()),int(self.endPosition[1].get())]
        print(finishPixel)
        # random Obstacle coordinat list ex:5x5 [0,3]
        obstacleCoordinats = self.generateRandomObstacleCoordinats(finishPixel,startPixel)
        self.env = Environment(startPixel ,finishPixel,obstacleCoordinats)
        # Calling for the main algorithm
        self.RL = QLearningTable(actions=list(range(self.env.n_actions)))
        # Running the main loop with Episodes by calling the function update()
        self.env.after(100, self.update)  # Or just update()
        self.env.mainloop()

    def update(self):
        # Resulted list for the plotting Episodes via Steps
        steps = []

    # Summed costs for all episodes in resulted list
        all_costs = []

        for episode in range(episodeAmount):
        # Initial Observation
            print(episode)
            observation = self.env.reset()
        # Updating number of Steps for each Episode
            i = 0

        # Updating the cost for each episode
            cost = 0

            while True:
            # Refreshing environment
                # self.env.render()

            # RL chooses action based on observation
                action = self.RL.choose_action(str(observation))

            # RL takes an action and get the next observation and reward
                observation_, reward, done = self.env.step(action)

            # RL learns from this transition and calculating the cost
                cost += self.RL.learn(str(observation), action, reward, str(observation_))

            # Swapping the observations - current and next
                observation = observation_

            # Calculating number of Steps in the current Episode
                i += 1

            # Break while loop when it is the end of current Episode
            # When agent reached the goal or obstacle
                if done:
                    steps += [i]
                    all_costs += [cost]
                    break

    # Showing the final route
        self.env.final()

    # Showing the Q-table with values for each action
        self.RL.print_q_table()

    # Plotting the results
        self.RL.plot_results(steps, all_costs)
    
    def generateRandomObstacleCoordinats(self,finishPixel,startPixel):

        obstacleAmount = int(env_height*env_width*randomPixelRatio) 
        xList = np.random.randint(env_width,size=obstacleAmount)
        yList =  np.random.randint(env_height,size=obstacleAmount)
        obstacleCoordinats = []
        f = open("./entities/engel.txt", "w")
        try:
            for i in range(obstacleAmount):
                if not(xList[i]==finishPixel[0] and yList[i]==finishPixel[1]) and not(xList[i]==startPixel[0] and yList[i]==startPixel[1]):
                    newObstacle = [xList[i] ,yList[i]]
                    obstacleCoordinats.append(newObstacle)
                    f.write("({}, {}, K)\n".format(xList[i], yList[i]))
            #print(obstacleCoordinats)
            #test icin 
            for i in range(obstacleAmount):
                if(xList[i]==finishPixel[0] and yList[i]==finishPixel[1]) or (xList[i]==startPixel[0] and yList[i]==startPixel[1]):
                    print("cakisiyor......")
        except(e):
            print("Dosyaya yazarken veyahut random atama yapilirken bir hata olustu!")
        finally:
            f.close();
            return obstacleCoordinats
    
# sadece bu dosya calistirilmak 
if __name__ == '__main__':
    env = HomePage()
    env.mainloop()
